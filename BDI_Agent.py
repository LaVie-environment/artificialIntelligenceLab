#!/usr/bin/env python3

class BDI_Agent:
    def __init__(self, beliefs, desires):
        self.beliefs = beliefs      
        self.desires = desires    
        self.intentions = []

    def update_beliefs(self, new_belief):
        """Update agent's beliefs based on new information."""
        self.beliefs.update(new_belief)

    def add_desire(self, new_desire):
        """Add a new goal to the agent's desires."""
        self.desires.append(new_desire)

    def generate_intentions(self):
        """Select an intention based on the current beliefs and desires."""
        self.intentions = [] 
        for desire in self.desires:
            if desire == "go for a walk" and self.beliefs.get("weather") == "sunny":
                self.intentions.append(f"Action for {desire}")
            elif desire == "read a book":
                self.intentions.append(f"Action for {desire}")
            else:
                print(f"Cannot commit to {desire} based on current beliefs.")

    def execute_intentions(self):
        """Perform actions according to the intentions."""
        for intention in self.intentions:
            print(f"Executing: {intention}")


beliefs = {"location": "home", "weather": "sunny"}
desires = ["go for a walk", "read a book"]

agent = BDI_Agent(beliefs, desires)

agent.update_beliefs({"weather": "rainy"})

agent.generate_intentions()

agent.execute_intentions()
