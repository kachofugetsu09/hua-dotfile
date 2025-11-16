#!/usr/bin/env bash
set -euo pipefail
icon_on="\uf294"
icon_off="\uf294"
show=$(bluetoothctl show 2>/dev/null || true)
powered=$(printf '%s' "$show" | awk -F': ' '/Powered/ {print $2}' | tr 'A-Z' 'a-z')
if [[ -z "$powered" || "$powered" != "yes" ]]; then
    printf '{"text":"%s Off","class":"off","tooltip":"Bluetooth is disabled"}' "$icon_off"
    exit 0
fi
connected_devices=$(bluetoothctl devices Connected 2>/dev/null || true)
if [[ -z "$connected_devices" ]]; then
    printf '{"text":"%s","class":"on","tooltip":"Bluetooth on, no devices connected"}' "$icon_on"
    exit 0
fi
primary_device=$(printf '%s' "$connected_devices" | head -n1 | cut -d' ' -f3-)
count=$(printf '%s' "$connected_devices" | grep -c '^Device' || true)
tooltip="Connected devices: $(printf '%s' "$connected_devices" | cut -d' ' -f3- | paste -sd ', ' -)"
if [[ "$count" -gt 1 ]]; then
    text="$icon_on $count"
else
    text="$icon_on $primary_device"
fi
printf '{"text":"%s","class":"connected","tooltip":"%s"}' "$text" "$tooltip"
