#!/usr/bin/env python3
import json
import subprocess
import sys

def read_json(cmd):
    return json.loads(subprocess.check_output(cmd, text=True))

def main():
    try:
        workspace = read_json(["hyprctl", "activeworkspace", "-j"])
        active_id = workspace.get("id")
    except Exception:
        active_id = None
    try:
        clients = read_json(["hyprctl", "clients", "-j"])
    except Exception:
        print(json.dumps({"text": "无法获取窗口"}, ensure_ascii=False))
        return
    labels = []
    for client in clients:
        workspace_info = client.get("workspace") or {}
        if workspace_info.get("id") == -1:
            continue
        if active_id is not None and workspace_info.get("id") != active_id:
            continue
        title = (client.get("title") or client.get("class") or "窗口").strip()
        if not title:
            title = "窗口"
        focused = client.get("focused")
        if focused:
            title = f"[{title}]"
        labels.append(title)
    if not labels:
        text = "无窗口"
        tooltip = "没有窗口"
    else:
        text = " | ".join(labels)
        tooltip = "\n".join(labels)
    print(json.dumps({"text": text, "tooltip": tooltip}, ensure_ascii=False))

if __name__ == "__main__":
    main()
