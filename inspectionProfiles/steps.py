import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog, scrolledtext
from tkinter import simpledialog
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import MouseEvent

class Node:
    def __init__ (self,nombre,x,y):
        self.nombre=nombre
        self.x=x
        self.y=y
        self.neighbors=[]
def AddNeighbor(p1,p2):
    i=0
    encontrado=False
    while i<len(p1.neighbors) and not encontrado:
        if p2.nombre==p1.neighbors[i].nombre:
            encontrado=True
            return False
        else:
            i=i+1
    if not encontrado:
        p1.neighbors.append(p2)
        return True
def Distance(p1,p2):
    dx=(p2.x - p1.x)**2
    dy=(p2.y - p1.y)**2
    distance=(dx+dy)**0.5
    return distance
class Segment:
    def __init__ (self,nombre,origen,destino):
        self.nombre=nombre
        self.origen=origen
        self.destino=destino
        self.cost=Distance(self.origen,self.destino)
class Graph:
    def __init__ (self):
        self.nodes=[]
        self.segments=[]
def AddNode(g,n):
    i = 0
    encontrado = False
    while i < len(g.nodes) and not encontrado:
        if n.nombre == g.nodes[i].nombre:
            encontrado = True
            return False
        else:
            i = i + 1
    if not encontrado:
        g.nodes.append(n)
        return True
def AddSegment(g,nombre,nOrigen,nDestino):
    i=0
    encontrado=False
    while i<len(g.nodes) and not encontrado:
        if nOrigen==g.nodes[i].nombre:
            encontrado=True
            origen=g.nodes[i]
        else:
            i=i+1
    if encontrado:
        encontrado=False
    i=0
    while i<len(g.nodes) and not encontrado:
        if nDestino==g.nodes[i].nombre:
            destino=g.nodes[i]
            encontrado=True
            print('True')
        else:
            i=i+1
    if not encontrado:
        print('False')
    s=Segment(nombre,origen,destino)
    g.segments.append(s)
def GetClosest (g,x,y):
    i=0
    min=99999999
    while i<len(g.nodes):
        dx=(g.nodes[i].x-x)**2
        dy=(g.nodes[i].y-y)**2
        distance=(dx+dy)**0.5
        if min>distance:
            min=distance
            nodemin=g.nodes[i]
        i=i+1
    return nodemin
def Plot(g):
    plt.grid(color='red', linestyle='dashed', linewidth=0.5)
    i=0
    while i<len(g.nodes):
        plt.plot(g.nodes[i].x,g.nodes[i].y,'o',color='red',markersize=5)
        plt.text(g.nodes[i].x + 0.2, g.nodes[i].y + 0.2, g.nodes[i].nombre, color='green',
                 weight='bold', fontsize=8)
        i = i + 1
    plt.title('Gráfico con nodos y segmentos')
    i = 0
    while i < len(g.segments):
        plt.arrow(g.segments[i].origen.x,g.segments[i].origen.y,g.segments[i].destino.x-g.segments[i].origen.x,
                  g.segments[i].destino.y-g.segments[i].origen.y,head_width=0.5,head_length=0.5,ec='blue',
                  linewidth=1)
        plt.text((g.segments[i].destino.x+g.segments[i].origen.x)/2,
                  (g.segments[i].destino.y+g.segments[i].origen.y)/2,
                 round(g.segments[i].cost,2),fontsize=9,color='black')
        i=i+1
    plt.show()
def PlotNode(g,nOrigen):
    plt.grid(color='red', linestyle='dashed', linewidth=0.5)
    i=0
    while i<len(g.nodes):
        plt.plot(g.nodes[i].x,g.nodes[i].y,'o',color='gray',markersize=5)
        plt.text(g.nodes[i].x + 0.2, g.nodes[i].y + 0.2, g.nodes[i].nombre, color='green',
                 weight='bold', fontsize=8)
        i=i+1
    i=0
    encontrado=False
    while i<len(g.nodes) and not encontrado:
        if g.nodes[i].nombre==nOrigen:
            plt.plot(g.nodes[i].x, g.nodes[i].y, 'o', color='red', markersize=5)
            encontrado=True
        i=i+1
    i=0
    while i<len(g.segments):
        if g.segments[i].origen.nombre==nOrigen:
            plt.arrow(g.segments[i].origen.x, g.segments[i].origen.y, g.segments[i].destino.x - g.segments[i].origen.x,
                      g.segments[i].destino.y - g.segments[i].origen.y, head_width=0.5, head_length=0.5, ec='blue',
                      linewidth=1)
            plt.text((g.segments[i].destino.x + g.segments[i].origen.x) / 2,
                     (g.segments[i].destino.y + g.segments[i].origen.y) / 2,
                     round(g.segments[i].cost, 2), fontsize=9, color='black')
        i = i + 1
    plt.show()
def PlotFile(file):
    F=open(file,'r')
    g=F.readline()
    g=Graph()
    l=F.readline()
    while l!='':
        e=l.strip('\n').split(' ')
        if e[0]=='Node':
            n=Node(e[1],int(e[2]),int(e[3]))
            AddNode(g,n)
        elif e[0]=='Segment':
            AddSegment(g,e[1],e[2],e[3])
        l=F.readline()
    F.close()
    Plot(g)
def CreateGraph_1 ():
    G = Graph()
    AddNode(G, Node("A",1,20))
    AddNode(G, Node("B",8,17))
    AddNode(G, Node("C",15,20))
    AddNode(G, Node("D",18,15))
    AddNode(G, Node("E",2,4))
    AddNode(G, Node("F",6,5))
    AddNode(G, Node("G",12,12))
    AddNode(G, Node("H",10,3))
    AddNode(G, Node("I",19,1))
    AddNode(G, Node("J",13,5))
    AddNode(G, Node("K",3,15))
    AddNode(G, Node("L",4,10))
    AddSegment(G, "AB","A","B")
    AddSegment(G, "AE","A","E")
    AddSegment(G, "AK","A","K")
    AddSegment(G, "BA","B","A")
    AddSegment(G, "BC","B","C")
    AddSegment(G, "BF","B","F")
    AddSegment(G, "BK", "B", "K")
    AddSegment(G, "BG", "B", "G")
    AddSegment(G, "CD", "C", "D")
    AddSegment(G, "CG", "C", "G")
    AddSegment(G, "DG", "D", "G")
    AddSegment(G, "DH", "D", "H")
    AddSegment(G, "DI", "D", "I")
    AddSegment(G, "EF", "E", "F")
    AddSegment(G, "FL", "F", "L")
    AddSegment(G, "GB", "G", "B")
    AddSegment(G, "GF", "G", "F")
    AddSegment(G, "GH", "G", "H")
    AddSegment(G, "ID", "I", "D")
    AddSegment(G, "IJ", "I", "J")
    AddSegment(G, "JI", "J", "I")
    AddSegment(G, "KA", "K", "A")
    AddSegment(G, "KL", "K", "L")
    AddSegment(G, "LK", "L", "K")
    AddSegment(G, "LF", "L", "F")
    return G
G=CreateGraph_1()
