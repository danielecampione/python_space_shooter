import tkinter as tk

class CommandsMenu:
    def __init__(self, canvas, root, game_instance):
        self.canvas = canvas
        self.root = root
        self.game = game_instance
        self.checkbox = None
        self.checkbox_label = None
        self.checkmark = None
    
    def show(self):
        """Mostra la schermata dei comandi"""
        self.canvas.delete("all")
        self.game.draw_gradient_background()
        
        self.canvas.create_text(
            400, 150, text="Impostazioni Comandi", font=("Arial", 30, "bold"), fill="white"
        )
        
        # Posizione della casella di controllo
        checkbox_x = 280
        checkbox_y = 300
        checkbox_size = 20
        
        # Disegna la casella di controllo
        self.checkbox = self.canvas.create_rectangle(
            checkbox_x, checkbox_y,
            checkbox_x + checkbox_size, checkbox_y + checkbox_size,
            outline="white", fill="", width=2, tags="checkbox"
        )
        
        # Disegna la spunta se necessario
        if self.game.control_with_mouse:
            self.draw_checkmark()
        
        # Disegna l'etichetta con dimensione di font originale
        self.checkbox_label = self.canvas.create_text(
            checkbox_x + 30, checkbox_y + checkbox_size / 2,
            text="Sposta la navicella attraverso il mouse",
            font=("Arial", 16), fill="white", anchor="w", tags="checkbox_label"
        )
        
        # Unisci casella di controllo ed etichetta in un unico gruppo per l'interazione
        self.canvas.addtag_withtag("checkbox_group", self.checkbox)
        self.canvas.addtag_withtag("checkbox_group", self.checkbox_label)
        
        # Associa l'evento clic all'intero gruppo
        self.canvas.tag_bind("checkbox_group", "<Button-1>", self.toggle_mouse_control)
        
        # Istruzioni per tornare al menù
        self.canvas.create_text(
            400, 500, text="Premi Esc per tornare al Menù", font=("Arial", 16),
            fill="yellow"
        )
        
        # Associazione del tasto Esc
        self.root.bind("<Escape>", self.back_to_main_menu)
    
    def draw_checkmark(self):
        """Disegna la spunta nella casella di controllo"""
        checkbox_x = 280
        checkbox_y = 300
        checkbox_size = 20
        
        # Verifica se la spunta è già stata disegnata
        if self.checkmark:
            self.canvas.delete(self.checkmark)
        
        self.checkmark = self.canvas.create_line(
            checkbox_x + 4, checkbox_y + checkbox_size / 2,
            checkbox_x + checkbox_size / 2, checkbox_y + checkbox_size - 4,
            checkbox_x + checkbox_size - 4, checkbox_y + 4,
            fill="white", width=2, tags="checkmark"
        )
        
        # Aggiungi la spunta al gruppo per l'interazione
        self.canvas.addtag_withtag("checkbox_group", self.checkmark)
    
    def remove_checkmark(self):
        """Rimuove la spunta dalla casella di controllo"""
        if self.checkmark:
            self.canvas.delete(self.checkmark)
            self.checkmark = None
    
    def toggle_mouse_control(self, event=None):
        """Attiva/disattiva il controllo con il mouse"""
        self.game.control_with_mouse = not self.game.control_with_mouse
        if self.game.control_with_mouse:
            self.draw_checkmark()  # Mostra la spunta
        else:
            self.remove_checkmark()
    
    def back_to_main_menu(self, event=None):
        """Torna al menù principale"""
        if hasattr(self.game, 'main_menu'):
            self.game.main_menu.show()
        else:
            self.game.show_main_menu()