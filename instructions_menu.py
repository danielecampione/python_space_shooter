import tkinter as tk

class InstructionsMenu:
    def __init__(self, canvas, root, game_instance):
        self.canvas = canvas
        self.root = root
        self.game = game_instance
    
    def show(self):
        """Mostra la schermata delle istruzioni"""
        self.canvas.delete("all")
        self.game.draw_gradient_background()
        
        instructions_text = (
            "Benvenuto in Space Shooter!\n\n"
            "Obiettivo del Gioco:\n"
            "Sopravvivi il più a lungo possibile distruggendo gli asteroidi.\n\n"
            "Controlli:\n"
            " - Freccia Sinistra: Muovi la navicella a sinistra\n"
            " - Freccia Destra: Muovi la navicella a destra\n"
            " - Barra Spaziatrice: Spara\n"
            " - P: Pausa/Riprendi il gioco\n\n"
            "Modalità Mouse Attiva:\n"
            " - Muovi il mouse per muovere la navicella\n"
            " - Clicca con il tasto sinistro per sparare\n\n"
            "Power-up:\n"
            "Raccogli i power-up per ottenere bonus come vite extra\n"
            "o proiettili potenziati.\n\n"
            "Buona fortuna, pilota!"
        )
        
        self.canvas.create_text(
            400, 250, text=instructions_text, font=("Arial", 14), fill="white", width=600
        )
        
        # Istruzioni per tornare al menù
        self.canvas.create_text(
            400, 500, text="Premi Esc per tornare al Menù", font=("Arial", 16),
            fill="yellow"
        )
        
        # Associazione del tasto Esc
        self.root.bind("<Escape>", self.back_to_main_menu)
    
    def back_to_main_menu(self, event=None):
        """Torna al menù principale"""
        if hasattr(self.game, 'main_menu'):
            self.game.main_menu.show()
        else:
            self.game.show_main_menu()