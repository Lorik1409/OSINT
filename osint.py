# -*- coding: utf-8 -*-

# ============================================================
# OSINT - OSINT TOOL
# Made by Lorik
# ============================================================

import os
import sys
import webbrowser
from html.parser import HTMLParser
from pathlib import Path

PAGE_SIZE = 12
CURRENT_LANG = "de"  # Standard-Sprache: Deutsch

# Terminal Farben
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"

def c(text, color=WHITE, bold=False):
    prefix = color + (BOLD if bold else "")
    return f"{prefix}{text}{RESET}"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def header():
    print(c("═" * 78, CYAN))
    print(c("   ██████╗ ███████╗██╗███╗   ██╗████████╗    ████████╗ ██████╗  ██████╗ ██╗", CYAN, True))
    print(c("  ██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║", CYAN, True))
    print(c("  ██║   ██║███████╗██║██╔██╗ ██║   ██║          ██║   ██║   ██║██║   ██║██║", CYAN, True))
    print(c("  ██║   ██║╚════██║██║██║╚██╗██║   ██║          ██║   ██║   ██║██║   ██║██║", CYAN, True))
    print(c("  ╚██████╔╝███████║██║██║ ╚████║   ██║          ██║   ╚██████╔╝╚██████╔╝███████╗", CYAN, True))
    print(c("   ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝          ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝", CYAN, True))
    print(c("                              Made by Lorik", MAGENTA, True))
    print(c("═" * 78, CYAN))

# ============================================================
# ÜBERSETZUNGEN (UI, TASTEN & LINKS)
# ============================================================

UI = {
    "de": {
        "search": "[S] Suche", "lang": "[L] Sprache", "prev_group": "Vorherige Gruppe",
        "next_group": "Nächste Gruppe", "exit": "[0] Beenden", "page": "Seite",
        "of": "von", "input": "Eingabe", "search_term": "Suchbegriff",
        "no_results": "Keine Ergebnisse gefunden. Drücke Enter...", "back": "[0] Zurück",
        "prev_page": "[P] Vorherige Seite", "next_page": "[N] Nächste Seite", "links": "Links",
        "choose_lang": "Wähle eine Sprache / Choose a language / Choisir une langue / Elija un idioma:",
        "key_next": "n", "key_prev": "p"
    },
    "en": {
        "search": "[S] Search", "lang": "[L] Language", "prev_group": "Previous Group",
        "next_group": "Next Group", "exit": "[0] Exit", "page": "Page",
        "of": "of", "input": "Input", "search_term": "Search term",
        "no_results": "No results found. Press Enter...", "back": "[0] Back",
        "prev_page": "[P] Previous Page", "next_page": "[N] Next Page", "links": "Links",
        "choose_lang": "Choose a language / Wähle eine Sprache / Choisir une langue / Elija un idioma:",
        "key_next": "n", "key_prev": "p"
    },
    "fr": {
        "search": "[S] Recherche", "lang": "[L] Langue", "prev_group": "Groupe Précédent",
        "next_group": "Groupe Suivant", "exit": "[0] Quitter", "page": "Page",
        "of": "sur", "input": "Entrée", "search_term": "Terme de recherche",
        "no_results": "Aucun résultat trouvé. Appuyez sur Entrée...", "back": "[0] Retour",
        "prev_page": "[P] Page Précédente", "next_page": "[S] Page Suivante", "links": "Liens",
        "choose_lang": "Choisir une langue / Wähle eine Sprache / Choose a language / Elija un idioma:",
        "key_next": "s", "key_prev": "p"
    },
    "es": {
        "search": "[S] Buscar", "lang": "[L] Idioma", "prev_group": "Grupo anterior",
        "next_group": "Siguiente grupo", "exit": "[0] Salir", "page": "Página",
        "of": "de", "input": "Entrada", "search_term": "Término de búsqueda",
        "no_results": "No se encontraron resultados. Presiona Enter...", "back": "[0] Volver",
        "prev_page": "[A] Página anterior", "next_page": "[S] Página siguiente", "links": "Enlaces",
        "choose_lang": "Elija un idioma / Wähle eine Sprache / Choose a language / Choisir une langue:",
        "key_next": "s", "key_prev": "a"
    }
}

# HIER KATEGORIEN EINTRAGEN
CATEGORY_TRANSLATIONS = {
    "THROWAWAY CONTACT": {"de": "EINWEG-KONTAKTE", "en": "THROWAWAY CONTACT", "fr": "CONTACTS JETABLES", "es": "CONTACTOS DESCARTABLES"},
    "Social Media": {"de": "Soziale Medien", "en": "Social Media", "fr": "Réseaux Sociaux", "es": "Redes Sociales"},
    "People / Identity": {"de": "Personen / Identität", "en": "People / Identity", "fr": "Personnes / Identité", "es": "Personas / Identidad"},
    "Search": {"de": "Suche", "en": "Search", "fr": "Recherche", "es": "Búsqueda"},
}

# HIER DEINE EINZELNEN LINKS EINTRAGEN
LINK_TRANSLATIONS = {
    "Send text free": {"de": "Gratis SMS senden", "en": "Send text free", "fr": "Envoyer SMS gratuit", "es": "Enviar SMS gratis"},
    "Free Fax": {"de": "Gratis Fax", "en": "Free Fax", "fr": "Fax gratuit", "es": "Fax gratis"},
    "Receive SMS Online": {"de": "SMS online empfangen", "en": "Receive SMS Online", "fr": "Recevoir SMS en ligne", "es": "Recibir SMS en línea"},
    "Receive SMS Online for FREE": {"de": "SMS online empfangen (Gratis)", "en": "Receive SMS Online for FREE", "fr": "Recevoir SMS en ligne (Gratuit)", "es": "Recibir SMS en línea gratis"},
    "Receive SMS Online For Free": {"de": "SMS online empfangen (Gratis)", "en": "Receive SMS Online For Free", "fr": "Recevoir SMS en ligne (Gratuit)", "es": "Recibir SMS en línea gratis"},
    "VoIP Guide: VoIPSuite": {"de": "VoIP Anleitung: VoIPSuite", "en": "VoIP Guide: VoIPSuite", "fr": "Guide VoIP: VoIPSuite", "es": "Guía VoIP: VoIPSuite"},
    "Twilio CLI Guide": {"de": "Twilio CLI Anleitung", "en": "Twilio CLI Guide", "fr": "Guide CLI Twilio", "es": "Guía CLI Twilio"},
}

def t(key):
    return UI[CURRENT_LANG].get(key, key)

def t_cat(cat_name):
    for original_name, translations in CATEGORY_TRANSLATIONS.items():
        if cat_name.lower() == original_name.lower() or cat_name.lower() == translations["de"].lower():
            if CURRENT_LANG in translations:
                return translations[CURRENT_LANG]
    return cat_name

def t_link(link_title):
    title_stripped = link_title.strip()
    for original_name, translations in LINK_TRANSLATIONS.items():
        if title_stripped.lower() == original_name.lower() or title_stripped.lower() == translations["de"].lower():
            if CURRENT_LANG in translations:
                return translations[CURRENT_LANG]
    return title_stripped

# ============================================================
# PARSER & LOGIK
# ============================================================

class BookmarkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.current_category = None
        self.current_title = ""
        self.current_href = None
        self.in_h3 = False
        self.in_a = False
        self.categories = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "h3":
            self.in_h3 = True
            self.current_title = ""
        elif tag == "a":
            self.in_a = True
            self.current_title = ""
            self.current_href = attrs.get("href", "")

    def handle_endtag(self, tag):
        if tag == "h3":
            self.in_h3 = False
            name = self.current_title.strip()
            if name and name != "OSINT":
                self.current_category = name
                self.categories.setdefault(name, [])
        elif tag == "a":
            self.in_a = False
            if self.current_category and self.current_title:
                self.categories[self.current_category].append(
                    (self.current_title.strip(), self.current_href or "")
                )
            self.current_title = ""
            self.current_href = None

    def handle_data(self, data):
        if self.in_h3 or self.in_a:
            self.current_title += data

def load_bookmarks():
    filename = Path("bookmarks.html")
    if not filename.exists():
        filename = Path("Export-2026-9-20-00e1a615adfe097e.html")
    
    if not filename.exists():
        print("FEHLER / ERROR / ERREUR / ERROR: HTML-Datei nicht gefunden!")
        input("\nDrücke Enter...")
        sys.exit(1)

    parser = BookmarkParser()
    parser.feed(filename.read_text(encoding="utf-8", errors="replace"))
    return {cat: items for cat, items in parser.categories.items() if items}

def change_language():
    global CURRENT_LANG
    clear()
    header()
    print(f"\n  {t('choose_lang')}\n")
    print(f"  {c('[1]', GREEN, True)} Deutsch")
    print(f"  {c('[2]', GREEN, True)} English")
    print(f"  {c('[3]', GREEN, True)} Français")
    print(f"  {c('[4]', GREEN, True)} Español")
    print(f"\n  {t('back')}")
    
    choice = input(f"\n  > ").strip()
    if choice == "1":
        CURRENT_LANG = "de"
    elif choice == "2":
        CURRENT_LANG = "en"
    elif choice == "3":
        CURRENT_LANG = "fr"
    elif choice == "4":
        CURRENT_LANG = "es"

def bookmark_menu(category, items):
    page = 0
    total_pages = max(1, (len(items) + PAGE_SIZE - 1) // PAGE_SIZE)

    while True:
        clear()
        header()
        print(f"\n[{category}] — {len(items)} {t('links')}\n")

        start = page * PAGE_SIZE
        visible = items[start:start + PAGE_SIZE]

        for i, (title, url) in enumerate(visible, 1):
            display_title = t_link(title)
            print(f"  {c(f'[{i}]', GREEN, True)} {c(display_title, WHITE, True)}")

        print("\n" + c("─" * 40, CYAN))
        print(f"  {t('back')}")
        if page > 0:
            print(f"  {t('prev_page')}")
        if page < total_pages - 1:
            print(f"  {t('next_page')}")
        
        print(c(f"\n  {t('page')} {page + 1} {t('of')} {total_pages}", YELLOW, True))

        choice = input(f"\n{t('input')}: ").strip().lower()
        key_n = UI[CURRENT_LANG]["key_next"]
        key_p = UI[CURRENT_LANG]["key_prev"]

        if choice == "0":
            return
        elif choice == key_n and page < total_pages - 1:
            page += 1
        elif choice == key_p and page > 0:
            page -= 1
        else:
            try:
                num = int(choice)
                if 1 <= num <= len(visible):
                    _, url = visible[num - 1]
                    webbrowser.open(url)
            except ValueError:
                pass

def main():
    categories = load_bookmarks()
    cat_keys = list(categories.keys())
    total_pages = len(cat_keys)

    current_page = 0

    while True:
        clear()
        header()
        
        cat_name = cat_keys[current_page]
        display_cat_name = t_cat(cat_name) 
        items = categories[cat_name]

        print(f"\n── {display_cat_name} ──\n")

        for i, (title, url) in enumerate(items[:15], 1):
            display_title = t_link(title)
            print(f"  {c(f'[{i}]', GREEN, True)} {c(display_title, WHITE, True)}")

        print("\n")
        print(f"  {t('search')}   {t('lang')}")
        print()

        key_n = UI[CURRENT_LANG]["key_next"]
        key_p = UI[CURRENT_LANG]["key_prev"]

        if current_page > 0:
            prev_group_name = t_cat(cat_keys[current_page - 1])
            print(f"  [{key_p.upper()}] {t('prev_group')} ({prev_group_name})")

        if current_page < total_pages - 1:
            next_group_name = t_cat(cat_keys[current_page + 1])
            print(f"  [{key_n.upper()}] {t('next_group')} ({next_group_name})")

        print(f"  {t('exit')}")
        print(c(f"\n  {t('page')} {current_page + 1} {t('of')} {total_pages}", YELLOW, True))

        choice = input(f"\n{t('input')}: ").strip().lower()

        if choice == "0":
            clear()
            print("OSINT - Beendet / Exit.")
            sys.exit()
        elif choice == "l":
            change_language()
        elif choice == key_n and current_page < total_pages - 1:
            current_page += 1
        elif choice == key_p and current_page > 0:
            current_page -= 1
        elif choice == "s":
            term = input(f"\n{t('search_term')}: ").strip().lower()
            if term:
                found = []
                for c_name, c_items in categories.items():
                    c_display = t_cat(c_name)
                    for title, url in c_items:
                        t_translated = t_link(title)
                        if term in title.lower() or term in url.lower() or term in t_translated.lower():
                            found.append((c_display, title, url))
                if found:
                    bookmark_menu(f"'{term}'", [(f"[{c_n}] {t}", u) for c_n, t, u in found])
                else:
                    input(f"{t('no_results')}")
        else:
            try:
                num = int(choice)
                if 1 <= num <= min(15, len(items)):
                    _, url = items[num - 1]
                    webbrowser.open(url)
            except ValueError:
                pass

if __name__ == "__main__":
    main()