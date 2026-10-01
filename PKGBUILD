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
# _commit pins an exact snapshot so builds are reproducible.
_commit=8aa8fe5aab159333ace615b2520f7079a19a8fb9
source=("$url/archive/$_commit.tar.gz")
sha256sums=('c8ca6ac8adccd2684f15e24e5eadd9920afcd2cafb97c4c289505ac72f154b32')

package() {
    # The GitHub tarball unpacks into a directory named after the
    # full commit sha.
    local _src=thinkpad_remapper-$_commit

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