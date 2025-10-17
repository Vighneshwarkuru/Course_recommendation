#!/usr/bin/env python3
"""
Test script for Grade Prediction System
"""

import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from test_predictor import test_predictor

if __name__ == "__main__":
    test_predictor()