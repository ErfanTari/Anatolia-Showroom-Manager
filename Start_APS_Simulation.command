#!/bin/zsh
cd -- "${0:A:h}"
printf 'Anatolia Studio: http://127.0.0.1:8765/studio/web/\nKeep this window open. Press Control-C to stop.\n'
python3 studio/backend/server.py --port 8765
