import random

class Star:
    def __init__(self, canvas, x=None, y=None):
        self.canvas = canvas
        self.x = x if x is not None else random.randint(0, 800)
        self.y = y if y is not None else random.randint(0, 600)
        self.size = random.randint(1, 3)
        self.brightness = random.uniform(0.3, 1.0)
        self.twinkle_speed = random.uniform(0.02, 0.05)
        self.twinkle_phase = random.uniform(0, 6.28)  # 2*pi
        self.star_id = self.create_visual()
    
    def create_visual(self):
        """Crea la rappresentazione visiva della stella"""
        color_intensity = int(255 * self.brightness)
        color = f"#{color_intensity:02x}{color_intensity:02x}{color_intensity:02x}"
        
        if self.size == 1:
            return self.canvas.create_oval(
                self.x, self.y, self.x + 1, self.y + 1,
                fill=color, outline=""
            )
        else:
            return self.canvas.create_oval(
                self.x - self.size//2, self.y - self.size//2,
                self.x + self.size//2, self.y + self.size//2,
                fill=color, outline=""
            )
    
    def update_twinkle(self):
        """Aggiorna l'effetto scintillio della stella"""
        import math
        self.twinkle_phase += self.twinkle_speed
        if self.twinkle_phase > 6.28:  # 2*pi
            self.twinkle_phase -= 6.28
        
        # Calcola la nuova luminosità basata sulla fase di scintillio
        twinkle_factor = (math.sin(self.twinkle_phase) + 1) / 2  # Normalizza tra 0 e 1
        current_brightness = self.brightness * (0.5 + 0.5 * twinkle_factor)
        
        color_intensity = int(255 * current_brightness)
        color = f"#{color_intensity:02x}{color_intensity:02x}{color_intensity:02x}"
        
        self.canvas.itemconfig(self.star_id, fill=color)
    
    def move_down(self, speed=1):
        """Muove la stella verso il basso"""
        self.y += speed
        self.canvas.move(self.star_id, 0, speed)
    
    def is_off_screen(self, screen_height=600):
        """Controlla se la stella è uscita dallo schermo"""
        return self.y > screen_height
    
    def reset_position(self, screen_width=800):
        """Riposiziona la stella in cima allo schermo"""
        old_x, old_y = self.x, self.y
        self.x = random.randint(0, screen_width)
        self.y = random.randint(-50, 0)
        
        # Muovi l'oggetto visivo
        dx = self.x - old_x
        dy = self.y - old_y
        self.canvas.move(self.star_id, dx, dy)
    
    def delete(self):
        """Elimina la stella dal canvas"""
        self.canvas.delete(self.star_id)