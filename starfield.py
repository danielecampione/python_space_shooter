import tkinter as tk
import random

class Star:
    def __init__(self, canvas, x, y, size):
        self.canvas = canvas
        self.speed = random.uniform(1, 3)
        self.brightness = random.uniform(0.5, 1.0)
        self.delta = random.uniform(-0.02, 0.02)
        
        # Crea la stella visuale
        self.id = self.canvas.create_oval(
            x, y, x + size, y + size, fill="white", outline=""
        )
    
    def update(self):
        """Aggiorna la luminosità e la posizione della stella"""
        # Aggiorna la luminosità
        self.brightness += self.delta
        if self.brightness <= 0.5 or self.brightness >= 1.0:
            self.delta *= -1
        brightness = int(255 * self.brightness)
        color = f"#{brightness:02x}{brightness:02x}{brightness:02x}"
        self.canvas.itemconfig(self.id, fill=color)
        
        # Muovi la stella
        self.canvas.move(self.id, 0, self.speed)
        coords = self.canvas.coords(self.id)
        if not coords or len(coords) < 4 or coords[3] > 600:
            x = random.randint(0, 800)
            y = -5
            self.canvas.coords(self.id, x, y, x + 2, y + 2)
    
    def get_id(self):
        """Restituisce l'ID della stella nel canvas"""
        return self.id
    
    def destroy(self):
        """Distrugge la stella rimuovendola dal canvas"""
        self.canvas.delete(self.id)

class StarField:
    def __init__(self, canvas, num_stars=100):
        self.canvas = canvas
        self.stars = []
        self.create_stars(num_stars)
    
    def create_stars(self, num_stars):
        """Crea il campo stellato iniziale"""
        for _ in range(num_stars):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            size = random.choice([1, 2])
            star = Star(self.canvas, x, y, size)
            self.stars.append(star)
    
    def update_all_stars(self):
        """Aggiorna tutte le stelle del campo stellato"""
        for star in self.stars:
            star.update()
    
    def get_stars(self):
        """Restituisce la lista delle stelle"""
        return self.stars
    
    def clear_all_stars(self):
        """Rimuove tutte le stelle"""
        for star in self.stars:
            star.destroy()
        self.stars.clear()
    
    def get_star_count(self):
        """Restituisce il numero di stelle nel campo"""
        return len(self.stars)