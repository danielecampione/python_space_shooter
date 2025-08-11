from rocket_flame_single import RocketFlame

class RocketFlameManager:
    def __init__(self, canvas, graphics_detail="low", game_instance=None):
        self.canvas = canvas
        self.flames = []
        self.graphics_detail = graphics_detail
        self.game_instance = game_instance
    
    def add_flame(self, x, y):
        """Aggiunge una nuova fiammata alla posizione specificata"""
        flame = RocketFlame(self.canvas, x, y, self.graphics_detail, self.game_instance)
        self.flames.append(flame)
        
        # Programma la rimozione dalla lista dopo la durata della fiammata
        self.canvas.after(flame.duration + 10, lambda: self._remove_flame_from_list(flame))
    
    def _remove_flame_from_list(self, flame):
        """Rimuove una fiammata dalla lista (metodo interno)"""
        if flame in self.flames:
            self.flames.remove(flame)
    
    def clear_all_flames(self):
        """Rimuove tutte le fiammate"""
        for flame in self.flames:
            flame.delete()
        self.flames.clear()
    
    def get_flame_count(self):
        """Restituisce il numero di fiammate attive"""
        return len(self.flames)