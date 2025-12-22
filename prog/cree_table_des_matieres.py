# cree_table_des_matieres.py — Version 6.26

version = ("cree_table_des_matieres.py", "6.26")
print(f"[Version] {version[0]} — {version[1]}")

import json
import re
from pathlib import Path

from lib1.options import DOSSIER_DOCUMENTS, DOSSIER_HTML, BASE_PATH
from lib1.config import CONFIG

def lire(variable: dict, element: str, defaut) -> object:
    """Lit une valeur dans un dictionnaire, retourne la valeur par défaut sinon."""
    return variable.get(element, defaut)

voir_structure = lire(CONFIG, "voir_structure", False)

def log(msg: str) -> None:
    """Affiche un message simple avec préfixe pour debug."""
    print(f"[TDM DEBUG] {msg}")

def appliquer_style(texte: str) -> str:
    """Applique les balises Markdown-like au texte pour coloration, gras, italique, etc.
    
    Utilise __texte__ pour italique afin d’éviter conflit avec les underscores simples des noms de fichiers.
    """
    texte = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', texte)
    texte = re.sub(r'__(.*?)__', r'<em>\1</em>', texte)  # Double underscore pour italique
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

def construire_arbo(dossier_sources: Path, prefixe_html: str = "") -> str:
    """Construit récursivement l'arbre HTML de la TDM avec puces + / - pour tous les niveaux."""
    html = ""
    structure_path = dossier_sources / "STRUCTURE.py"
    if structure_path.exists():
        try:
            from importlib.machinery import SourceFileLoader
            module = SourceFileLoader("STRUCTURE", str(structure_path)).load_module()
            struc = module.STRUCTURE
        except Exception as e:
            log(f"ERREUR lecture STRUCTURE.py : {e}")
            struc = {"dossiers": [], "fichiers": []}
    else:
        struc = {"dossiers": [], "fichiers": []}

    struc["dossiers"].sort(key=lambda x: x.get("position", 9999))
    struc["fichiers"].sort(key=lambda x: x.get("position", 9999))

    for item in struc["dossiers"]:
        if not item.get("affiché_TDM", True):
            continue
        nom_html = item["nom_html"]
        nom_affiché = appliquer_style(item.get("nom_TDM", item["nom_document"]))
        chemin_html = f"{prefixe_html}/{nom_html}/index.html"
        lien = f"{BASE_PATH}{chemin_html}"
        sous_arbo = construire_arbo(dossier_sources / item["nom_document"], f"{prefixe_html}/{nom_html}")
        if sous_arbo:
            html += f'<li><details><summary><a href="{lien}" class="folder-link">{nom_affiché}</a></summary><ul>{sous_arbo}</ul></details></li>\n'
        else:
            html += f'<li><a href="{lien}" class="folder-link">{nom_affiché}</a></li>\n'

    for item in struc["fichiers"]:
        if not item.get("affiché_TDM", True):
            continue
        nom_html = item["nom_html"]
        nom_affiché = appliquer_style(item.get("nom_affiché", item["nom_document"]))
        chemin_html = f"{prefixe_html}/{nom_html}"
        lien = f"{BASE_PATH}{chemin_html}"
        html += f'<li><a href="{lien}">{nom_affiché}</a></li>\n'

    return html

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

def _generer_navigation(chemin_relatif: list[str]) -> str:
    """Génère la barre de navigation avec BASE_PATH."""
    nav = f'<nav class="navigation"><div class="gauche"><a href="{BASE_PATH}/index.html" class="monbouton">Accueil</a>'
    for i in range(len(chemin_relatif) - 1):
        lien_parts = [normaliser_nom(p) for p in chemin_relatif[:i+1]]
        lien = BASE_PATH + "/" + "/".join(lien_parts)
        nav += f' → <a href="{lien}/index.html" class="monbouton">{appliquer_style(chemin_relatif[i])}</a>'
    nav += f'</div><div class="droite"><a href="{BASE_PATH}/TDM/index.html" class="monbouton">Sommaire</a></div></nav>'
    if voir_structure:
        nav = f"<div><!-- début navigation -->{nav}<!-- fin navigation --></div>"
    return nav

def normaliser_nom(nom: str) -> str:
    """Normalise un nom pour URL (minuscules, underscore, sans accent)."""
    import unicodedata
    nom = unicodedata.normalize('NFD', nom)
    nom = ''.join(c for c in nom if unicodedata.category(c) != 'Mn')
    return nom.replace(" ", "_").lower()

def generer_tdm() -> None:
    """Génère le fichier TDM/index.html avec entête local au lieu de <h1> et table-container."""
    log("=== DÉBUT GÉNÉRATION TDM ===")
    racine_sources = Path(DOSSIER_DOCUMENTS)
    if not racine_sources.exists():
        log("ERREUR : dossier sources n'existe pas !")
        return

    tdm_sources = racine_sources / "TDM"
    tdm_structure_path = tdm_sources / "STRUCTURE.py"
    if tdm_structure_path.exists():
        try:
            from importlib.machinery import SourceFileLoader
            module = SourceFileLoader("STRUCTURE", str(tdm_structure_path)).load_module()
            tdm_struc = module.STRUCTURE
        except Exception as e:
            log(f"ERREUR lecture TDM STRUCTURE.py : {e}")
            tdm_struc = {}
    else:
        log("TDM STRUCTURE.py NON trouvé → pas d'entête/pied spécifique")
        tdm_struc = {}

    arbre_html = construire_arbo(racine_sources)

    titre_site = "Table des matières"
    html_parts = []
    html_parts.append(deb_html(titre_site))

    # entete_general avec fallback
    if tdm_struc.get("entete_general", False):
        html_parts.append(plage_html_avec_fallback(tdm_sources, "entete_general.html", "début", "_général"))

    # entete local (remplace <h1>)
    if tdm_struc.get("entete", False):
        html_parts.append(plage_html_avec_fallback(tdm_sources, "entete.html", "début", ""))
    else:
        html_parts.append("<h1>Table des matières</h1>")

    # navigation
    if tdm_struc.get("navigation", False):
        html_parts.append(_generer_navigation([]))

    # TDM dans table-container
    html_parts.append('<div class="table-container"><table class="dossiers"><tbody><tr><td>')
    html_parts.append(f'<ul class="tree">{arbre_html}</ul>')
    html_parts.append('</td></tr></tbody></table></div>')

    # pied local
    if tdm_struc.get("pied", False):
        html_parts.append(plage_html_avec_fallback(tdm_sources, "pied.html", "fin", ""))

    # pied_general avec fallback
    if tdm_struc.get("pied_general", False):
        html_parts.append(plage_html_avec_fallback(tdm_sources, "pied_general.html", "fin", "_général"))

    html_parts.append(fin_html())

    html_brut = "".join(html_parts)
    from bs4 import BeautifulSoup
    html_prettify = BeautifulSoup(html_brut, 'html.parser').prettify()

    tdm_path = Path(DOSSIER_HTML) / "TDM"
    tdm_path.mkdir(parents=True, exist_ok=True)
    (tdm_path / "index.html").write_text(html_prettify, encoding="utf-8")
    log("TDM/index.html généré avec succès")
    log("=== FIN GÉNÉRATION TDM ===")

if __name__ == "__main__":
    generer_tdm()

# fin du "cree_table_des_matieres.py" version "6.26"