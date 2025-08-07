import random

class Powerup:
    def __init__(self, canvas, x, y, powerup_type, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.powerup_type = powerup_type
        self.color = color
        self.speed = 2
        self.powerup_id = self.create_visual()
    
    def create_visual(self):
        """Crea la rappresentazione visiva del power-up"""
        return self.canvas.create_oval(
            self.x - 10, self.y - 10, self.x + 10, self.y + 10,
            fill=self.color, outline="white", width=2
        )
    
    def move_down(self):
        """Muove il power-up verso il basso"""
        self.y += self.speed
        self.canvas.move(self.powerup_id, 0, self.speed)
    
    def is_off_screen(self, screen_height=600):
        """Controlla se il power-up è uscito dallo schermo"""
        return self.y > screen_height + 20
    
    def get_bbox(self):
        """Restituisce il bounding box del power-up"""
        return self.canvas.bbox(self.powerup_id)
    
    def get_coords(self):
        """Restituisce le coordinate del power-up per il controllo delle collisioni"""
        return self.canvas.bbox(self.powerup_id)
    
    def get_type(self):
        """Restituisce il tipo di power-up"""
        return self.powerup_type
    
    def activate(self, game):
        """Attiva l'effetto del power-up - da implementare nelle sottoclassi"""
        pass
    
    def delete(self):
        """Elimina il power-up dal canvas"""
        self.canvas.delete(self.powerup_id)