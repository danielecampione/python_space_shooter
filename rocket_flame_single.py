import random

class RocketFlame:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.flame_ids = []
        self.duration = 100  # millisecondi
        self.colors = ["yellow", "orange", "red"]
        self.create_flame()
        self.schedule_removal()
    
    def create_flame(self):
        """Crea l'effetto fiammata con gradienti"""
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