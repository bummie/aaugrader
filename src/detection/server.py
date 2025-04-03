import os
from datetime import datetime
from pathlib import Path

import syscallgrouper as sg
import syscallparser as sp
from flask import Flask, request, render_template

app = Flask(__name__)


def parse_request_data_to_syscalls(data) -> list[sp.Syscall]:
    syscalls: list[sp.Syscall] = []

    for line in data.splitlines():
        syscall = None
        try:
            syscall = sp.parse_strace_output(str(line))
            syscalls.append(syscall)
        except Exception:
            # print(f"failed parsing line: {err}\n{line}", file=sys.stderr)
            continue

    return syscalls


def list_files(directory):
    return [f.name for f in Path(directory).iterdir() if f.is_file()]


def load_syscallgroups_from_path(path: str) -> list[sg.SyscallGroup]:
    syscall_groups = []

    try:
        for filepath in list_files(path):
            syscallGroup = sg.SyscallGroup()
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()
                syscallGroup.from_json(content)
            syscall_groups.append(syscallGroup)
    except Exception:
        print("Could not load directory")
    return syscall_groups


def save_data(data: str, folder: str, filename: str):
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, filename)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(data)

    print(f"Data saved at file saved at: {file_path}")


@app.route("/")
def main_page():
    syscall_groups = load_syscallgroups_from_path("waiting")

    return render_template("index.html", syscallgroups=syscall_groups)


@app.post("/upload")
def upload():
    data = request.get_data()
    syscalls = parse_request_data_to_syscalls(data)
    syscallsgrouped = sg.group_syscalls(syscalls)
    print(syscallsgrouped.to_json())

    # TODO: Save file
    # Compare to average, get score, move file to directory based on score
    #
    #
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    save_data(syscallsgrouped.to_json(), "waiting", f"{timestamp}.json")

    return "Thanks!"


if __name__ == "__main__":
    from waitress import serve

    print("Running IDS on port 8080")
    serve(app, host="0.0.0.0", port=8080)
