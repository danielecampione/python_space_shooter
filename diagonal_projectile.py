from projectile import Projectile

# EN: Class for diagonal projectiles (double fire)
# IT: Classe per proiettili diagonali (doppio fuoco)
class DiagonalProjectile(Projectile):
    def __init__(self, canvas, x, y, angle_offset, speed=15, graphics_detail="low"):
        self.angle_offset = angle_offset
        super().__init__(canvas, x, y, angle_offset / 10, speed, graphics_detail)
    
    def create_visual(self):
        """EN: Creates the visual representation of the diagonal projectile"""
        """IT: Crea la rappresentazione visiva del proiettile diagonale"""
        if self.graphics_detail == "very_low":
            # EN: Very low graphics: simple line
            # IT: Grafica molto bassa: linea semplice
            return self.canvas.create_line(
                self.x, self.y, self.x, self.y - 10, fill="yellow", width=2
            )
        elif self.graphics_detail == "low":
            # EN: Low graphics: thick and bright line
            # IT: Grafica bassa: linea spessa e luminosa
            return self.canvas.create_line(
                self.x, self.y, self.x, self.y - 12, 
                fill="#ffff00", width=3, capstyle="round"
            )
        else:  # high
            # EN: High graphics: line with bright core
            # IT: Grafica alta: linea con nucleo luminoso
            main_id = self.canvas.create_line(
                self.x, self.y, self.x, self.y - 15,
                fill="#ffffff", width=4, capstyle="round"
            )
            # EN: Inner core
            # IT: Nucleo interno
            core_id = self.canvas.create_line(
                self.x, self.y, self.x, self.y - 15,
                fill="#ffff00", width=2, capstyle="round"
            )
            self.visual_elements.extend([main_id, core_id])
            return main_id