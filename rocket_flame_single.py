import random

class RocketFlame:
    def __init__(self, canvas, x, y, graphics_detail="low", game_instance=None):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.flame_ids = []
        self.duration = 100  # millisecondi
        self.colors = ["yellow", "orange", "red"]
        self.graphics_detail = graphics_detail
        self.game_instance = game_instance
        self.create_flame()
        self.schedule_removal()
    
    def create_flame(self):
        """Crea l'effetto fiammata"""
        if self.graphics_detail == "high" and self.game_instance:
            # Usa l'immagine della fiamma
            image = self.game_instance.load_image("rocket_flame.png", (30, 40))
            if image:
                flame = self.canvas.create_image(
                    self.x, self.y + 10, image=image, tags="rocket_flame"
                )
                self.flame_ids.append(flame)
                # Mantieni un riferimento all'immagine
                if not hasattr(self.canvas, 'flame_images'):
                    self.canvas.flame_images = []
                self.canvas.flame_images.append(image)
                return
        
        if self.graphics_detail == "low":
            # Grafica vettoriale migliorata per livello "Bassa"
            # Fiamma principale con gradiente di colori più elaborato
            flame_colors = ["#FFD700", "#FF8C00", "#FF6347", "#DC143C", "#8B0000"]
            
            # Fiamma centrale più grande e dettagliata
            for i, color in enumerate(flame_colors):
                width_factor = 1.0 - (i * 0.15)
                height_offset = i * 3
                
                flame = self.canvas.create_polygon(
                    self.x - 6 * width_factor, self.y + 8 + height_offset,
                    self.x - 10 * width_factor, self.y + 20 + height_offset,
                    self.x - 8 * width_factor, self.y + 30 + height_offset,
                    self.x, self.y + 35 + height_offset,
                    self.x + 8 * width_factor, self.y + 30 + height_offset,
                    self.x + 10 * width_factor, self.y + 20 + height_offset,
                    self.x + 6 * width_factor, self.y + 8 + height_offset,
                    fill=color, outline="", tags="rocket_flame", smooth=True
                )
                self.flame_ids.append(flame)
            
            # Aggiunge particelle scintillanti casuali
            for _ in range(3):
                spark_x = self.x + random.randint(-8, 8)
                spark_y = self.y + random.randint(15, 35)
                spark = self.canvas.create_oval(
                    spark_x - 1, spark_y - 1, spark_x + 1, spark_y + 1,
                    fill="#FFFF00", outline="", tags="rocket_flame"
                )
                self.flame_ids.append(spark)
        else:
            # Fallback alla grafica vettoriale minimale per "Molto bassa"
            for i, color in enumerate(self.colors):
                flame = self.canvas.create_polygon(
                    self.x - 5, self.y + 10 + i * 5,
                    self.x - 8 + i * 2, self.y + 25 + i * 5,
                    self.x + 8 - i * 2, self.y + 25 + i * 5,
                    self.x + 5, self.y + 10 + i * 5,
                    fill=color, outline="", tags="rocket_flame"
                )
                self.flame_ids.append(flame)
    
    def schedule_removal(self):
        """Programma la rimozione della fiammata"""
        self.canvas.after(self.duration, self.remove_flame)
    
    def remove_flame(self):
        """Rimuove la fiammata dal canvas"""
        for flame_id in self.flame_ids:
            self.canvas.delete(flame_id)
        self.flame_ids.clear()
    
    def delete(self):
        """Elimina immediatamente la fiammata"""
        self.remove_flame()