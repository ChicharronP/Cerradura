import tkinter as tk
from app.gui import KeypadGUI
from app.core import KeypadSystem

class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.system = KeypadSystem()
        self.admin_password = "1234" # Clave del administrador
        self.root.title("Sistema de Control de Acceso")
        self.gui = KeypadGUI(self.root, self._key_handler)
        self.root.after(2000, self._reset_status)
    
    def _key_handler(self, key_buffer):
        # Verificar si es modo admin
        if key_buffer == self.admin_password:
            self._handle_system_response('admin_mode')
        else:
            # Verificar clave normal
            exists = self.system.key_exists(key_buffer)
            self._handle_system_response('access_granted' if exists else 'access_denied')
    
    def _handle_system_response(self, message):
        if message == 'access_granted':
            print(1)
            self.gui.update_status("ACCESO PERMITIDO", '#2ecc71')
            return True
        elif message == 'access_denied':
            print(0)
            self.gui.update_status("ACCESO DENEGADO", '#e74c3c')
            return False
        elif message == 'admin_mode':
            print("[TERMINAL] Modo administrador activado")
            self.gui.show_admin_panel(
                self.system.add_key,
                self.system.get_all_keys
            )
            self.gui.update_status("MODO ADMINISTRADOR", '#9b59b6')
        elif message == 'invalid_admin':
            print("[TERMINAL] Intento de acceso admin fallido")
            self.gui.update_status("CLAVE ADMIN INVÁLIDA", '#e67e22')
        elif message == 'exit_admin':
            print("[TERMINAL] Modo administrador desactivado")
            self.gui.update_status("MODO USUARIO", '#34495e')
    
        self.root.after(2000, self._reset_status)
    
    def _reset_status(self):
        self.gui.update_status("Modo: Usuario")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Application()
    app.run()