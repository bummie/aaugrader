import json
from collections import defaultdict

import syscallparser as sp


class SyscallGroup:
    def __init__(
        self,
        pids: int,
        syscalls: dict[str, int],
        read: dict[str, int],
        write: dict[str, int],
    ):
        self.pids = pids
        self.syscalls = syscalls
        self.read = read
        self.write = write

    def to_json(self) -> str:
        return json.dumps(self.__dict__)


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
