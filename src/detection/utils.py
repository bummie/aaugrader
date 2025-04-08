import os
import sys
from pathlib import Path

import syscallgrouper as sg
import syscallparser as sp


def syscallgroupFolder() -> str:
    return "syscallgroups"


def parse_request_data_to_syscalls(data) -> list[sp.Syscall]:
    syscalls: list[sp.Syscall] = []

    for line in data.splitlines():
        syscall = None
        try:
            syscall = sp.parse_strace_output(str(line))
            syscalls.append(syscall)
        except Exception as err:
            #   print(f"failed parsing line: {str(err)}\n{line}", file=sys.stderr)
            continue

    return syscalls


def list_files(directory):
    os.makedirs(directory, exist_ok=True)
    return [
        Path.joinpath(Path(directory), f.name)
        for f in Path(directory).iterdir()
        if f.is_file()
    ]


def load_syscallgroup_from_name(name: str) -> sg.SyscallGroup:
    syscallGroup = None
    try:
        syscallGroup = sg.SyscallGroup()
        with open(f"syscallgroups/{name}.json", "r", encoding="utf-8") as file:
            syscallGroup.from_json(file.read())
    except Exception as e:
        print("Could not load directory " + str(e))
        return None

    return syscallGroup


def load_syscallgroups_from_path(path: str) -> list[sg.SyscallGroup]:
    syscall_groups = []

    try:
        for filepath in list_files(path):
            syscallGroup = sg.SyscallGroup()
            with open(filepath, "r", encoding="utf-8") as file:
                syscallGroup.from_json(file.read())
            syscall_groups.append(syscallGroup)
    except Exception as e:
        print("Could not load directory " + str(e))
    return syscall_groups


def save_data(data: str, folder: str, filename: str):
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, filename)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(data)

    print(f"Data saved at file saved at: {file_path}")


def update_scoring():
    all_syscall_groups = load_syscallgroups_from_path(syscallgroupFolder())
    verified_syscall_groups = [syscallgroup for syscallgroup in all_syscall_groups if syscallgroup.verified]

    avg_syscall_group = sg.calculate_average_syscallgroup(verified_syscall_groups)

    if avg_syscall_group is None:
        return

    for sysgroup in all_syscall_groups:
        sysgroup.calculate_malicious_score(avg_syscall_group)
        save_data(sysgroup.to_json(), syscallgroupFolder(), f"{sysgroup.name}.json")