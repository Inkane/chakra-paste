# Maintainer: Inkane <neoinkaneglade@aol.com> 

pkgname="chakra-paste-git"
pkgver=0.1
pkgrel=2
pkgdesc="Allows to upload text files to paste.chakra-project.org"
arch=("any")
url="https://github.com/Inkane/chakra-paste"
license=('BSD')
makedepends=('git')

_gitroot="git://github.com/Inkane/chakra-paste.git"
_gitname="chakra-paste"

package() {
  cd "$srcdir"
  msg "Connecting to GIT server...."

  if [[ -d "$_gitname" ]]; then
    cd "$_gitname" && git pull origin
    msg "The local files are updated."
  else
    git clone "$_gitroot" "$_gitname"
  fi

  msg "GIT checkout done or server timeout"
  msg "Starting build..."

  rm -rf "$srcdir/$_gitname-build"
  git clone "$srcdir/$_gitname" "$srcdir/$_gitname-build"
  cd "$srcdir/$_gitname-build"
  python2 setup.py install --root="${pkgdir}"

}

# vim:set ts=2 sw=2 et:
