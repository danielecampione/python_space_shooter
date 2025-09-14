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
        self.visual_elements = []  # Lista per tenere traccia di tutti gli elementi grafici
        
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
        elif self.graphics_detail == "low":
            # Grafica migliorata per livello "Bassa" - asteroide con forma irregolare e sfumature
            asteroid_ids = []
            
            # Genera punti per una forma irregolare
            center_x = x + self.size / 2
            center_y = y + self.size / 2
            radius = self.size / 2
            
            # Crea una forma irregolare con 8-12 punti
            num_points = random.randint(8, 12)
            points = []
            for i in range(num_points):
                angle = (2 * 3.14159 * i) / num_points
                # Varia il raggio per creare irregolarità
                point_radius = radius * random.uniform(0.7, 1.3)
                point_x = center_x + point_radius * (angle ** 0.5 % 1) * 2 - 1
                point_y = center_y + point_radius * ((angle * 1.3) ** 0.5 % 1) * 2 - 1
                points.extend([point_x, point_y])
            
            # Colori basati sulla dimensione dell'asteroide
            if self.size <= 30:
                colors = ["#8B4513", "#A0522D", "#CD853F"]  # Marrone per piccoli
            elif self.size <= 50:
                colors = ["#696969", "#808080", "#A9A9A9"]  # Grigio per medi
            else:
                colors = ["#2F4F4F", "#708090", "#778899"]  # Grigio scuro per grandi
            
            # Crea più strati per effetto di profondità
            for i, color in enumerate(colors):
                # Scala i punti per ogni strato
                scaled_points = []
                scale_factor = 1.0 - (i * 0.15)
                for j in range(0, len(points), 2):
                    scaled_x = center_x + (points[j] - center_x) * scale_factor
                    scaled_y = center_y + (points[j+1] - center_y) * scale_factor
                    scaled_points.extend([scaled_x, scaled_y])
                
                layer = self.canvas.create_polygon(
                    scaled_points, fill=color, outline="", tags="asteroid", smooth=True
                )
                asteroid_ids.append(layer)
                self.visual_elements.append(layer)  # Aggiungi alla lista degli elementi
            
            # Aggiunge alcuni dettagli superficiali (crateri)
            for _ in range(random.randint(2, 4)):
                crater_x = center_x + random.uniform(-radius*0.6, radius*0.6)
                crater_y = center_y + random.uniform(-radius*0.6, radius*0.6)
                crater_size = random.uniform(2, 6)
                crater = self.canvas.create_oval(
                    crater_x - crater_size, crater_y - crater_size,
                    crater_x + crater_size, crater_y + crater_size,
                    fill="#2F2F2F", outline="", tags="asteroid"
                )
                asteroid_ids.append(crater)
                self.visual_elements.append(crater)  # Aggiungi alla lista degli elementi
            
            # Restituisce l'ID del primo strato per il tracking
            return asteroid_ids[0] if asteroid_ids else None
        
        # Fallback alla grafica vettoriale minimale (Molto bassa)
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
        
        # Muove tutti gli elementi grafici dell'asteroide
        if self.visual_elements:
            for element_id in self.visual_elements:
                self.canvas.move(element_id, dx, dy)
        else:
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
        # Elimina tutti gli elementi grafici dell'asteroide
        if self.visual_elements:
            for element_id in self.visual_elements:
                self.canvas.delete(element_id)
            self.visual_elements.clear()
        else:
            self.canvas.delete(self.id)
    
    def get_size(self):
        """Restituisce la dimensione dell'asteroide"""
        return self.size
    
    def get_id(self):
        """Restituisce l'ID dell'asteroide nel canvas"""
        return self.id