import random
from asteroid import Asteroid

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