import random
from star import Star

class StarField:
    def __init__(self, canvas, num_stars=100):
        self.canvas = canvas
        self.stars = []
        self.create_stars(num_stars)
    
    def create_stars(self, num_stars):
        """Crea le stelle iniziali"""
        for _ in range(num_stars):
            star = Star(self.canvas)
            self.stars.append(star)
    
    def update_stars(self):
        """Aggiorna tutte le stelle (movimento e scintillio)"""
        for star in self.stars:
            star.move_down(random.uniform(0.5, 2.0))
            star.update_twinkle()
            
            if star.is_off_screen():
                star.reset_position()
    
    def clear_all_stars(self):
        """Rimuove tutte le stelle dal canvas"""
        for star in self.stars:
            star.delete()
        self.stars.clear()