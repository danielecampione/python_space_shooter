import random

class Powerup:
    """Classe base per tutti i power-up del gioco."""
    
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.speed = 3
        self.width = 15
        self.height = 30
        self.id = None
        self.type = None
        self.color = "white"
        self.create_visual()
    
    def create_visual(self):
        """Crea la rappresentazione visiva del power-up sulla canvas."""
        self.id = self.canvas.create_rectangle(
            self.x - self.width, self.y - self.height,
            self.x + self.width, self.y,
            fill=self.color, outline="white", tags="power_up"
        )
    
    def move(self):
        """Muove il power-up verso il basso."""
        self.canvas.move(self.id, 0, self.speed)
        coords = self.canvas.coords(self.id)
        if coords and len(coords) >= 4:
            self.y = coords[1] + self.height
    
    def is_off_screen(self):
        """Verifica se il power-up è uscito dallo schermo."""
        coords = self.canvas.coords(self.id)
        return not coords or len(coords) < 4 or coords[3] > 600
    
    def get_coords(self):
        """Restituisce le coordinate del power-up."""
        return self.canvas.coords(self.id)
    
    def destroy(self):
        """Rimuove il power-up dalla canvas."""
        if self.id:
            self.canvas.delete(self.id)
            self.id = None
    
    def activate(self, game_instance):
        """Attiva l'effetto del power-up. Da implementare nelle sottoclassi."""
        raise NotImplementedError("Le sottoclassi devono implementare il metodo activate")
    
    def get_display_text(self):
        """Restituisce il testo da mostrare quando il power-up viene raccolto."""
        raise NotImplementedError("Le sottoclassi devono implementare il metodo get_display_text")


class ExtraLifePowerup(Powerup):
    """Power-up che aggiunge una vita extra al giocatore."""
    
    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)
        self.type = "extra_life"
        self.color = "green"
        # Ricrea il visual con il colore corretto
        self.destroy()
        self.create_visual()
    
    def activate(self, game_instance):
        """Aggiunge una vita al giocatore."""
        game_instance.lives += 1
        game_instance.update_lives()
    
    def get_display_text(self):
        """Restituisce il testo da mostrare."""
        return "Vita Extra!"


class DoubleFirePowerup(Powerup):
    """Power-up che attiva il doppio fuoco per un periodo limitato."""
    
    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)
        self.type = "double_fire"
        self.color = "purple"
        self.duration = 500  # Durata in frame
        # Ricrea il visual con il colore corretto
        self.destroy()
        self.create_visual()
    
    def activate(self, game_instance):
        """Attiva il doppio fuoco."""
        game_instance.power_up_active = True
        game_instance.power_up_type = self.type
        game_instance.power_up_timer = self.duration
    
    def get_display_text(self):
        """Restituisce il testo da mostrare."""
        return "Doppio Fuoco!"


class PowerupManager:
    """Gestisce la collezione di power-up nel gioco."""
    
    def __init__(self, canvas):
        self.canvas = canvas
        self.powerups = []
        self.spawn_rate = 500  # 1 su 500 possibilità per frame
    
    def spawn_powerup(self):
        """Genera casualmente un power-up."""
        if random.randint(1, self.spawn_rate) == 1:
            x = random.randint(50, 750)
            powerup_type = random.choice(["extra_life", "double_fire"])
            
            if powerup_type == "extra_life":
                powerup = ExtraLifePowerup(self.canvas, x, -30)
            else:  # double_fire
                powerup = DoubleFirePowerup(self.canvas, x, -30)
            
            self.powerups.append(powerup)
    
    def move_all_powerups(self):
        """Muove tutti i power-up e rimuove quelli usciti dallo schermo."""
        for powerup in self.powerups[:]:
            powerup.move()
            if powerup.is_off_screen():
                powerup.destroy()
                self.powerups.remove(powerup)
    
    def get_powerups(self):
        """Restituisce la lista dei power-up attivi."""
        return self.powerups[:]
    
    def remove_powerup(self, powerup):
        """Rimuove un power-up specifico dalla collezione."""
        if powerup in self.powerups:
            powerup.destroy()
            self.powerups.remove(powerup)
    
    def clear_all_powerups(self):
        """Rimuove tutti i power-up dalla collezione e dalla canvas."""
        for powerup in self.powerups[:]:
            powerup.destroy()
        self.powerups.clear()
    
    def count_powerups(self):
        """Restituisce il numero di power-up attivi."""
        return len(self.powerups)