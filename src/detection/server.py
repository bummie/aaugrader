import sys

import syscallgrouper as sg
import syscallparser as sp
from flask import Flask, request

app = Flask(__name__)

def parse_request_data_to_syscalls(data) -> list[sp.Syscall]:
    syscalls: list[sp.Syscall] = []

    for line in data.splitlines():
        syscall = None
        try:
            syscall = sp.parse_strace_output(str(line))
            syscalls.append(syscall)
        except Exception as err:
            # print(f"failed parsing line: {err}\n{line}", file=sys.stderr)
            continue

    return syscalls


@app.route("/")
def hello_world():
    return "<h1>IDS Central 1337 - Welcome!</h1>\nLet's detect some naughty hackers!"


@app.post("/upload")
def upload():
    data = request.get_data()
    syscalls = parse_request_data_to_syscalls(data)
    syscallsgrouped = sg.group_syscalls(syscalls)
    print(syscallsgrouped.to_json())

    return "Thanks!"


if __name__ == "__main__":
    from waitress import serve

    print("Running IDS on port 8080")
    serve(app, host="0.0.0.0", port=8080)
