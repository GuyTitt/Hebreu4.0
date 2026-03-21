# serveur_manuels_v1.0.py — Version 1.0
# v1.0 : creation
#   Serveur HTTP local pour consulter la documentation HTML.
#   Lance un serveur sur le port 3501 (ou PORT passe en argument)
#   et ouvre automatiquement index.html dans le navigateur.
#
# Usage :
#   python serveur_manuel.py          (port 3501 par defaut)
#   python serveur_manuel.py 3502     (port personnalise)
#   Double-clic sur serveur_manuel.py

import sys
import os
import threading
import webbrowser
import time
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler

version = ("serveur_manuels.py", "1.0")

# ─────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────
PORT_DEFAUT = 3501
DOSSIER     = Path(__file__).parent   # dossier du script = manuel\


# ─────────────────────────────────────────────────────────────────────
# HANDLER silencieux (pas de log de chaque requete)
# ─────────────────────────────────────────────────────────────────────
class HandlerSilencieux(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass   # supprimer les logs HTTP dans la console

    def log_error(self, format, *args):
        # Afficher quand meme les erreurs reelles (404, etc.)
        print(f"  [!] {format % args}")


# ─────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────
def main():
    # Port depuis argument ou defaut
    port = PORT_DEFAUT
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"  Port invalide '{sys.argv[1]}' — utilisation de {PORT_DEFAUT}")

    # Se placer dans le dossier du script
    os.chdir(DOSSIER)

    # Activer les couleurs ANSI sur Windows
    os.system("")

    print()
    print("\033[1m\033[94m" + "=" * 52 + "\033[0m")
    print("\033[1m  Documentation Hébreu4.0 — Serveur local\033[0m")
    print(f"\033[94m" + "=" * 52 + "\033[0m")
    print(f"  Dossier : {DOSSIER}")
    print(f"  Adresse : \033[92mhttp://localhost:{port}/index.html\033[0m")
    print(f"  Arrêt   : Ctrl+C")
    print("\033[94m" + "=" * 52 + "\033[0m")
    print()

    # Vérifier que index.html existe
    if not (DOSSIER / "index.html").exists():
        print("  \033[93mATTENTION : index.html absent dans ce dossier\033[0m")
        print(f"  Dossier servi : {DOSSIER}")
        print()

    # Ouvrir le navigateur après un délai court
    def ouvrir_navigateur():
        time.sleep(0.8)
        webbrowser.open(f"http://localhost:{port}/index.html")

    threading.Thread(target=ouvrir_navigateur, daemon=True).start()

    # Démarrer le serveur
    try:
        serveur = HTTPServer(("", port), HandlerSilencieux)
        print(f"  Serveur démarré sur le port {port}...")
        print()
        serveur.serve_forever()
    except OSError as e:
        if "Address already in use" in str(e) or "10048" in str(e):
            print(f"  \033[91mERREUR : le port {port} est déjà utilisé.\033[0m")
            print(f"  Essayez un autre port : python serveur_manuel.py {port + 1}")
        else:
            print(f"  \033[91mERREUR : {e}\033[0m")
        sys.exit(1)
    except KeyboardInterrupt:
        print()
        print("  Serveur arrêté.")
        print()


if __name__ == "__main__":
    main()

# fin serveur_manuels_v1.0.py — Version 1.0
