# STRUCTURE.py – Corrigé automatiquement
# Templates {{variable}} pour flexibilité

STRUCTURE = {
    "dossiers": [],
    "fichiers": [
        {
            "nom_document": "Cas speciaux.pdf",
            "nom_html": "cas_speciaux.pdf",
            "nom_affiché": "Cas spéciaux",
            "nom_TDM": "{{nom_affiché}}",
            "ajout_affichage": True,
            "affiché_index": True,
            "affiché_TDM": True,
            "position": 1
        },
        {
            "nom_document": "Commentaires rabbiniques sur Qo 8.10.pdf",
            "nom_html": "commentaires_rabbiniques_sur_qo_8.10.pdf",
            "nom_affiché": "Commentaires rabbiniques sur Qo 8:10",
            "nom_TDM": "{{nom_affiché}}",
            "ajout_affichage": True,
            "affiché_index": True,
            "affiché_TDM": True,
            "position": 2
        },
        {
            "nom_document": "Recension des te'amim.pdf",
            "nom_html": "recension_des_te_amim.pdf",
            "nom_affiché": "{{nom_document_sans_ext}}",
            "nom_TDM": "{{nom_affiché}}",
            "ajout_affichage": True,
            "affiché_index": True,
            "affiché_TDM": True,
            "position": 3
        },
        {
            "nom_document": "Syntaxe des te'amim.10.pdf",
            "nom_html": "syntaxe_des_te_amim.10.pdf",
            "nom_affiché": "Syntaxe des te´amim",
            "nom_TDM": "{{nom_affiché}}",
            "ajout_affichage": True,
            "affiché_index": True,
            "affiché_TDM": True,
            "position": 4
        }
    ],
    "titre_dossier": "Les te'amim, pour &laquo; savourer &raquo;  l'hébreu",
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
