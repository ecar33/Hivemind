#!/bin/bash
npx tailwindcss -i ./hivemind/static/css/input.css -o ./hivemind/static/css/output.css --watch &
py run.py