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
source=("${pkgname}-${pkgver}.tar.gz::${url}/archive/refs/tags/v${pkgver}.tar.gz")
sha256sums=('SKIP')

package() {
    # Belépés a kicsomagolt mappába
    cd "${srcdir}/${pkgname}-${pkgver}"

    # 1. Program telepítése kiterjesztés nélkül
    install -Dm755 "envycontrol-tray.py" "${pkgdir}/usr/bin/envycontrol-tray"
    
    # 2. Ikonok telepítése a várt helyre
    install -d "${pkgdir}/usr/share/envycontrol-tray"
    install -m644 "prime-intel.png"  "${pkgdir}/usr/share/envycontrol-tray/prime-intel.png"
    install -m644 "prime-nvidia.png" "${pkgdir}/usr/share/envycontrol-tray/prime-nvidia.png"
    install -m644 "prime-hybrid.png" "${pkgdir}/usr/share/envycontrol-tray/prime-hybrid.png"

    # 3. Menü bejegyzés
    install -Dm644 "envycontrol-tray.desktop" "${pkgdir}/usr/share/applications/envycontrol-tray.desktop"

    # 4. Automatikus indítás minden bejelentkezéskor
    install -Dm644 "envycontrol-tray.desktop" "${pkgdir}/etc/xdg/autostart/envycontrol-tray.desktop"

    # 5. Licenc
    install -Dm644 "LICENSE" "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
}
