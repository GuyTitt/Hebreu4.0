# cree_table_des_matieres.py — Version 6.13 — TDM générée à partir de structure_site.json

import json
from pathlib import Path
from datetime import datetime

from lib1.options import DOSSIER_HTML, DOSSIER_REEL
from lib1.config import CONFIG

version = ("cree_table_des_matieres.py", "6.13")
print(f"[Version] {version[0]} — {version[1]}")

DOSSIER_TDM = CONFIG["dossier_tdm"]
AJOUT = CONFIG["ajout_affichage"]  # [avant_dossier, après_dossier, avant_fichier, après_fichier]

def log(msg: str) -> None:
    """Affiche un message de debug."""
    print(msg)

def construire_arbo(arbre: dict, prefixe: str = "") -> str:
    """
    Construit récursivement l'arborescence HTML de la TDM à partir de l'arbre JSON.

    Args:
        arbre (dict): Noeud courant de structure_site.json
        prefixe (str): Chemin relatif pour les liens

    Returns:
        str: Code HTML de l'arborescence
    """
    html = ""
    dossiers = sorted(arbre.get("dossiers", []), key=lambda x: x.get("position", 9999))
    fichiers = sorted(arbre.get("fichiers", []), key=lambda x: x.get("position", 9999))

    entries = dossiers + fichiers
    if not entries:
        return ""

    html += "<ul class=\"tree\">\n"

    for entry in entries:
        # Vérifie si l'entrée doit être affichée dans la TDM
        if not entry.get("affiché_TDM", True):
            continue

        nom_visible = entry.get("nom_TDM", entry.get("nom_affiché", entry["nom_html"]))
        if entry.get("ajout_affichage", True):
            if "dossiers" in arbre and entry in dossiers:  # c'est un dossier
                nom_visible = f"{AJOUT[0]}{nom_visible}{AJOUT[1]}"
            else:  # c'est un fichier
                nom_visible = f"{AJOUT[2]}{nom_visible}{AJOUT[3]}"

        if "dossiers" in entry:  # c'est un dossier
            lien = f"{prefixe}/{entry['nom_html']}/index.html"
            sous_html = construire_arbo(entry, f"{prefixe}/{entry['nom_html']}")
            html += f'  <li>\n    <details>\n      <summary><a href="{lien}" class="folder-link">{nom_visible}</a></summary>\n'
            if sous_html:
                html += sous_html
            html += '    </details>\n  </li>\n'
        else:  # c'est un fichier
            lien = f"{prefixe}/{entry['nom_html']}"
            html += f'  <li><a href="{lien}">{nom_visible}</a></li>\n'

    html += "</ul>\n"
    return html

def main() -> None:
    """Génère la TDM à partir de structure_site.json."""
    tdm_path = Path(DOSSIER_HTML) / DOSSIER_TDM
    json_path = tdm_path / "structure_site.json"

    if not json_path.exists():
        print("[ERREUR] Fichier structure_site.json introuvable — lance genere_site.py d'abord")
        return

    log("Lecture de structure_site.json")
    with open(json_path, "r", encoding="utf-8") as f:
        arbre_site = json.load(f)

    log("Génération de la table des matières à partir de l'arbre JSON...")
    contenu = construire_arbo(arbre_site)

    haut_page = "".join(CONFIG.get("haut_page", []))
    bas_page = "".join(CONFIG.get("bas_page", [])).replace("{{date}}", datetime.now().strftime("%d/%m/%Y"))
    navigation = '<nav class="navigation"><div class="gauche"><a href="/index.html" class="monbouton">Accueil</a></div><div class="droite"><a href="/TDM/index.html" class="monbouton">Sommaire</a></div></nav>'

    css_tree = """
.tree { --spacing: 1.8rem; --radius: 12px; line-height: 2.2rem; font-family: "Segoe UI", sans-serif; }
.tree li { display: block; position: relative; padding-left: calc(2 * var(--spacing) - var(--radius) - 2px); }
.tree ul { margin-left: 0; padding-left: 0; }
.tree ul li { border-left: 2px solid #ddd; }
.tree ul li:last-child { border-color: transparent; }
.tree ul li::before { content: ""; position: absolute; top: calc(var(--spacing)/-2); left: -2px; width: calc(var(--spacing)+2px); height: calc(var(--spacing)+1px); border: solid #ddd; border-width: 0 0 2px 2px; }
.tree summary { cursor: default; }
.tree summary::marker, .tree summary::-webkit-details-marker { display: none; }
.tree li::after, .tree summary::before { content: ""; position: absolute; top: calc(var(--spacing)/2 - var(--radius)); left: calc(var(--spacing) - var(--radius) - 1px); width: calc(2*var(--radius)); height: calc(2*var(--radius)); border-radius: 50%; background: #ddd; }
.tree summary::before { content: "+"; z-index: 1; background: #2c3e50; color: white; font-weight: bold; text-align: center; line-height: calc(2*var(--radius)); }
.tree details[open] > summary::before { content: "−"; }
.folder-link { color: #2c3e50; text-decoration: none; font-weight: 600; padding: 4px 8px; border-radius: 6px; }
.folder-link:hover { background: #ecf0f1; }
.tree a { color: #2980b9; text-decoration: none; padding: 4px 8px; border-radius: 6px; }
.tree a:hover { background: #ecf0f1; }
"""

    if not CONFIG.get("lien_souligné_TDM", True):
        css_tree += "\n.tree a, .folder-link, .tree a:hover, .folder-link:hover { text-decoration: none !important; }\n"

    html = f"""<!DOCTYPE html>
<html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Sommaire – Hébreu 4.0</title>
        <base href="{DOSSIER_REEL}">
        <link rel="stylesheet" href="/style.css">
        <style>{css_tree}</style>
    </head>
<body>
{haut_page}
{navigation}
<h1>Sommaire du site</h1>
<div class="tdm-content">{contenu}</div>
{bas_page}
</body>
</html>"""

    (tdm_path / "index.html").write_text(html, encoding="utf-8")
    print(f"[SUCCÈS] TDM générée à partir de structure_site.json — version {version[1]}")

if __name__ == "__main__":
    main()

# Fin de "cree_table_des_matieres.py" version "6.13"