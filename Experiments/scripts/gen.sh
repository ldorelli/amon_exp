#/bin/bash
neato -Gratio=0.13 -Tsvg $1.dot -o $1.svg -Ncolor='#00000000' -Nshape='point' -Esize=0.3 -Ecolor='#A2AADBCC:#70B89BCC;0.5' -Earrowshape='crow' -Earrowsize=0.3
