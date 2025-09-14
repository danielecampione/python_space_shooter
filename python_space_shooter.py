import tkinter as tk
from PIL import Image, ImageDraw, ImageTk, ImageFont, ImageFilter
import random
import math
from spaceship import Spaceship
from projectile import Projectile
from diagonal_projectile import DiagonalProjectile
from asteroid import Asteroid
from asteroid_manager import AsteroidManager
from star_field import StarField
from powerup_manager import PowerupManager
from rocket_flame_manager_single import RocketFlameManager
from main_menu import MainMenu
from instructions_menu import InstructionsMenu
from commands_menu import CommandsMenu
from graphics_options_menu import GraphicsOptionsMenu
from language_menu import LanguageMenu
from i18n import i18n, _

# Importa Resampling se la versione di Pillow è 9.1.0 o successiva
try:
    from PIL import Resampling
    RESAMPLE_FILTER = Resampling.LANCZOS
except ImportError:
    RESAMPLE_FILTER = Image.LANCZOS  # Per le versioni precedenti

class SpaceShooterGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Space Shooter")
        self.root.geometry("800x600")
        self.root.attributes("-alpha", 0.0)  # Imposta l'opacità iniziale a 0
        self.root.resizable(False, False)

        # Stato del gioco
        self.game_running = False
        self.control_with_mouse = True  # Di default, il controllo è con il mouse
        self.game_over = False  # Stato per il game over
        self.game_paused = False  # Stato per la pausa
        
        # Opzioni grafiche
        self.graphics_detail = "high"  # "low" o "high"
        self.loaded_images = {}  # Cache per le immagini caricate

        # Variabili per tenere traccia degli eventi after
        self.game_loop_after_id = None
        self.game_over_after_id = None

        # Canvas per il gioco
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()

        # Disegna sfondo con gradiente
        self.draw_gradient_background()

        # Inizializza i menù object-oriented
        self.main_menu = MainMenu(self.canvas, self.root, self)
        self.instructions_menu = InstructionsMenu(self.canvas, self.root, self)
        self.commands_menu = CommandsMenu(self.canvas, self.root, self)
        self.graphics_menu = GraphicsOptionsMenu(self.canvas, self.root, self)
        self.language_menu = LanguageMenu(self.canvas, self.root, self)

        # Mostra il menù principale
        self.main_menu.show()
        
        self.fade_in()

    def fade_in(self, alpha=0.0):
        if alpha < 1.0:
            self.root.attributes("-alpha", alpha)
            self.root.after(50, self.fade_in, alpha + 0.05)  # Incrementa gradualmente l'opacità
        else:
            self.root.attributes("-alpha", 1.0)  # Assicura che rimanga completamente visibile

    # Funzione per disegnare un gradiente verticale più scuro
    def draw_gradient_background(self):
        self.canvas.delete("gradient")
        for i in range(256):
            blue_value = int(i * 0.3)  # Riduci l'intensità del blu
            color = f"#0000{format(blue_value, '02x')}"
            self.canvas.create_rectangle(0, i * 2.35, 800, (i + 1) * 2.35, fill=color, outline="", tags="gradient")
        # Porta in primo piano gli elementi del gioco dopo aver disegnato lo sfondo
        self.canvas.tag_lower("gradient")

    # Funzione per mostrare il menù principale (ora delegata alla classe MainMenu)
    def show_main_menu(self):
        self.main_menu.show()

    # Funzioni per navigare nel menù (ora gestite dalle classi del menù)
    # Mantenute per compatibilità con eventuali riferimenti esterni

    # Funzione per tornare al menù principale (ora delegata alla classe MainMenu)
    def back_to_main_menu(self, event=None):
        self.main_menu.back_to_main_menu(event)

    # Funzione per mostrare le istruzioni (ora delegata alla classe InstructionsMenu)
    def show_instructions(self):
        self.instructions_menu.show()

    # Funzione per mostrare il menù "Comandi" (ora delegata alla classe CommandsMenu)
    def show_commands_menu(self):
        self.commands_menu.show()
    
    # Funzione per mostrare il menù "Lingua" (ora delegata alla classe LanguageMenu)
    def show_language_menu(self):
        self.language_menu.show()
    
    # Funzione chiamata quando la lingua cambia per aggiornare l'interfaccia
    def on_language_changed(self):
        """Aggiorna l'interfaccia quando cambia la lingua"""
        # Se il gioco è in corso, aggiorna le etichette
        if self.game_running and hasattr(self, 'score_label') and hasattr(self, 'lives_label'):
            self.update_score()
            self.update_lives()
            
            # Se il gioco è in pausa, aggiorna la schermata di pausa
            if self.game_paused:
                self.show_pause_screen()

    # Funzioni per il controllo mouse (ora delegate alla classe CommandsMenu)
    def draw_checkmark(self):
        self.commands_menu.draw_checkmark()

    def remove_checkmark(self):
        self.commands_menu.remove_checkmark()

    def toggle_mouse_control(self, event=None):
        self.commands_menu.toggle_mouse_control(event)

    # Funzione per mostrare le opzioni grafiche (ora delegata alla classe GraphicsOptionsMenu)
    def show_graphics_options(self):
        self.graphics_options_menu.show()

    def set_graphics_detail(self, index):
        """Imposta il livello di dettaglio grafico (ora delegata alla classe GraphicsOptionsMenu)"""
        self.graphics_options_menu.set_graphics_detail(index)

    def update_detail_colors(self):
        """Aggiorna i colori delle opzioni di dettaglio (ora delegata alla classe GraphicsOptionsMenu)"""
        self.graphics_options_menu.update_detail_colors()

    def load_image(self, image_name, size=None):
        """Carica un'immagine dalla cartella img e la ridimensiona se necessario"""
        cache_key = f"{image_name}_{size}" if size else image_name
        
        if cache_key in self.loaded_images:
            return self.loaded_images[cache_key]
        
        try:
            image_path = f"img/{image_name}"
            image = Image.open(image_path)
            
            if size:
                image = image.resize(size, RESAMPLE_FILTER)
            
            photo = ImageTk.PhotoImage(image)
            self.loaded_images[cache_key] = photo
            return photo
        except Exception as e:
            print(f"Errore nel caricamento dell'immagine {image_name}: {e}")
            return None

    def get_asteroid_image_name(self, size):
        """Restituisce il nome dell'immagine dell'asteroide in base alla dimensione"""
        if self.graphics_detail == "high":
            # Con definizione alta, aumentiamo le soglie per usare tutte e tre le immagini
            if size <= 35:
                return "asteroid_01.png"  # Piccolo
            elif size <= 42:
                return "asteroid_02.png"  # Medio
            else:
                return "asteroid_03.png"  # Grande
        else:
            # Con definizione bassa, manteniamo le soglie originali
            if size <= 30:
                return "asteroid_01.png"  # Piccolo
            elif size <= 50:
                return "asteroid_02.png"  # Medio
            else:
                return "asteroid_03.png"  # Grande

    # Funzione per gestire la pausa
    def toggle_pause(self, event=None):
        if self.game_running and not self.game_over:
            self.game_paused = not self.game_paused
            if self.game_paused:
                self.show_pause_screen()
            else:
                self.hide_pause_screen()
                self.game_loop()  # Riprendi il ciclo del gioco

    # Funzione per mostrare la schermata di pausa
    def show_pause_screen(self):
        # Crea un rettangolo semi-trasparente per coprire lo schermo
        self.canvas.create_rectangle(
            0, 0, 800, 600, fill="black", stipple="gray50", tags="pause_screen"
        )
        
        # Crea la scritta "PAUSA" con contorno nero
        self.pause_text_shadow = self.canvas.create_text(
            402, 302, text=_("paused"), font=("Arial", 60, "bold"),
            fill="black", tags="pause_screen"
        )
        self.pause_text = self.canvas.create_text(
            400, 300, text=_("paused"), font=("Arial", 60, "bold"),
            fill="white", tags="pause_screen"
        )
        
        # Istruzioni per riprendere
        self.pause_instructions_shadow = self.canvas.create_text(
            402, 372, text=_("pause_instruction"), font=("Arial", 20),
            fill="black", tags="pause_screen"
        )
        self.pause_instructions = self.canvas.create_text(
            400, 370, text=_("pause_instruction"), font=("Arial", 20),
            fill="white", tags="pause_screen"
        )

    # Funzione per nascondere la schermata di pausa
    def hide_pause_screen(self):
        self.canvas.delete("pause_screen")

    # Funzione per iniziare il gioco
    def start_game(self):
        # Se c'è un eventuale callback pendente del game over, annullalo
        if self.game_over_after_id is not None:
            self.root.after_cancel(self.game_over_after_id)
            self.game_over_after_id = None

        self.game_running = True
        self.game_over = False  # Resetta lo stato di game over
        self.game_paused = False  # Resetta lo stato di pausa
        self.canvas.delete("all")
        self.draw_gradient_background()

        # Rimuovi le associazioni del menù
        self.root.unbind("<Up>")
        self.root.unbind("<Down>")
        self.root.unbind("<Return>")
        self.root.unbind("<Escape>")
        self.canvas.unbind("<Button-1>")

        # Rimuovi eventuali widget
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Checkbutton):
                widget.destroy()

        # Variabili di gioco
        self.ship_speed = 10
        self.bullet_speed = 15
        self.score = 0
        self.lives = 3
        self.power_up_active = False
        self.power_up_type = None
        self.power_up_timer = 0

        # Crea la navicella
        self.ship = Spaceship(self.canvas, 375, 550, speed=self.ship_speed, graphics_detail=self.graphics_detail, game_instance=self)

        # Manager per gli asteroidi
        self.asteroid_manager = AsteroidManager(self.canvas, base_speed=2, max_speed=8, graphics_detail=self.graphics_detail, game_instance=self)

        # Liste per proiettili e particelle, manager per power-up e fiammate
        self.bullets = []
        self.powerup_manager = PowerupManager(self.canvas, graphics_detail=self.graphics_detail, game_instance=self)
        self.rocket_flame_manager = RocketFlameManager(self.canvas, graphics_detail=self.graphics_detail, game_instance=self)
        self.particles = []

        # Etichette per il punteggio e le vite
        self.score_label = self.canvas.create_text(
            10, 10, text=f"{_("score")}: {self.score}", font=("Arial", 14),
            fill="white", anchor="nw"
        )
        self.lives_label = self.canvas.create_text(
            790, 10, text=f"{_("lives")}: {self.lives}", font=("Arial", 14),
            fill="white", anchor="ne"
        )

        # Sfondo stellato con stelle scintillanti
        self.starfield = StarField(self.canvas, num_stars=100)

        # Associazione dei controlli
        self.bind_game_controls()

        # Avvio del ciclo del gioco
        self.game_loop()

    # Funzione per associare i controlli di gioco
    def bind_game_controls(self):
        if self.control_with_mouse:
            self.canvas.bind("<Motion>", self.move_ship_with_mouse)
            self.canvas.bind("<Button-1>", self.mouse_shoot)
            # Rimuovi i controlli da tastiera per il movimento orizzontale
            self.root.unbind("<Left>")
            self.root.unbind("<Right>")
        else:
            self.root.bind("<Left>", self.move_ship_left)
            self.root.bind("<Right>", self.move_ship_right)
            # Rimuovi i controlli da mouse
            self.canvas.unbind("<Motion>")
            self.canvas.unbind("<Button-1>")
        # La barra spaziatrice deve funzionare sempre per sparare
        self.root.bind("<space>", self.shoot_bullet)
        # Tasto P per la pausa
        self.root.bind("<p>", self.toggle_pause)
        self.root.bind("<P>", self.toggle_pause)  # Maiuscolo
        # Tasto Esc per tornare al menù
        self.root.bind("<Escape>", self.back_to_main_menu)

    # Funzione per aggiungere l'effetto fiammata con gradienti
    def add_rocket_effect(self):
        if self.game_paused:
            return
        ship_x, ship_y = self.ship.get_position()
        self.rocket_flame_manager.add_flame(ship_x, ship_y + 30)

    # Movimento della navicella a sinistra
    def move_ship_left(self, event):
        if not self.game_over and not self.game_paused:
            if self.ship.move_left():
                self.add_rocket_effect()

    # Movimento della navicella a destra
    def move_ship_right(self, event):
        if not self.game_over and not self.game_paused:
            if self.ship.move_right():
                self.add_rocket_effect()

    # Movimento della navicella con il mouse
    def move_ship_with_mouse(self, event):
        if not self.game_over and not self.game_paused:
            ship_bbox = self.ship.get_bbox()
            if ship_bbox:
                ship_width = ship_bbox[2] - ship_bbox[0]
                new_x = event.x - ship_width / 2
                if self.ship.move_to_x(new_x):
                    self.add_rocket_effect()

    # Funzione per sparare con il mouse in modalità mouse attiva
    def mouse_shoot(self, event):
        if not self.game_over and not self.game_paused and self.control_with_mouse:
            self.shoot_bullet(event)

    # Funzione per sparare un proiettile con scia luminosa
    def shoot_bullet(self, event):
        if not self.game_over and not self.game_paused:
            center_x = self.ship.get_center_x()
            top_y = self.ship.get_top_y()
            if self.power_up_active and self.power_up_type == "double_fire":
                # Spara due proiettili diagonali
                angle_offsets = [-10, 10]
                for offset in angle_offsets:
                    projectile = DiagonalProjectile(self.canvas, center_x, top_y, offset, self.bullet_speed)
                    self.bullets.append({"id": projectile.get_id(), "dx": offset / 10})
            else:
                # Spara un proiettile dritto
                projectile = Projectile(self.canvas, center_x, top_y, 0, self.bullet_speed)
                self.bullets.append({"id": projectile.get_id(), "dx": 0})




    # Ciclo principale del gioco
    def game_loop(self):
        if self.game_over or self.game_paused:
            return  # Interrompe il ciclo se il gioco è finito o in pausa
        self.move_bullets()
        self.asteroid_manager.spawn_asteroid(self.score)
        self.asteroid_manager.move_all_asteroids()
        self.powerup_manager.spawn_powerup()
        self.powerup_manager.move_all_powerups()
        self.move_particles()
        self.check_collisions()
        self.starfield.update_stars()
        self.update_power_up()
        self.game_loop_after_id = self.canvas.after(30, self.game_loop)

    # Funzione per muovere i proiettili
    def move_bullets(self):
        for bullet in self.bullets[:]:
            self.canvas.move(bullet["id"], bullet["dx"], -self.bullet_speed)
            bbox = self.canvas.bbox(bullet["id"])
            if not bbox or len(bbox) < 4 or bbox[1] < 0 or bbox[0] < 0 or bbox[2] > 800:
                self.canvas.delete(bullet["id"])
                self.bullets.remove(bullet)





    # Funzione per creare un effetto particellare migliorato
    def create_explosion(self, x, y, num_particles=50):
        colors = ["#fffae3", "#ffc857", "#ff6b35", "#d7263d", "#a20021"]
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 7)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            size = random.randint(2, 5)
            color = random.choice(colors)
            particle = {
                "id": self.canvas.create_oval(
                    x, y, x + size, y + size, fill=color, outline=""
                ),
                "dx": dx,
                "dy": dy,
                "life": random.randint(30, 60)
            }
            self.particles.append(particle)

    # Funzione per muovere le particelle
    def move_particles(self):
        for particle in self.particles[:]:
            self.canvas.move(particle["id"], particle["dx"], particle["dy"])
            particle["life"] -= 1
            if particle["life"] <= 0:
                self.canvas.delete(particle["id"])
                self.particles.remove(particle)
            else:
                # Effetto dissolvenza
                alpha = int(255 * (particle["life"] / 60))
                fill = self.canvas.itemcget(particle["id"], "fill")
                self.canvas.itemconfig(particle["id"], fill=fill, stipple="gray50")

    # Funzione per controllare le collisioni
    def check_collisions(self):
        if self.game_over:
            return  # Esce dalla funzione se il gioco è finito
        ship_coords = self.ship.get_bbox()
        if not ship_coords or len(ship_coords) < 4:
            return  # Esce se le coordinate della navicella non sono valide
        # Collisioni proiettili - asteroidi
        for bullet in self.bullets[:]:
            bullet_coords = self.canvas.bbox(bullet["id"])
            if not bullet_coords or len(bullet_coords) < 4:
                continue
            for asteroid in self.asteroid_manager.get_asteroids()[:]:
                asteroid_coords = asteroid.get_bbox()
                if not asteroid_coords or len(asteroid_coords) < 4:
                    continue
                if self.check_overlap(bullet_coords, asteroid_coords):
                    self.canvas.delete(bullet["id"])
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    self.destroy_asteroid(asteroid)
                    self.score += 1
                    self.update_score()
                    # Controlla se il punteggio ha raggiunto 500
                    if self.score >= 500 and not self.game_over:
                        self.game_over_screen(win=True)
                    break
        # Collisioni navicella - asteroidi
        for asteroid in self.asteroid_manager.get_asteroids()[:]:
            asteroid_coords = asteroid.get_bbox()
            if not asteroid_coords or len(asteroid_coords) < 4:
                continue
            if self.check_overlap(ship_coords, asteroid_coords):
                asteroid.destroy()
                self.asteroid_manager.remove_asteroid(asteroid)
                self.lives -= 1
                self.update_lives()
                # Lampeggia la navicella senza congelare il gioco
                self.flash_ship()
                if self.lives <= 0:
                    if not self.game_over:
                        self.game_over_screen(win=False)
                    return
        # Collisioni navicella - power-up
        for powerup in self.powerup_manager.get_powerups()[:]:
            powerup_coords = powerup.get_coords()
            if not powerup_coords or len(powerup_coords) < 4:
                continue
            if self.check_overlap(ship_coords, powerup_coords):
                self.powerup_manager.remove_powerup(powerup)
                powerup.activate(self)

    # Funzione per verificare sovrapposizione
    def check_overlap(self, bbox1, bbox2):
        if len(bbox1) < 4 or len(bbox2) < 4:
            return False  # Non c'è sovrapposizione se le bounding box non sono valide
        return not (bbox1[2] < bbox2[0] or
                    bbox1[0] > bbox2[2] or
                    bbox1[3] < bbox2[1] or
                    bbox1[1] > bbox2[3])

    # Funzione per fare lampeggiare la navicella senza congelare il gioco
    def flash_ship(self):
        if self.game_over:
            return
        if not self.game_paused:
            self.ship.flash()

    # Aggiornamento del punteggio
    def update_score(self):
        self.canvas.itemconfig(self.score_label, text=f"{_("score")}: {self.score}")

    # Aggiornamento delle vite
    def update_lives(self):
        self.canvas.itemconfig(self.lives_label, text=f"{_("lives")}: {self.lives}")



    # Funzione per gestire i power-up attivi
    def update_power_up(self):
        if self.power_up_active:
            self.power_up_timer -= 1
            if self.power_up_timer <= 0:
                self.deactivate_power_up()



    # Funzione per mostrare il nome del power-up con effetto animato
    def show_power_up_text(self, power_up_type):
        if power_up_type == "extra_life":
            text = _("extra_life")
        elif power_up_type == "double_fire":
            text = _("double_fire")
        else:
            text = _("power_up")
        # Creiamo un gruppo per gestire facilmente gli elementi del testo
        group = []
        # Crea il testo nero per il contorno (più copie leggermente spostate)
        offsets = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
        for dx, dy in offsets:
            shadow = self.canvas.create_text(
                400 + dx, 300 + dy, text=text, font=("Arial", 40, "bold"),
                fill="black", tags="power_up_text"
            )
            group.append(shadow)
        # Crea il testo bianco sopra
        main_text = self.canvas.create_text(
            400, 300, text=text, font=("Arial", 40, "bold"),
            fill="",  # Inizialmente trasparente
            tags="power_up_text"
        )
        group.append(main_text)
        # Effetto fade-in e fade-out
        self.fade_in_out(group, steps=10, stay_time=500)

    # Funzione per l'effetto fade-in e fade-out del testo
    def fade_in_out(self, items, steps=10, stay_time=500):
        def fade_in(step):
            if not self.game_paused and step <= steps:  # Controllo pausa
                alpha = int(255 * (step / steps))
                color = f"#{alpha:02x}{alpha:02x}{alpha:02x}"
                for item in items:
                    self.canvas.itemconfig(item, fill=color)
                self.root.after(50, fade_in, step + 1)
            elif self.game_paused:
                self.root.after(50, fade_in, step)  # Sospende l'animazione
            else:
                self.root.after(stay_time, fade_out, steps)
                
        def fade_out(step):
            if not self.game_paused and step >= 0:  # Controllo pausa
                alpha = int(255 * (step / steps))
                color = f"#{alpha:02x}{alpha:02x}{alpha:02x}"
                for item in items:
                    self.canvas.itemconfig(item, fill=color)
                self.root.after(50, fade_out, step - 1)
            elif self.game_paused:
                self.root.after(50, fade_out, step)  # Sospende l'animazione
            else:
                for item in items:
                    self.canvas.delete(item)
        fade_in(0)

    # Disattivazione del power-up
    def deactivate_power_up(self):
        self.power_up_active = False
        self.power_up_type = None

    # Funzione per distruggere un asteroide con effetto esplosione
    def destroy_asteroid(self, asteroid):
        x, y, size = self.asteroid_manager.destroy_asteroid(asteroid)
        # Calcola il numero di particelle in base alla dimensione dell'asteroide
        num_particles = int(size * 0.8)  # Numero proporzionale alla dimensione
        self.create_explosion(x, y, num_particles)

    # Funzione per mostrare lo schermo di Game Over con animazione 3D
    def game_over_screen(self, win=False):
        if self.game_over:  # Se il game over è già attivo, esci
            return
        self.game_over = True
        # Elimina gli oggetti sullo schermo
        self.clear_game_objects()
        # Rimuovi le associazioni dei tasti
        self.unbind_game_controls()
        # Mostra la scritta "GAME OVER" o "YOU WIN" con effetto 3D
        self.show_game_over_3d(win)

    # Funzione per terminare il gioco e tornare al menù
    def end_game(self):
        self.game_running = False
        # Annulla il ciclo di gioco se attivo
        if self.game_loop_after_id is not None:
            self.canvas.after_cancel(self.game_loop_after_id)
            self.game_loop_after_id = None
        if self.game_over_after_id is not None:
            self.root.after_cancel(self.game_over_after_id)
            self.game_over_after_id = None
        # Elimina gli oggetti di gioco
        self.clear_game_objects()
        # Rimuovi le associazioni dei tasti
        self.unbind_game_controls()
        self.canvas.delete("all")
        self.draw_gradient_background()
        self.show_main_menu()

    # Funzione per eliminare gli oggetti di gioco
    def clear_game_objects(self):
        if hasattr(self, 'ship') and self.ship:
            self.ship.delete()
        for bullet in self.bullets:
            self.canvas.delete(bullet["id"])
        self.bullets.clear()
        self.asteroid_manager.clear_all_asteroids()
        self.powerup_manager.clear_all_powerups()
        self.rocket_flame_manager.clear_all_flames()
        for particle in self.particles:
            self.canvas.delete(particle["id"])
        self.particles.clear()
        self.canvas.delete("power_up_text")
        if hasattr(self, 'score_label'):
            self.canvas.delete(self.score_label)
        if hasattr(self, 'lives_label'):
            self.canvas.delete(self.lives_label)

    # Funzione per rimuovere le associazioni dei tasti di gioco
    def unbind_game_controls(self):
        self.root.unbind("<Left>")
        self.root.unbind("<Right>")
        self.root.unbind("<space>")
        self.root.unbind("<Escape>")
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<Button-1>")

    # Funzione per creare un testo 3D con animazione breve
    def show_game_over_3d(self, win=False):
        # Crea un'immagine con il testo "GAME OVER" o "YOU WIN"
        image = Image.new("RGBA", (800, 600), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        font_size = 70
        text = _("you_win") if win else _("game_over")
        main_color = (0, 255, 0, 255) if win else (255, 0, 0, 255)  # Verde per win, rosso per game over
        
        # Definisci il font usando ImageFont di Pillow
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
            small_font = ImageFont.truetype("arial.ttf", 30)
        except IOError:
            font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # Calcola le dimensioni del testo
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = 400 - text_width / 2
        y = 250 - text_height / 2  # Spostato leggermente in alto per fare spazio al punteggio
        
        # Disegna il testo con ombra per effetto 3D
        shadow_color = (50, 50, 50, 255)
        offset = 5
        for i in range(10):
            draw.text((x + offset + i, y + offset + i), text, font=font, fill=shadow_color)
        draw.text((x, y), text, font=font, fill=main_color)
        
        # Aggiungi il testo del punteggio
        score_text = f"{_("final_score")}: {self.score}"
        score_bbox = small_font.getbbox(score_text)
        score_width = score_bbox[2] - score_bbox[0]
        score_x = 400 - score_width / 2
        score_y = y + text_height + 30  # Posiziona sotto il testo principale
        
        # Disegna il testo del punteggio con ombra
        for i in range(5):
            draw.text((score_x + 2 + i, score_y + 2 + i), score_text, font=small_font, fill=shadow_color)
        draw.text((score_x, score_y), score_text, font=small_font, fill=(255, 255, 255, 255))  # Bianco per il punteggio
        
        # Applica una lieve sfocatura all'ombra
        image = image.filter(ImageFilter.GaussianBlur(radius=2))
        
        # Animazione di ridimensionamento e movimento
        frames = 20  # Numero di fotogrammi
        duration = 1000  # Durata totale dell'animazione in millisecondi
        delay = duration // frames  # Ritardo tra i fotogrammi
        images = []
        for i in range(frames):
            # Calcola il fattore di scala e la posizione per l'animazione
            scale_factor = 1 + 0.5 * (frames - i) / frames  # Scala da 1.5 a 1.0
            dx = -200 * (frames - i) / frames  # Sposta da sinistra verso il centro
            # Applica la scala
            resized_image = image.resize(
                (int(800 * scale_factor), int(600 * scale_factor)),
                RESAMPLE_FILTER
            )
            photo = ImageTk.PhotoImage(resized_image)
            images.append(photo)  # Conserva l'immagine per evitare il garbage collection
            # Aggiorna il canvas
            self.canvas.delete("game_over_image")
            self.canvas.create_image(400 + dx, 300, image=photo, tags="game_over_image")
            self.canvas.update()
            self.root.after(delay)
        
        # Mostra l'immagine finale
        self.canvas.delete("game_over_image")
        self.canvas.create_image(400, 300, image=images[-1], tags="game_over_image")
        # Salva l'id dell'after per poterlo annullare se necessario
        self.game_over_after_id = self.root.after(1050 if win else 1000, self.back_to_main_menu)

def main():
    root = tk.Tk()
    game = SpaceShooterGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
