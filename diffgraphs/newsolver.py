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
def coupledvdp(Y, t, p, G, coupling_term, equation, node_number):

    # get initial y's and z's
    equations = Y
    
##    for i in range(len(Y)):
##        equations.append(Y[i])

    # generate coupling term
    #coupling_terms = coupling(graph,coupling_term,Y, node_number)
    
    #coupling_terms = np.dot(coupled,np.matrix(equations).T)
    #print(coupling_terms)
    # generate derivatives
    derivatives = []
    for n,node in enumerate(G):
        i = p[0]*n
        oscillator = equation(equations[i:i+p[0]],p)
        diag = np.dot(coupling_term,Y[i:i+p[0]])
        neighbor_info = G.pred if G.is_directed() else G
        coupling_terms = np.zeros((1,p[0]))
        for nbr,dataset in G[node].items():
            wt = dataset['weight']
            m = node_number[nbr]
            coupling_terms += float(wt)*np.dot(coupling_term,Y[m*p[0]:(m+1)*p[0]])
            coupling_terms -= float(wt)*diag
        derivatives.append(np.array(oscillator+coupling_terms))
        #print(len(oscillator),coupling_terms.shape)
    #print(np.array(derivatives).flatten())
    return np.array(derivatives).flatten()

def graphyt(solution,p,t):
    plt.figure()
    i = 0
    j = 1
    label = []
    while i < len(solution[0,:]):
        plt.plot(t,solution[:,i],label="y"+str(j))
        i += p[0]
        j += 1

    plt.xlabel('t')
    plt.legend()
    plt.show(block=False)

def graphyz(solution,p):
    plt.figure()
    i = 0
    j = 1
    label = []
    while i < len(solution[0,:]):
        plt.subplot(2,2,j)
        plt.plot(solution[:,i],solution[:,i+1],label = "osci"+str(j))
        i += p[0]
        j += 1
    plt.xlabel('y')
    plt.ylabel('z')
    plt.show(block=False)

def graphzt(solution,p,t):
    plt.figure()
    i = 0
    j = 1
    label = []
    while i < len(solution[0,:]):
        plt.plot(t,solution[:,i+1],label="z"+str(j))
        i += p[0]
        j += 1

    plt.xlabel('t')
    plt.legend()
    plt.show(block=False)

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

    graphyt(sol,param,t)
    graphzt(sol,param,t)
    graphyz(sol,param)
    #plt.savefig('vanderpol2.png')


#main()
