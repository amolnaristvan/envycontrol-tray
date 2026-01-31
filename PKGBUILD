# Maintainer: amolnaristvan <https://github.com>
pkgname=envycontrol-tray
pkgver=1.0.0
pkgrel=1
pkgdesc="A simple GTK tray application for switching GPU modes using EnvyControl"
arch=('any')
url="https://github.com"
license=('MIT')
depends=('python' 'python-gobject' 'gtk3' 'envycontrol' 'polkit')
optdepends=('libappindicator-gtk3: Status icon support for GNOME and KDE Plasma')
source=("envycontrol-tray.py"
        "envycontrol-tray.desktop"
        "prime-intel.png"
        "prime-nvidia.png"
        "prime-hybrid.png"
        "LICENSE")
sha256sums=('SKIP' 'SKIP' 'SKIP' 'SKIP' 'SKIP' 'SKIP')

package() {
    # 1. Program telepítése kiterjesztés nélkül
    install -Dm755 "${srcdir}/envycontrol-tray.py" "${pkgdir}/usr/bin/envycontrol-tray"
    
    # 2. Ikonok telepítése a várt helyre
    install -d "${pkgdir}/usr/share/envycontrol-tray"
    install -m644 "${srcdir}/prime-intel.png"  "${pkgdir}/usr/share/envycontrol-tray/prime-intel.png"
    install -m644 "${srcdir}/prime-nvidia.png" "${pkgdir}/usr/share/envycontrol-tray/prime-nvidia.png"
    install -m644 "${srcdir}/prime-hybrid.png" "${pkgdir}/usr/share/envycontrol-tray/prime-hybrid.png"

    # 3. Menü bejegyzés
    install -Dm644 "${srcdir}/envycontrol-tray.desktop" "${pkgdir}/usr/share/applications/envycontrol-tray.desktop"

    # 4. Automatikus indítás minden bejelentkezéskor
    install -Dm644 "${srcdir}/envycontrol-tray.desktop" "${pkgdir}/etc/xdg/autostart/envycontrol-tray.desktop"

    # 5. Licenc telepítése
    install -Dm644 "${srcdir}/LICENSE" "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
}
