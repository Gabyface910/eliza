import re
import random
import json
import sys
import os

class Eliza:
    def __init__(self, model_file="default"):
        # Load the specified model (persona)
        self.load_model(model_file)
        self.memory = []

    def load_model(self, model_file):
        # 1. Properly construct the full path
        home_dir = os.path.expanduser("~")
        full_path = f"{home_dir}/eliza/models/{model_file}.elz"
        
        # 2. Check existence
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Model file '{full_path}' not found.")
        
        # 3. Open using the full path
        with open(full_path, 'r') as f:
            data = json.load(f)
            self.rules = data['rules']
            self.default_responses = data['default_responses']
            self.name = data.get('name', 'Eliza-2')
          
    def reflect(self, fragment):
        tokens = fragment.lower().split()
        replacements = {"i": "you", "am": "are", "you": "i", "are": "am", "my": "your", "your": "my"}
        return " ".join([replacements.get(t, t) for t in tokens])

    def prompt(self, user_input):
        """The primary interface for interacting with the model."""
        text = user_input.lower().strip()
        self.memory.append(text)
        
        for pattern, responses in self.rules.items():
            match = re.search(pattern, text)
            if match:
                if match.groups():
                    reflected = self.reflect(match.group(1))
                    return random.choice(responses).format(reflected)
                return random.choice(responses)
        
        return random.choice(self.default_responses)

