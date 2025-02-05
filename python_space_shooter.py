import tkinter as tk
from PIL import Image, ImageDraw, ImageTk, ImageFont, ImageFilter
import random
import math

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
        self.root.resizable(False, False)

        # Stato del gioco
        self.game_running = False

        # Canvas per il gioco
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()

        # Disegna sfondo con gradiente
        self.draw_gradient_background()

        # Mostra il menù principale
        self.show_main_menu()

    # Funzione per disegnare un gradiente verticale più scuro
    def draw_gradient_background(self):
        self.canvas.delete("gradient")
        for i in range(256):
            blue_value = int(i * 0.3)  # Riduci l'intensità del blu
            color = f"#0000{format(blue_value, '02x')}"
            self.canvas.create_rectangle(0, i * 2.35, 800, (i + 1) * 2.35, fill=color, outline="", tags="gradient")
        # Porta in primo piano gli elementi del gioco dopo aver disegnato lo sfondo
        self.canvas.tag_lower("gradient")

    # Funzione per mostrare il menù principale
    def show_main_menu(self):
        # Cancella tutto
        self.canvas.delete("all")
        self.draw_gradient_background()

        # Titolo del gioco
        self.canvas.create_text(
            400, 150, text="Space Shooter", font=("Arial", 50), fill="white"
        )

        # Bottone "Inizia Partita"
        start_button = tk.Button(
            self.root, text="Inizia Partita", font=("Arial", 20),
            command=self.start_game
        )
        self.canvas.create_window(400, 300, window=start_button)

        # Bottone "Istruzioni"
        instructions_button = tk.Button(
            self.root, text="Istruzioni", font=("Arial", 20),
            command=self.show_instructions
        )
        self.canvas.create_window(400, 370, window=instructions_button)

        # Bottone "Esci"
        exit_button = tk.Button(
            self.root, text="Esci", font=("Arial", 20),
            command=self.root.destroy
        )
        self.canvas.create_window(400, 440, window=exit_button)

    # Funzione per mostrare le istruzioni
    def show_instructions(self):
        self.canvas.delete("all")
        self.draw_gradient_background()

        instructions_text = (
            "Benvenuto in Space Shooter!\n\n"
            "Obiettivo del Gioco:\n"
            "Sopravvivi il più a lungo possibile distruggendo gli asteroidi.\n\n"
            "Controlli:\n"
            " - Freccia Sinistra: Muovi la navicella a sinistra\n"
            " - Freccia Destra: Muovi la navicella a destra\n"
            " - Barra Spaziatrice: Spara\n\n"
            "Power-up:\n"
            "Raccogli i power-up per ottenere bonus come vite extra\n"
            "o proiettili potenziati.\n\n"
            "Buona fortuna, pilota!"
        )

        self.canvas.create_text(
            400, 250, text=instructions_text, font=("Arial", 14), fill="white", width=600
        )

        # Bottone per tornare al menù
        back_button = tk.Button(
            self.root, text="Torna al Menù", font=("Arial", 16),
            command=self.show_main_menu
        )
        self.canvas.create_window(400, 500, window=back_button)

    # Funzione per iniziare il gioco
    def start_game(self):
        self.game_running = True
        self.canvas.delete("all")
        self.draw_gradient_background()

        # Rimuovi tutti i widget (bottoni)
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()

        # Variabili di gioco
        self.ship_speed = 10
        self.bullet_speed = 15
        self.asteroid_base_speed = 2  # Velocità base degli asteroidi
        self.asteroid_max_speed = 8   # Velocità massima degli asteroidi
        self.score = 0
        self.game_over = False
        self.lives = 3
        self.power_up_active = False
        self.power_up_type = None
        self.power_up_timer = 0

        # Crea la navicella
        self.ship = self.create_spaceship(375, 550)

        # Liste per proiettili, asteroidi, power-up e particelle
        self.bullets = []
        self.asteroids = []
        self.power_ups = []
        self.particles = []

        # Etichette per il punteggio e le vite
        self.score_label = self.canvas.create_text(
            10, 10, text=f"Punteggio: {self.score}", font=("Arial", 14),
            fill="white", anchor="nw"
        )
        self.lives_label = self.canvas.create_text(
            790, 10, text=f"Vite: {self.lives}", font=("Arial", 14),
            fill="white", anchor="ne"
        )

        # Sfondo stellato con stelle scintillanti
        self.stars = []
        for _ in range(100):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            size = random.choice([1, 2])
            star = {
                "id": self.canvas.create_oval(
                    x, y, x + size, y + size, fill="white", outline=""
                ),
                "speed": random.uniform(1, 3),
                "brightness": random.uniform(0.5, 1.0),
                "delta": random.uniform(-0.02, 0.02)
            }
            self.stars.append(star)

        # Associazione dei tasti
        self.root.bind("<Left>", self.move_ship_left)
        self.root.bind("<Right>", self.move_ship_right)
        self.root.bind("<space>", self.shoot_bullet)

        # Avvio del ciclo del gioco
        self.game_loop()

    # Funzione per creare la navicella con effetto glow
    def create_spaceship(self, x, y):
        points = [
            x + 25, y - 25,  # Punta superiore
            x, y + 10,       # Base sinistra
            x + 50, y + 10   # Base destra
        ]
        ship = self.canvas.create_polygon(
            points, fill="blue", outline="cyan", width=2, tags="ship"
        )
        return ship

    # Funzione per aggiungere l'effetto fiammata con gradienti
    def add_rocket_effect(self, x, y):
        flame_colors = ["yellow", "orange", "red"]
        for i, color in enumerate(flame_colors):
            flame = self.canvas.create_polygon(
                x + 20, y + 10 + i * 5,
                x + 17 - i * 2, y + 25 + i * 5,
                x + 33 + i * 2, y + 25 + i * 5,
                x + 30, y + 10 + i * 5,
                fill=color, outline="", tags="effect"
            )
            self.canvas.tag_lower(flame, self.ship)
            self.canvas.after(100, lambda f=flame: self.canvas.delete(f))

    # Movimento della navicella a sinistra
    def move_ship_left(self, event):
        if not self.game_over:
            coords = self.canvas.coords(self.ship)
            if coords and coords[0] > 0:
                self.canvas.move(self.ship, -self.ship_speed, 0)
                self.add_rocket_effect(coords[0], coords[3])

    # Movimento della navicella a destra
    def move_ship_right(self, event):
        if not self.game_over:
            coords = self.canvas.coords(self.ship)
            if coords and coords[4] < 800:
                self.canvas.move(self.ship, self.ship_speed, 0)
                self.add_rocket_effect(coords[0], coords[3])

    # Funzione per sparare un proiettile con scia luminosa
    def shoot_bullet(self, event):
        if not self.game_over:
            coords = self.canvas.coords(self.ship)
            center_x = (coords[0] + coords[4]) / 2
            top_y = coords[1]

            if self.power_up_active and self.power_up_type == "double_fire":
                # Spara due proiettili diagonali
                angle_offsets = [-10, 10]
                for offset in angle_offsets:
                    bullet = self.canvas.create_line(
                        center_x, top_y,
                        center_x + offset, top_y - 20,
                        fill="yellow", width=3, tags="bullet"
                    )
                    self.bullets.append({"id": bullet, "dx": offset / 10})
            else:
                # Spara un proiettile dritto
                bullet = self.canvas.create_line(
                    center_x, top_y, center_x, top_y - 20,
                    fill="yellow", width=3, tags="bullet"
                )
                self.bullets.append({"id": bullet, "dx": 0})

            # Aggiungi scia luminosa
            trail = self.canvas.create_line(
                center_x, top_y, center_x, top_y + 10,
                fill="white", width=2, tags="trail"
            )
            self.canvas.after(100, lambda: self.canvas.delete(trail))

    # Ciclo principale del gioco
    def game_loop(self):
        if self.game_over:
            return  # Interrompe il ciclo se il gioco è finito

        self.move_bullets()
        self.spawn_asteroids()
        self.move_asteroids()
        self.spawn_power_up()
        self.move_power_ups()
        self.move_particles()
        self.check_collisions()
        self.update_stars()
        self.update_power_up()
        self.canvas.after(30, self.game_loop)

    # Funzione per muovere i proiettili
    def move_bullets(self):
        for bullet in self.bullets[:]:
            self.canvas.move(bullet["id"], bullet["dx"], -self.bullet_speed)
            bbox = self.canvas.bbox(bullet["id"])
            if not bbox or len(bbox) < 4 or bbox[1] < 0 or bbox[0] < 0 or bbox[2] > 800:
                self.canvas.delete(bullet["id"])
                self.bullets.remove(bullet)

    # Funzione per generare asteroidi con velocità crescente
    def spawn_asteroids(self):
        difficulty_factor = 1 + self.score / 20  # Incrementa difficoltà con il punteggio
        spawn_chance = max(1, int(50 / difficulty_factor))
        if random.randint(1, spawn_chance) == 1:
            x = random.randint(0, 750)
            size = random.randint(20, 50)
            speed = min(self.asteroid_base_speed * difficulty_factor, self.asteroid_max_speed)
            direction = random.choice(["straight", "diagonal"])
            asteroid = self.canvas.create_oval(
                x, 0, x + size, size, fill="gray", outline="darkgray", tags="asteroid"
            )
            self.asteroids.append({"id": asteroid, "size": size, "speed": speed, "direction": direction})

    # Funzione per muovere gli asteroidi
    def move_asteroids(self):
        for asteroid in self.asteroids[:]:
            dx = 0
            dy = asteroid["speed"]
            if asteroid["direction"] == "diagonal":
                dx = random.choice([-1, 1]) * asteroid["speed"] / 2
            self.canvas.move(asteroid["id"], dx, dy)
            coords = self.canvas.coords(asteroid["id"])
            if not coords or len(coords) < 4 or coords[3] > 600 or coords[2] < 0 or coords[0] > 800:
                self.canvas.delete(asteroid["id"])
                self.asteroids.remove(asteroid)

    # Funzione per generare power-up
    def spawn_power_up(self):
        if random.randint(1, 500) == 1:
            x = random.randint(50, 750)
            power_up_type = random.choice(["extra_life", "double_fire"])
            if power_up_type == "extra_life":
                color = "green"
            else:
                color = "purple"
            power_up = self.canvas.create_rectangle(
                x - 15, -30, x + 15, 0, fill=color, outline="white", tags="power_up"
            )
            self.power_ups.append({"id": power_up, "type": power_up_type})

    # Funzione per muovere i power-up
    def move_power_ups(self):
        for power_up in self.power_ups[:]:
            self.canvas.move(power_up["id"], 0, 3)
            coords = self.canvas.coords(power_up["id"])
            if not coords or len(coords) < 4 or coords[3] > 600:
                self.canvas.delete(power_up["id"])
                self.power_ups.remove(power_up)

    # Funzione per creare un effetto particellare
    def create_explosion(self, x, y):
        for _ in range(20):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 5)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            particle = {
                "id": self.canvas.create_oval(
                    x, y, x + 3, y + 3, fill="orange", outline=""
                ),
                "dx": dx,
                "dy": dy,
                "life": random.randint(20, 50)
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

    # Funzione per controllare le collisioni
    def check_collisions(self):
        if self.game_over:
            return  # Esce dalla funzione se il gioco è finito

        ship_coords = self.canvas.bbox(self.ship)
        if not ship_coords or len(ship_coords) < 4:
            return  # Esce se le coordinate della navicella non sono valide

        # Collisioni proiettili - asteroidi
        for bullet in self.bullets[:]:
            bullet_coords = self.canvas.bbox(bullet["id"])
            if not bullet_coords or len(bullet_coords) < 4:
                continue
            for asteroid in self.asteroids[:]:
                asteroid_coords = self.canvas.coords(asteroid["id"])
                if not asteroid_coords or len(asteroid_coords) < 4:
                    continue
                if self.check_overlap(bullet_coords, asteroid_coords):
                    self.canvas.delete(bullet["id"])
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    self.destroy_asteroid(asteroid)
                    self.score += 1
                    self.update_score()
                    break

        # Collisioni navicella - asteroidi
        for asteroid in self.asteroids[:]:
            asteroid_coords = self.canvas.coords(asteroid["id"])
            if not asteroid_coords or len(asteroid_coords) < 4:
                continue
            if self.check_overlap(ship_coords, asteroid_coords):
                self.canvas.delete(asteroid["id"])
                if asteroid in self.asteroids:
                    self.asteroids.remove(asteroid)
                self.lives -= 1
                self.update_lives()
                # Lampeggia la navicella senza congelare il gioco
                self.flash_ship()
                if self.lives <= 0:
                    self.game_over_screen()
                    return

        # Collisioni navicella - power-up
        for power_up in self.power_ups[:]:
            power_up_coords = self.canvas.coords(power_up["id"])
            if not power_up_coords or len(power_up_coords) < 4:
                continue
            if self.check_overlap(ship_coords, power_up_coords):
                self.canvas.delete(power_up["id"])
                if power_up in self.power_ups:
                    self.power_ups.remove(power_up)
                self.activate_power_up(power_up["type"])

    # Funzione per verificare sovrapposizione
    def check_overlap(self, bbox1, bbox2):
        if len(bbox1) < 4 or len(bbox2) < 4:
            return False  # Non c'è sovrapposizione se le bounding box non sono valide
        return not (bbox1[2] < bbox2[0] or
                    bbox1[0] > bbox2[2] or
                    bbox1[3] < bbox2[1] or
                    bbox1[1] > bbox2[3])

    # Funzione per lampeggiare la navicella senza congelare il gioco
    def flash_ship(self):
        if self.game_over:
            return

        colors = ["orange", "red", "blue"]
        self.flash_index = 0
        self.flash_steps = 10

        def flash():
            if self.flash_index < self.flash_steps and not self.game_over:
                color = colors[self.flash_index % len(colors)]
                self.canvas.itemconfig(self.ship, fill=color)
                self.flash_index += 1
                self.root.after(100, flash)
            else:
                self.canvas.itemconfig(self.ship, fill="blue")

        flash()

    # Aggiornamento del punteggio
    def update_score(self):
        self.canvas.itemconfig(self.score_label, text=f"Punteggio: {self.score}")

    # Aggiornamento delle vite
    def update_lives(self):
        self.canvas.itemconfig(self.lives_label, text=f"Vite: {self.lives}")

    # Funzione per aggiornare le stelle con effetto scintillio
    def update_stars(self):
        for star in self.stars:
            # Aggiorna la luminosità
            star["brightness"] += star["delta"]
            if star["brightness"] <= 0.5 or star["brightness"] >= 1.0:
                star["delta"] *= -1
            brightness = int(255 * star["brightness"])
            color = f"#{brightness:02x}{brightness:02x}{brightness:02x}"
            self.canvas.itemconfig(star["id"], fill=color)
            # Muovi la stella
            self.canvas.move(star["id"], 0, star["speed"])
            coords = self.canvas.coords(star["id"])
            if not coords or len(coords) < 4 or coords[3] > 600:
                x = random.randint(0, 800)
                y = -5
                self.canvas.coords(star["id"], x, y, x + 2, y + 2)

    # Funzione per gestire i power-up attivi
    def update_power_up(self):
        if self.power_up_active:
            self.power_up_timer -= 1
            if self.power_up_timer <= 0:
                self.deactivate_power_up()

    # Attivazione del power-up
    def activate_power_up(self, power_up_type):
        if power_up_type == "extra_life":
            self.lives += 1
            self.update_lives()
        elif power_up_type == "double_fire":
            self.power_up_active = True
            self.power_up_type = power_up_type
            self.power_up_timer = 500  # Durata del power-up

    # Disattivazione del power-up
    def deactivate_power_up(self):
        self.power_up_active = False
        self.power_up_type = None

    # Funzione per distruggere un asteroide con effetto esplosione
    def destroy_asteroid(self, asteroid):
        coords = self.canvas.coords(asteroid["id"])
        x = (coords[0] + coords[2]) / 2
        y = (coords[1] + coords[3]) / 2
        self.canvas.delete(asteroid["id"])
        if asteroid in self.asteroids:
            self.asteroids.remove(asteroid)
        self.create_explosion(x, y)

    # Funzione per mostrare lo schermo di Game Over con animazione 3D
    def game_over_screen(self):
        self.game_over = True

        # Elimina gli oggetti sullo schermo
        for bullet in self.bullets:
            self.canvas.delete(bullet["id"])
        self.bullets.clear()
        for asteroid in self.asteroids:
            self.canvas.delete(asteroid["id"])
        self.asteroids.clear()
        for power_up in self.power_ups:
            self.canvas.delete(power_up["id"])
        self.power_ups.clear()
        for particle in self.particles:
            self.canvas.delete(particle["id"])
        self.particles.clear()

        # Mostra la scritta "GAME OVER" con effetto 3D
        self.show_game_over_3d()

    # Funzione per creare un testo 3D con animazione breve
    def show_game_over_3d(self):
        # Crea un'immagine con il testo "GAME OVER"
        image = Image.new("RGBA", (800, 600), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        font_size = 70
        text = "GAME OVER"

        # Definisci il font usando ImageFont di Pillow
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        # Calcola le dimensioni del testo
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = 400 - text_width / 2
        y = 300 - text_height / 2

        # Disegna il testo con ombra per effetto 3D
        shadow_color = (50, 50, 50, 255)
        main_color = (255, 0, 0, 255)
        offset = 5

        for i in range(10):
            draw.text((x + offset + i, y + offset + i), text, font=font, fill=shadow_color)

        draw.text((x, y), text, font=font, fill=main_color)

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

        # Riavvia il gioco dopo l'animazione
        self.root.after(1000, self.show_main_menu)

    # Funzione per riavviare il gioco
    def restart_game(self):
        self.start_game()

def main():
    root = tk.Tk()
    game = SpaceShooterGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
