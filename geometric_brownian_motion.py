import numpy as np
import matplotlib.pyplot as plt


def geometric_browning_motion(mu, n, dt, x0, sigma):
    # Stochastic Differential Equation
    # mu - percentage drift
    # sigma - volatility
    x = np.exp((mu-sigma**2 / 2)*dt + sigma *
               np.random.normal(0, np.sqrt(dt), size=(1, n)).T)
    x = x0 * x.cumprod(axis=0)
    x = np.insert(x, 0, x0, axis=0)
    t = np.arange(0, len(x))*dt
    return t, x


if __name__ == "__main__":
    mu = 0.1
    n = 5000
    dt = 0.01
    x0 = 100
    sigma = 0.2
    # np.random.seed(1)
    t, v = geometric_browning_motion(mu, n, dt, x0, sigma)
    
    # print(t)
    # print(len(v))
    fontname = 'serif'
    plt.style.use('classic')
    plt.plot(t,v, '-b')
    plt.xlabel('Time', fontname=fontname, fontsize=18)
    plt.ylabel('Security Price', fontname=fontname, fontsize=18)
    plt.show()
