import tkinter as tk
from i18n import i18n, _

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
            f"{_("instructions_title")}\n\n"
            f"{_("game_objective")}\n"
            f"{_("game_objective_text")}\n\n"
            f"{_("controls")}\n"
            f"{_("control_left")}\n"
            f"{_("control_right")}\n"
            f"{_("control_space")}\n"
            f"{_("control_pause")}\n\n"
            f"{_("mouse_mode")}\n"
            f"{_("mouse_move")}\n"
            f"{_("mouse_click")}\n\n"
            f"{_("powerups")}\n"
            f"{_("powerups_text")}\n\n"
            f"{_("good_luck")}"
        )
        
        self.canvas.create_text(
            400, 250, text=instructions_text, font=("Arial", 14), fill="white", width=600
        )
        
        # Istruzioni per tornare al menù
        self.canvas.create_text(
            400, 500, text=_("back_to_menu"), font=("Arial", 16),
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