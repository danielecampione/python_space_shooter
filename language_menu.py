import tkinter as tk
from i18n import i18n, _

class LanguageMenu:
    def __init__(self, canvas, root, game_instance):
        self.canvas = canvas
        self.root = root
        self.game = game_instance
        self.language_options = [
            {'code': 'en', 'name': 'english'},
            {'code': 'it', 'name': 'italian'},
            {'code': 'zh', 'name': 'chinese'}
        ]
    
    def show(self):
        """Mostra la schermata di selezione della lingua"""
        self.canvas.delete("all")
        self.game.draw_gradient_background()
        
        # Titolo
        self.canvas.create_text(
            400, 150, text=_("language_selection"), font=("Arial", 36, "bold"), fill="white"
        )
        
        # Opzioni di lingua
        lang_y_start = 250
        lang_y_gap = 60
        
        for index, lang_option in enumerate(self.language_options):
            # Evidenzia la lingua corrente
            color = "yellow" if lang_option['code'] == i18n.get_current_language() else "white"
            
            text_id = self.canvas.create_text(
                400, lang_y_start + index * lang_y_gap, 
                text=_(lang_option['name']), 
                font=("Arial", 24),
                fill=color, 
                tags=f"lang_option_{index}"
            )
            
            # Associa eventi di clic e hover
            self.canvas.tag_bind(f"lang_option_{index}", "<Button-1>", 
                               lambda e, code=lang_option['code']: self.set_language(code))
            self.canvas.tag_bind(f"lang_option_{index}", "<Enter>", 
                               lambda e, idx=index: self.canvas.itemconfig(f"lang_option_{idx}", fill="cyan"))
            self.canvas.tag_bind(f"lang_option_{index}", "<Leave>", 
                               lambda e: self.update_language_colors())
        
        # Istruzioni per tornare al menù
        self.canvas.create_text(
            400, 500, text=_("back_to_menu"), font=("Arial", 16),
            fill="yellow"
        )
        
        # Associazione del tasto Esc
        self.root.bind("<Escape>", self.back_to_main_menu)
    
    def set_language(self, language_code):
        """Imposta la lingua e aggiorna l'interfaccia"""
        if i18n.set_language(language_code):
            # Aggiorna immediatamente questo menu
            self.show()
            # Notifica al gioco che la lingua è cambiata
            if hasattr(self.game, 'on_language_changed'):
                self.game.on_language_changed()
            
            # Aggiorna tutti i menu per riflettere la nuova lingua
            if hasattr(self.game, 'main_menu'):
                self.game.main_menu.update_menu_options()
    
    def update_language_colors(self):
        """Aggiorna i colori delle opzioni di lingua"""
        for i, lang_option in enumerate(self.language_options):
            if lang_option['code'] == i18n.get_current_language():
                self.canvas.itemconfig(f"lang_option_{i}", fill="yellow")
            else:
                self.canvas.itemconfig(f"lang_option_{i}", fill="white")
    
    def back_to_main_menu(self, event=None):
        """Torna al menù principale"""
        if hasattr(self.game, 'main_menu'):
            self.game.main_menu.show()
        else:
            self.game.show_main_menu()