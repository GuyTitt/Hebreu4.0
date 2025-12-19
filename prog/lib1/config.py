# Début de "config.py" version "2.2"

CONFIG = {
    "version": "2.2",
    "titre_site": "Hébreu Biblique v4.0",
    "fichier_index": "index.html",
    "classe_dossier": "dossier-item",
    "classe_fichier": "fichier-pdf",
    "lien_souligné_index": False,    # False = pas de soulignement dans les pages index
    "lien_souligné_TDM": False,      # False = pas de soulignement dans la TDM
    "haut_page": [
        "<div><!-- debut haut_page -->",
#        "<div class=\"monTitre\">Hébreu biblique</div>",
#        "<div class=\"monSousTitre\">Mes dossiers partagés</div>",
        "<!-- fin haut_page --></div>",
    ],
    "bas_page": [
        "<div><!-- debut bas_page -->",
#        "<div>bas de la page</div>",
        '<footer><a href="mailto:fraboulanger@orange.fr" class="btn-mail">Pour me joindre</a></footer>',
        "<!-- fin bas_page --></div>",
    ],
    "navigation": {
        "sous_dossiers_position": "gauche",
        "afficher_sommaire": True
    },
    "affichage": {
        "afficher_icones": True,
        "table_align": "centre",
        "table_largeur_max": "80%"
    },
    "couleurs": {
        "dossiers": "#0066cc",
        "pdf": "#c0392b",
        "images": "#27ae60"
    },
    "ignorer": [
        "nppBackup", ".git", ".gitignore", "Thumbs.db",
        "entete_general.html", "pied_general.html",
        "entete.html", "pied.html", "structure.json",
        "index.html", "style.css","__pycache__"
    ],
    "extensions_acceptees": ["pdf"],
    "dossier_tdm": "TDM",
    "ajout_affichage": ["📁 ", "", "📘 ", ""],
    "logging": ["console", "generation.log"]  # "console", "fichier.log", ou les deux
}

# Fin de "config.py" version "2.2"