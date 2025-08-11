import tkinter as tk

class Spaceship:
    def __init__(self, canvas, x, y, speed=10, graphics_detail="low", game_instance=None):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.speed = speed
        self.graphics_detail = graphics_detail
        self.game_instance = game_instance
        self.ship_id = self.create_visual()
        
    def create_visual(self):
        """Crea la rappresentazione visiva della navicella"""
        if self.graphics_detail == "high" and self.game_instance:
            # Usa l'immagine della navicella
            image = self.game_instance.load_image("spaceship.png", (50, 50))
            if image:
                ship = self.canvas.create_image(
                    self.x + 25, self.y, image=image, tags="ship"
                )
                # Mantieni un riferimento all'immagine per evitare che venga garbage collected
                self.canvas.image_ref = image
                return ship
        
        # Fallback alla grafica vettoriale
        points = [
            self.x + 25, self.y - 25,  # Punta superiore
            self.x, self.y + 10,       # Base sinistra
            self.x + 50, self.y + 10   # Base destra
        ]
        ship = self.canvas.create_polygon(
            points, fill="blue", outline="cyan", width=2, tags="ship"
        )
        return ship
    
    def get_id(self):
        """Restituisce l'ID della navicella"""
        return self.ship_id
    
    def get_coords(self):
        """Restituisce le coordinate della navicella"""
        return self.canvas.coords(self.ship_id)
    
    def get_bbox(self):
        """Restituisce il bounding box della navicella"""
        return self.canvas.bbox(self.ship_id)
    
    def move_left(self):
        """Muove la navicella a sinistra"""
        bbox = self.get_bbox()
        if bbox and bbox[0] > 0:
            self.canvas.move(self.ship_id, -self.speed, 0)
            self.x -= self.speed
            return True
        return False
    
    def move_right(self, screen_width=800):
        """Muove la navicella a destra"""
        bbox = self.get_bbox()
        if bbox and bbox[2] < screen_width:
            self.canvas.move(self.ship_id, self.speed, 0)
            self.x += self.speed
            return True
        return False
    
    def move_to_x(self, new_x, screen_width=800):
        """Muove la navicella a una posizione x specifica"""
        bbox = self.get_bbox()
        if bbox:
            ship_width = bbox[2] - bbox[0]
            # Limita il movimento ai bordi dello schermo
            if new_x < 0:
                new_x = 0
            elif new_x + ship_width > screen_width:
                new_x = screen_width - ship_width
            # Sposta la navicella
            delta_x = new_x - bbox[0]
            self.canvas.move(self.ship_id, delta_x, 0)
            self.x = new_x
            return True
        return False
    
    def get_center_x(self):
        """Restituisce la coordinata x del centro della navicella"""
        bbox = self.get_bbox()
        if bbox:
            return (bbox[0] + bbox[2]) / 2
        # Fallback alle coordinate memorizzate
        return self.x + 25
    
    def get_top_y(self):
        """Restituisce la coordinata Y della parte superiore della navicella"""
        bbox = self.get_bbox()
        if bbox:
            return bbox[1]
        # Fallback alle coordinate memorizzate
        return self.y
    
    def get_position(self):
        """Restituisce la posizione centrale della navicella"""
        bbox = self.get_bbox()
        if bbox:
            center_x = (bbox[0] + bbox[2]) / 2
            center_y = (bbox[1] + bbox[3]) / 2
            return center_x, center_y
        # Fallback alle coordinate memorizzate
        return self.x + 25, self.y + 25
    
    def flash(self, colors=["orange", "red", "blue"], steps=10, delay=100):
        """Fa lampeggiare la navicella con i colori specificati"""
        flash_index = 0
        original_state = "normal"
        
        def flash_step():
            nonlocal flash_index
            if flash_index < steps:
                if self.graphics_detail == "high":
                    # Per le immagini, alterna tra nascosto e visibile
                    state = "hidden" if flash_index % 2 == 0 else "normal"
                    self.canvas.itemconfig(self.ship_id, state=state)
                else:
                    # Per i poligoni, cambia il colore
                    color = colors[flash_index % len(colors)]
                    self.canvas.itemconfig(self.ship_id, fill=color)
                flash_index += 1
                self.canvas.after(delay, flash_step)
            else:
                # Ripristina lo stato originale
                if self.graphics_detail == "high":
                    self.canvas.itemconfig(self.ship_id, state="normal")
                else:
                    self.canvas.itemconfig(self.ship_id, fill="blue")
        
        flash_step()
    

    
    def delete(self):
        """Elimina la navicella dal canvas"""
        self.canvas.delete(self.ship_id)