import tkinter as tk
from menu_item import MenuItem
from i18n import i18n, _

class MainMenu:
    def __init__(self, canvas, root, game_instance):
        self.canvas = canvas
        self.root = root
        self.game = game_instance
        self.menu_items = []
        self.selected_option = 0
        self.cursor = None
        
        # Definizione delle opzioni del menù
        self.menu_options = [
            MenuItem(_("start_game"), self.start_game),
            MenuItem(_("instructions"), self.show_instructions),
            MenuItem(_("commands"), self.show_commands),
            MenuItem(_("graphics_options"), self.show_graphics_options),
            MenuItem(_("language"), self.show_language_menu),
            MenuItem(_("exit"), self.exit_game)
        ]
    
    def show(self):
        """Mostra il menù principale"""
        # Cancella tutto
        self.canvas.delete("all")
        self.game.draw_gradient_background()
        
        # Titolo del gioco con font divertente
        self.canvas.create_text(
            400, 150, text=_("game_title"), font=("Comic Sans MS", 50, "bold"), fill="white"
        )
        
        # Posizioni delle opzioni di menù
        menu_y_start = 300
        menu_y_gap = 60
        
        # Cursore per indicare l'opzione selezionata
        self.cursor = self.canvas.create_text(
            300, menu_y_start + self.selected_option * menu_y_gap, text="➤", font=("Arial", 20),
            fill="yellow", anchor="e"
        )
        
        # Aggiorna le opzioni del menù con le traduzioni correnti
        self.update_menu_options()
        
        # Crea le opzioni del menù
        self.menu_items = []
        for index, menu_option in enumerate(self.menu_options):
            item_id = menu_option.create_on_canvas(
                self.canvas, 310, menu_y_start + index * menu_y_gap, 
                anchor="w", tag=f"menu_option_{index}"
            )
            self.menu_items.append(item_id)
            
            # Associa gli eventi del mouse per ogni opzione
            menu_option.bind_events(
                self.canvas, 
                hover_callback=self.menu_hover,
                click_callback=self.menu_click,
                index=index
            )
        
        # Associazione dei tasti per il menù
        self.root.bind("<Up>", self.menu_up)
        self.root.bind("<Down>", self.menu_down)
        self.root.bind("<Return>", self.menu_select)
        self.root.bind("<Escape>", self.back_to_main_menu)
    
    def menu_up(self, event):
        """Naviga verso l'alto nel menù"""
        if not self.game.game_running:
            self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            self.update_menu_selection()
    
    def menu_down(self, event):
        """Naviga verso il basso nel menù"""
        if not self.game.game_running:
            self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            self.update_menu_selection()
    
    def update_menu_selection(self):
        """Aggiorna la posizione del cursore"""
        menu_y_start = 300
        menu_y_gap = 60
        self.canvas.coords(
            self.cursor, 300, menu_y_start + self.selected_option * menu_y_gap
        )
    
    def menu_select(self, event):
        """Seleziona l'opzione corrente"""
        if not self.game.game_running:
            self.execute_menu_option(self.selected_option)
    
    def menu_hover(self, index):
        """Gestisce l'hover del mouse su un'opzione"""
        if not self.game.game_running:
            self.selected_option = index
            self.update_menu_selection()
    
    def menu_click(self, index):
        """Gestisce il clic del mouse su un'opzione"""
        if not self.game.game_running:
            self.execute_menu_option(index)
    
    def execute_menu_option(self, index):
        """Esegue l'azione dell'opzione selezionata"""
        if 0 <= index < len(self.menu_options):
            self.menu_options[index].execute_action()
    
    def back_to_main_menu(self, event=None):
        """Torna al menù principale"""
        if self.game.game_running:
            # Se il gioco è in corso, attiva il game over solo se non è già attivo
            if not self.game.game_over:
                self.game.lives = 0
                self.game.update_lives()
                self.game.game_over_screen()
            self.game.end_game()
            self.selected_option = 0
        else:
            self.selected_option = 0
        self.show()
    
    # Azioni del menù
    def start_game(self):
        """Avvia il gioco"""
        self.game.start_game()
    
    def show_instructions(self):
        """Mostra le istruzioni"""
        if hasattr(self.game, 'instructions_menu'):
            self.game.instructions_menu.show()
        else:
            self.game.show_instructions()
    
    def show_commands(self):
        """Mostra il menù dei comandi"""
        if hasattr(self.game, 'commands_menu'):
            self.game.commands_menu.show()
        else:
            self.game.show_commands_menu()
    
    def show_graphics_options(self):
        """Mostra le opzioni grafiche"""
        if hasattr(self.game, 'graphics_menu'):
            self.game.graphics_menu.show()
        else:
            self.game.show_graphics_options()
    
    def show_language_menu(self):
        """Mostra il menu di selezione della lingua"""
        if hasattr(self.game, 'language_menu'):
            self.game.language_menu.show()
        else:
            self.game.show_language_menu()
    
    def update_menu_options(self):
        """Aggiorna le opzioni del menù con le traduzioni correnti"""
        self.menu_options = [
            MenuItem(_("start_game"), self.start_game),
            MenuItem(_("instructions"), self.show_instructions),
            MenuItem(_("commands"), self.show_commands),
            MenuItem(_("graphics_options"), self.show_graphics_options),
            MenuItem(_("language"), self.show_language_menu),
            MenuItem(_("exit"), self.exit_game)
        ]
    
    def exit_game(self):
        """Esce dal gioco"""
        self.root.destroy()