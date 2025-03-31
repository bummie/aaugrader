#!/usr/bin/env python3

import json
import re
import sys

import rustworkx as rx
from rustworkx.visualization import graphviz_draw


class Syscall:
    def __init__(self, pid: int, syscall: str, args: list[str], result: str, raw: str):
        self.pid = pid
        self.syscall = syscall
        self.args = args
        self.result = result
        self.raw = raw

    def to_json(self) -> str:
        return json.dumps(self.__dict__)


def regex_match_syscall(line: str) -> list:
    return re.findall(r"(\w+)\((.*)\)\s+=\s+(0x[0-9a-fA-F]+|-?\d+)", line)


def parse_strace_output(input_line: str) -> Syscall:
    # Regex that matches strace output
    # read(3</home/bummie/projects/AAUGrader/grades.txt>, "", 262144) = 0
    # SYSCALL: read
    # Syscall args: 3</home/bummie/projects/AAUGrader/grades.txt>, "", 262144
    # Output syscall: 0

    # Process might spawn babies
    # Syscall wills tart with their PID then
    # [pid 122345] read(args) = 1

    pid = -1
    matches = None

    if input_line.lower().startswith("[pid"):
        pid = int(input_line.split("[pid ")[1].split("]")[0])
        strace_output_no_pid = "".join(input_line.split("]")[1:])
        matches = regex_match_syscall(strace_output_no_pid)
    elif input_line.lower().startswith("<..."):
        raise ValueError(f"unwanted line: {input_line}")
    else:
        matches = regex_match_syscall(input_line)

    if len(matches) <= 0:
        # Found no matches
        raise ValueError("found no matches")

    if len(matches[0]) == 3:
        syscall = matches[0][0]
        args = matches[0][1].split(", ")
        result = matches[0][2]

        return Syscall(pid, syscall, args, result, input_line)

    elif len(matches[0]) == 2:
        syscall = matches[0][0]
        result = matches[0][1]
        return Syscall(pid, syscall, [], result, input_line)
    else:
        raise ValueError(f"failed parsing regex matches {matches}")


def int_to_color_str(index: int) -> str:
    colors = ["gold", "lightskyblue", "lightsalmon", "lightgreen", "lightcoral", "lightcoral"]
    return colors[ index % len(colors)]
    
def node_attr(node: Syscall) -> str:
    return { "color": int_to_color_str(node.pid), "label": node.syscall }

if __name__ == "__main__":
    graph = rx.PyDiGraph()

    prev_node = None
    for line in sys.stdin:
        try:
            syscall = parse_strace_output(line)
            node_index = graph.add_node(syscall)
            if prev_node is not None:
                graph.add_edge(prev_node, node_index, None)
            prev_node = node_index
            print(syscall.to_json())
        except Exception as err:
            print(f"failed parsing line: {err}\n{line}", file=sys.stderr)

#   print(graph.edge_indices())
    graphviz_draw(graph, node_attr_fn=node_attr, filename="/tmp/test.png", method="dot")
