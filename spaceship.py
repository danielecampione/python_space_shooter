import tkinter as tk

class Spaceship:
    def __init__(self, canvas, x, y, speed=10):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.speed = speed
        self.ship_id = self.create_visual()
        
    def create_visual(self):
        """Crea la rappresentazione visiva della navicella con effetto glow"""
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
        coords = self.get_coords()
        if coords and coords[0] > 0:
            self.canvas.move(self.ship_id, -self.speed, 0)
            self.x -= self.speed
            return True
        return False
    
    def move_right(self, screen_width=800):
        """Muove la navicella a destra"""
        coords = self.get_coords()
        if coords and coords[4] < screen_width:
            self.canvas.move(self.ship_id, self.speed, 0)
            self.x += self.speed
            return True
        return False
    
    def move_to_x(self, new_x, screen_width=800):
        """Muove la navicella a una posizione x specifica"""
        coords = self.get_coords()
        if coords:
            ship_width = coords[4] - coords[0]
            # Limita il movimento ai bordi dello schermo
            if new_x < 0:
                new_x = 0
            elif new_x + ship_width > screen_width:
                new_x = screen_width - ship_width
            # Sposta la navicella
            delta_x = new_x - coords[0]
            self.canvas.move(self.ship_id, delta_x, 0)
            self.x = new_x
            return True
        return False
    
    def get_center_x(self):
        """Restituisce la coordinata x del centro della navicella"""
        coords = self.get_coords()
        if coords:
            return (coords[0] + coords[4]) / 2
        return self.x + 25
    
    def get_top_y(self):
        """Restituisce la coordinata Y della parte superiore della navicella"""
        coords = self.get_coords()
        if coords:
            return coords[1]
        return None
    
    def get_position(self):
        """Restituisce la posizione centrale della navicella"""
        coords = self.get_coords()
        if coords:
            center_x = (coords[0] + coords[2]) / 2
            center_y = (coords[1] + coords[3]) / 2
            return center_x, center_y
        return None, None
    
    def flash(self, colors=["orange", "red", "blue"], steps=10, delay=100):
        """Fa lampeggiare la navicella con i colori specificati"""
        flash_index = 0
        
        def flash_step():
            nonlocal flash_index
            if flash_index < steps:
                color = colors[flash_index % len(colors)]
                self.canvas.itemconfig(self.ship_id, fill=color)
                flash_index += 1
                self.canvas.after(delay, flash_step)
            else:
                self.canvas.itemconfig(self.ship_id, fill="blue")
        
        flash_step()
    

    
    def delete(self):
        """Elimina la navicella dal canvas"""
        self.canvas.delete(self.ship_id)