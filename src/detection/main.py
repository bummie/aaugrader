#!/usr/bin/env python3
import argparse
import sys

import syscallparser as sp


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detection graph builder 1337")
    parser.add_argument(
        "-o", "--output", type=str, help="Name for output image and json graph"
    )
    args = parser.parse_args()

    syscalls: list[sp.Syscall] = parse_stdin_to_syscalls()
    sp.syscalls_to_jsonl(syscalls, f"/tmp/{args.output}.jsonl")
