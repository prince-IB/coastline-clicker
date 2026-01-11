#!/bin/bash

cd "$(dirname "$0")"

source venv/bin/activate

echo "Building and starting server..."
echo ""
echo "Access your game at: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

pygbag --ume_block 0 main.py