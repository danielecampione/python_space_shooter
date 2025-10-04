import random
from wall import Wall

class WallManager:
    def __init__(self, canvas, screen_width=800, screen_height=600, graphics_detail="low"):
        self.canvas = canvas
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.graphics_detail = graphics_detail
        self.walls = []
        self.walls_spawned = 0
        self.max_walls = 2  # Massimo 2 muri per livello
        self.wall_spawn_timer = 0
        self.wall_spawn_interval = 300  # Frames tra un muro e l'altro
        self.game_progress = 0  # Progresso del gioco (0-100)
        self.walls_enabled = True
        
    def update(self, game_progress, asteroid_count):
        """Aggiorna il manager dei muri"""
        self.game_progress = game_progress
        
        # Spawna i muri solo se siamo nel primo livello e non abbiamo ancora spawnato tutti i muri
        if (self.walls_spawned < self.max_walls and 
            self.walls_enabled and 
            asteroid_count > 5):  # Assicurati che ci siano ancora abbastanza asteroidi
            
            self.wall_spawn_timer += 1
            
            # Spawna il primo muro quando il gioco è al 30% di progresso
            if self.walls_spawned == 0 and game_progress >= 30:
                self.spawn_wall()
            
            # Spawna il secondo muro quando il gioco è al 60% di progresso
            elif (self.walls_spawned == 1 and 
                  game_progress >= 60 and 
                  self.wall_spawn_timer >= self.wall_spawn_interval):
                self.spawn_wall()
        
        # Muovi tutti i muri verso il basso
        self.move_walls()
        
        # Rimuovi i muri che sono usciti dallo schermo
        self.cleanup_walls()
    
    def spawn_wall(self):
        """Spawna un nuovo muro in una posizione casuale"""
        if self.walls_spawned >= self.max_walls:
            return
        
        # Calcola posizione casuale per il muro
        wall_width = random.randint(150, 250)  # Larghezza variabile
        wall_height = random.randint(60, 100)  # Altezza variabile
        
        # Assicurati che ci sia spazio per passare ai lati
        min_gap = 120  # Spazio minimo per passare
        max_x = self.screen_width - wall_width - min_gap
        min_x = min_gap
        
        if max_x > min_x:
            wall_x = random.randint(min_x, max_x)
        else:
            wall_x = min_x
        
        # Spawna il muro fuori dallo schermo (sopra)
        wall_y = -wall_height - 50
        
        # Crea il muro
        wall = Wall(self.canvas, wall_x, wall_y, wall_width, wall_height, self.graphics_detail)
        self.walls.append(wall)
        self.walls_spawned += 1
        self.wall_spawn_timer = 0
        
        print(f"Muro spawnato: {self.walls_spawned}/{self.max_walls} - Posizione: ({wall_x}, {wall_y})")
    
    def move_walls(self):
        """Muove tutti i muri verso il basso"""
        wall_speed = 2  # Velocità dei muri
        
        for wall in self.walls:
            wall.move(0, wall_speed)
    
    def cleanup_walls(self):
        """Rimuove i muri che sono usciti dallo schermo"""
        walls_to_remove = []
        
        for wall in self.walls:
            if wall.is_off_screen(self.screen_height):
                walls_to_remove.append(wall)
        
        for wall in walls_to_remove:
            wall.destroy()
            self.walls.remove(wall)
    
    def check_collision_with_spaceship(self, spaceship_bbox):
        """Controlla le collisioni tra la navicella e i muri"""
        for wall in self.walls:
            wall_bbox = wall.get_bbox()
            if self.check_overlap(spaceship_bbox, wall_bbox):
                return True
        return False
    
    def check_collision_with_bullet(self, bullet_bbox):
        """Controlla le collisioni tra i proiettili e i muri"""
        for wall in self.walls:
            wall_bbox = wall.get_bbox()
            if self.check_overlap(bullet_bbox, wall_bbox):
                return wall
        return None
    
    def check_overlap(self, bbox1, bbox2):
        """Controlla se due bounding box si sovrappongono"""
        if not bbox1 or not bbox2 or len(bbox1) < 4 or len(bbox2) < 4:
            return False
        
        x1_min, y1_min, x1_max, y1_max = bbox1
        x2_min, y2_min, x2_max, y2_max = bbox2
        
        return not (x1_max < x2_min or x2_max < x1_min or y1_max < y2_min or y2_max < y1_min)
    
    def reset(self):
        """Resetta il manager dei muri per un nuovo gioco"""
        # Rimuovi tutti i muri esistenti
        for wall in self.walls:
            wall.destroy()
        
        self.walls.clear()
        self.walls_spawned = 0
        self.wall_spawn_timer = 0
        self.game_progress = 0
        self.walls_enabled = True
    
    def disable_walls(self):
        """Disabilita la generazione di nuovi muri"""
        self.walls_enabled = False
    
    def get_wall_count(self):
        """Restituisce il numero di muri attualmente attivi"""
        return len(self.walls)