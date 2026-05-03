import networkx as nx
from collections import Counter
import matplotlib.pyplot as plt

def plot_Ck(G):
    clustering = nx.clustering(G)
    values = list(clustering.values())
    plt.figure()
    plt.hist(values, bins=30)
    plt.xlabel("klasterizačný koeficient C")
    plt.ylabel("počet uzlov")
    plt.title("Distribúcia klasterizačných koeficientov")
    plt.show()

def plot_degree_distribution(G):
    degrees = [d for _, d in G.degree()]
    degree_counts = Counter(degrees)

    x = list(degree_counts.keys())
    y = list(degree_counts.values())

    plt.figure()
    plt.scatter(x, y)
    plt.xlabel("stupeň k")
    plt.ylabel("počet vrcholov stupňa k")
    plt.title("Distribúcia stupňa uzlov ER grafu")
    plt.show()

if __name__ == "__main__":
    p = 0.5
    n = 10000
    G = nx.erdos_renyi_graph(n, p)
    plot_degree_distribution(G)

    p = 0.5
    n = 1000
    G = nx.erdos_renyi_graph(n, p)
    plot_Ck(G)
