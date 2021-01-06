import math as m
import random as r
import numpy as np

def mapr(x, xmin, xmax, ymin, ymax): return (x-xmin)/(xmax-xmin)*(ymax-ymin)+ymin

def const(x, minX, maxX): return min(maxX, max(x, minX))

def length(vec): return m.sqrt(sum([x*x for x in vec]))

def circle(vec, r): return length(vec)-r

def cube(pvec, svec):
    q = Ladd(Labs(pvec),Lmuln(svec,-1))
    return length(Lmax(q,0))+min(max(q),0)

def norm(vec): return Lmuln(vec,1/l) if (l:=length(vec))!=0 else vec

def chess(vec, c1, c2): return c1 if sum(map(m.floor,Lmuln(vec,10))) % 2 == 0 else c2

def mapC(c1, c2, p):
    p = const(p, 0, 1)
    return (int(mapr(p, 0, 1, c1[0], c2[0])), int(mapr(p, 0, 1, c1[1], c2[1])), int(mapr(p, 0, 1, c1[2], c2[2])))

def Lmuln(list1,i): return list([x*i for x in list1])

def Lmod(list1,list2): return list([x[0]%x[1] if x[1]!=0 else x[0] for x in zip(list1,list2)])

def Laddn(list1,i): return list([x+i for x in list1])
def Ladd(list1,list2): return list([x[0]+x[1] for x in zip(list1,list2)])

def Labs(list1): return list(map(abs,list1))

def Lmax(list1,i:int): return list(map(lambda x:max(x,i),list1))

def rXm(x):return np.array([[1,0,0],[0,m.cos(x),-m.sin(x)],[0,m.sin(x),m.cos(x)]])
def rYm(x):return np.array([[m.cos(x),0,m.sin(x)],[0,1,0],[-m.sin(x),0,m.cos(x)]])
def rZm(x):return np.array([[m.cos(x),-m.sin(x),0],[m.sin(x),m.cos(x),0],[0,0,1]])