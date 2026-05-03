import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def plot_deg_BA(G):
    degrees = [d for _, d in G.degree() if d > 0]
    k = np.array(degrees)

    # logarithmic binnning
    bins = np.logspace(np.log10(min(k)), np.log10(max(k)), 20)
    hist, bin_edges = np.histogram(degrees, bins=bins, density=True)
    bin_centers = np.sqrt(bin_edges[:-1] * bin_edges[1:])

    plt.figure()
    plt.scatter(bin_centers, hist)

    # reference c * k^-3 line
    C = hist[0] * bin_centers[0]**3
    ref_line = C * bin_centers**(-3)
    plt.plot(bin_centers, ref_line, 'r--', label=r"$k^{-3}$")

    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel("k")
    plt.ylabel("P(k)")
    plt.title("Distribúcia stupňa uzlov BA grafu")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    G = nx.barabasi_albert_graph(30000, 2)
    plot_deg_BA(G)