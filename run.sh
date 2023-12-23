#!/bin/bash

cd ~/watch-sleep-tracker

source .venv/bin/activate
cd src
python main.py &

cd svelte-front
npm start
