import tkinter as tk
from i18n import i18n, _

class GraphicsOptionsMenu:
    def __init__(self, canvas, root, game_instance):
        self.canvas = canvas
        self.root = root
        self.game = game_instance
        # Le opzioni verranno aggiornate dinamicamente con le traduzioni
    
    def show(self):
        """Mostra la schermata delle opzioni grafiche"""
        self.canvas.delete("all")
        self.game.draw_gradient_background()
        
        # Titolo
        self.canvas.create_text(
            400, 150, text=_("graphics_options_title"), font=("Arial", 36, "bold"), fill="white"
        )
        
        # Opzioni di dettaglio
        detail_y_start = 250
        detail_y_gap = 60
        detail_options = [_("very_low"), _("high")]
        
        for index, option in enumerate(detail_options):
            color = "yellow" if (index == 0 and self.game.graphics_detail == "low") or (index == 1 and self.game.graphics_detail == "high") else "white"
            self.canvas.create_text(
                400, detail_y_start + index * detail_y_gap, text=option, font=("Arial", 24),
                fill=color, tags=f"detail_option_{index}"
            )
            
            # Associa eventi di clic
            self.canvas.tag_bind(f"detail_option_{index}", "<Button-1>", lambda e, idx=index: self.set_graphics_detail(idx))
            self.canvas.tag_bind(f"detail_option_{index}", "<Enter>", lambda e, idx=index: self.canvas.itemconfig(f"detail_option_{idx}", fill="cyan"))
            self.canvas.tag_bind(f"detail_option_{index}", "<Leave>", lambda e, idx=index: self.update_detail_colors())
        
        # Descrizione
        desc_text = _("graphics_desc")
        self.canvas.create_text(
            400, 400, text=desc_text, font=("Arial", 16), fill="lightgray", justify="center"
        )
        
        # Istruzioni per tornare al menù
        self.canvas.create_text(
            400, 500, text=_("back_to_menu"), font=("Arial", 16),
            fill="yellow"
        )
        
        # Associazione del tasto Esc
        self.root.bind("<Escape>", self.back_to_main_menu)
    
    def set_graphics_detail(self, index):
        """Imposta il livello di dettaglio grafico"""
        if index == 0:
            self.game.graphics_detail = "low"
        elif index == 1:
            self.game.graphics_detail = "high"
        self.update_detail_colors()
    
    def update_detail_colors(self):
        """Aggiorna i colori delle opzioni di dettaglio"""
        for i in range(2):
            if (i == 0 and self.game.graphics_detail == "low") or (i == 1 and self.game.graphics_detail == "high"):
                self.canvas.itemconfig(f"detail_option_{i}", fill="yellow")
            else:
                self.canvas.itemconfig(f"detail_option_{i}", fill="white")
    
    def back_to_main_menu(self, event=None):
        """Torna al menù principale"""
        if hasattr(self.game, 'main_menu'):
            self.game.main_menu.show()
        else:
            self.game.show_main_menu()