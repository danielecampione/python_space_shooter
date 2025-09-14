from powerup_base import Powerup

class ExtraLifePowerup(Powerup):
    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y, "extra_life", "green")
    
    def activate(self, game):
        """Attiva l'effetto vita extra"""
        game.lives += 1
        game.update_lives()
        game.show_power_up_text("extra_life")