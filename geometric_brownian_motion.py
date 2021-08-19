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
    x = x.T[0]
    t = np.arange(0, len(x))*dt
    t.tolist()
    return t, x


def gmb_simulation(mu, n, dt, x0, sigma, N=100):
    t = []
    v = []
    for i in range(N):
        ti, vi = geometric_browning_motion(mu, n, dt, x0, sigma)
        t.append(ti)
        v.append(vi.tolist())

    v = np.vstack(v)
    v = v.T

    means = []
    medians = []
    pct_25 = []
    pct_75 = []
    pct_10 = []
    pct_90 = []
    mins = []
    maxs = []
    for row in v:
        means.append(np.mean(row))
        medians.append(np.median(row))
        pct_25.append(np.percentile(row, 25))
        pct_75.append(np.percentile(row, 75))
        pct_10.append(np.percentile(row, 10))
        pct_90.append(np.percentile(row, 90))
        mins.append(min(row))
        maxs.append(max(row))

    fontname = 'serif'
    plt.style.use('classic')
    # plt.plot(ti, means, '-b')
    plt.fill_between(ti, medians, pct_75, facecolor='yellow')
    plt.fill_between(ti, medians, pct_25, facecolor='yellow')
    plt.fill_between(ti, pct_75, pct_90, facecolor='orange')
    plt.fill_between(ti, pct_25, pct_10, facecolor='orange')

    plt.plot(ti, medians, '-g', linewidth=2, label='median')
    plt.plot(ti, pct_25, '-r', label=r'$25^{th}$ percentile')
    plt.plot(ti, pct_75, '-r', label=r'$75^{th}$ percentile')
    plt.plot(ti, pct_10, '-b', label=r'$10^{th}$ percentile')
    plt.plot(ti, pct_90, '-b', label=r'$90^{th}$ percentile')
    plt.legend(loc='best')
    plt.title(f'$\sigma = {sigma}, \mu = {mu}, N = {N}$',
              fontsize=18, fontname=fontname)
    plt.xlabel('Time', fontname=fontname, fontsize=18)
    plt.ylabel('Security Price', fontname=fontname, fontsize=18)
    # plt.plot(ti, mins, '--k')
    # plt.plot(ti, maxs, '--k')

    plt.show()

    return ti, v


if __name__ == "__main__":
    mu = 0.1
    n = 2000
    dt = 0.01
    x0 = 100
    sigma = 0.2
    # np.random.seed(1)

    gmb_simulation(mu, n, dt, x0, sigma, 10000)

    t, v = geometric_browning_motion(mu, n, dt, x0, sigma)

    print(t)
    print(len(v))
    fontname = 'serif'
    plt.style.use('classic')
    plt.plot(t, v, '-b')
    plt.title(f'$\sigma = {sigma}, \mu = {mu}$',
              fontsize=18, fontname=fontname)
    plt.xlabel('Time', fontname=fontname, fontsize=18)
    plt.ylabel('Security Price', fontname=fontname, fontsize=18)
    plt.show()
