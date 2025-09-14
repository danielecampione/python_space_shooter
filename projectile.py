import tkinter as tk

# Classe base per i proiettili
class Projectile:
    def __init__(self, canvas, x, y, dx=0, speed=15, graphics_detail="low"):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.dx = dx  # Movimento orizzontale
        self.speed = speed
        self.graphics_detail = graphics_detail
        self.visual_elements = []  # Lista per tenere traccia di tutti gli elementi grafici
        self.id = self.create_visual()
    
    def create_visual(self):
        """Crea la rappresentazione visiva del proiettile"""
        # Usa la stessa grafica semplice per tutti i livelli per evitare bug della scia
        bullet_id = self.canvas.create_line(
            self.x, self.y, self.x, self.y - 20,
            fill="yellow", width=3, tags="bullet"
        )
        self.visual_elements.append(bullet_id)
        return bullet_id
    
    def get_id(self):
        """Restituisce l'ID del proiettile"""
        return self.id
    
    def destroy(self):
        """Distrugge il proiettile rimuovendo tutti i suoi elementi grafici"""
        if self.visual_elements:
            for element_id in self.visual_elements:
                self.canvas.delete(element_id)
            self.visual_elements.clear()
        else:
            self.canvas.delete(self.id)