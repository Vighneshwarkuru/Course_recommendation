#!/usr/bin/env python3
"""
Command-line interface runner for Grade Prediction System
"""

import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from cli_interface import interactive_predictor

if __name__ == "__main__":
    interactive_predictor()