import numpy as np
import networkx as nx

import newsolver1 as ode
import network as nt


def vanderpol(Y,p):
    return [Y[1],p[1]*(1-Y[0]**2)*Y[1]-Y[0]]

def harmonic(Y,p):
    return [Y[1],-p[1]*Y[0]]

def buildGraph():
    return nt.construct()


def solve(equation,param,time,graph,coupling_term):
    return ode.simulate(equation,param,time,graph,coupling_term)


def main():
    #graph = buildGraph()
    graph = nx.binomial_graph(10,0.1)
    (t,sol) = solve(harmonic,[2,2],np.linspace(0, 100, 500),graph,np.matrix([[0,0],[1,0]]))
    return (t,sol)

(t,sol) = main()

