import os
import sys

# Add the parent directory (project root) to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db import get_interaction_history

logs = get_interaction_history()

for log in logs:
    timestamp, agent, question, response = log[4], log[1], log[2], log[3]
    print(f"[{timestamp}] ({agent.capitalize()}): {question} → {response[:60]}...")
