# genere_site.py — Version 20.0

version = ("genere_site.py", "20.0")

# Importation des librairies
import os
import json
import shutil
import unicodedata
import re
import psutil
import tempfile
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from bs4 import BeautifulSoup  # Pour prettify des index.html

# Conversion .doc/.docx → .pdf via Microsoft Word (Windows uniquement)
try:
    from win32com.client import Dispatch
    word_app = Dispatch("Word.Application")
    word_app.Visible = False
except ImportError:
    word_app = None

from lib1.options import DOSSIER_DOCUMENTS, DOSSIER_HTML, BASE_PATH
from lib1.config import CONFIG

print(f"[Version] {version[0]} — {version[1]}")

# Acquisition des constantes
def lire(variable: dict, element: str, defaut: Any) -> Any:
    """Lit une valeur dans un dictionnaire, retourne la valeur par défaut sinon."""
    return variable.get(element, defaut)

STYLE_CSS_SRC = Path(__file__).parent / "lib1" / "style.css"
IGNORER = set(lire(CONFIG, "ignorer", [])) | {"__pycache__", ".pyc", "structure.py", r"~\$"}
FICHIERS_ENTETE_PIED = {"entete.html", "entete_general.html", "pied.html", "pied_general.html"}
EXTENSIONS_ACCEPTEES = {".html", ".htm", ".pdf", ".txt"}
DOSSIER_TDM = lire(CONFIG, "dossier_tdm", "TDM")
AJOUT = lire(CONFIG, "ajout_affichage", ["", "", "", ""])
voir_structure = lire(CONFIG, "voir_structure", False)

log_file = Path("generation.log")
log_file.write_text(f"--- DÉBUT GÉNÉRATION — {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ---\n", encoding="utf-8")

# Fonctions utilitaires
def log(msg: str) -> None:
    """Écrit un message dans la console et dans generation.log."""
    print(msg)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

def normaliser_nom(nom: str) -> str:
    """Normalise un nom pour URL (minuscules, underscore, sans accent)."""
    nom = unicodedata.normalize('NFD', nom)
    nom = ''.join(c for c in nom if unicodedata.category(c) != 'Mn')
    return nom.replace(" ", "_").lower()

def appliquer_style(texte: str) -> str:
    """Applique les balises Markdown-like au texte pour coloration, gras, etc."""
    texte = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', texte)
    texte = re.sub(r'_(.*?)_', r'<em>\1</em>', texte)
    texte = re.sub(r'~~(.*?)~~', r'<del>\1</del>', texte)

    couleurs = {"rouge": "red", "bleu": "blue", "vert": "green", "jaune": "gold",
                "violet": "purple", "orange": "orange", "gris": "gray", "noir": "black"}
    for nom, code in couleurs.items():
        texte = texte.replace(f"[{nom}]", f'<span style="color:{code}">')
        texte = texte.replace(f"[/{nom}]", "</span>")

    texte = re.sub(r'\[couleur:(#[0-9a-fA-F]{6}|rgba?\([^)]+\))\]', lambda m: f'<span style="color:{m.group(1)}">', texte)
    texte = texte.replace("[/couleur]", "</span>")
    texte = texte.replace("{grand}", '<span style="font-size:1.8em">').replace("{/grand}", "</span>")
    texte = texte.replace("{petit}", '<span style="font-size:0.8em">').replace("{/petit}", "</span>")
    texte = re.sub(r'\{taille:([^}]+)\}', lambda m: f'<span style="font-size:{m.group(1)}">', texte)
    texte = texte.replace("{/taille}", "</span>")
    return texte

def deb_html(titre: str) -> str:
    """Générateur départ html."""
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="utf-8"/>
    <title>{titre}</title>
    <link href="{BASE_PATH}/style.css" rel="stylesheet"/>
</head>
<body>"""

def fin_html() -> str:
    """Générateur fin html."""
    return """</body>
</html>"""

def plage_html_avec_fallback(dossier: Path, fichier: str, position: str, commun: str) -> str:
    """Lit un fichier HTML avec fallback à la racine pour entete_general et pied_general."""
    local = dossier / fichier
    if local.exists():
        modele = local
    else:
        if fichier in ("entete_general.html", "pied_general.html"):
            racine = Path(DOSSIER_DOCUMENTS)
            modele = racine / fichier
            if not modele.exists():
                return ""
        else:
            return ""

    with open(modele, "r", encoding="utf-8") as f:
        h = f.read()

    if voir_structure:
        h = f"<div><!-- début {position}{commun} -->{h}<!-- fin {position}{commun} --></div>"
    return h

def _generer_navigation(chemin_relatif: List[str]) -> str:
    """Génère la barre de navigation avec BASE_PATH."""
    nav = f'<nav class="navigation"><div class="gauche"><a href="{BASE_PATH}/index.html" class="monbouton">Accueil</a>'
    for i in range(len(chemin_relatif) - 1):
        lien_parts = [normaliser_nom(p) for p in chemin_relatif[:i+1]]
        lien = BASE_PATH + "/" + "/".join(lien_parts)
        nav += f' → <a href="{lien}/index.html" class="monbouton">{chemin_relatif[i]}</a>'
    nav += f'</div><div class="droite"><a href="{BASE_PATH}/TDM/index.html" class="monbouton">Sommaire</a></div></nav>'
    if voir_structure:
        nav = f"<div><!-- début navigation -->{nav}<!-- fin navigation --></div>"
    return nav

def get_word_processes() -> List[Any]:
    """Retourne la liste des processus Word actifs."""
    return [proc for proc in psutil.process_iter(['pid', 'name']) if proc.info['name'] and proc.info['name'].upper() == 'WINWORD.EXE']

def kill_word_processes(processes: List[Any]) -> None:
    """Ferme proprement les processus Word."""
    for proc in processes:
        print(".", end=" ")
        try:
            proc.terminate()
            proc.wait(timeout=5)
        except Exception:
            proc.kill()
    print(" !")

def traiter_docx(dossier: Path, temp_dir: Path) -> None:
    """Traite tous les .doc/.docx du dossier : crée PDF au début si nécessaire."""
    log(f"Traitement .doc/.docx dans {dossier}")
    entries = list(dossier.iterdir())
    nb_conversions = 0
    for entry in entries:
        if entry.is_file() and entry.suffix.lower() in (".doc", ".docx"):
            nom_pdf = normaliser_nom(entry.stem + ".pdf")
            cible_pdf = dossier / nom_pdf
            if not cible_pdf.exists() or entry.stat().st_mtime > cible_pdf.stat().st_mtime:
                log(f"Conversion : {entry.name} → {nom_pdf}")
                cree_pdf(dossier, entry.name, cible_pdf, temp_dir)
                nb_conversions += 1
    if nb_conversions == 0:
        log("Aucune conversion nécessaire")

def cree_pdf(chemin_doc: Path, fichier_doc: str, cible_pdf: Path, temp_dir: Path) -> None:
    """Convertit un .doc/.docx en .pdf via Word sans modifier la date du .docx original."""
    processes = get_word_processes()
    if processes:
        log("Fermeture processus Word")
        kill_word_processes(processes)

    temp_doc = temp_dir / fichier_doc
    shutil.copy2(chemin_doc / fichier_doc, temp_doc)

    if word_app is None:
        log("Word non disponible — copie simple")
        shutil.copy2(temp_doc, cible_pdf)
        return

    try:
        full_path = str(temp_doc.resolve())
        doc = word_app.Documents.Open(full_path)
        doc.SaveAs(str(cible_pdf.resolve()), FileFormat=17)
        doc.Close()
        log(f"PDF créé : {cible_pdf.name}")
    except Exception as e:
        log(f"Conversion échouée {fichier_doc} : {e}")
        shutil.copy2(temp_doc, cible_pdf)

def _creer_structure_complete(dossier: Path, temp_dir: Path) -> Dict[str, Any]:
    """Crée ou complète structure.py : source de vérité unique pour index.html et TDM."""
    log(f"Traitement dossier : {dossier}")
    # Création PDF au début
    traiter_docx(dossier, temp_dir)

    struc = {
        "titre_dossier": dossier.name if dossier != Path(DOSSIER_DOCUMENTS) else CONFIG.get("titre_site", "Site"),
        "entete_general": True,
        "pied_general": True,
        "entete": True,
        "pied": True,
        "navigation": True,
        "haut_page": True,
        "bas_page": True,
        "ajout_affichage": True,
        "dossiers": [],
        "fichiers": []
    }

    existing = {}
    p = dossier / "STRUCTURE.py"
    if p.exists():
        try:
            from importlib.machinery import SourceFileLoader
            module = SourceFileLoader("STRUCTURE", str(p)).load_module()
            existing = module.STRUCTURE
        except Exception as e:
            log(f"Erreur lecture STRUCTURE.py : {e}")
    struc.update(existing)

    entries = list(dossier.iterdir())
    for entry in sorted(entries, key=lambda x: x.name.lower()):
        if entry.name in IGNORER or entry.name in FICHIERS_ENTETE_PIED:
            continue

        if entry.suffix.lower() in (".doc", ".docx", ".py"):
            continue

        if entry.suffix.lower() not in EXTENSIONS_ACCEPTEES and not entry.is_dir():
            continue

        nom_html = normaliser_nom(entry.name)

        item_defaults = {
            "nom_document": entry.name,
            "nom_html": nom_html,
            "nom_affiché": entry.stem if entry.is_file() else entry.name,
            "nom_TDM": entry.stem if entry.is_file() else entry.name,
            "ajout_affichage": True
        }

        found = False
        for cat in [struc["dossiers"], struc["fichiers"]]:
            for existing_item in cat:
                if existing_item["nom_document"] == entry.name:
                    existing_item.update({k: v for k, v in item_defaults.items() if k not in existing_item})
                    found = True
                    break
        if not found:
            max_pos = max((it.get("position", 0) for it in struc["dossiers"] + struc["fichiers"]), default=0)
            item = item_defaults.copy()
            item.update({
                "affiché_index": True,
                "affiché_TDM": True,
                "position": max_pos + 1
            })
            (struc["dossiers"] if entry.is_dir() else struc["fichiers"]).append(item)

    # Tri des listes par position croissante avant sauvegarde
    struc["dossiers"].sort(key=lambda x: x.get("position", 9999))
    struc["fichiers"].sort(key=lambda x: x.get("position", 9999))

    # Sauvegarde
    content = f"""# STRUCTURE.py – Généré automatiquement
STRUCTURE = {json.dumps(struc, ensure_ascii=False, indent=4).replace("true", "True").replace("false", "False")}
"""
    p.write_text(content, encoding="utf-8")
    log(f"STRUCTURE.py mis à jour : {dossier}")

    return struc

def copie_site(temp_dir: Path) -> None:
    """Copie /documents vers /html avec gestion .docx → .pdf."""
    log(f"Création du dossier HTML : {DOSSIER_HTML}")
    if Path(DOSSIER_HTML).exists():
        shutil.rmtree(DOSSIER_HTML)
    Path(DOSSIER_HTML).mkdir(parents=True, exist_ok=True)

    if STYLE_CSS_SRC.exists():
        shutil.copy2(STYLE_CSS_SRC, Path(DOSSIER_HTML) / "style.css")
        log("style.css copié")

    arbre_site = _construire_arbre_complet(Path(DOSSIER_DOCUMENTS), temp_dir)
    tdm_path = Path(DOSSIER_HTML) / DOSSIER_TDM
    tdm_path.mkdir(parents=True, exist_ok=True)
    (tdm_path / "structure_site.json").write_text(json.dumps(arbre_site, ensure_ascii=False, indent=4), encoding="utf-8")
    log("structure_site.json généré")

    for racine, dirs, files in os.walk(DOSSIER_DOCUMENTS):
        dirs[:] = [d for d in dirs if d not in IGNORER]

        rel_path = Path(racine).relative_to(DOSSIER_DOCUMENTS)
        cible_rel_norm = Path(*(normaliser_nom(part) for part in rel_path.parts))
        cible = Path(DOSSIER_HTML) / cible_rel_norm
        cible.mkdir(parents=True, exist_ok=True)

        _creer_structure_complete(Path(racine), temp_dir)

        for fichier in files:
            if any(re.search(pattern, fichier) for pattern in IGNORER):
                continue

            src_file = Path(racine) / fichier

            if fichier.lower().endswith((".doc", ".docx")):
                nom_pdf = normaliser_nom(Path(fichier).stem + ".pdf")
                cible_pdf_documents = Path(racine) / nom_pdf
                cible_pdf_html = cible / nom_pdf
                if cible_pdf_documents.exists():
                    shutil.copy2(cible_pdf_documents, cible_pdf_html)
                    log(f"PDF copié : {nom_pdf}")
                else:
                    log(f"PDF manquant pour {fichier} — ignoré")
            elif fichier.lower().endswith(".html"):
                nom_html = normaliser_nom(fichier)
                shutil.copy2(src_file, cible / nom_html)
            else:
                nom_html = normaliser_nom(fichier)
                shutil.copy2(src_file, cible / nom_html)

def _construire_arbre_complet(dossier: Path, temp_dir: Path) -> Dict[str, Any]:
    """Construit l’arbre pour structure_site.json."""
    arbre = {
        "titre_dossier": dossier.name if dossier != Path(DOSSIER_DOCUMENTS) else CONFIG.get("titre_site", "Site"),
        "nom_html": normaliser_nom(dossier.name) if dossier != Path(DOSSIER_DOCUMENTS) else "",
        "dossiers": [],
        "fichiers": []
    }

    struc = _creer_structure_complete(dossier, temp_dir)

    for cat in ["dossiers", "fichiers"]:
        for item in struc.get(cat, []):
            arbre[cat].append(item.copy())

    for entry in arbre["dossiers"]:
        entry.update(_construire_arbre_complet(dossier / entry["nom_document"], temp_dir))

    return arbre

def table_index(liste_fils: List[Dict[str, Any]]) -> str:
    """Génère le HTML de la table des éléments avec <br> après chaque lien et style appliqué."""
    h = []
    for fils in liste_fils:
        if not fils.get("affiché_index", True):
            continue
        nom_affiché = fils.get("nom_affiché", Path(fils.get("nom_document", "inconnu")).stem)
        nom_stylé = appliquer_style(nom_affiché)
        if fils.get("genre") == "dossier":
            nom = f"{AJOUT[0]}{nom_stylé}{AJOUT[1]}" if fils.get("ajout_affichage", True) else nom_stylé
            h.append(f'<a class="dossier-item" href="{fils["nom_html"]}/index.html">{nom}</a><br>')
        else:
            nom = f"{AJOUT[2]}{nom_stylé}{AJOUT[3]}" if fils.get("ajout_affichage", True) else nom_stylé
            h.append(f'<a class="dossier-item" href="{fils["nom_html"]}">{nom}</a><br>')
    return "".join(h)

def generer_page_index(dossier: Path, temp_dir: Path) -> None:
    """Génère index.html avec BeautifulSoup prettify et fallback pour entete/pied general."""
    log(f"Génération page : {dossier}")
    rel_path = dossier.relative_to(DOSSIER_DOCUMENTS)
    cible_rel_norm = Path(*(normaliser_nom(part) for part in rel_path.parts))
    cible = Path(DOSSIER_HTML) / cible_rel_norm
    cible.mkdir(parents=True, exist_ok=True)

    struc = _creer_structure_complete(dossier, temp_dir)

    for item in struc.get("dossiers", []):
        item["genre"] = "dossier"
    for item in struc.get("fichiers", []):
        item["genre"] = "fichier"

    liste_fils = sorted(struc.get("dossiers", []) + struc.get("fichiers", []), key=lambda x: x.get("position", 9999))

    html_parts = []
    titre = struc.get("titre_dossier", dossier.name)
    html_parts.append(deb_html(titre))

    # haut_page global (si configuré)
    if struc.get("haut_page", False):
        html_parts.append("".join(CONFIG.get("haut_page", [])))

    # entete_general avec fallback
    if struc.get("entete_general", False):
        html_parts.append(plage_html_avec_fallback(dossier, "entete_general.html", "début", "_général"))

    # entete local
    if struc.get("entete", False):
        html_parts.append(plage_html_avec_fallback(dossier, "entete.html", "début", ""))

    # navigation
    if struc.get("navigation", False):
        html_parts.append(_generer_navigation(list(rel_path.parts)))

    # table
    html_parts.append(f"<div class=\"table-container\"><table class=\"dossiers\"><tbody><tr><td>{table_index(liste_fils)}</td></tr></tbody></table></div>")

    # pied local
    if struc.get("pied", False):
        html_parts.append(plage_html_avec_fallback(dossier, "pied.html", "fin", ""))

    # pied_general avec fallback
    if struc.get("pied_general", False):
        html_parts.append(plage_html_avec_fallback(dossier, "pied_general.html", "fin", "_général"))

    # bas_page global
    if struc.get("bas_page", False):
        html_parts.append("".join(CONFIG.get("bas_page", [])))

    html_parts.append(fin_html())

    html_brut = "".join(html_parts)
    html_prettify = BeautifulSoup(html_brut, 'html.parser').prettify()
    (cible / "index.html").write_text(html_prettify, encoding="utf-8")
    log(f"Page générée : {cible / 'index.html'}")

def main() -> None:
    """Lance la génération complète du site."""
    log("=== DÉBUT GÉNÉRATION ===")
    with tempfile.TemporaryDirectory() as tmpdirname:
        temp_dir = Path(tmpdirname)
        copie_site(temp_dir)
        for racine, dirs, files in os.walk(DOSSIER_DOCUMENTS):
            dirs[:] = [d for d in dirs if d not in IGNORER]
            generer_page_index(Path(racine), temp_dir)
    processes = get_word_processes()
    if processes:
        log("Fermeture processus Word résiduels")
        kill_word_processes(processes)
    log("=== FIN GÉNÉRATION ===")

if __name__ == "__main__":
    main()

# fin du "genere_site.py" version "20.0"