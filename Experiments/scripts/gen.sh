#/bin/bash
sfdp -Tpdf $1.dot -o $1.pdf -Eedgecolor='red;blue' -Nshape='point' -Esize=0.3 -Ecolor='#DA91E0AA:#72D0C3AA;0.5' -Earrowshape='crow' -Earrowsize=0.3
