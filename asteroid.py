import tkinter as tk
import random

class Asteroid:
    def __init__(self, canvas, x, y, size, speed, direction):
        self.canvas = canvas
        self.size = size
        self.speed = speed
        self.direction = direction
        
        # Crea l'asteroide visuale
        self.id = self.canvas.create_oval(
            x, y, x + size, y + size, 
            fill="gray", outline="darkgray", tags="asteroid"
        )
    
    def move(self):
        """Muove l'asteroide secondo la sua direzione e velocità"""
        dx = 0
        dy = self.speed
        if self.direction == "diagonal":
            dx = random.choice([-1, 1]) * self.speed / 2
        self.canvas.move(self.id, dx, dy)
    
    def get_coords(self):
        """Restituisce le coordinate dell'asteroide"""
        return self.canvas.coords(self.id)
    
    def is_out_of_bounds(self):
        """Verifica se l'asteroide è uscito dai limiti dello schermo"""
        coords = self.get_coords()
        if not coords or len(coords) < 4:
            return True
        return coords[3] > 600 or coords[2] < 0 or coords[0] > 800
    
    def get_center(self):
        """Restituisce le coordinate del centro dell'asteroide"""
        coords = self.get_coords()
        if coords and len(coords) >= 4:
            x = (coords[0] + coords[2]) / 2
            y = (coords[1] + coords[3]) / 2
            return x, y
        return None, None
    
    def destroy(self):
        """Distrugge l'asteroide rimuovendolo dal canvas"""
        self.canvas.delete(self.id)
    
    def get_size(self):
        """Restituisce la dimensione dell'asteroide"""
        return self.size
    
    def get_id(self):
        """Restituisce l'ID dell'asteroide nel canvas"""
        return self.id

class AsteroidManager:
    def __init__(self, canvas, base_speed=2, max_speed=8):
        self.canvas = canvas
        self.asteroids = []
        self.base_speed = base_speed
        self.max_speed = max_speed
    
    def spawn_asteroid(self, score):
        """Genera un nuovo asteroide con difficoltà basata sul punteggio"""
        difficulty_factor = 1 + score / 20
        spawn_chance = max(1, int(50 / difficulty_factor))
        
        if random.randint(1, spawn_chance) == 1:
            x = random.randint(0, 750)
            size = random.randint(20, 50)
            speed = min(self.base_speed * difficulty_factor, self.max_speed)
            direction = random.choice(["straight", "diagonal"])
            
            asteroid = Asteroid(self.canvas, x, 0, size, speed, direction)
            self.asteroids.append(asteroid)
    
    def move_all_asteroids(self):
        """Muove tutti gli asteroidi e rimuove quelli fuori schermo"""
        for asteroid in self.asteroids[:]:
            asteroid.move()
            if asteroid.is_out_of_bounds():
                asteroid.destroy()
                self.asteroids.remove(asteroid)
    
    def get_asteroids(self):
        """Restituisce la lista degli asteroidi"""
        return self.asteroids
    
    def remove_asteroid(self, asteroid):
        """Rimuove un asteroide specifico dalla lista"""
        if asteroid in self.asteroids:
            self.asteroids.remove(asteroid)
    
    def clear_all_asteroids(self):
        """Rimuove tutti gli asteroidi"""
        for asteroid in self.asteroids:
            asteroid.destroy()
        self.asteroids.clear()
    
    def destroy_asteroid(self, asteroid):
        """Distrugge un asteroide e restituisce le sue coordinate centrali per l'esplosione"""
        x, y = asteroid.get_center()
        size = asteroid.get_size()
        asteroid.destroy()
        self.remove_asteroid(asteroid)
        return x, y, size