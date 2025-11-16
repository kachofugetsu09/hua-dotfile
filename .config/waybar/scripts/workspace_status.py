#!/usr/bin/env python3
import json
import subprocess
import sys
from html import escape


def hyprctl_json(*args):
    return json.loads(
        subprocess.check_output(["hyprctl", *args, "-j"], text=True)
    )


def main():
    try:
        workspaces = hyprctl_json("workspaces")
        clients = hyprctl_json("clients")
        active_ws = hyprctl_json("activeworkspace").get("id")
    except Exception as exc:
        print(
            json.dumps(
                {
                    "text": f"<span class='ws-tag'>WS ERR</span>",
                    "tooltip": str(exc),
                },
                ensure_ascii=False,
            )
        )
        return

    win_counts = {}
    for client in clients:
        ws_info = client.get("workspace") or {}
        ws_id = ws_info.get("id")
        if ws_id is None or ws_id == -1:
            continue
        win_counts[ws_id] = win_counts.get(ws_id, 0) + 1

    entries = []
    for ws in workspaces:
        ws_id = ws.get("id")
        if ws_id is None:
            continue
        count = win_counts.get(ws_id, 0)
        if ws_id == active_ws or count > 0:
            entries.append(
                {
                    "id": ws_id,
                    "name": ws.get("name") or str(ws_id),
                    "windows": count,
                    "active": ws_id == active_ws,
                }
            )

    if not any(e.get("active") for e in entries) and active_ws is not None:
        entries.append(
            {
                "id": active_ws,
                "name": str(active_ws),
                "windows": win_counts.get(active_ws, 0),
                "active": True,
            }
        )

    entries.sort(key=lambda item: item.get("id", 0))

    if entries:
        parts = []
        tooltip_lines = []
        for entry in entries:
            classes = ["ws-tag"]
            if entry.get("active"):
                classes.append("active")
            elif entry.get("windows", 0) > 0:
                classes.append("busy")
            name = escape(str(entry.get("name", "?")))
            parts.append(
                f"<span class='{' '.join(classes)}'>{name}</span>"
            )
            tooltip_lines.append(
                f"{name}：{entry.get('windows', 0)} 个窗口"
                if entry.get("windows", 0) > 0
                else f"{name}：空"
            )
        text = "".join(parts)
        tooltip = "\n".join(tooltip_lines)
    else:
        text = "<span class='ws-tag'>无</span>"
        tooltip = "没有可显示的工作区"

    print(
        json.dumps(
            {
                "text": text,
                "tooltip": tooltip,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
