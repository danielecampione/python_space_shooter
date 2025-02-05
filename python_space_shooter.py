import tkinter as tk
import random

class SpaceShooterGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Space Shooter")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Canvas per il gioco
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="black")
        self.canvas.pack()

        # Variabili di gioco
        self.ship_speed = 10
        self.bullet_speed = 15
        self.asteroid_speed = 5
        self.score = 0

        # Crea la navicella (forma di astronave)
        self.ship = self.create_spaceship(375, 550)

        # Lista per i proiettili
        self.bullets = []

        # Lista per gli asteroidi
        self.asteroids = []

        # Etichetta per il punteggio
        self.score_label = self.canvas.create_text(
            10, 10, text=f"Score: {self.score}", font=("Arial", 14), fill="white", anchor="nw"
        )

        # Sfondo stellato
        self.stars = []
        for _ in range(100):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            size = random.choice([1, 2])
            star = self.canvas.create_oval(x, y, x + size, y + size, fill="white")
            self.stars.append(star)

        # Associazione dei tasti
        self.root.bind("<Left>", self.move_ship_left)
        self.root.bind("<Right>", self.move_ship_right)
        self.root.bind("<space>", self.shoot_bullet)

        # Avvio del ciclo del gioco
        self.game_loop()

    # Funzione per creare la navicella
    def create_spaceship(self, x, y):
        # Coordinate per la forma della navicella
        points = [
            x + 25, y - 25,  # Punta superiore
            x, y + 10,       # Base sinistra
            x + 50, y + 10   # Base destra
        ]
        return self.canvas.create_polygon(points, fill="blue", outline="white", tags="ship")

    # Funzione per aggiungere un effetto di razzo posteriore
    def add_rocket_effect(self, x, y):
        rocket = self.canvas.create_polygon(
            x + 10, y + 15,
            x + 20, y + 30,
            x + 30, y + 15,
            fill="orange", outline="red"
        )
        self.canvas.after(200, lambda: self.canvas.delete(rocket))

    # Funzione per spostare la navicella a sinistra
    def move_ship_left(self, event):
        coords = self.canvas.coords(self.ship)
        if coords[0] > 0:  # Controlla la coordinata x sinistra
            self.canvas.move(self.ship, -self.ship_speed, 0)
            self.add_rocket_effect(coords[0], coords[3])  # Effetto razzo

    # Funzione per spostare la navicella a destra
    def move_ship_right(self, event):
        coords = self.canvas.coords(self.ship)
        if coords[4] < 800:  # Controlla la coordinata x destra
            self.canvas.move(self.ship, self.ship_speed, 0)
            self.add_rocket_effect(coords[0], coords[3])  # Effetto razzo

    # Funzione per sparare un missile
    def shoot_bullet(self, event):
        coords = self.canvas.coords(self.ship)
        # Calcola il centro della navicella
        center_x = (coords[0] + coords[4]) / 2
        top_y = coords[1]  # Coordinata y della punta superiore

        # Costruisci un missile a forma di freccia
        bullet = self.canvas.create_polygon(
            center_x, top_y - 20,  # Punteggiola superiore
            center_x - 5, top_y - 10,  # Base sinistra
            center_x + 5, top_y - 10,  # Base destra
            fill="yellow", outline="orange", tags="bullet"
        )
        self.bullets.append(bullet)

    # Ciclo principale del gioco
    def game_loop(self):
        self.move_bullets()
        self.spawn_asteroids()
        self.move_asteroids()
        self.check_collisions()
        self.update_stars()
        self.canvas.after(30, self.game_loop)

    # Funzione per muovere i proiettili
    def move_bullets(self):
        for bullet in self.bullets[:]:
            self.canvas.move(bullet, 0, -self.bullet_speed)
            bbox = self.canvas.bbox(bullet)
            if bbox[1] < 0:
                self.canvas.delete(bullet)
                self.bullets.remove(bullet)

    # Funzione per generare nuovi asteroidi
    def spawn_asteroids(self):
        if random.randint(1, 50) == 1:
            x = random.randint(0, 800)
            asteroid = self.canvas.create_rectangle(x, 0, x + 50, 50, fill="red", tags="asteroid")
            self.asteroids.append(asteroid)

    # Funzione per muovere gli asteroidi
    def move_asteroids(self):
        for asteroid in self.asteroids[:]:
            self.canvas.move(asteroid, 0, self.asteroid_speed)
            coords = self.canvas.coords(asteroid)
            if coords[3] > 600:
                self.canvas.delete(asteroid)
                self.asteroids.remove(asteroid)

    # Funzione per controllare le collisioni
    def check_collisions(self):
        for bullet in self.bullets[:]:
            bbox = self.canvas.bbox(bullet)
            for asteroid in self.asteroids[:]:
                coords = self.canvas.coords(asteroid)
                if self.is_collision(bbox, coords):
                    self.canvas.delete(bullet)
                    self.canvas.delete(asteroid)
                    self.bullets.remove(bullet)
                    self.asteroids.remove(asteroid)
                    self.score += 10
                    self.update_score()

    # Funzione per verificare le collisioni tra due oggetti
    def is_collision(self, obj1, obj2):
        x1_obj1, y1_obj1, x2_obj1, y2_obj1 = obj1
        x1_obj2, y1_obj2, x2_obj2, y2_obj2 = obj2
        return not (
            x2_obj1 < x1_obj2 or
            x1_obj1 > x2_obj2 or
            y2_obj1 < y1_obj2 or
            y1_obj1 > y2_obj2
        )

    # Funzione per aggiornare il punteggio
    def update_score(self):
        self.canvas.itemconfig(self.score_label, text=f"Score: {self.score}")

    # Funzione per aggiornare lo sfondo stellato
    def update_stars(self):
        for star in self.stars:
            self.canvas.move(star, 0, 2)
            coords = self.canvas.coords(star)
            if coords[3] > 600:
                self.canvas.move(star, 0, -600)

def main():
    root = tk.Tk()
    game = SpaceShooterGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()