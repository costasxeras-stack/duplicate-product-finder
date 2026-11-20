#!/bin/sh
# Downloads the Walmart-Amazon and Abt-Buy benchmark splits from the Ditto repository (Apache 2.0) into work/.
set -e
mkdir -p work && cd work
for ds in "Structured/Walmart-Amazon" "Textual/Abt-Buy"; do
  n=$(basename "$ds"); mkdir -p "$n"
  for s in train valid test; do curl -sSfL -o "$n/$s.txt" "https://raw.githubusercontent.com/megagonlabs/ditto/master/data/er_magellan/$ds/$s.txt"; done
done
echo "Downloaded to work/"
