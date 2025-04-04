import json
import math
import operator
from collections import defaultdict

import syscallparser as sp


class SyscallGroup:
    def __init__(
        self,
        name: str = "",
        pids: int = 0,
        syscalls: dict[str, int] = {},
        read: dict[str, int] = {},
        write: dict[str, int] = {},
        verified: bool = False,
        score: int = 0,
    ):
        self.name = name
        self.pids = pids
        self.syscalls = syscalls
        self.read = read
        self.write = write
        self.verified = verified
        self.score = score

    def to_json(self) -> str:
        return json.dumps(self.__dict__)

    def from_json(self, json_str: str):
        sg = json.loads(json_str)
        self.name = sg.get("name", "")
        self.pids = sg.get("pids", 0)
        self.syscalls = sg.get("syscalls", {})
        self.read = sg.get("read", {})
        self.write = sg.get("write", {})
        self.verified = sg.get("verified", False)
        self.score = sg.get("score", 0)

    def calculate_malicious_score(self, base_group):
        # TODO: return reasons for score given

        if base_group is None:
            return
        
        # Score multipliers
        multiplier_new_syscall = 10
        multiplier_new_file_write = 10
        multiplier_new_file_read = 10

        score = 0

        # One point for each different extra PID
        pid_difference = self.pids - base_group.pids
        if pid_difference > 0:
            score += pid_difference

        # Check if the group we are testing has more syscall than base
        for key in self.syscalls.keys():
            if key not in base_group.syscalls:
                score += 1 * multiplier_new_syscall

        # TODO: Check difference in amount of readings and writings? Compare
        for key in self.read.keys():
            if key not in base_group.read:
                score += 1 * multiplier_new_file_read
                score += self.read[key]

        for key in self.write.keys():
            if key not in base_group.write:
                score += 1 * multiplier_new_file_write
                score += self.write[key]

        self.score = score


# read a list of syscalls and groups them into one object
# that makes a summary
def group_syscalls(syscalls: list[sp.Syscall]) -> SyscallGroup:
    syscalls_counter = defaultdict(lambda: 0)
    read_files = defaultdict(lambda: 0)
    write_files = defaultdict(lambda: 0)
    pids = set()

    for syscall in syscalls:
        pids.add(syscall.pid)
        syscalls_counter[syscall.syscall] += 1

        # Grab first arguement of read syscall
        # This should be the path to the file opened
        # Should filter on which fd in the future
        # TODO: filter on FD
        if syscall.syscall.lower() == "read":
            if len(syscall.args) == 3:
                read_files[syscall.args[0]] += 1

        if syscall.syscall.lower() == "write":
            if len(syscall.args) == 3:
                write_files[syscall.args[0]] += 1

        # TODO: learn more about the other syscalls
        # Filter out interesting information
        # socket if ip port is exposed

    return SyscallGroup(
        pids=len(pids),
        syscalls=dict(syscalls_counter),
        read=dict(read_files),
        write=dict(write_files),
    )


def combine_dicts(a, b, op=operator.add):
    return dict(list(a.items()) + list(b.items()) + [(k, op(a[k], b[k])) for k in set(b) & set(a)])


def calculate_average_syscallgroup(syscallgroups: list[SyscallGroup]) -> SyscallGroup:
    avg_syscallgroup = None

    for syscallgroup in syscallgroups:
        if avg_syscallgroup is None:
            avg_syscallgroup = syscallgroup
            continue

        avg_syscallgroup.pids += syscallgroup.pids
        avg_syscallgroup.syscalls = combine_dicts(
            avg_syscallgroup.syscalls, syscallgroup.syscalls
        )
        avg_syscallgroup.read = combine_dicts(avg_syscallgroup.read, syscallgroup.read)
        avg_syscallgroup.write = combine_dicts(
            avg_syscallgroup.write, syscallgroup.write
        )

    if avg_syscallgroup is None:
        return None
    
    avg_syscallgroup.pids = math.ceil(avg_syscallgroup.pids / len(syscallgroups))

    for key in avg_syscallgroup.syscalls:
        avg_syscallgroup.syscalls[key] = math.ceil(
            avg_syscallgroup.syscalls[key] / len(syscallgroups)
        )
    for key in avg_syscallgroup.read:
        avg_syscallgroup.read[key] = math.ceil(
            avg_syscallgroup.read[key] / len(syscallgroups)
        )
    for key in avg_syscallgroup.write:
        avg_syscallgroup.write[key] = math.ceil(
            avg_syscallgroup.write[key] / len(syscallgroups)
        )

    return avg_syscallgroup
