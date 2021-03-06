import fire
import igraph
import numpy as np
import pandas as pd


def arrow_to_graph(path):
    df = pd.read_parquet(path)# .sort_values("mutationId")
    vertex_mapping = dict((mutationId, vertexId) for vertexId, mutationId in enumerate(df["mutationId"]))
    is_root = np.array(df["ancestors"].map(lambda x: len(x))) == 1
    graph = igraph.Graph()
    graph.add_vertices(len(vertex_mapping))
    links = list(zip(
        (vertex_mapping[x[-2]] for x in df["ancestors"][~is_root]),
        (vertex_mapping[x] for x in df["mutationId"][~is_root])
    ))
    graph.add_edges(links)
    graph.vs["mutationId"] = df["mutationId"]
    graph.vs["type_count"] = df["typeCount"]
    graph.vs["mutation_count"] = df["mutationCount"]
    roots = np.where(is_root)
    return graph, roots[0]


def make_visual_style(graph):
    visual_style = {
        "vertex_size": (np.array(graph.vs["type_count"]) + 1) ** (1 / 4),
        "vertex_label": graph.vs["mutationId"], "margin": 100
    }
    return visual_style


def mutation_tree_plot(data_path, output_path):
    g, roots = arrow_to_graph(data_path)

    # g_layout = g.layout_reingold_tilford(root=[int(x) for x in roots])
    # visual_style = make_visual_style(g)

    # _ = jgraph.plot(g,
    #            output_path, 
    #            layout=g_layout, 
    #            inline=False, 
    #            bbox=(3840,1080), 
    #            **visual_style)

    h = g.subgraph(g.vs.select(mutation_count_gt=100000))
    h_visual_style = make_visual_style(h)
    h_layout = h.layout_reingold_tilford("OUT")

    _ = igraph.plot(h,
                    output_path,
                    layout=h_layout,
                    inline=False,
                    bbox=(3840, 1080),
                    **h_visual_style)


if __name__ == "__main__":
    fire.Fire(mutation_tree_plot)
