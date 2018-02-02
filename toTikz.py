#This file permits to display disk graphs in pdf.
#TikZ code is generated, readily compilable.

#typical use:
#python toTikz.py < solution.txt > sol.tex
#See disks.py to make it work to generate solution.tex

###########
# Display #
###########

import sys

scale=8
col="red"
cont="red"   

print("\documentclass{minimal}\n\\usepackage{tikz}\n\\begin{document}\n\\begin{tikzpicture}")

cpt = 1
        
for l in sys.stdin:
    opacity=0.2
    foo,label = l.split(';')
    x,y,r = foo.split(',')
    x = x[1:].strip()
    r = r[:-2].strip()
    y=y.strip()
    x = str(float(x)*scale)
    y = str(float(y)*scale)
    r = str(float(r)*scale)    
    print ("\\draw[color="+cont+", fill="+col+", fill opacity="+str(opacity)+"] (" + x + ", " + y + ") circle ("+ r + ");")
    print ("\\node at ("+ x + ", " + y + ") {$" + str(cpt) +"$};")
    cpt += 1

print ("\\end{tikzpicture}\n\\end{document}")
