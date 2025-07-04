import re
import json


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
    if input_line.lower().lstrip().startswith("[pid") or input_line.lower().lstrip().startswith("b'[pid"):
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


# Writes a list of syscall to a jsonl file
def syscalls_to_jsonl(syscalls: list[Syscall], outputPath: str):
    with open(outputPath, "a") as f:
        for syscall in syscalls:
            f.write(f"{syscall.to_json()}\n")
