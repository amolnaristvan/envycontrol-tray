#!/usr/bin/env python3
# License: MIT
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")

from gi.repository import Gtk, GLib, AppIndicator3
import subprocess
import os
import threading
import locale

# --- TRANSLATION TABLE ---
LANG_TABLE = {
    "hu": {
        "menu_intel":  "Integrált (Intel)",
        "menu_nvidia": "NVIDIA",
        "menu_hybrid": "Hibrid (On-Demand)",
        "menu_quit":   "Kilépés",
        "dlg_reboot_q": "A módosítások érvényesítéséhez újraindítás szükséges. Újraindítja most?",
        "dlg_yes": "Igen", "dlg_no": "Nem",
    },
    "de": {
        "menu_intel":  "Integriert (Intel)",
        "menu_nvidia": "NVIDIA",
        "menu_hybrid": "Hybrid (On-Demand)",
        "menu_quit":   "Beenden",
        "dlg_reboot_q": "Ein Neustart ist erforderlich. Jetzt neu starten?",
        "dlg_yes": "Ja", "dlg_no": "Nein",
    },
    "fr": {
        "menu_intel":  "Intégré (Intel)",
        "menu_nvidia": "NVIDIA",
        "menu_hybrid": "Hybride (On-Demand)",
        "menu_quit":   "Quitter",
        "dlg_reboot_q": "Un redémarrage est nécessaire. Redémarrer maintenant ?",
        "dlg_yes": "Oui", "dlg_no": "Non",
    },
    "es": {
        "menu_intel":  "Integrada (Intel)",
        "menu_nvidia": "NVIDIA",
        "menu_hybrid": "Híbrida (On-Demand)",
        "menu_quit":   "Salir",
        "dlg_reboot_q": "Se requiere un reinicio. ¿Reiniciar ahora?",
        "dlg_yes": "Sí", "dlg_no": "No",
    },
    "en": {
        "menu_intel":  "Integrated (Intel)",
        "menu_nvidia": "NVIDIA",
        "menu_hybrid": "Hybrid (On-Demand)",
        "menu_quit":   "Quit",
        "dlg_reboot_q": "A reboot is required to apply changes. Reboot now?",
        "dlg_yes": "Yes", "dlg_no": "No",
    }
}

def get_lang():
    try:
        loc = locale.getdefaultlocale()[0]
        if loc:
            lang = loc.split("_")[0].lower()
            if lang in LANG_TABLE:
                return lang
    except:
        pass
    return "en"

T = LANG_TABLE[get_lang()]

ICON_BASE = "/usr/share/envycontrol-tray"
ICONS = {
    "intel":  os.path.join(ICON_BASE, "prime-intel.png"),
    "nvidia": os.path.join(ICON_BASE, "prime-nvidia.png"),
    "hybrid": os.path.join(ICON_BASE, "prime-hybrid.png"),
}

def query_current_mode():
    try:
        out = subprocess.check_output(["envycontrol", "-q"], text=True).lower()
        if "integrated" in out: return "intel"
        if "nvidia" in out: return "nvidia"
        if "hybrid" in out: return "hybrid"
    except:
        return None
    return None

def ask_reboot():
    def _show():
        dialog = Gtk.MessageDialog(
            transient_for=None,
            flags=0,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.NONE,
            text=T["dlg_reboot_q"]
        )
        dialog.add_button(T["dlg_yes"], Gtk.ResponseType.YES)
        dialog.add_button(T["dlg_no"], Gtk.ResponseType.NO)

        response = dialog.run()
        if response == Gtk.ResponseType.YES:
            subprocess.Popen(["systemctl", "reboot"])
        dialog.destroy()
    GLib.idle_add(_show)

class GpuTray:
    def __init__(self):
        self.ind = AppIndicator3.Indicator.new(
            "envycontrol-tray",
            ICONS["intel"],
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.ind.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        self.menu = Gtk.Menu()

        for mode in ["intel", "nvidia", "hybrid"]:
            item = Gtk.MenuItem(label=T[f"menu_{mode}"])
            item.connect("activate", self.switch_mode, mode)
            self.menu.append(item)

        self.menu.append(Gtk.SeparatorMenuItem())

        item_quit = Gtk.MenuItem(label=T["menu_quit"])
        item_quit.connect("activate", lambda _: Gtk.main_quit())
        self.menu.append(item_quit)

        self.menu.show_all()
        self.ind.set_menu(self.menu)

        self.refresh()

    def refresh(self):
        mode = query_current_mode()
        if mode and os.path.exists(ICONS[mode]):
            self.ind.set_icon_full(ICONS[mode], mode)

    def switch_mode(self, widget, mode):
        cmd_map = {"intel": "integrated", "nvidia": "nvidia", "hybrid": "hybrid"}

        def worker():
            res = subprocess.run(
                ["pkexec", "envycontrol", "-s", cmd_map[mode]],
                text=True, capture_output=True
            )
            out = (res.stdout + res.stderr).lower()
            GLib.idle_add(self.refresh)
            if "reboot" in out:
                ask_reboot()

        threading.Thread(target=worker, daemon=True).start()

if __name__ == "__main__":
    GpuTray()
    Gtk.main()
