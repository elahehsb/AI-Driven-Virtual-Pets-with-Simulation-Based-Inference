import numpy as np
import pandas as pd

class VirtualPet:
    def __init__(self):
        # Initial attributes of the pet
        self.happiness = 50
        self.health = 50
        self.hunger = 50

    def interact(self, action):
        if action == 'feed':
            self.hunger = max(0, self.hunger - 10)
            self.happiness += 5
        elif action == 'play':
            self.happiness += 10
            self.health += 5
        elif action == 'rest':
            self.health += 10
        else:
            raise ValueError("Unknown action")

    def update_state(self):
        # Simulate state changes over time
        self.happiness = max(0, self.happiness - 1)
        self.health = max(0, self.health - 1)
        self.hunger = min(100, self.hunger + 1)

    def get_state(self):
        return {'happiness': self.happiness, 'health': self.health, 'hunger': self.hunger}
