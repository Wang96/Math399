import newsolver as ode
import network as nt
import numpy as np

def equation(Y,p):
    return [Y[1],p[1]*(1-Y[0]**2)*Y[1]-Y[0]]

def buildGraph():
    return nt.construct()


def solve(equation,graph,coupling_term):
    ode.simulate(equation,graph,coupling_term)


def main():
    graph = buildGraph()
    solve(equation,graph,np.matrix([[0,0],[1,0]]))

main()
