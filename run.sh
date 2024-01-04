#!/bin/bash
tmux new-session -d -A -s dev \; send -t dev ".venv/bin/python3 ./dev/main.py" ENTER \;
tmux new-session -d -A -s web \; send -t web "sudo .venv/bin/python3 ./web/web.py" ENTER \;
