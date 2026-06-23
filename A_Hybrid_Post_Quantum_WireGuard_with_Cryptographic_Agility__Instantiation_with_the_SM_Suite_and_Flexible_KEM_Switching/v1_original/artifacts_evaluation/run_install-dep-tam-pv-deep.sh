#!/bin/sh

#
# Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
#

## /!\ root password is required /!\ 
## /!\ when prompted to choose options: always press ENTER (this will select default option) /!\ 

sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1
sudo sysctl -w net.ipv6.conf.default.disable_ipv6=1
sudo sysctl -w net.ipv6.conf.lo.disable_ipv6=1

sudo apt remove -y needrestart 
sudo add-apt-repository --remove ppa:avsm/ppa -y
sudo apt update -y
sudo apt full-upgrade -y
sudo apt install software-properties-common -y
sudo apt install rename time libgtk2.0-dev pkg-config opam haskell-stack curl make unzip graphviz build-essential bubblewrap parallel python3-pip locales -y

pip3 install sympy --break-system-packages --no-warn-script-location

curl -L https://github.com/maude-lang/Maude/releases/download/Maude3.5/Maude-3.5-linux-x86_64.zip > maude.zip
unzip -oj maude.zip -d ~/.local/bin/
chmod a+x ~/.local/bin/maude
rm maude.zip

git clone https://github.com/tamarin-prover/tamarin-prover.git
cd tamarin-prover
stack update
stack upgrade
git checkout master
make default
cd ..

bash -c "sh <(curl -fsSL https://raw.githubusercontent.com/ocaml/opam/master/shell/install.sh)"
opam init
opam update 
opam install "proverif=2.05"

eval $(opam env)

opam install ocamlbuild
git clone https://github.com/DeepSec-prover/deepsec.git
cd deepsec
make
cp deepsec $HOME/.local/bin/
cp deepsec_worker $HOME/.local/bin/
cp deepsec_api $HOME/.local/bin/
cd ..