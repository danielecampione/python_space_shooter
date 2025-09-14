import random

class Powerup:
    def __init__(self, canvas, x, y, powerup_type, color, graphics_detail="low", game_instance=None):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.powerup_type = powerup_type
        self.color = color
        self.speed = 2
        self.graphics_detail = graphics_detail
        self.game_instance = game_instance
        self.powerup_id = self.create_visual()
    
    def create_visual(self):
        """Crea la rappresentazione visiva del power-up"""
        if self.graphics_detail == "high" and self.game_instance:
            # Usa l'immagine specifica per il powerup con definizione alta
            image_name = self.get_powerup_image_name()
            if image_name:
                # Aumenta le dimensioni di 5 volte con definizione grafica alta
                size = (120, 120) if self.graphics_detail == "high" else (24, 24)
                image = self.game_instance.load_image(image_name, size)
                if image:
                    powerup_id = self.canvas.create_image(
                        self.x, self.y, image=image, tags="powerup"
                    )
                    # Mantieni un riferimento all'immagine
                    if not hasattr(self.canvas, 'powerup_images'):
                        self.canvas.powerup_images = []
                    self.canvas.powerup_images.append(image)
                    return powerup_id
        
        # Fallback alla grafica vettoriale
        if self.graphics_detail == "low":
            # Disegno migliorato specifico per ciascun powerup
            if self.powerup_type == "double_fire":
                # Icona doppio proiettile per "Doppio Fuoco"
                powerup_ids = []
                
                # Sfondo circolare
                bg_circle = self.canvas.create_oval(
                    self.x - 12, self.y - 12, self.x + 12, self.y + 12,
                    fill="#FF4500", outline="#FFD700", width=2, tags="powerup"
                )
                powerup_ids.append(bg_circle)
                
                # Due proiettili diagonali stilizzati
                # Proiettile sinistro
                left_projectile = self.canvas.create_line(
                    self.x - 6, self.y + 4, self.x - 2, self.y - 6,
                    fill="#FFFF00", width=3, tags="powerup"
                )
                powerup_ids.append(left_projectile)
                
                # Proiettile destro
                right_projectile = self.canvas.create_line(
                    self.x + 2, self.y - 6, self.x + 6, self.y + 4,
                    fill="#FFFF00", width=3, tags="powerup"
                )
                powerup_ids.append(right_projectile)
                
                # Effetti scintilla alle punte
                left_spark = self.canvas.create_oval(
                    self.x - 3, self.y - 7, self.x - 1, self.y - 5,
                    fill="#FFFFFF", outline="", tags="powerup"
                )
                powerup_ids.append(left_spark)
                
                right_spark = self.canvas.create_oval(
                    self.x + 1, self.y - 7, self.x + 3, self.y - 5,
                    fill="#FFFFFF", outline="", tags="powerup"
                )
                powerup_ids.append(right_spark)
                
                return bg_circle  # Restituisce l'ID principale per il tracking
            else:
                # Forma a cuore per "Vita Extra"
                path = [
                    self.x, self.y + 8,
                    self.x - 10, self.y - 4,
                    self.x - 6, self.y - 12,
                    self.x, self.y - 6,
                    self.x + 6, self.y - 12,
                    self.x + 10, self.y - 4
                ]
                return self.canvas.create_polygon(path, fill=self.color, outline="white", width=2, smooth=True, tags="powerup")
        
        # Modalità molto bassa: semplice cerchio
        radius = 10
        return self.canvas.create_oval(
            self.x - radius, self.y - radius, self.x + radius, self.y + radius,
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
    
    def get_powerup_image_name(self):
        """Restituisce il nome dell'immagine del powerup in base al tipo"""
        if self.powerup_type == "double_fire":
            return "double_fire_powerup.png"
        elif self.powerup_type == "extra_life":
            return "extralife_powerup.png"
        return None
    
    def activate(self, game):
        """Attiva l'effetto del power-up - da implementare nelle sottoclassi"""
        pass
    
    def delete(self):
        """Elimina il power-up dal canvas"""
        self.canvas.delete(self.powerup_id)
