from datetime import datetime

import utils
import syscallgrouper as sg
from flask import Flask, request, render_template, redirect

app = Flask(__name__)


def sort_syscallgroups(syscallgroup):

    try:
        dt = datetime.strptime(syscallgroup.name, "%Y-%m-%d_%H-%M-%S")
        return int(dt.timestamp())
    except ValueError:
        return 0

@app.route("/")
def main_page():
    syscall_groups = utils.load_syscallgroups_from_path(utils.syscallgroupFolder())
    sorted_sycalls = sorted(syscall_groups, key=sort_syscallgroups, reverse=True)
    return render_template("index.html", syscallgroups=sorted_sycalls)


@app.route("/event")
def view_event():
    syscallgroup_name = request.args.get("name", "")
    syscallgroup = utils.load_syscallgroup_from_name(syscallgroup_name)

    if syscallgroup is None:
        return "<h1>Could not find syscallgroup!</h1>"

    return render_template("event.html", syscallgroup=syscallgroup)


@app.route("/verify")
def verify_event():
    syscallgroup_name = request.args.get("name", "")
    syscallgroup = utils.load_syscallgroup_from_name(syscallgroup_name)

    if syscallgroup is None:
        return "<h1>Could not find syscallgroup!</h1>"

    try:
        syscallgroup.verified = not syscallgroup.verified
        utils.save_data(
            syscallgroup.to_json(),
            utils.syscallgroupFolder(),
            f"{syscallgroup.name}.json",
        )
    except Exception as e:
        return str(e)

    utils.update_scoring()
    return redirect("/", code=302)


@app.post("/upload")
def upload():
    data = request.get_data()
    syscalls = utils.parse_request_data_to_syscalls(data)
    syscallsgrouped = sg.group_syscalls(syscalls)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    syscallsgrouped.name = timestamp
    utils.save_data(
        syscallsgrouped.to_json(), utils.syscallgroupFolder(), f"{timestamp}.json"
    )

    utils.update_scoring()
    return "Thanks!"


if __name__ == "__main__":
    from waitress import serve

    print("Running IDS on port 8080")
    serve(app, host="0.0.0.0", port=8080)
