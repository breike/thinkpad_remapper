# Maintainer: Rusty <rusty@localhost>
# Contributor: t184256 <https://github.com/t184256>

pkgname=thinkpad_remapper
pkgver=0.1.0
pkgrel=1
pkgdesc="Remap the ThinkPad built-in keyboard (evdev grab, uinput inject)"
arch=('any')
url="https://github.com/breike/laptop_remapper"
license=('CC0-1.0')
depends=('python' 'python-evdev')
install=thinkpad_remapper.install

source=("thinkpad_remapper.py"
        "thinkpad-remapper.service"
        "thinkpad_remapper.install")
sha256sums=('SKIP'
            'SKIP'
            'SKIP')

package() {
    # Script
    install -Dm755 "${srcdir}/thinkpad_remapper.py" \
        "${pkgdir}/usr/local/bin/thinkpad_remapper.py"

    # Systemd unit
    install -Dm644 "${srcdir}/thinkpad-remapper.service" \
        "${pkgdir}/usr/lib/systemd/system/thinkpad-remapper.service"

    # A module-load line so uinput exists after a reboot (the service
    # runs early and grabs the keyboard).
    install -Dm644 /dev/null \
        "${pkgdir}/usr/lib/modules-load.d/thinkpad-remapper.conf"
    printf 'uinput\n' > \
        "${pkgdir}/usr/lib/modules-load.d/thinkpad-remapper.conf"
}