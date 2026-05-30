import networkx as nx
import matplotlib.pyplot as plt
import math
from collections import deque
from pydantic import BaseModel
from typing import List
from .Book import Book
from . import utils


class RegimeStats(BaseModel):
    slope: float
    intercept: float
    confidence: float
    r2: float


class MultiRegimeRegression(BaseModel):
    bk: List
    bp_k: List
    small: RegimeStats
    large: RegimeStats

    def get_data_for_plotting(self):
        return self.bk, self.bp_k, self.small.slope, self.small.intercept, self.large.slope, self.large.intercept


class SingleRegimeRegression(BaseModel):
    bk: List
    bp_k: List
    stats: RegimeStats

    def get_data_for_plotting(self):
        return self.bk, self.bp_k, self.stats.slope, self.stats.intercept


class Wordweb:
    def __init__(self, book: Book, num_of_links_from_new_word=2, punctuation=False):
        self.G: nx.Graph = nx.Graph()
        self.m = num_of_links_from_new_word
        self.file_name = book.file_name

        self.title = book.title
        if not punctuation:
            tokens = book.get_tokens()
            self.title += " (no punctuation)"
        else:
            tokens = book.get_tokens_punctuation()

        last_tokens = deque(maxlen=num_of_links_from_new_word)

        for token in tokens:
            self.G.add_node(token)
            for previous_token in last_tokens:
                self.G.add_edge(token, previous_token)
            last_tokens.append(token)

    def draw_graph(self):
        plt.figure(figsize=(6, 6))

        if self.G.number_of_nodes() > 100:
            # or visualize in gephi? 👀
            # spring layout algorithm takes a while

            degrees = dict(self.G.degree())
            node_sizes = [v * 5 for v in degrees.values()]
            node_color = [math.log(v) for v in degrees.values()]

            pos = nx.spring_layout(self.G, k=0.3, iterations=10)

            plt.figure(figsize=(15, 15), facecolor='white')
            nx.draw_networkx_edges(self.G, pos, width=0.1, alpha=0.05, edge_color='grey')
            nodes = nx.draw_networkx_nodes(
                self.G,
                pos,
                node_size=node_sizes,
                node_color=node_color,
                alpha=0.8,
                cmap=plt.cm.viridis
            )

            nodes.set_edgecolor('white')
            nodes.set_linewidth(0.5)

            plt.axis('off')
            plt.tight_layout()
            plt.show()

        else:
            nx.draw(
                self.G,
                nx.spring_layout(self.G),
                with_labels=True,
                node_size=2000,
                node_color="lightblue",
                font_size=12,
                font_weight="bold",
                edge_color="gray"
            )
        plt.show()

    def num_of_nodes(self):
        return self.G.number_of_nodes()

    def avg_k(self):
        return sum(dict(self.G.degree()).values()) / self.num_of_nodes()

    def avg_l_and_diameter(self):
        sum_of_lengths = 0
        count_of_lengths = 0
        diameter = 0
        seen = set()
        for u, lengths in nx.all_pairs_shortest_path_length(self.G):
            seen.add(u)
            for v, length in lengths.items():
                if v not in seen:
                    sum_of_lengths += length
                    count_of_lengths += 1

                    if length > diameter:
                        diameter = length

        avg_l = sum_of_lengths / count_of_lengths if count_of_lengths > 0 else 0
        return avg_l, diameter

    def avg_c(self):
        return nx.average_clustering(self.G)

    def sw_index(self, avg_k, avg_l, avg_c):
        num_of_nodes = self.num_of_nodes()
        c_rand = avg_k / num_of_nodes
        l_rand = math.log(num_of_nodes) / math.log(avg_k)
        return (avg_c / c_rand) / (avg_l / l_rand)

    def density(self):
        return nx.density(self.G)

    def multi_regime_gammas(self) -> MultiRegimeRegression:
        degrees = [k for _, k in self.G.degree()]
        k, p_k = utils.samples_to_probability(degrees)
        bk, bp_k = utils.log_bin(k, p_k, 35)
        left, right, slope, intercept, r2, confidence = utils.linear_regression(bk, bp_k)

        bk = list(bk[left:right])
        bp_k = list(bp_k[left:right])
        print(f"trimmed {left} points from both tails")
        if left > 5:
            print("\n!!! Cutting too much, check out why !!!\n")

        mid = len(bk) // 2
        bk_small = bk[:mid]
        bp_k_small = bp_k[:mid]
        _, _, slope_small, intercept_small, r2_small, confidence_small = utils.linear_regression(bk_small, bp_k_small, trim_statistics=False)
        small_regime = RegimeStats(slope=slope_small, intercept=intercept_small, confidence=confidence_small, r2=r2_small)

        bk_large = bk[mid:]
        bp_k_large = bp_k[mid:]
        _, _, slope_large, intercept_large, r2_large, confidence_large = utils.linear_regression(bk_large, bp_k_large, trim_statistics=False)
        large_regime = RegimeStats(slope=slope_large, intercept=intercept_large, confidence=confidence_large, r2=r2_large)

        multi_regime = MultiRegimeRegression(bk=bk, bp_k=bp_k, small=small_regime, large=large_regime)

        return multi_regime

    def plot_multi_regime_degree_distribution(self):
        data = self.multi_regime_gammas()
        print(f"Gamma 1: {-data.small.slope:.3f} ± {data.small.confidence:.3f}, R2: {data.small.r2:.3f}\nGamma 2: {-data.large.slope:.3f} ± {data.large.confidence:.3f}, R2: {data.large.r2:.3f}")
        utils.plot_multi_regime_degree_distribution(self.title, *data.get_data_for_plotting())

    def nodes_difference(self, other):

        if self.G.number_of_nodes() > other.G.number_of_nodes():
            return self.G.nodes() - other.G.nodes()

        return other.G.nodes() - self.G.nodes()

    def print_info(self):
        print(f"--------------- {self.title} ------------------")

        num_of_operations = 6

        num_of_nodes = self.num_of_nodes()
        print(f"1/{num_of_operations}")

        avg_k = self.avg_k()
        print(f"2/{num_of_operations}")

        avg_l, diameter = self.avg_l_and_diameter()
        print(f"3/{num_of_operations}")

        avg_c = self.avg_c()
        print(f"4/{num_of_operations}")

        sw_index = self.sw_index(avg_k, avg_l, avg_c)
        print(f"5/{num_of_operations}")

        multi_regime = self.multi_regime_gammas()
        gamma_1 = -multi_regime.small.slope
        gamma_2 = -multi_regime.large.slope

        m_r = self.m * (gamma_2 - 3) / (1 - gamma_2)  # solution for m_r of: gamma_2 == 2 + (m - m_r) / (m + m_r)
        density = self.density()

        print(
            f"Wordweb from file: {self.file_name}\n"
            f"Number of nodes: {num_of_nodes}\n"
            f"Number of edges: {self.G.number_of_edges()}\n"
            f"Density: {density}\n"
            f"Diameter: {diameter}\n"
            f"Average degree: {avg_k:.2f}\n"
            f"Average shortest path length: {avg_l:.2f}\n"
            f"Average clustering coefficient: {avg_c:.2f}\n"
            f"Small-world index: {sw_index:.2f}\n"
            f"Power-law exponent (gamma_1): {gamma_1:.3f} ± {multi_regime.small.confidence:.3f} with R^2 = {multi_regime.small.r2:.4f}\n"
            f"Power-law exponent (gamma_2): {gamma_2:.3f} ± {multi_regime.large.confidence:.3f} with R^2 = {multi_regime.large.r2:.4f}\n"
            f"m_r parameter in WW model: {m_r:.3f}\n"
        )
