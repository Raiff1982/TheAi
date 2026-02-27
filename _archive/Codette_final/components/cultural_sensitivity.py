class CulturalSensitivityEngine:
    """Ensures responses are culturally sensitive and inclusive"""
    def __init__(self):
        self.guidelines = {
            "respect": "Respect diverse cultures and perspectives.",
            "inclusivity": "Promote inclusivity in all responses.",
            "awareness": "Be aware of cultural nuances and sensitivities."
        }

    def apply_guidelines(self, response: str) -> str:
        """Apply cultural sensitivity guidelines to the response"""
        for key, guideline in self.guidelines.items():
            response += f"\n{key.capitalize()}: {guideline}"
        return response