#!/bin/bash

cd "$(dirname "$0")"

source venv/bin/activate

python3 -m pygbag --build --bind 0.0.0.0 .
cd build/web
python3 -m http.server 8000 --bind 0.0.0.0
LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "unavailable")
echo "Server built and started"
echo ""
echo "Access your game at:"
echo "  Local:   http://localhost:8000"
echo "  Network: http://$LOCAL_IP:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""