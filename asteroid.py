import tkinter as tk
import random

class Asteroid:
    def __init__(self, canvas, x, y, size, speed, direction):
        self.canvas = canvas
        self.size = size
        self.speed = speed
        self.direction = direction
        
        # Crea l'asteroide visuale
        self.id = self.canvas.create_oval(
            x, y, x + size, y + size, 
            fill="gray", outline="darkgray", tags="asteroid"
        )
    
    def move(self):
        """Muove l'asteroide secondo la sua direzione e velocità"""
        dx = 0
        dy = self.speed
        if self.direction == "diagonal":
            dx = random.choice([-1, 1]) * self.speed / 2
        self.canvas.move(self.id, dx, dy)
    
    def get_coords(self):
        """Restituisce le coordinate dell'asteroide"""
        return self.canvas.coords(self.id)
    
    def is_out_of_bounds(self):
        """Verifica se l'asteroide è uscito dai limiti dello schermo"""
        coords = self.get_coords()
        if not coords or len(coords) < 4:
            return True
        return coords[3] > 600 or coords[2] < 0 or coords[0] > 800
    
    def get_center(self):
        """Restituisce le coordinate del centro dell'asteroide"""
        coords = self.get_coords()
        if coords and len(coords) >= 4:
            x = (coords[0] + coords[2]) / 2
            y = (coords[1] + coords[3]) / 2
            return x, y
        return None, None
    
    def destroy(self):
        """Distrugge l'asteroide rimuovendolo dal canvas"""
        self.canvas.delete(self.id)
    
    def get_size(self):
        """Restituisce la dimensione dell'asteroide"""
        return self.size
    
    def get_id(self):
        """Restituisce l'ID dell'asteroide nel canvas"""
        return self.id