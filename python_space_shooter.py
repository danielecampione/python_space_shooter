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
        self.game_over = False

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
            star = self.canvas.create_oval(x, y, x + size, y + size, fill="white", tags="star")
            self.stars.append(star)

        # Associazione dei tasti
        self.root.bind("<Left>", self.move_ship_left)
        self.root.bind("<Right>", self.move_ship_right)
        self.root.bind("<space>", self.shoot_bullet)

        # Avvio del ciclo del gioco
        self.game_loop()

    # Funzione per creare la navicella
    def create_spaceship(self, x, y):
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
        if not self.game_over:
            coords = self.canvas.coords(self.ship)
            if coords[0] > 0:
                self.canvas.move(self.ship, -self.ship_speed, 0)
                self.add_rocket_effect(coords[0], coords[3])

    # Funzione per spostare la navicella a destra
    def move_ship_right(self, event):
        if not self.game_over:
            coords = self.canvas.coords(self.ship)
            if coords[4] < 800:
                self.canvas.move(self.ship, self.ship_speed, 0)
                self.add_rocket_effect(coords[0], coords[3])

    # Funzione per sparare un missile
    def shoot_bullet(self, event):
        if not self.game_over:
            coords = self.canvas.coords(self.ship)
            center_x = (coords[0] + coords[4]) / 2
            top_y = coords[1]

            bullet = self.canvas.create_polygon(
                center_x, top_y - 20,
                center_x - 5, top_y - 10,
                center_x + 5, top_y - 10,
                fill="yellow", outline="orange", tags="bullet"
            )
            self.bullets.append(bullet)

    # Ciclo principale del gioco
    def game_loop(self):
        if not self.game_over:
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
            if bbox and bbox[1] < 0:
                self.canvas.delete(bullet)
                self.bullets.remove(bullet)

    # Funzione per generare nuovi asteroidi
    def spawn_asteroids(self):
        if random.randint(1, 50) == 1:
            x = random.randint(0, 800)
            asteroid = self.create_asteroid(x, 0)
            self.asteroids.append(asteroid)

    # Funzione per creare un asteroide
    def create_asteroid(self, x, y):
        asteroid = []
        for _ in range(random.randint(5, 10)):  # Numero casuale di cerchi
            size = random.randint(5, 20)
            circle = self.canvas.create_oval(
                x, y, x + size, y + size, fill="#8B4513", outline="#5C3317", tags="asteroid"
            )
            asteroid.append(circle)
            x += random.randint(-10, 10)
            y += random.randint(-10, 10)
        return asteroid

    # Funzione per muovere gli asteroidi
    def move_asteroids(self):
        for asteroid in self.asteroids[:]:
            for piece in asteroid:
                if self.canvas.find_withtag(piece):  # Verifica se il pezzo esiste ancora
                    self.canvas.move(piece, 0, self.asteroid_speed)
            piece_coords = self.canvas.coords(asteroid[0])
            if piece_coords and piece_coords[3] > 600:
                for piece in asteroid:
                    self.canvas.delete(piece)
                self.asteroids.remove(asteroid)

    # Funzione per controllare le collisioni
    def check_collisions(self):
        ship_coords = self.canvas.bbox(self.ship)
        if not ship_coords:  # Se la navicella non ha coordinate valide, esci
            return

        # Controlla collisioni tra proiettili e asteroidi
        for bullet in self.bullets[:]:
            bbox = self.canvas.bbox(bullet)
            if not bbox:  # Ignora i proiettili senza coordinate valide
                continue
            for asteroid in self.asteroids[:]:
                for piece in asteroid[:]:  # Itera su una copia della lista dei pezzi
                    piece_coords = self.canvas.coords(piece)
                    if not piece_coords:  # Ignora i pezzi senza coordinate valide
                        continue
                    if self.is_collision(bbox, piece_coords):
                        self.canvas.delete(bullet)
                        self.bullets.remove(bullet)
                        self.destroy_asteroid(asteroid)  # Elimina l'intero asteroide
                        self.score += 1
                        self.update_score()
                        break

        # Controlla collisioni tra asteroidi e navicella
        for asteroid in self.asteroids[:]:
            for piece in asteroid[:]:  # Itera su una copia della lista dei pezzi
                piece_coords = self.canvas.coords(piece)
                if not piece_coords:  # Ignora i pezzi senza coordinate valide
                    continue
                if self.is_collision(ship_coords, piece_coords):
                    self.game_over_screen()
                    return  # Esci dalla funzione dopo il Game Over

    # Funzione per eliminare completamente un asteroide
    def destroy_asteroid(self, asteroid):
        for piece in asteroid:
            if self.canvas.find_withtag(piece):  # Verifica se il pezzo esiste ancora
                self.canvas.delete(piece)
        if asteroid in self.asteroids:  # Rimuovi l'asteroide dalla lista
            self.asteroids.remove(asteroid)

    # Funzione per verificare le collisioni tra due oggetti
    def is_collision(self, obj1, obj2):
        if not obj1 or not obj2:  # Verifica che entrambi gli oggetti abbiano coordinate valide
            return False
        try:
            x1_obj1, y1_obj1, x2_obj1, y2_obj1 = obj1
            x1_obj2, y1_obj2, x2_obj2, y2_obj2 = obj2
        except ValueError:  # Gestisci eventuali errori di unpacking
            return False
        return not (
            x2_obj1 < x1_obj2 or
            x1_obj1 > x2_obj2 or
            y2_obj1 < y1_obj2 or
            y1_obj1 > y2_obj2
        )

    # Funzione per mostrare lo schermo di Game Over
    def game_over_screen(self):
        self.game_over = True
        # Cancella tutto tranne le stelle per evitare errori
        for item in self.canvas.find_all():
            tags = self.canvas.gettags(item)
            if "star" not in tags:  # Conserva solo le stelle
                self.canvas.delete(item)
        self.canvas.create_text(
            400, 300, text="GAME OVER", font=("Arial", 50), fill="red", anchor="center"
        )
        self.root.after(1000, self.restart_game)  # Riavvia dopo 1 secondo

    # Funzione per riavviare il gioco
    def restart_game(self):
        self.canvas.delete("all")  # Cancella tutto
        self.score = 0
        self.game_over = False

        # Ricrea la navicella
        self.ship = self.create_spaceship(375, 550)

        # Resetta le liste di proiettili e asteroidi
        self.bullets = []
        self.asteroids = []

        # Ricrea l'etichetta del punteggio
        self.score_label = self.canvas.create_text(
            10, 10, text=f"Score: {self.score}", font=("Arial", 14), fill="white", anchor="nw"
        )

        # Ricrea lo sfondo stellato
        self.stars = []
        for _ in range(100):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            size = random.choice([1, 2])
            star = self.canvas.create_oval(x, y, x + size, y + size, fill="white", tags="star")
            self.stars.append(star)

        # Riavvia il ciclo principale del gioco
        self.game_loop()

    # Funzione per aggiornare il punteggio
    def update_score(self):
        self.canvas.itemconfig(self.score_label, text=f"Score: {self.score}")

    # Funzione per aggiornare lo sfondo stellato
    def update_stars(self):
        for star in self.stars[:]:  # Itera su una copia della lista delle stelle
            if not self.canvas.find_withtag(star):  # Ignora le stelle eliminate
                continue
            self.canvas.move(star, 0, 2)
            coords = self.canvas.coords(star)
            if coords and coords[3] > 600:  # Verifica se le coordinate sono valide
                self.canvas.move(star, 0, -600)

def main():
    root = tk.Tk()
    game = SpaceShooterGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()