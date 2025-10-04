import tkinter as tk
import random

class Wall:
    def __init__(self, canvas, x, y, width=200, height=80, graphics_detail="low"):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.graphics_detail = graphics_detail
        self.wall_elements = []
        self.brick_elements = []
        self.id = self.create_wall()
    
    def create_wall(self):
        """Crea il segmento murato con grafica vettoriale dei mattoni"""
        # Colore base del muro (marrone)
        wall_color = "#8B4513"  # Marrone scuro
        brick_color = "#A0522D"  # Marrone più chiaro per i mattoni
        mortar_color = "#654321"  # Colore malta più scuro
        
        # Crea il rettangolo base del muro
        wall_base = self.canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height,
            fill=wall_color, outline=mortar_color, width=2, tags="wall"
        )
        self.wall_elements.append(wall_base)
        
        # Aggiungi i mattoni solo se la grafica non è molto bassa
        if self.graphics_detail != "very_low":
            self.create_bricks()
        
        return wall_base
    
    def create_bricks(self):
        """Crea la grafica vettoriale dei mattoni all'interno del muro"""
        brick_width = 40
        brick_height = 16
        mortar_thickness = 2
        
        # Colori per i mattoni
        brick_colors = ["#A0522D", "#CD853F", "#D2691E", "#B8860B"]
        mortar_color = "#654321"
        
        rows = int(self.height // (brick_height + mortar_thickness))
        
        for row in range(rows):
            y_pos = self.y + row * (brick_height + mortar_thickness) + mortar_thickness
            
            # Offset alternato per creare il pattern dei mattoni
            offset = (brick_width // 2) if row % 2 == 1 else 0
            
            # Calcola quanti mattoni entrano in questa riga
            cols = int((self.width + offset) // (brick_width + mortar_thickness))
            
            for col in range(cols):
                x_pos = self.x + col * (brick_width + mortar_thickness) + mortar_thickness - offset
                
                # Assicurati che il mattone non esca dai bordi del muro
                if x_pos < self.x:
                    continue
                if x_pos + brick_width > self.x + self.width:
                    brick_width_adjusted = self.x + self.width - x_pos
                    if brick_width_adjusted < 10:  # Troppo piccolo, salta
                        continue
                else:
                    brick_width_adjusted = brick_width
                
                # Scegli un colore casuale per il mattone
                brick_color = random.choice(brick_colors)
                
                # Crea il mattone
                brick = self.canvas.create_rectangle(
                    x_pos, y_pos, x_pos + brick_width_adjusted, y_pos + brick_height,
                    fill=brick_color, outline=mortar_color, width=1, tags="wall"
                )
                self.brick_elements.append(brick)
                
                # Aggiungi dettagli ai mattoni per grafica alta
                if self.graphics_detail == "high":
                    # Linee di texture sui mattoni
                    line1 = self.canvas.create_line(
                        x_pos + 5, y_pos + 4, x_pos + brick_width_adjusted - 5, y_pos + 4,
                        fill="#8B4513", width=1, tags="wall"
                    )
                    line2 = self.canvas.create_line(
                        x_pos + 3, y_pos + 12, x_pos + brick_width_adjusted - 3, y_pos + 12,
                        fill="#8B4513", width=1, tags="wall"
                    )
                    self.brick_elements.extend([line1, line2])
    
    def get_bbox(self):
        """Restituisce il bounding box del muro per le collisioni"""
        return (self.x, self.y, self.x + self.width, self.y + self.height)
    
    def move(self, dx, dy):
        """Muove il muro di dx, dy pixel"""
        self.x += dx
        self.y += dy
        
        # Muovi tutti gli elementi grafici
        for element in self.wall_elements + self.brick_elements:
            self.canvas.move(element, dx, dy)
    
    def is_off_screen(self, screen_height):
        """Controlla se il muro è uscito dallo schermo"""
        return self.y > screen_height
    
    def destroy(self):
        """Rimuove il muro dal canvas"""
        for element in self.wall_elements + self.brick_elements:
            self.canvas.delete(element)
        self.wall_elements.clear()
        self.brick_elements.clear()