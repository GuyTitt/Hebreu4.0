# cree_table_des_matieres.py — Version 6.14

version = ("cree_table_des_matieres.py", "6.14")
print(f"[Version] {version[0]} — {version[1]}")

import json
from pathlib import Path

from lib1.options import DOSSIER_HTML, BASE_PATH

def log(msg: str) -> None:
    print(msg)

def construire_arbo(dossier: Path, prefixe: str = "") -> str:
    html = ""
    structure_path = dossier / "STRUCTURE.py"
    if structure_path.exists():
        try:
            from importlib.machinery import SourceFileLoader
            module = SourceFileLoader("STRUCTURE", str(structure_path)).load_module()
            struc = module.STRUCTURE
        except Exception:
            struc = {"dossiers": [], "fichiers": []}
    else:
        struc = {"dossiers": [], "fichiers": []}

    struc["dossiers"].sort(key=lambda x: x.get("position", 9999))
    struc["fichiers"].sort(key=lambda x: x.get("position", 9999))

    for item in struc["dossiers"]:
        if not item.get("affiché_TDM", True):
            continue
        nom_html = item["nom_html"]
        nom_affiché = item.get("nom_affiché", item["nom_document"])
        chemin = f"{prefixe}/{nom_html}/index.html"
        lien = f"{BASE_PATH}{chemin}"
        sous_arbo = construire_arbo(dossier / item["nom_document"], f"{prefixe}/{nom_html}")
        if sous_arbo:
            html += f'<li><details open><summary><a href="{lien}">{nom_affiché}</a></summary><ul>{sous_arbo}</ul></details></li>\n'
        else:
            html += f'<li><a href="{lien}">{nom_affiché}</a></li>\n'

    for item in struc["fichiers"]:
        if not item.get("affiché_TDM", True):
            continue
        nom_html = item["nom_html"]
        nom_affiché = item.get("nom_affiché", item["nom_document"])
        chemin = f"{prefixe}/{nom_html}"
        lien = f"{BASE_PATH}{chemin}"
        html += f'<li><a href="{lien}">{nom_affiché}</a></li>\n'

    return html

def generer_tdm() -> None:
    log("Génération de la Table des Matières")
    racine = Path(DOSSIER_HTML)
    tdm_path = racine / "TDM"
    tdm_path.mkdir(parents=True, exist_ok=True)

    arbre_html = construire_arbo(racine)

    titre_site = "Site"  # Peut être amélioré si besoin
    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="utf-8"/>
    <title>Table des matières - {titre_site}</title>
    <link href="{BASE_PATH}/style.css" rel="stylesheet"/>
    <style>
        .tree ul {{ margin-left: 20px; }}
        .tree details {{ margin: 5px 0; }}
        .tree summary {{ cursor: pointer; font-weight: bold; }}
        .tree a {{ text-decoration: none; color: #0066cc; }}
        .tree a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>Table des matières</h1>
    <ul class="tree">
        {arbre_html}
    </ul>
</body>
</html>"""

    (tdm_path / "index.html").write_text(html, encoding="utf-8")
    log("TDM/index.html généré")

if __name__ == "__main__":
    generer_tdm()

# fin du "cree_table_des_matieres.py" version "6.14"