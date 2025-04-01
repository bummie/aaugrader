import rustworkx as rx
from rustworkx.visualization import graphviz_draw
import syscallparser as sp

def int_to_color_str(index: int) -> str:
    colors = [
        "gold",
        "lightskyblue",
        "lightsalmon",
        "lightgreen",
        "lightcoral",
        "lightcoral",
    ]
    return colors[index % len(colors)]


def node_attr(node: sp.Syscall) -> str:
    return {"color": int_to_color_str(node.pid), "label": node.syscall}


def build_graph(syscalls: list[sp.Syscall]) -> rx.PyDiGraph:
    graph = rx.PyDiGraph()
    prev_pid_nodes = {}
    prev_node = None

    for syscall in syscalls:
        print(syscall.to_json())

        node_index = graph.add_node(syscall)
        if syscall.pid in prev_pid_nodes:
            graph.add_edge(prev_pid_nodes[syscall.pid], node_index, None)
        elif prev_node is not None:
            graph.add_edge(prev_node, node_index, None)

        prev_pid_nodes[syscall.pid] = node_index
        prev_node = node_index

    return graph

def draw_graph(graph: rx.PyDiGraph, outputPath: str):
    graphviz_draw(graph, node_attr_fn=node_attr, filename=outputPath)
