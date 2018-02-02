#This file contains useful primitives to generate, recognize, and in general, experiment with disk graphs and unit disk graphs.
#The typical use is to test if a particular graph is a disk graph, or to automatize tests for graphs from a specified class/family.
#We use the free solver SCIP to decide the quadratic inequalities stemming from disk and unit disk recognition.

#For the visualization, see file toTikz.py 
#TikZ code is generated, readily compilable to a pdf.
#This approach yields at the same time nice and modular pictures and LaTeX source to easily share and edit. 

##############
#   How to   #
##############

### append typically:
#G=nx.Graph()
#G=[insert the interesting graph you want to test]
#testGraph(G)

#From a terminal:
#python disks.py 
### this will put in solution.txt a potential disk representation of G

#Then you can try:
#python toTikz.py < solution.txt > solution.tex
### this will generate a tex file of the disk representation ready to compile

import networkx as nx
import random
from pyscipopt import Model

##############
# Generation #
##############

#from a list of centers/radii (x,y,r) build the disk intersection graph
def diskGraphFromList(t):
    G = nx.Graph()
    G.add_nodes_from(range(1,n+1)) #add the vertices 1,2,...,n
    for i in range(1,n+1):
        for j in range(i+1,n+1):
            (xi,yi,ri) = t[i-1]
            (xj,yj,rj) = t[j-1]
            if (xi - xj)**2 + (yi - yj)**2 - (ri + rj)**2 <= 0: #add an edge between two vertices iff their disks intersect
                G.add_edge(i,j)
    return G

#return a disk graph on n vertices where the centers and radii are chosen uniformly at random.
def randomDiskGraph(n,unit=False,xBox=2,yBox=2,maxRadius=1):
    t = n * [0]
    for i in range(1,n+1): #randomly select the center 
        x = xBox * random.random()
        y = yBox * random.random()
        if unit:
            r = 1 
        else: #and the radius
            r = maxRadius * random.random()
        t[i] = (x,y,r)
    return graphFromDisks(t), t

#same for unit disk graphs.
def randomUnitDiskGraph(n,xBox=2,yBox=2):
    return randomDiskGraph(n,True,xBox,yBox)

###############
# Recognition #
###############

#variables chosen to help IPOPT
eps = 0.00001
xMin = 1.0
xMax = 2.0
yMin = 1.0
yMax = 2.0
rMin = 0.0
rMax = 1.5

#generate the n*(n-1)/2 inequalities for a graph on n vertices to be a disk graph.
#produce a pyscipopt model with 3 lists of variables for the two coordinates and the centers.
def diskInequalities(G):
   model = Model("disk")
   X,Y,R = {},{},{}
   for u in G.nodes(): #defining the 3|V(G)| continuous variables
      R[u] = model.addVar("r"+str(u), vtype="C", lb=rMin, ub=rMax)
      X[u] = model.addVar("x"+str(u), vtype="C", lb=xMin, ub=xMax)
      Y[u] = model.addVar("y"+str(u), vtype="C", lb=yMin, ub=yMax)
   for (u,v) in G.edges(): #inequality for an edge
      model.addCons(pow(X[u] - X[v], 2) + pow(Y[u] - Y[v], 2) - pow(R[u] + R[v], 2) <= 0)
   for (u,v) in (nx.complement(G)).edges(): #inequality for a non-edge
      model.addCons(pow(X[u] - X[v], 2) + pow(Y[u] - Y[v], 2) - pow(R[u] + R[v], 2) >= eps)
   return model, X, Y, R

#same with unit disks. 
#The upper bound for the x- and y-coordinates of the centers shall now be greater and is an optional parameter.
def unitDiskInequalities(G,xMax=10,yMax=10):
   model = Model("unit disk")
   X,Y = {},{}
   for u in G.nodes(): #defining the 2|V(G)| continuous variables
      X[u] = model.addVar("x"+str(u), vtype="C", lb=xMin, ub=xMax)
      Y[u] = model.addVar("y"+str(u), vtype="C", lb=yMin, ub=yMax)
   for (u,v) in G.edges(): #inequality for an edge
      model.addCons(pow(X[u] - X[v], 2) + pow(Y[u] - Y[v], 2) <= 4)
   for (u,v) in (nx.complement(G)).edges():#inequality for a non-edge
      model.addCons(pow(X[u] - X[v], 2) + pow(Y[u] - Y[v], 2) >= 4+eps)
   return model, X, Y

#test if a graph is a disk graph. Output is put by default in "solution.txt". 
def testGraph(G,f="solution.txt",timeOut=0):
    model,X,Y,R = diskInequalities(G)
    print("inequalities generated")
    print("starts solving")
    if timeOut != 0:
        model.setRealParam("limits/time", timeOut)
    model.optimize()
    solFound = (model.getStatus() == "optimal")
    if solFound:
        print("solution found")
        sol = open(f, "w")
        for v in G.nodes():
            sol.write( '('+ str(model.getVal(X[v])) + ',' + str(model.getVal(Y[v])) + ',' +  str(model.getVal(R[v])) + ") ; " + "\n")
        sol.close()
    return solFound

#test if a graph is a unit disk graph.
def testUnitGraph(G,f="unitSolution.txt",timeOut=0):
    model,X,Y = unitDiskInequalities(G)
    print("inequalities generated")
    print("starts solving")
    if timeOut != 0:
        model.setRealParam("limits/time", timeOut)
    model.optimize()
    solFound = (model.getStatus() == "optimal")
    if solFound:
        print("solution found")
        sol = open(f, "w")
        for v in G.nodes():
            sol.write( '('+ str(model.getVal(X[v])) + ',' + str(model.getVal(Y[v])) + ',' +  str(1) + ") ; " + "\n")
        sol.close()
    return solFound


### Examples

### disk graph
#G = nx.Graph()
#G.add_cycle([1,2,3,4])
#G.add_cycle([5,6,7,8])
#H=nx.complement(G)
#testGraph(H)

### non disk graph
#G = nx.Graph()
#G.add_cycle([1,2,3])
#G.add_cycle([4,5,6])
#H=nx.complement(G)
#testGraph(H)




