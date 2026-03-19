# remplace_v16.py — Version 16
# v16 : creation html\Hebreu4.0\html\ + copie style.css (requis pour node.js local)
# v15 : scan recursif de package/prog (sous-dossiers = modules reutilisables)
#        dossiers 'archive' et 'ancien' ignores
#        cree prog/ et prog/lib/ s'ils n'existent pas (1er deploiement)
# v14 : liste auto-generee (plus de liste codee en dur), lib1 -> lib
# v13 : cree_table_des_matieres v6.32, genere_site v25.5
#
# CONVENTION DE NOMMAGE (source -> cible) :
#   package/prog/fichier_vX.Y.ext          -> prog/fichier.ext
#   package/prog/lib/fichier_vX.Y.ext      -> prog/lib/fichier.ext
#   package/prog/utils/fichier_vX.Y.ext    -> prog/utils/fichier.ext
#   package/prog/lib_xxx_vX.Y.py           -> prog/lib/xxx.py  (compat. ancienne conv.)
#   package/prog/archive/...               -> IGNORE
#   package/prog/ancien/...                -> IGNORE
#
# Usage : python remplace.py  (depuis n'importe quel dossier)

import shutil
import sys
import re
from pathlib import Path

version = ("remplace.py", "16")

# ─────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────
RACINE = Path("C:/SiteGITHUB/Hebreu4.0")
SRC    = RACINE / "package" / "prog"
DST    = RACINE / "prog"
LIB    = DST / "lib"

# Noms de dossiers ignores lors du scan recursif
DOSSIERS_IGNORES = {"archive", "ancien", "__pycache__"}

# Fichiers cibles optionnels (absence non bloquante)
OPTIONNELS = {"remplace.py", "versions.py"}

# Anciens fichiers/dossiers a supprimer a la 1ere execution
SUPPRIMER = [
    DST / "Place_Bouton_PDF.py",
    DST / "place_bouton_v01.py",
    DST / "lib1",            # ancien dossier renomme en lib
    LIB / "config.py",       # ancien shim (settings.py importe directement)
    LIB / "options.py",      # ancien shim (settings.py importe directement)
]

# Extensions deployees
EXT_GEREES = {".py", ".cmd", ".css", ".yaml", ".docx", ".md", ".txt"}

# Ignorés dans prog/ pour le rapport "non repertories"
IGNORER_EXT = {".pyc", ".pyo", ".log"}
IGNORER_NOM = {"__pycache__", "__init__.py"}

# Regex : suffixe de version en fin de stem (_vX, _vX.Y, _vX_Y)
_RE_VER = re.compile(r'_v(\d+(?:[._]\d+)*)$', re.IGNORECASE)


# ─────────────────────────────────────────────────────────────────────
# AUTO-DECOUVERTE (recursive)
# ─────────────────────────────────────────────────────────────────────

def _cible(fichier: Path) -> tuple | None:
    """
    Deduit (chemin_cible, obligatoire) depuis le chemin source.

    Cas 1 — fichier a la RACINE de SRC avec prefixe lib_ :
        SRC/lib_xxx_vX.Y.py  ->  DST/lib/xxx.py    (compat. ancienne convention)

    Cas 2 — fichier dans un SOUS-DOSSIER de SRC :
        SRC/subdir/fichier_vX.Y.ext  ->  DST/subdir/fichier.ext  (miroir)

    Cas 3 — fichier a la RACINE de SRC sans prefixe lib_ :
        SRC/fichier_vX.Y.ext  ->  DST/fichier.ext
    """
    if fichier.suffix not in EXT_GEREES:
        return None
    m = _RE_VER.search(fichier.stem)
    if not m:
        return None

    base = fichier.stem[:m.start()]   # nom sans _vX.Y
    ext  = fichier.suffix
    rel  = fichier.relative_to(SRC)   # chemin relatif depuis SRC

    depth = len(rel.parts) - 1        # 0 = racine, 1 = sous-dossier, ...

    if depth == 0:
        # Fichier direct dans SRC
        if base.lower().startswith("lib_"):
            cible = LIB / (base[4:] + ext)    # lib_xxx -> lib/xxx
        else:
            cible = DST / (base + ext)
    else:
        # Sous-dossier : miroir de la structure
        sous_chemin = rel.parent      # ex: lib/ ou utils/
        cible = DST / sous_chemin / (base + ext)

    oblig = cible.name not in OPTIONNELS
    return cible, oblig


def decouvrir() -> list:
    """
    Scan recursif de SRC.
    - Ignore les dossiers nommes dans DOSSIERS_IGNORES (et leurs contenus).
    - Retourne [(nom_src_relatif, chemin_cible, obligatoire)] tries par cible.
    """
    res = []

    def _walk(dossier: Path):
        for item in sorted(dossier.iterdir()):
            if item.is_dir():
                if item.name.lower() in DOSSIERS_IGNORES:
                    continue
                _walk(item)
            else:
                r = _cible(item)
                if r:
                    res.append((str(item.relative_to(SRC)), r[0], r[1]))

    _walk(SRC)
    return sorted(res, key=lambda x: str(x[1]))


# ─────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────

def extraire_version(chemin: Path) -> str:
    try:
        c = chemin.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r'version\s*=\s*\([^,]+,\s*["\']([^"\']+)["\']', c)
        if m:
            return m.group(1)
        m = re.search(r'[Vv]ersion\s+([\d.]+)', c)
        if m:
            return m.group(1)
    except Exception:
        pass
    return "?"


def afficher(statut, src_r, dst_r, vs="", vd="", note=""):
    cs  = str(src_r)[:42].ljust(42)
    cd  = str(dst_r)[:30].ljust(30)
    ver = f"  v{vs} -> v{vd}" if (vs or vd) else ""
    nt  = f"  [{note}]" if note else ""
    print(f"  {statut:<8} {cs} -> {cd}{ver}{nt}")


def rel(p: Path) -> Path:
    try:    return p.relative_to(RACINE)
    except: return p


# ─────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────

def main():
    print()
    print("=" * 76)
    print("  remplace.py v16  —  deploiement automatique (scan recursif)")
    print(f"  Source : {SRC}")
    print(f"  Cible  : {DST}")
    print("=" * 76)

    erreurs = copies = a_jour = 0

    # Verifier SRC
    if not SRC.exists():
        print(f"  ERREUR : dossier source introuvable : {SRC}")
        sys.exit(1)

    # Creer DST et LIB si absent (1er deploiement)
    for d in (DST, LIB):
        if not d.exists():
            d.mkdir(parents=True, exist_ok=True)
            print(f"  CREE    {rel(d)}\\")

    # ── Auto-decouverte ───────────────────────────────────────────────
    FICHIERS = decouvrir()
    print()
    print(f"  {len(FICHIERS)} fichier(s) decouvert(s) dans {rel(SRC)}")
    print()
    print("  DEPLOIEMENT")
    print()

    # Index des cibles connues par dossier (pour rapport "non repertories")
    cibles_par_dossier: dict[Path, set] = {}

    for nom_src, chemin_dst, obligatoire in FICHIERS:
        chemin_src = SRC / nom_src
        parent = chemin_dst.parent
        cibles_par_dossier.setdefault(parent, set()).add(chemin_dst.name)

        if not chemin_src.exists():
            note = "OBLIGATOIRE" if obligatoire else "optionnel"
            afficher("ABSENT", rel(chemin_src), rel(chemin_dst), note=note)
            if obligatoire:
                erreurs += 1
            continue

        vs = extraire_version(chemin_src)
        vd = extraire_version(chemin_dst) if chemin_dst.exists() else "—"

        if vs == vd:
            afficher("OK",    rel(chemin_src), rel(chemin_dst), vs, vd, "a jour")
            a_jour += 1
        else:
            chemin_dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(chemin_src), str(chemin_dst))
            afficher("COPIE", rel(chemin_src), rel(chemin_dst), vs, vd)
            copies += 1

    # ── Suppressions ─────────────────────────────────────────────────
    print()
    print("  SUPPRESSIONS (anciens fichiers)")
    print()
    for chemin in SUPPRIMER:
        chemin = Path(chemin)
        if chemin.is_dir():
            shutil.rmtree(str(chemin))
            print(f"  SUPPRIME {rel(chemin)}\\  (dossier)")
        elif chemin.exists():
            chemin.unlink()
            print(f"  SUPPRIME {rel(chemin)}")
        else:
            print(f"  ABSENT   {rel(chemin)}  (deja supprime)")

    # ── Rapport fichiers non repertories ─────────────────────────────
    def inconnus_dans(dossier: Path, connus: set) -> list:
        if not dossier.exists():
            return []
        res = []
        for f in dossier.iterdir():
            if f.is_dir() or f.suffix in IGNORER_EXT or f.name in IGNORER_NOM:
                continue
            if f.name not in connus:
                res.append(f)
        return sorted(res)

    total_inconnus = 0
    premiere_ligne = True
    for dossier, connus in sorted(cibles_par_dossier.items()):
        inc = inconnus_dans(dossier, connus)
        if inc:
            if premiere_ligne:
                print()
                print("  FICHIERS NON REPERTORIES (a verifier / supprimer manuellement)")
                print()
                premiere_ligne = False
            prefix = str(rel(dossier)) + "\\"
            for f in inc:
                print(f"  ?? {prefix}{f.name:<44}  v{extraire_version(f)}")
            total_inconnus += len(inc)

    if premiere_ligne:
        print()
        print("  Aucun fichier non repertorie dans prog\\ et sous-dossiers")

    # ── Structure html\ pour node.js local ──────────────────────────
    # html\Hebreu4.0\html\style.css est requis pour la consultation locale
    # (node.js sert html\ mais le CSS est genere dans prog\ par genere_site)
    style_src = DST / "style.css"
    style_dst_dir = RACINE / "html" / "Hebreu4.0" / "html"
    style_dst = style_dst_dir / "style.css"

    print()
    print("  STRUCTURE HTML (consultation locale node.js)")
    print()
    if not style_src.exists():
        print(f"  ABSENT   prog\style.css — copie impossible (lancer remplace.py apres le 1er deploiement)")
    else:
        style_dst_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(style_src), str(style_dst))
        print(f"  OK       html\Hebreu4.0\html\style.css cree/mis a jour")

    # ── Bilan ─────────────────────────────────────────────────────────
    print()
    print("=" * 76)
    if erreurs:
        print(f"  ATTENTION : {erreurs} erreur(s) — voir ABSENT OBLIGATOIRE ci-dessus")
    else:
        extra = f"   {total_inconnus} non repertorie(s)" if total_inconnus else ""
        print(f"  OK : {copies} copie(s)   {a_jour} deja a jour{extra}")
    print("=" * 76)
    print()

    sys.exit(1 if erreurs else 0)


if __name__ == "__main__":
    main()

# fin remplace.py — Version 15
