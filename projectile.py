import tkinter as tk

# Classe base per i proiettili
class Projectile:
    def __init__(self, canvas, x, y, dx=0, speed=15):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.dx = dx  # Movimento orizzontale
        self.speed = speed
        self.id = self.create_visual()
    
    def create_visual(self):
        """Crea la rappresentazione visiva del proiettile"""
        return self.canvas.create_line(
            self.x, self.y, self.x, self.y - 20,
            fill="yellow", width=3, tags="bullet"
        )
    
    def get_id(self):
        """Restituisce l'ID del proiettile"""
        return self.id