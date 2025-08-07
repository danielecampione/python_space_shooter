import random
from extra_life_powerup import ExtraLifePowerup
from double_fire_powerup import DoubleFirePowerup

class PowerupManager:
    def __init__(self, canvas):
        self.canvas = canvas
        self.powerups = []
        self.spawn_timer = 0
        self.spawn_interval = 600  # 20 secondi a 30 FPS
    
    def spawn_powerup(self):
        """Genera un nuovo power-up casualmente"""
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            x = random.randint(50, 750)
            y = -20
            
            # Scegli casualmente il tipo di power-up
            if random.choice([True, False]):
                powerup = ExtraLifePowerup(self.canvas, x, y)
            else:
                powerup = DoubleFirePowerup(self.canvas, x, y)
            
            self.powerups.append(powerup)
    
    def move_all_powerups(self):
        """Muove tutti i power-up e rimuove quelli fuori schermo"""
        powerups_to_remove = []
        
        for powerup in self.powerups:
            powerup.move_down()
            if powerup.is_off_screen():
                powerup.delete()
                powerups_to_remove.append(powerup)
        
        for powerup in powerups_to_remove:
            self.powerups.remove(powerup)
    
    def get_powerups(self):
        """Restituisce la lista dei power-up attivi"""
        return self.powerups
    
    def remove_powerup(self, powerup):
        """Rimuove un power-up specifico"""
        if powerup in self.powerups:
            powerup.delete()
            self.powerups.remove(powerup)
    
    def clear_all_powerups(self):
        """Rimuove tutti i power-up"""
        for powerup in self.powerups:
            powerup.delete()
        self.powerups.clear()