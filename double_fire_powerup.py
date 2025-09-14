from powerup_base import Powerup

class DoubleFirePowerup(Powerup):
    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y, "double_fire", "blue")
    
    def activate(self, game):
        """Attiva l'effetto doppio fuoco"""
        game.double_fire_active = True
        game.double_fire_timer = 300  # 10 secondi a 30 FPS
        game.show_power_up_text("double_fire")