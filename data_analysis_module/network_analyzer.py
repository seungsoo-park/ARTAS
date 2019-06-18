import networkx as nx
import matplotlib.pyplot as plt
import os
from operator import itemgetter


class NetworkAnalyzer:
    def __init__(self):
        for self.data_dir in os.listdir('../morpheme_analyzed_data'):
            year_dir_list = os.listdir('../morpheme_analyzed_data/{}'.format(self.data_dir))
            for self.year_dir in year_dir_list:
                self.network_data_list = []
                for file_name in os.listdir('../morpheme_analyzed_data/{}/{}/'.format(self.data_dir, self.year_dir)):
                    with open('{}{}'.format('../morpheme_analyzed_data/{}/{}/'.format(self.data_dir, self.year_dir), file_name)) as fp:
                        data = fp.read().splitlines()
                    if not data:
                        continue
                    temp = []
                    for val in data:
                        temp.append(val.split(', ')[0].strip())
                    self.network_data_list.append(temp)
                self.drawing_graph()

    def drawing_graph(self):
        base_g = nx.Graph()
        for data in self.network_data_list:
            if not data:
                continue
            g = nx.complete_graph(data)
            g.add_weighted_edges_from((u, v, 1) for u, v in g.edges())
            new_g = nx.compose(base_g, g)
            new_edges = self.combine_graph_edges(base_g, g)
            new_g.add_weighted_edges_from(new_edges)
            base_g = new_g.copy()
        weights = [base_g[u][v]['weight'] for u, v in base_g.edges()]
        degree = nx.degree_centrality(base_g)
        # layout = nx.drawing.nx_agraph.pygraphviz_layout(base_g, 'dot')
        layout = nx.drawing.kamada_kawai_layout(base_g)
        nodes = base_g.nodes

        temp = nx.draw_networkx_labels(base_g, layout, font_size=10, font_family='sans-serif', labels=None)
        plt.clf()
        nx.draw_networkx_nodes(base_g, layout, nodelist=nodes, alpha=0.1, node_color='blue', node_size=[val * 3000 for val in degree.values()])
        nx.draw_networkx_edges(base_g, layout, width=[val * 2 for val in weights], edge_color=[val for val in weights], edge_cmap=plt.cm.Blues, alpha=0.5)

        node_labels = {}
        for val in temp.items():
            text_temp = str(val[1]).replace('Text(', '').replace("'", '').replace(')', '').split(',')
            x = text_temp[0]
            y = text_temp[1]
            word = text_temp[2].replace(' ', '\n')
            new_map = plt.text(float(x), float(y), word,  verticalalignment='center', horizontalalignment='center', fontsize=8)
            node_labels[val[0]] = new_map
        nx.relabel_nodes(base_g, node_labels)

        fig = plt.gcf()
        fig.set_size_inches(12, 6)
        plt.axis('off'), plt.xticks([]), plt.yticks([])
        plt.tight_layout()
        plt.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=0, wspace=0)
        save_path = '../analyzed_data/{}/'.format(self.data_dir)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        plt.savefig('{}{}_{}'.format(save_path, self.year_dir, 'result.png'), dpi=300)
        plt.clf()

        analysis_result = []
        for u, v in base_g.edges():
            analysis_result.append([u, v, int(base_g[u][v]['weight'])])
        analysis_result.sort(key=itemgetter(2), reverse=True)
        with open('{}{}_{}'.format(save_path, self.year_dir, 'result.txt'), 'w') as fp:
            for val in analysis_result:
                fp.write('{}, {}, {}\n'.format(val[0], val[1], val[2]))

    @staticmethod
    def combine_graph_edges(g1, g2):
        combine_edges = []
        for s1, e1, weight1 in g1.edges(data=True):
            for s2, e2, weight2 in g2.edges(data=True):
                if s1 == s2 and e1 == e2 or s1 == e2 and e1 == s2:
                    combine_edges.append((s1, e1, weight1['weight'] + weight2['weight']))
        return combine_edges


if __name__ == '__main__':
    NetworkAnalyzer()
