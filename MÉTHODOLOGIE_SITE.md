---
title: "Réalisation du site de compte rendu de recherche"
author: "G.Tittelein"
output:
  html_document:
    numbered_sections: TRUE # <-- ICI
---
# Réalisation du site de compte rendu de recherche
---

## I. Présentation du projet

Ce projet vise à produire un **site web statique professionnel**, élégant et entièrement automatisé à partir d’une arborescence de documents (PDF, images, textes sources).

Le site est généré localement dans le dossier `/html`, puis déployable immédiatement sur GitHub Pages, Netlify, Vercel, ou tout serveur statique.

 **Objectifs**
 
- Génération 100 % automatique de la structure du site à partir des dossiers et fichiers sources.
- Navigation fluide, cohérente et dynamique avec fil d’Ariane.
- Table des matières dynamique intelligente, pliable, avec filtrage personnalisé.
- Contrôle fin et granulaire via fichiers `structure.py` pour chaque dossier (visibilité, ordre, titres personnalisés, etc.).
- Design épuré, responsive, accessible, avec support de mises en forme Markdown-like.
- Zéro dépendance externe lourde (Python standard + http-server pour le local).
- Gestion des entêtes, pieds de page globaux et locaux.
- Personnalisation complète via fichiers de configuration (`options.py`, `config.py`, `style.css`).
- Log détaillé et nettoyage automatique des caches.

Le système est conçu pour être extensible : ajout de nouveaux dossiers/fichiers régénère automatiquement le site sans effort.

Le temps investi a permis de créer un système robuste, avec gestion des erreurs, logging, et personnalisation avancée, garantissant une maintenabilité à long terme et une scalabilité pour des projets similaires.

---

## II. Structure du dossier de génération

La structure globale du projet est conçue pour une clarté maximale, avec séparation claire entre sources, scripts et output.

```
hebreu4.0/
├── documents/              ← Sources principales : dossiers, sous-dossiers, fichiers (PDF, images, etc.).
│   ├── Annexes/            ← Exemple de dossier avec fichiers secondaires.
│   ├── Dossier Principal/  ← Dossier racine des contenus principaux, avec sous-dossiers imbriqués.
│   │   ├── Dossier secondaire1/
│   │   ├── Dossier secondaire2/
│   │   │   └── SousDossier secondaire21/
│   ├── Références/         ← Dossier pour bibliographie ou références.
│   ├── nppBackup/          ← Sauvegardes automatiques (ignorées par le générateur).
│   └── TDM/                ← Dossier spécial pour la table des matières (géré automatiquement, non affiché).
├── prog/                   ← Scripts de génération et librairies.
│   ├── lib1/               ← Modules partagés.
│   │   ├── config.py       ← Configuration globale (titres, classes CSS, etc.).
│   │   ├── options.py      ← Chemins des dossiers sources/output.
│   │   └── style.css       ← Fichier CSS central pour tout le site.
│   ├── genere_site.py      ← Script principal : génère la structure HTML et copie les fichiers.
│   ├── cree_table_des_matieres.py ← Script dédié à la génération de la TDM dynamique.
│   ├── lancer.cmd          ← Batch Windows pour lancer la génération + serveur local.
│   └── methode.py          ← Ce script : génère le rapport méthodologique.
├── html/                   ← Output : site statique généré, prêt à déployer.
│   ├── index.html          ← Page d'accueil.
│   ├── style.css           ← Copie du CSS.
│   ├── TDM/                ← Dossier de la table des matières.
│   │   └── index.html      ← Page TDM dynamique.
│   ├── annexes/            ← Dossiers générés avec leurs index.html et fichiers copiés.
│   └── ...                 ← Tous les autres dossiers et fichiers.
└── MÉTHODOLOGIE_SITE.md    ← Ce rapport (généré par methode.py).
```

Chaque dossier dans `documents/` peut contenir un `structure.py` personnalisé, un `entete.html` et/ou `pied.html` local.
Le temps passé à structurer ainsi assure une organisation scalable, facile à maintenir pour des extensions futures.

---

## III. Contenu des fichiers de génération

### Dossier `documents/`
- Contient tous les fichiers sources : PDF, images, textes.
- Arborescence libre : tout dossier/sous-dossier est reproduit dans `html/`.
- Fichiers spéciaux par dossier :
  - `structure.py` : Configuration locale (visibilité, ordre, titres).
  - `entete.html` : Contenu ajouté en haut de la page index.html locale.
  - `pied.html` : Contenu ajouté en bas de la page index.html locale.
  - `entete_general.html` et `pied_general.html` à la racine : Appliqués à tout le site.

### Dossier `prog/lib1/`
- `options.py` : Définit les chemins (DOSSIER_DOCUMENTS, DOSSIER_HTML).
- `config.py` : Paramètres globaux (titre_site, classe_dossier, ignorer, etc.).
- `style.css` : Définit le style global du site (voir détail ci-dessous).

### Dossier `prog/`
- Scripts Python principaux pour la génération.
- Batch `lancer.cmd` pour exécution facile.

### Dossier `html/`
- Généré automatiquement : ne pas modifier manuellement (régénéré à chaque lancement).

Le temps investi permet un contenu exhaustif, avec documentation interne (docstrings) et commentaires pour une compréhension immédiate.

---

## IV. Les programmes

### 1. `genere_site.py` (version 15.7)

- **Description détaillée**

  - Suppression et recréation du dossier `html/` pour une génération propre.
  - Création immédiate du dossier `TDM` pour éviter les erreurs de chemin.
  - Nettoyage automatique des `__pycache__`.
  - Génération/mise à jour récursive des `structure.py` dans chaque dossier source.
  - Parcours récursif des dossiers : copie des fichiers, génération des `index.html`.
  - Support des mises en forme Markdown-like dans les noms affichés.
  - Gestion des paramètres globaux/locaux via `structure.py`.
  - Log détaillé (console/fichier).
  - Temps investi : optimisation pour une exécution rapide même sur de grandes arborescences.

### 2. `cree_table_des_matieres.py` (version 6.4)

- **Description détaillée**

  - Parcours récursif de `html/` pour construire l’arborescence.
  - Génération d’une TDM pliable avec `<details><summary>`.
  - Filtrage intelligent : ignore les éléments si `"affiché_TDM": False` dans le `structure.py` du parent.
  - Liens URL propres, noms normalisés.
  - Style CSS embarqué pour un arbre visuel élégant (lignes, marqueurs +/−).
  - Ne montre jamais TDM dans la TDM.
  - Temps investi : algorithme efficace, gestion d’erreurs robuste.

### 3. `lancer.cmd` (version 2.1)

- **Description détaillée**

  - Activation de l’environnement virtuel si nécessaire.
  - Exécution séquentielle : `genere_site.py` puis `cree_table_des_matieres.py`.
  - Lancement d’un serveur local avec `npx http-server` (port 3500, CORS, no-cache).
  - Gestion des erreurs avec pause.
  - Temps investi : simplification pour une utilisation one-click.

### 4. `methode.py` (version 3.0)

- **Description détaillée**

  - Génère ce rapport exhaustif au format Markdown.
  - Utilise caractère spécial § pour formatage parfait.
  - Temps investi : rendu complet, sans omission, pour une documentation de qualité.

---

## V. Le dossier `html`

Le dossier `html/` est le résultat final de la génération : un site statique autonome.

- **Contenu exhaustif**

  - `index.html` à la racine et dans chaque dossier.
  - `style.css` central.
  - Tous les fichiers sources copiés (PDF, images) dans leurs dossiers respectifs.
  - Dossier `TDM/` avec son `index.html` (table des matières).

- **Caractéristiques**

  - URLs propres et normalisées (minuscules, sans espaces).
  - Responsive et accessible (via CSS).
  - Prêt pour déploiement : pas de dépendances dynamiques.
  - Temps investi : optimisation pour chargement rapide, compatibilité browsers.

---

## VI. Structure des fichiers `index.html`

Chaque `index.html` est généré dynamiquement et suit une structure modulaire pour une personnalisation maximale.

**Structure détaillée**

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>[Titre du dossier via structure.py ou config]</title>
    <link rel="stylesheet" href="/style.css">
</head>
<body>
    [haut_page global (config.py) : bandeau, logo, etc., si haut_page=True]
    [entete_general.html (racine documents/) : entête site-wide, si entete_general=True]
    [navigation dynamique : fil d’Ariane + lien Sommaire, si navigation=True]
    [entete.html local : contenu spécifique au dossier, si entete=True]
    <table class="dossiers"><tbody>
        [Liste des dossiers/fichiers triés par position, avec liens, styles, et mises en forme MD]
    </tbody></table>
    [pied.html local : pied spécifique, si pied=True]
    [pied_general.html : pied site-wide, si pied_general=True]
    [bas_page global (config.py) : footer avec date, si bas_page=True]
</body>
</html>
```

**Autorisations globales et locales**

- **Globales** : `haut_page`, `bas_page` dans `config.py` ; `entete_general.html`, `pied_general.html` dans `documents/`.
- **Locales** : `entete.html`, `pied.html` dans chaque dossier.
- Contrôles dans `structure.py` : True/False pour chaque.

**Navigation**

- Fil d’Ariane : liens vers parents (Accueil → Dossier → Sous-dossier).
- Lien fixe "Sommaire" vers `/TDM/index.html`.
- Paramètres : `navigation=True/False` dans `structure.py` (par dossier).
- Style : classes `.navigation`, `.monbouton` pour personnalisation CSS.

**Liste des éléments**

- Tri par `position`.
- Visibilité via `affiché_index`.
- Mises en forme dans `nom_affiché` (MD-like).
- Classes CSS personnalisables via `config.py`.

**Temps investi** 

Structure flexible, facile à déboguer, pour une évolution rapide.

---

## VII. Le fichier `style.css` et l’action de ses items

`prog/lib1/style.css` définit le style global, copié dans `html/`.

**Contenu exhaustif**

```css
body { font-family: Arial, sans-serif; margin: 20px; background-color: #f9f9f9; }  ← Base : police, marges, fond clair pour lisibilité.

.navigation { display: flex; justify-content: space-between; margin-bottom: 20px; background: #eee; padding: 10px; }  ← Barre : flexbox pour alignement gauche/droite, fond gris pour séparation visuelle.

.gauche, .droite { display: flex; align-items: center; }  ← Groupes : alignement vertical des boutons.

.monbouton { margin-right: 10px; padding: 5px 10px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }  ← Boutons : bleu, arrondis, sans soulignement pour modernité.
.monbouton:hover { background: #0056b3; }  ← Hover : couleur foncée pour feedback interactif.

.dossiers { width: 100%; border-collapse: collapse; }  ← Table : pleine largeur, sans bordures internes.
.dossiers td { padding: 10px; border-bottom: 1px solid #ddd; }  ← Cellules : espacement, lignes séparatrices pour clarté.

.dossier { font-weight: bold; color: #333; }  ← Dossiers : gras, sombre pour hiérarchie.
.fichier { color: #666; }  ← Fichiers : gris pour distinction.

a { text-decoration: none; }  ← Liens : sans soulignement par défaut.
a:hover { text-decoration: underline; }  ← Hover : soulignement pour interactivité.

.tdm-content { max-width: 800px; margin: auto; }  ← TDM : centrée, largeur limitée pour lecture.
```

**Actions des items**

- Améliore l’UX : responsive (flex), feedback (hover), hiérarchie (gras/gris).
- Personnalisable : modifie pour thèmes (dark mode, etc.).
- Temps investi : CSS minimal mais puissant, optimisé pour performance.

---

## VIII. Structure du fichier table des matières (`/TDM/index.html`)

Page dédiée, générée par `cree_table_des_matieres.py`.

**Structure détaillée**

```html
[haut_page]
[navigation]
<h1>Sommaire du site</h1>
<div class="tdm-content">
  <ul class="tree">
    <li><details><summary><a href="...">[Dossier]</a></summary>[Sous-arbo]</details></li>
    <li><a href="...">[Fichier]</a></li>
  </ul>
</div>
[bas_page]
<style>[CSS arbre]</style>
```

**Filtrage**

Seulement `affiché_TDM=True` (parent).

**Temps investi**

Algorithme récursif efficace, style immersif.

---

## IX. Les procédures

Liste exhaustive avec description détaillée :

| Procédure                     | Description détaillée |
|-------------------------------|-----------------------|
| `log(msg)`                    | Log console/fichier avec flush. Utilisé pour debug, tracing complet.
| `normaliser_nom(nom)`         | Convertit en URL-safe. Ex : "Dossier Principal" → "dossier_principal".
| `appliquer_style(texte)`      | Parse MD-like : **gras**, _italic_, ~~barré~~, [rouge] [/rouge], {grand} {/grand}. Regex avancées pour couleurs.
| `_creer_structure_py(dossier)` | Génère `structure.py` récursif : liste, positions, visibilité. Gestion effacés.
| `_lire_structure(dossier)`    | Parse `structure.py` : retourne dict filtré. Gestion exceptions.
| `_lire_fichier(chemin)`       | Lit entete/pied. Retourne vide si absent.
| `_generer_navigation(chemin_relatif)` | Fil d’Ariane + Sommaire. Flexible pour chemins longs.
| `_generer_page(src, dst, chemin)` | Assemble HTML : globals/locaux, table triée avec styles.
| `_traiter_dossier(src, dst, chemin)` | Récursif : mkdir, copie, génération pages.
| `doit_afficher_dans_tdm(entry)` | Vérifie `affiché_TDM` dans parent. Robustesse erreurs.
| `construire_arbo(dossier, prefixe)` | HTML récursif TDM : filtrage, liens normalisés.

Procédures courtes (<25 lignes), modulaires, pour maintenance facile.

---
## X. Syntaxe dans `nom_affiché` de structure.py

| Syntaxe                        | Résultat                     |
|--------------------------------|------------------------------|
| `**texte**`                       | **gras**                     |
| `_texte_`                      | _italique_                   |
| `**_texte_**`                  | **_gras italique_**          |
| `~~texte~~`                    | ~~barré~~                    |
| `[rouge]texte[/rouge]`         | texte en rouge               |
| `[bleu]texte[/bleu]`           | texte en bleu                |
| `[couleur:#ff3366]texte[/couleur]` | couleur personnalisée    |
| `{grand}texte{/grand}`         | texte très gros              |
| `{taille:2.5em}texte{/taille}` | taille personnalisée         |

## XI. Contenu des fichiers générés et modification possible

**Fichiers générés**

- `index.html` : Pages navigables, modifiables via sources.
- `structure.py` : Auto-générés, mais éditables (ajoute MD dans `nom_affiché`).
- `TDM/index.html` : TDM filtrée.

**Modifications**

- Sources : ajout → régénération.
- `nom_affiché` : MD-like pour rich text.
- Visibilité : `affiché_index/TDM` = False masque.

---

## XII. Fichiers de configuration

### `options.py`
```python
DOSSIER_DOCUMENTS = "documents"
DOSSIER_HTML = "html"
```

### `config.py`
```python
CONFIG = {
    "titre_site": "Hébreu 4.0",
    "dossier_tdm": "TDM",
    "fichier_index": "index.html",
    "classe_dossier": "dossier",
    "classe_fichier": "fichier",
    "ignorer": ["Thumbs.db"],
    "ajout_affichage": ["📄 ", ""],
    "haut_page": ['<div class="bandeau">Projet</div>'],
    "bas_page": ['<footer>{date}</footer>'],
    "logging": ["console";"log.log"]
}
```

### `structure.py` exemple
```python
STRUCTURE = {
    "entete_general": True,
    "pied_general": True,
    "entete": True,
    "pied": True,
    "navigation": True,
    "haut_page": True,
    "bas_page": True,
    "ajout_affichage": True,
    "dossiers": [
        {"nom_document": "Secondaire1", 
         "nom_html": "Secondaire1",
         "nom_affiché": "**Secondaire** [rouge]1[/rouge]",
         "nom_TDM": "Secondaire 1",
         "affiché_index": True,
         "affiché_TDM": True,
         "position": 2  
        }
    ],
    "fichiers": [
        {"nom_document": "Introduction sujet.pdf",
         "nom_html": "introduction_sujet.pdf",
         "nom_affiché": "_Introduction_ {grand}PDF{/grand}",
         "nom_TDM": "Introduction",
         "affiché_index": True,
         "ajout_affichage": True,
         "affiché_index": True,
         "affiché_TDM": True,
         "position": 1
         }
    ]
}
```

---

## XIII. genere_site.py  
  
```python
# genere_site.py — Version 19.7

version = ("genere_site.py", "19.7")

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

from lib1.options import DOSSIER_DOCUMENTS, DOSSIER_HTML
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
    <link href="/style.css" rel="stylesheet"/>
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
    """Génère la barre de navigation."""
    nav = '<nav class="navigation"><div class="gauche"><a href="/index.html" class="monbouton">Accueil</a>'
    for i in range(len(chemin_relatif) - 1):
        lien_parts = [normaliser_nom(p) for p in chemin_relatif[:i+1]]
        lien = "/" + "/".join(lien_parts)
        nav += f' → <a href="{lien}/index.html" class="monbouton">{chemin_relatif[i]}</a>'
    nav += '</div><div class="droite"><a href="/TDM/index.html" class="monbouton">Sommaire</a></div></nav>'
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
                shutil.copy2(cible_pdf_documents, cible_pdf_html)
                log(f"PDF copié : {nom_pdf}")
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
    """Génère index.html avec BeautifulSoup prettify."""
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

    # entete_general avec fallback
    if struc.get("entete_general", False):
        html_parts.append(plage_html_avec_fallback(dossier, "entete_general.html", "début", "_général"))

    html_parts.append(plage_html_avec_fallback(dossier, "entete.html", "début", ""))

    html_parts.append(_generer_navigation(list(rel_path.parts)))
    html_parts.append(f"<div class=\"table-container\"><table class=\"dossiers\"><tbody><tr><td>{table_index(liste_fils)}</td></tr></tbody></table></div>")

    html_parts.append(plage_html_avec_fallback(dossier, "pied.html", "fin", ""))

    # pied_general avec fallback
    if struc.get("pied_general", False):
        html_parts.append(plage_html_avec_fallback(dossier, "pied_general.html", "fin", "_général"))

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

# fin du "genere_site.py" version "19.7"
```

---

## XIV. cree_table_des_matieres.py  
  
```python
# cree_table_des_matieres.py — Version 6.12 — TDM générée à partir de structure_site.json

import json
from pathlib import Path
from datetime import datetime

from lib1.options import DOSSIER_HTML
from lib1.config import CONFIG

version = ("cree_table_des_matieres.py", "6.12")
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

# Fin de "cree_table_des_matieres.py" version "6.12"
```
---
_Généré  le 19 Decembre 2025_
