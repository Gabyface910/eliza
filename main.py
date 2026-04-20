import sys
import os
import json
import re
import random

class Eliza:
    def __init__(self, model_file="default"):
        self.load_model(model_file)
        self.memory = []

    def load_model(self, model_file):
        home_dir = os.path.expanduser("~")
        full_path = f"{home_dir}/eliza/models/{model_file}.elz"
        
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Model file '{full_path}' not found.")
        
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

if __name__ == "__main__":
    # Get model name from argv, default to 'default'
    model_name = sys.argv[1] if len(sys.argv) > 1 else "default"
    
    try:
        bot = Eliza(model_name)
        print(f"--- {bot.name} Loaded ---")
        while True:
            user_input = input("> ")
            if user_input.lower() in ['exit', 'quit']: break
            print(bot.prompt(user_input))
    except Exception as e:
        print(f"Error: {e}")
