import os
import random

class Fruit:
    def __init__(self, image_folder):
        self.image_folder = image_folder
        self.items = [
            {"name": "Rocket", "probability": 0.50},
            {"name": "Spin", "probability": 0.50},
            {"name": "Chop", "probability": 0.50},
            {"name": "Spring", "probability": 0.50},
            {"name": "Bomb", "probability": 0.50},
            {"name": "Smoke", "probability": 0.50},
            {"name": "Spike", "probability": 0.50},
            {"name": "Flame", "probability": 0.50},
            {"name": "Falcon", "probability": 0.50},
            {"name": "Ice", "probability": 0.50},
            {"name": "Sand", "probability": 0.50},
            {"name": "Dark", "probability": 0.50},
            {"name": "Diamond", "probability": 0.50},
            {"name": "Light", "probability": 0.50},
            {"name": "Rubber", "probability": 0.50},
            {"name": "Barrier", "probability": 0.50},
            {"name": "Ghost", "probability": 0.50},
            {"name": "Magma", "probability": 0.50},
            {"name": "Quake", "probability": 0.50},
            {"name": "Buddha", "probability": 0.50},
            {"name": "Love", "probability": 0.50},
            {"name": "Spider", "probability": 0.50},
            {"name": "Sound", "probability": 0.50},
            {"name": "Phoenix", "probability": 0.50},
            {"name": "Portal", "probability": 0.50},
            {"name": "Rumble", "probability": 0.50},
            {"name": "Pain", "probability": 0.50},
            {"name": "Blizzard", "probability": 0.50},
            {"name": "Gravity", "probability": 0.50},
            {"name": "Mammoth", "probability": 0.50},
            {"name": "Dough", "probability": 0.50},
            {"name": "Shadow", "probability": 0.50},
            {"name": "Venom", "probability": 0.50},
            {"name": "Control", "probability": 0.50},
            {"name": "Spirit", "probability": 0.50},
            {"name": "Dragon", "probability": 0.50},
            {"name": "Leopard", "probability": 0.50},
        ]
        self.fruits_rarity = {
            'Rocket': 'Common',
            'Bomb': 'Common',
            'Chop': 'Common',
            'Spike': 'Common',
            'Spin': 'Common',
            'Spring': 'Common',
            'Smoke': 'Common',
            'Dark': 'Uncommon',
            'Diamond': 'Uncommon',
            'Falcon': 'Uncommon',
            'Flame': 'Uncommon',
            'Ice': 'Uncommon',
            'Sand': 'Uncommon',
            'Barrier': 'Rare',
            'Ghost': 'Rare',
            'Light': 'Rare',
            'Magma': 'Rare',
            'Rubber': 'Rare',
            'Blizzard': 'Legendary',
            'Buddha': 'Legendary',
            'Love': 'Legendary',
            'Phoenix': 'Legendary',
            'Portal': 'Legendary',
            'Pain' : 'Legendary',
            'Rumble': 'Legendary',
            'Sound': 'Legendary',
            'Spider': 'Legendary',
            'Quake': 'Legendary',
            'Gravity': 'Mythical',
            'Mammoth': 'Mythical',
            'Dough': 'Mythical',
            'Shadow': 'Mythical',
            'Venom': 'Mythical',
            'Control': 'Mythical',
            'Spirit': 'Mythical',
            'Dragon': 'Mythical',
            'Leopard': 'Mythical',
        }

        self.chance_percentage = {
            'common': 50,
            'uncommon': 25,
            'rare': 20,
            'legendary': 4.5,
            'mythical': 0.5,
        }


    def get_random_fruit(self):
        random_number = random.uniform(0, 1)

        if random_number < self.chance_percentage['common'] / 100:
            # Common fruits with 50% probability
            return random.choice([
                {"name": "Rocket", "probability": 0.5},
                {"name": "Bomb", "probability": 0.5},
                {"name": "Chop", "probability": 0.5},
                {"name": "Spike", "probability": 0.5},
                {"name": "Spin", "probability": 0.5},
                {"name": "Spring", "probability": 0.5},
                {"name": "Smoke", "probability": 0.5},
            ])

        elif random_number < (self.chance_percentage['common'] + self.chance_percentage['uncommon']) / 100:
            # Uncommon fruits with 25% probability
            return random.choice([
                {"name": "Dark", "probability": 0.25},
                {"name": "Diamond", "probability": 0.25},
                {"name": "Falcon", "probability": 0.25},
                {"name": "Flame", "probability": 0.25},
                {"name": "Ice", "probability": 0.25},
                {"name": "Sand", "probability": 0.25},
            ])

        elif random_number < (self.chance_percentage['common'] + self.chance_percentage['uncommon'] + self.chance_percentage['rare']) / 100:
            # Rare fruits with 20% probability
            return random.choice([
                {"name": "Barrier", "probability": 0.2},
                {"name": "Light", "probability": 0.2},
                {"name": "Magma", "probability": 0.2},
                {"name": "Ghost", "probability": 0.2},
                {"name": "Rubber", "probability": 0.2},
            ])

        elif random_number < (self.chance_percentage['common'] + self.chance_percentage['uncommon'] + self.chance_percentage['rare'] + self.chance_percentage['legendary']) / 100:
            # Legendary fruits with updated probabilities
            return random.choice([
                {"name": "Blizzard", "probability": 0.03},
                {"name": "Buddha", "probability": 0.025},
                {"name": "Love", "probability": 0.035},
                {"name": "Phoenix", "probability": 0.03},
                {"name": "Portal", "probability": 0.02},
                {"name": "Pain", "probability": 0.02},
                {"name": "Rumble", "probability": 0.025},
                {"name": "Sound", "probability": 0.02},
                {"name": "Spider", "probability": 0.035},
                {"name": "Quake", "probability": 0.035},
            ])

        elif random_number < (self.chance_percentage['common'] + self.chance_percentage['uncommon'] + self.chance_percentage['rare'] + self.chance_percentage['legendary'] + self.chance_percentage['mythical']) / 100:
            # Mythical fruits with specified probabilities
            return random.choice([
                {"name": "Gravity", "probability": 0.0035},
                {"name": "Mammoth", "probability": 0.003},
                {"name": "Dough", "probability": 0.0008},
                {"name": "Shadow", "probability": 0.002},
                {"name": "Venom", "probability": 0.0015},
                {"name": "Control", "probability": 0.001},
                {"name": "Spirit", "probability": 0.0025},
                {"name": "Dragon", "probability": 0.0004},
                {"name": "Leopard", "probability": 0.0003},
            ])


    def get_fruit_value(self, fruit_name):
        fruit_values = {
            "Rocket": 50,
            "Spin" : 75,
            "Chop" :300,
            "Spring" : 600,
            "Bomb" : 800,
            "Smoke": 1000,
            "Spike": 1800,
            "Flame": 2500,
            "Falcon" : 3000,
            "Ice": 3500,
            "Sand" : 4200,
            "Dark" : 5000,
            "Diamond" : 6000,
            "Light": 6500,
            "Rubber" : 7500,
            "Barrier" : 8000,
            "Ghost": 9400,
            "Magma": 9600,
            "Quake" : 10000,
            "Buddha": 12000,
            "Love": 13000,
            "Spider" : 15000,
            "Sound" : 17000,
            "Phoenix": 18000 ,
            "Portal": 19000,
            "Rumble": 21000,
            "Pain" : 23000,
            "Blizzard": 24000,
            "Gravity" : 25000,
            "Mammoth" : 27000,
            "Dough": 28000,
            "Shadow": 29000,
            "Venom": 30000,
            "Control": 32000,
            "Spirit": 34000,
            "Dragon": 35000,
            "Leopard": 50000,
        }
        return fruit_values.get(fruit_name, 0)

    def get_fruit_image(self, fruit):
        fruit_name = fruit["name"]
        image_path = os.path.join(self.image_folder, f"{fruit_name}.png")
        return image_path
    def get_fruit_names(self):
        return [item["name"] for item in self.items]
