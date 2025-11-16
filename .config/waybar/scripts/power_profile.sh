#!/usr/bin/env bash
set -euo pipefail
if ! mode=$(powerprofilesctl get 2>/dev/null); then
    mode="unknown"
fi
mode=${mode//$'\n'/}
case "$mode" in
    performance)
        icon=$'\uf0e7'
        label="性能"
        ;;
    balanced)
        icon=$'\uf24e'
        label="均衡"
        ;;
    power-saver)
        icon=$'\uf06c'
        label="节能"
        ;;
    *)
        icon=$'\uf059'
        label="未知"
        mode="unknown"
        ;;
esac
printf '{"text":"%s %s","tooltip":"电源模式：%s","class":["%s"]}\n' "$icon" "$label" "$mode" "$mode"
