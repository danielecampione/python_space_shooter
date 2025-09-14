import tkinter as tk
import random

class Asteroid:
    def __init__(self, canvas, x, y, size, speed, direction, graphics_detail="low", game_instance=None):
        self.canvas = canvas
        self.size = size
        self.speed = speed
        self.direction = direction
        self.graphics_detail = graphics_detail
        self.game_instance = game_instance
        
        # Crea l'asteroide visuale
        self.id = self.create_visual(x, y)
    
    def create_visual(self, x, y):
        """Crea la rappresentazione visiva dell'asteroide"""
        if self.graphics_detail == "high" and self.game_instance:
            # Usa l'immagine dell'asteroide con dimensioni aumentate per definizione alta
            image_name = self.game_instance.get_asteroid_image_name(self.size)
            # Aumenta le dimensioni dell'immagine per definizione grafica alta
            image_size = int(self.size * 1.8)  # Aumenta del 80% le dimensioni
            image = self.game_instance.load_image(image_name, (image_size, image_size))
            if image:
                asteroid_id = self.canvas.create_image(
                    x + self.size/2, y + self.size/2, image=image, tags="asteroid"
                )
                # Mantieni un riferimento all'immagine
                if not hasattr(self.canvas, 'asteroid_images'):
                    self.canvas.asteroid_images = []
                self.canvas.asteroid_images.append(image)
                return asteroid_id
        
        # Fallback alla grafica vettoriale
        return self.canvas.create_oval(
            x, y, x + self.size, y + self.size, 
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
    
    def get_bbox(self):
        """Restituisce il bounding box dell'asteroide"""
        return self.canvas.bbox(self.id)
    
    def is_out_of_bounds(self):
        """Verifica se l'asteroide è uscito dai limiti dello schermo"""
        bbox = self.get_bbox()
        if not bbox or len(bbox) < 4:
            return True
        return bbox[3] > 600 or bbox[2] < 0 or bbox[0] > 800
    
    def get_center(self):
        """Restituisce le coordinate del centro dell'asteroide"""
        bbox = self.get_bbox()
        if bbox and len(bbox) >= 4:
            x = (bbox[0] + bbox[2]) / 2
            y = (bbox[1] + bbox[3]) / 2
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