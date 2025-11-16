#!/usr/bin/env bash
set -euo pipefail
choice=$(cliphist list | rofi -dmenu)
[ -z "$choice" ] && exit 0
decoded=$(printf "%s" "$choice" | cliphist decode)
printf "%s" "$decoded" | wl-copy
printf "%s" "$decoded" | wtype -
