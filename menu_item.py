class MenuItem:
    def __init__(self, text, action=None, font=("Arial", 24), color="white", selected_color="yellow"):
        self.text = text
        self.action = action
        self.font = font
        self.color = color
        self.selected_color = selected_color
        self.canvas_item = None
        self.is_selected = False
        self.x = 0
        self.y = 0
        
    def create_on_canvas(self, canvas, x, y, anchor="w", tag=None):
        """Crea l'elemento del menù sul canvas"""
        self.x = x
        self.y = y
        color = self.selected_color if self.is_selected else self.color
        
        self.canvas_item = canvas.create_text(
            x, y, text=self.text, font=self.font,
            fill=color, anchor=anchor, tags=tag
        )
        return self.canvas_item
    
    def set_selected(self, selected, canvas=None):
        """Imposta lo stato di selezione dell'elemento"""
        self.is_selected = selected
        if canvas and self.canvas_item:
            color = self.selected_color if selected else self.color
            canvas.itemconfig(self.canvas_item, fill=color)
    
    def execute_action(self, *args, **kwargs):
        """Esegue l'azione associata all'elemento del menù"""
        if self.action:
            return self.action(*args, **kwargs)
    
    def bind_events(self, canvas, hover_callback=None, click_callback=None, index=None):
        """Associa gli eventi del mouse all'elemento del menù"""
        if self.canvas_item:
            if hover_callback:
                canvas.tag_bind(self.canvas_item, "<Enter>", 
                               lambda e: hover_callback(index if index is not None else self))
            if click_callback:
                canvas.tag_bind(self.canvas_item, "<Button-1>", 
                               lambda e: click_callback(index if index is not None else self))
    
    def update_position(self, canvas, x, y):
        """Aggiorna la posizione dell'elemento sul canvas"""
        if self.canvas_item:
            self.x = x
            self.y = y
            canvas.coords(self.canvas_item, x, y)