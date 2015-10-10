#/bin/bash
neato -Tpdf $1.dot -o $1.pdf -Nlabel='' -Nnodesep='12' -Nshape='point' -Nwidth='0.01' -Ncolor='#6600FF' -Ecolor='#00000040' 
