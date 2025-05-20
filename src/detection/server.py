from datetime import datetime
import os
import utils
import syscallgrouper as sg
import validate_trace as vs
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
    return render_template("index.html")


@app.route("/syscalls")
def syscalls_page():
    syscall_groups = utils.load_syscallgroups_from_path(utils.syscallgroupFolder())
    sorted_sycalls = sorted(syscall_groups, key=sort_syscallgroups, reverse=True)
    return render_template("syscalls.html", syscallgroups=sorted_sycalls)


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


@app.post("/uploadcfg")
def upload_cfg():
    data = request.get_data().decode("UTF-8")
    file_name = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.cfg"
    file_path = os.path.join(utils.cfgFolder(), file_name)

    if not os.path.exists(utils.cfgFolder()):
        os.makedirs(utils.cfgFolder())

    with open(file_path, "w") as file:
        file.write(data)

    return "Thanks!"


@app.route("/cfg")
def cfg_events():
    files = utils.list_files(utils.cfgFolder())
    traces = vs.validate_multiple_cfgs(files)

    sorted_traces = traces  # sorted(traces, key=sort_syscallgroups, reverse=True)
    return render_template("cfg.html", traces=sorted_traces)


if __name__ == "__main__":
    from waitress import serve

    print("Running IDS on port 8080")
    serve(app, host="0.0.0.0", port=8080)
