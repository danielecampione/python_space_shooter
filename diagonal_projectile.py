from projectile import Projectile

# Classe per proiettili diagonali (doppio fuoco)
class DiagonalProjectile(Projectile):
    def __init__(self, canvas, x, y, angle_offset, speed=15, graphics_detail="low"):
        self.angle_offset = angle_offset
        super().__init__(canvas, x, y, angle_offset / 10, speed, graphics_detail)
    
    def create_visual(self):
        """Crea la rappresentazione visiva del proiettile diagonale"""
        # Usa la stessa grafica semplice per tutti i livelli per evitare bug della scia
        bullet_id = self.canvas.create_line(
            self.x, self.y,
            self.x + self.angle_offset, self.y - 20,
            fill="yellow", width=3, tags="bullet"
        )
        self.visual_elements.append(bullet_id)
        return bullet_id