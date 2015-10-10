#/bin/bash
sfdp -Tpdf $1.dot -o $1.pdf -Nlabel='' -Nshape='point' -Nwidth='0.01' -Ncolor='#6600FF' -Ecolor='#00000077' 
