# agents.py
from flood_agent import flood_agent
from safety_agent import safety_agent

class FloodRiskAgent:
    def run(self, place_name):
        """
        Agent to get flood forecast for a location
        """
        return flood_agent(place_name)


class SafetyAgent:
    def run(self, lat, lon):
        """
        Agent to get safer nearby locations
        """
        return safety_agent(lat, lon)
