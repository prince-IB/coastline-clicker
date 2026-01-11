#!/bin/bash

cd "$(dirname "$0")"

source venv/bin/activate

echo "Building and starting server..."
echo ""
LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "unavailable")
echo "Access your game at:"
echo "  Local:   http://localhost:8000"
echo "  Network: http://$LOCAL_IP:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

pygbag --ume_block 0 main.py