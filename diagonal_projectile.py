from projectile import Projectile

# Classe per proiettili diagonali (doppio fuoco)
class DiagonalProjectile(Projectile):
    def __init__(self, canvas, x, y, angle_offset, speed=15):
        self.angle_offset = angle_offset
        super().__init__(canvas, x, y, angle_offset / 10, speed)
    
    def create_visual(self):
        """Crea la rappresentazione visiva del proiettile diagonale"""
        return self.canvas.create_line(
            self.x, self.y,
            self.x + self.angle_offset, self.y - 20,
            fill="yellow", width=3, tags="bullet"
        )