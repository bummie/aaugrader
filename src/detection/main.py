#!/usr/bin/env python3
import argparse
import sys

import rustworkx as rx
import syscallparser as sp
from rustworkx.visualization import graphviz_draw


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


def parse_stdin_to_syscalls() -> list[sp.Syscall]:
    syscalls: list[sp.Syscall] = []

    for line in sys.stdin:
        syscall = None
        try:
            syscall = sp.parse_strace_output(line)
            syscalls.append(syscall)
        except Exception as err:
            print(f"failed parsing line: {err}\n{line}", file=sys.stderr)
            continue

    return syscalls


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detection graph builder 1337")
    parser.add_argument(
        "-o", "--output", type=str, help="Name for output image and json graph"
    )
    args = parser.parse_args()

    syscalls: list[sp.Syscall] = parse_stdin_to_syscalls()
    sp.syscalls_to_jsonl(syscalls, f"/tmp/{args.output}.jsonl")

    graph = build_graph(syscalls)
    graphviz_draw(graph, node_attr_fn=node_attr, filename=f"/tmp/{args.output}.png")
