import tkinter as tk
from tkinter import ttk, messagebox

class KeypadGUI:
    def __init__(self, root, key_handler):
        self.root = root
        self.key_handler = key_handler
        self.input_buffer = ""
        self._create_display()
        self._configure_styles()
        self._build_interface()
    
    def _configure_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Arial', 14), padding=10)
        self.style.configure('Status.TLabel', font=('Arial', 12), background='#34495e', foreground='white')
    
    def _build_interface(self):
        self.root.title("Sistema de Acceso")
        self.root.geometry('320x480')
        self.root.resizable(False, False)
        
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill='both', expand=True)
        
        # Pantalla de estado
        self.status = ttk.Label(
            main_frame,
            style='Status.TLabel',
            text='Modo: Usuario',
            anchor='center'
        )
        self.status.pack(fill='x', pady=(0, 10))
        
        # Teclado numérico
        self._build_keypad(main_frame)
    
    def _create_display(self):
        self.display = ttk.Entry(
            self.root,
            font=('Arial', 18),
            justify='center',
            show='*'  # Oculta la entrada real
        )
        self.display.pack(fill='x', pady=10)
    
    def _build_keypad(self, parent):
        buttons = [
            ['7', '8', '9'],
            ['4', '5', '6'],
            ['1', '2', '3'],
            ['*', '0', '#']  # Botones faltantes añadidos
        ]
        
        keypad_frame = ttk.Frame(parent)
        keypad_frame.pack(fill='both', expand=True)
        
        for row_idx, row in enumerate(buttons):
            for col_idx, btn_text in enumerate(row):
                btn = ttk.Button(
                    keypad_frame,
                    text=btn_text,
                    command=lambda t=btn_text: self._on_key_press(t)
                )
                btn.grid(
                    row=row_idx, 
                    column=col_idx, 
                    sticky='nsew', 
                    padx=2, 
                    pady=2
                )
                keypad_frame.columnconfigure(col_idx, weight=1)
            keypad_frame.rowconfigure(row_idx, weight=1)
    
    def _on_key_press(self, key):
        if key == '#':
            self._process_input()
        else:
            self.input_buffer += key
            self._update_display()
    
    def _process_input(self):  # ¡Método faltante!
        self.key_handler(self.input_buffer)
        self.input_buffer = ""
        self._update_display()

    def _update_display(self):
        masked_input = '*' * len(self.input_buffer)
        self.status.config(text=f"Entrada: {masked_input}")
    
    def update_status(self, message, bg_color='#34495e'):
        self.status.config(text=message, background=bg_color)
    
    def show_admin_panel(self, add_callback, get_callback):
        AdminPanel(self.root, add_callback, get_callback)

class AdminPanel(tk.Toplevel):
    def __init__(self, parent, add_callback, get_callback):
        super().__init__(parent)
        self.title("Panel de Administración")
        self.geometry('400x300')
        
        self.add_callback = add_callback
        self.get_callback = get_callback
        
        self._build_interface()
        self._update_list()
    
    def _build_interface(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill='both', expand=True)
        
        # Entrada nueva clave
        ttk.Label(main_frame, text="Nueva Clave:").pack(anchor='w')
        self.key_entry = ttk.Entry(main_frame)
        self.key_entry.pack(fill='x', pady=5)
        
        # Botones
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x', pady=5)
        
        ttk.Button(btn_frame, text="Agregar", command=self._add_key).pack(side='left')
        ttk.Button(btn_frame, text="Actualizar", command=self._update_list).pack(side='right')
        
        # Listado
        self.listbox = tk.Listbox(main_frame)
        self.listbox.pack(fill='both', expand=True)
    
    def _add_key(self):
        key = self.key_entry.get()
        if key:
            if self.add_callback(key):
                self._update_list()
                self.key_entry.delete(0, tk.END)
                tk.messagebox.showinfo("Éxito", "Clave agregada correctamente")
            else:
                tk.messagebox.showerror("Error", "La clave ya existe")
    
    def _update_list(self):
        self.listbox.delete(0, tk.END)
        keys = self.get_callback()
        for key, _ in keys:
            self.listbox.insert(tk.END, key)