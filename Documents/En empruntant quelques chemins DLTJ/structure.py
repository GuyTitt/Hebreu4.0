# STRUCTURE.py – Corrigé automatiquement v2.0
# Templates {{variable}} pour flexibilité

STRUCTURE = {
    "dossiers": [
        {
            "nom_document": "petit guide pour les eventuels egares",
            "nom_html": "petit_guide_pour_les_eventuels_egares",
            "nom_affiché": "Petit guide pour les éventuels égarés",
            "nom_TDM": "{{nom_affiché}}",
            "ajout_affichage": True,
            "affiché_index": True,
            "affiché_TDM": True,
            "position": 1,
            "nom_navigation": "{{nom_affiché}}"
        },
        {
            "nom_document": "Le four d'Aknai",
            "nom_html": "le_four_d_aknai",
            "nom_affiché": "Le four d'Aknaï",
            "nom_TDM": "{{nom_affiché}}",
            "ajout_affichage": True,
            "affiché_index": True,
            "affiché_TDM": True,
            "position": 2,
            "nom_navigation": "{{nom_affiché}}"
        },
        {
            "nom_document": "Na'aseh we-Nishma'. Midrash",
            "nom_html": "na_aseh_we-nishma_._midrash",
            "nom_affiché": "Na'aseh we-Nishma' __(Midrash)__",
            "nom_TDM": "{{nom_affiché}}",
            "ajout_affichage": True,
            "affiché_index": True,
            "affiché_TDM": True,
            "position": 3,
            "nom_navigation": "{{nom_affiché}}"
        },
        {
            "nom_document": "Quatre sont entrés au Pardes",
            "nom_html": "quatre_sont_entres_au_pardes",
            "nom_affiché": "{{nom_document_sans_ext}}",
            "nom_TDM": "{nom_affiché}}",
            "ajout_affichage": True,
            "affiché_index": True,
            "affiché_TDM": True,
            "position": 4,
            "nom_navigation": "{{nom_affiché}}"
        },
        {
            "nom_document": "Sujets en vrac",
            "nom_html": "sujets_en_vrac",
            "nom_affiché": "{{nom_document_sans_ext}}",
            "nom_TDM": "{{nom_document}}",
            "ajout_affichage": True,
            "affiché_index": True,
            "affiché_TDM": True,
            "position": 5,
            "nom_navigation": "{{nom_document}}"
        },
        {
            "nom_document": "Chants hebreux et Yiddish. Partitions",
            "nom_html": "chants_hebreux_et_yiddish._partitions",
            "nom_affiché": "Chants hébreux et Yiddish__(Partitions)__",
            "nom_TDM": "Chants hébreux et Yiddish",
            "ajout_affichage": True,
            "affiché_index": True,
            "affiché_TDM": True,
            "position": 6,
            "nom_navigation": "Chants hebreux et Yiddish __(Partitions)__"
        }
    ],
    "fichiers": [
        {
            "nom_document": "Petit équipement de l'emprunteur novice.docx",
            "nom_html": "petit_equipement_de_l_emprunteur_novice.pdf",
            "nom_affiché": "Petit équipement de l'emprunteur novice",
            "nom_TDM": "{{nom_affiché}}",
            "ajout_affichage": False,
            "affiché_index": False,
            "affiché_TDM": True,
            "position": 7
        }
    ],
    "titre_dossier": "En empruntant quelques chemins dans la tradition juive",
    "entete_general": True,
    "pied_general": True,
    "entete": True,
    "pied": True,
    "navigation": True,
    "haut_page": True,
    "bas_page": True,
    "ajout_affichage": True,
    "titre_table": "{{titre_dossier}}"
}
