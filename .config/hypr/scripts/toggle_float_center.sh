#!/bin/sh
hyprctl dispatch togglefloating
if [ "$(hyprctl activewindow -j | jq -r '.floating')" = "true" ]; then
    hyprctl dispatch centerwindow 1
    hyprctl dispatch resizeactive exact 92% 90%
fi
