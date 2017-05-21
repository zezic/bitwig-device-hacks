#!/bin/bash
cd "$(dirname "${0}")"

python repack.py || exit ${?}
sudo cp resources/MathX.bwmodulator /opt/bitwig-studio/Library/modulators/
