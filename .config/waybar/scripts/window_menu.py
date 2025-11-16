#!/usr/bin/env python3
import json
import subprocess
import sys


def load_clients():
    data = subprocess.check_output(["hyprctl", "clients", "-j"], text=True)
    return json.loads(data)


def pick_window(labels):
    joined = "\n".join(labels)
    if not joined:
        return None
    result = subprocess.run(
        ["rofi", "-dmenu", "-i", "-p", "窗口"],
        input=joined,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        return None
    choice = result.stdout.strip()
    return choice or None


def main():
    try:
        clients = load_clients()
    except Exception as exc:
        print(exc, file=sys.stderr)
        return
    entries = []
    for client in clients:
        workspace = client.get("workspace") or {}
        ws_name = workspace.get("name") or str(workspace.get("id", ""))
        if workspace.get("id") == -1:
            ws_name = "magic"
        app_class = client.get("class") or client.get("initialClass") or "App"
        title = client.get("title") or app_class
        label = f"{ws_name} · {app_class} — {title}"
        address = client.get("address")
        if not address:
            continue
        entries.append((label, address))
    if not entries:
        return
    labels = [label for label, _ in entries]
    choice = pick_window(labels)
    if not choice:
        return
    target = None
    for label, address in entries:
        if label == choice:
            target = address
            break
    if not target:
        return
    subprocess.run(["hyprctl", "dispatch", "focuswindow", f"address:{target}"])


if __name__ == "__main__":
    main()
