#/bin/bash
sfdp -Tpdf $1.dot -o $1.pdf -Nlabel='' -Nnodesep='12' -Nshape='point' -Nwidth='0.01' -Ncolor='#6600FF' -Ecolor='#00000040' -splines='true' -GK='0.9'
