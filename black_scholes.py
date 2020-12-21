import numpy as np
import math
import matplotlib.pyplot as plt
import statistics as stats
from matplotlib import cm


def simple_black_scholes(r, sigma, Smax, k, T, Ns, Nt, plotting=True):

    # First-order finite-difference approx to 
    # Black-Scholes PDE 

    # r is the risk free rate
    # Sigma is the volatility
    # Smax is the max Stock Price
    # Smin is the min stock price
    # k is the strike price
    # T is the time to expiration in years

    dtt = T/Nt

    # Initialize
    V = np.zeros((Ns, Nt))
    S = np.linspace(0, Smax, Ns)
    tau = np.linspace(0, T, Nt)

    # Boundary Conditions
    for i in range(0, Ns,):
        V[i, 0] = max(S[i]-k, 0)

    for j in range(0, Nt):
        V[Ns-1, j] = Smax - k*math.exp(-r*tau[j])


    # Explicit Algorithm
    for j in range(0, Nt-1):
        for n in range(1, Ns-1):
            V[n, j+1] = 0.5*dtt*(sigma*sigma*n*n-r*n)*V[n-1, j] + \
                (1-dtt*(sigma*sigma*n*n+r))*V[n, j] + \
                0.5*dtt*(sigma*sigma*n*n+r*n)*V[n+1, j]

    # Plotting can comment out
    if plotting == True:
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        t, s = np.meshgrid(tau, S)
        surf = ax.plot_surface(t, s, V, cmap=cm.coolwarm,
                            linewidth=0, antialiased=False)

        plt.xlabel('Time (Years)')
        plt.ylabel('Security Price')
        ax.set_zlabel('Option Price')
        plt.show()

    return tau, S, V 


# Example 
# Plotting a payoff diagram at expiration
# r = 0.02
# sigma = 0.25 
# Smax = 150 
# k = 100 
# T = 0.9 
# Ns = 160
# Nt = 1600
# plotting = False
# tau, S, V = simple_black_scholes(r, sigma, Smax, k, T, Ns, Nt, plotting)

# payoff = V[:,0]
# plt.style.use('classic')
# fontsize = 16
# plt.tight_layout()
# plt.rcParams["font.family"] = "serif"
# plt.plot(S, payoff, '-b', label='Payoff at Expiration, Strike = {}'.format(k))
# plt.xlabel('Stock Price', fontsize=fontsize)
# plt.ylabel('Option Value', fontsize=fontsize)
# plt.legend(loc='upper left')
# plt.ylim([-10, 50])
# plt.show()


def simple_black_scholes_dte(r, sigma, Smax, k, dte, Ns, Nt, plotting=True):
    # Modification with days to expiration as input

    # First-order finite-difference approx to 
    # Black-Scholes PDE 

    # r is the risk free rate
    # Sigma is the volatility
    # Smax is the max Stock Price
    # Smin is the min stock price
    # k is the strike price
    # T is the time to expiration in years

    T = round(dte/365, 2)
    dtt = T/Nt
    

    # Initialize
    V = np.zeros((Ns, Nt))
    S = np.linspace(0, Smax, Ns)
    tau = np.linspace(0, T, Nt)
    dte_vector = np.linspace(0, dte, Nt)

    # Boundary Conditions
    for i in range(0, Ns,):
        V[i, 0] = max(S[i]-k, 0)

    for j in range(0, Nt):
        V[Ns-1, j] = Smax - k*math.exp(-r*tau[j])


    # Explicit Algorithm
    for j in range(0, Nt-1):
        for n in range(1, Ns-1):
            V[n, j+1] = 0.5*dtt*(sigma*sigma*n*n-r*n)*V[n-1, j] + \
                (1-dtt*(sigma*sigma*n*n+r))*V[n, j] + \
                0.5*dtt*(sigma*sigma*n*n+r*n)*V[n+1, j]

    # Plotting can comment out
    if plotting == True:
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        t, s = np.meshgrid(dte_vector, S)
        surf = ax.plot_surface(t, s, V, cmap=cm.coolwarm,
                            linewidth=0, antialiased=False)

        plt.xlabel('Days to Expiration')
        plt.ylabel('Security Price')
        ax.set_zlabel('Option Price')
        plt.show()

    return dte_vector, S, V 
