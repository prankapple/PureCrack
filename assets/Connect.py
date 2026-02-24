import requests

def startPCS(host="0.0.0.0", port=5000):
    BASE_URL = "http://" + str(host) +":" + str(port) +"/run"

    while True:
        cwd = requests.post(BASE_URL, json={"command": ""}).json().get("cwd", "unknown")
        command = input(f"{cwd}> ").strip()
        
        if command.lower() in ("exit", "quit"):
            break
        if not command:
            continue

        response = requests.post(BASE_URL, json={"command": command})
        data = response.json()
        
        if data["output"]:
            print(data["output"])