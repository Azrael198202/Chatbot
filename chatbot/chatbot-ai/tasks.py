#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
File Name: tasks.py
Author: Kan
Create Date: 2025-03-12
Description: Background tasks, including continuous learning and model optimization.
Version: 1.0.0
"""

import time
from document_loader import continuous_learning
from llm_handler import retrain_model

def schedule_tasks():
    """Scheduled tasks"""
    while True:
        # Execute continuous learning every hour
        continuous_learning()
        # Perform model optimization once a day at 2 AM.
        if time.localtime().tm_hour == 2:
            retrain_model()
        time.sleep(3600)  # Check every hour