import tkinter as tk
import random

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
        self.trail_elements = []  # Lista per la scia luminosa
        self.trail_positions = []  # Posizioni precedenti per la scia
        self.id = self.create_visual()
    
    def create_visual(self):
        """Crea la rappresentazione visiva del proiettile"""
        if self.graphics_detail == "very_low":
            # Grafica molto bassa: semplice linea
            bullet_id = self.canvas.create_line(
                self.x, self.y, self.x, self.y - 20,
                fill="yellow", width=3, tags="bullet"
            )
        elif self.graphics_detail == "low":
            # Grafica bassa: linea più spessa e luminosa
            bullet_id = self.canvas.create_line(
                self.x, self.y, self.x, self.y - 15,
                fill="#ffff00", width=4, tags="bullet", capstyle="round"
            )
        else:  # high
            # Grafica alta: linea con nucleo luminoso
            bullet_id = self.canvas.create_line(
                self.x, self.y, self.x, self.y - 18,
                fill="#ffffff", width=5, tags="bullet", capstyle="round"
            )
            # Nucleo interno
            core_id = self.canvas.create_line(
                self.x, self.y, self.x, self.y - 18,
                fill="#ffff00", width=2, tags="bullet", capstyle="round"
            )
            self.visual_elements.append(core_id)
        
        self.visual_elements.append(bullet_id)
        return bullet_id
    
    def get_id(self):
        """Restituisce l'ID del proiettile"""
        return self.id
    
    def update_position(self, new_x, new_y):
        """Aggiorna la posizione del proiettile e gestisce la scia"""
        if self.graphics_detail in ["low", "high"]:
            # Salva la posizione precedente per la scia
            self.trail_positions.append((self.x, self.y))
            
            # Limita il numero di posizioni nella scia
            max_trail_length = 8 if self.graphics_detail == "high" else 5
            if len(self.trail_positions) > max_trail_length:
                self.trail_positions.pop(0)
            
            # Aggiorna la scia
            self.update_trail()
        
        # Calcola il movimento necessario
        dx = new_x - self.x
        dy = new_y - self.y
        
        # Aggiorna le coordinate interne
        self.x = new_x
        self.y = new_y
        
        # Muovi tutti gli elementi grafici del proiettile
        if dx != 0 or dy != 0:
            for element_id in self.visual_elements:
                self.canvas.move(element_id, dx, dy)
    
    def update_trail(self):
        """Aggiorna la scia luminosa del proiettile con effetto cometa"""
        # Rimuovi la scia precedente
        for trail_id in self.trail_elements:
            self.canvas.delete(trail_id)
        self.trail_elements.clear()
        
        # Crea scia con effetto cometa (linee che si collegano)
        if len(self.trail_positions) >= 2:
            for i in range(1, len(self.trail_positions)):
                prev_x, prev_y = self.trail_positions[i-1]
                curr_x, curr_y = self.trail_positions[i]
                
                # Calcola l'intensità basata sulla posizione nella scia
                intensity = i / len(self.trail_positions)
                
                if self.graphics_detail == "low":
                    # Scia semplice con linee che si assottigliano
                    width = max(1, int(3 * intensity))
                    # Colore che va dal rosso-arancio al giallo
                    if intensity > 0.7:
                        color = "#ffaa00"
                    elif intensity > 0.4:
                        color = "#ff8800"
                    else:
                        color = "#ff6600"
                    
                    trail_id = self.canvas.create_line(
                        prev_x, prev_y, curr_x, curr_y,
                        fill=color, width=width, tags="bullet_trail", capstyle="round"
                    )
                else:  # high
                    # Scia elaborata con effetto cometa più realistico
                    width = max(1, int(4 * intensity))
                    # Gradiente di colore più sofisticato
                    if intensity > 0.8:
                        color = "#ffffff"  # Bianco brillante
                    elif intensity > 0.6:
                        color = "#ffff88"  # Giallo chiaro
                    elif intensity > 0.3:
                        color = "#ffaa44"  # Arancione
                    else:
                        color = "#ff6622"  # Rosso-arancione
                    
                    trail_id = self.canvas.create_line(
                        prev_x, prev_y, curr_x, curr_y,
                        fill=color, width=width, tags="bullet_trail", capstyle="round"
                    )
                
                self.trail_elements.append(trail_id)
    
    def destroy(self):
        """Distrugge il proiettile rimuovendo tutti i suoi elementi grafici"""
        # Rimuovi elementi principali
        if self.visual_elements:
            for element_id in self.visual_elements:
                self.canvas.delete(element_id)
            self.visual_elements.clear()
        else:
            self.canvas.delete(self.id)
        
        # Rimuovi scia
        for trail_id in self.trail_elements:
            self.canvas.delete(trail_id)
        self.trail_elements.clear()