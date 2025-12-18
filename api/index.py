"""
Vercel Serverless Function Entry Point
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import WasteDetectionApp

# Create app instance
waste_app = WasteDetectionApp()
app = waste_app.app

# Vercel handler
def handler(request):
    return app(request.environ, lambda *args: None)
