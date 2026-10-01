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

# Source comes straight from the upstream git repo on GitHub.
# master.tar.gz follows the default branch, so the checksum is
# intentionally SKIP — a moving target cannot be pinned.
source=("$url/archive/refs/heads/master.tar.gz")
sha256sums=('SKIP')

package() {
    # The GitHub master tarball unpacks into a directory named
    # after the repo + branch.
    local _src=thinkpad_remapper-master

    # Script
    install -Dm755 "${srcdir}/${_src}/thinkpad_remapper.py" \
        "${pkgdir}/usr/local/bin/thinkpad_remapper.py"

    # Systemd unit
    install -Dm644 "${srcdir}/${_src}/thinkpad-remapper.service" \
        "${pkgdir}/usr/lib/systemd/system/thinkpad-remapper.service"

    # A module-load line so uinput exists after a reboot (the service
    # runs early and grabs the keyboard).
    install -Dm644 /dev/null \
        "${pkgdir}/usr/lib/modules-load.d/thinkpad-remapper.conf"
    printf 'uinput\n' > \
        "${pkgdir}/usr/lib/modules-load.d/thinkpad-remapper.conf"
}