import json
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
        score: int = 0,
    ):
        self.name = name
        self.pids = pids
        self.syscalls = syscalls
        self.read = read
        self.write = write
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
        self.score = sg.get("score", 0)

    def calculate_malicious_score(self, base_group):
        # TODO: return reasons for score given

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
        len(pids), dict(syscalls_counter), dict(read_files), dict(write_files)
    )
