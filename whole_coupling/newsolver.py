from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt


# generate coupling terms
def coupling(G,position,Y,node_number):
    c = G.number_of_nodes()
    coefficient = np.zeros((c, c))
    for i,j,wt in G.edges_iter(data="weight"):
        #print(i,j,wt)
        i = node_number[i]
        j = node_number[j]
        wt = float(wt)
        coefficient[j][i] += wt
        coefficient[j][j] += -1*wt
    return np.dot(np.kron(coefficient,position),np.matrix(Y).T)


# calculating coupled oscillators
def coupledvdp(Y, t, p, graph, coupling_term, equation, node_number):

    # get initial y's and z's
    equations = Y
    
##    for i in range(len(Y)):
##        equations.append(Y[i])

    # generate coupling term
    coupling_terms = coupling(graph,coupling_term,Y, node_number)
    
    #coupling_terms = np.dot(coupled,np.matrix(equations).T)
    #print(coupling_terms)
    # generate derivatives
    derivatives = []
    i = 0
    j = 0
    while i < len(equations):
        for k in range(p[0]):
            derivatives.append(equation(equations[i:i+p[0]],p)[k] + np.array(coupling_terms[j][0]).flatten()[0])
            j += 1
        i += p[0]
    return derivatives

# main function
# solve ode and generate graphs
def simulate(equation,graph,coupling_term):
    # in the future will get from user input
    # coefficient
    mu = 2

    # number of equations
    num = 2

    # adjacent matrix
    # will get from network
    #adj = np.matrix([[0,0.2,0.2,0],[0.2,0,0,0.2],[0.2,0,0,0.2],[0,0.2,0.2,0]])
    
    # initial value
    # in the future will get from user input
    Y0 = input("Enter initial positions (separate by space): ")
    Y0 = list(map(int,Y0.split()))

    node_number = {}
    for i in range(len(graph)):
        node_number[list(graph)[i]] = i

    param = [num,mu]

    t = np.linspace(0, 100, 500)
    
    sol = odeint(coupledvdp, Y0, t, args=(param,graph,coupling_term,equation, node_number))

    plt.figure()
    i = 0
    j = 1
    label = []
    while i < len(sol[0,:]):
        plt.plot(t,sol[:,i],label="y"+str(j))
        i += param[0]
        j += 1

    plt.xlabel('t')
    plt.legend()
    plt.show()
    #plt.savefig('vanderpol2.png')


#main()
