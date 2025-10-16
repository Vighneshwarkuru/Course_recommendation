#!/usr/bin/env python3
"""
Web API runner for Grade Prediction System
"""

import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from web_api import start_api

if __name__ == "__main__":
    start_api()