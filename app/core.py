from .database import DatabaseManager

class KeypadSystem:
    def __init__(self):
        self.db = DatabaseManager()
        self.current_input = ""
        self.admin_mode = False
    
    def handle_input(self, key):
        if key == '#':
            return self._process_input()
        elif key == '*' and not self.admin_mode:
            return self._check_admin_mode()
        else:
            self.current_input += key
            return False, None
    
    def _process_input(self):
        if self.admin_mode:
            self.admin_mode = False
            return True, 'exit_admin'
        
        if self.db.key_exists(self.current_input):
            self.current_input = ""
            return True, 'access_granted'
        else:
            self.current_input = ""
            return True, 'access_denied'
    
    def _check_admin_mode(self):
        if self.db.verify_admin(self.current_input):
            self.admin_mode = True
            self.current_input = ""
            return True, 'admin_mode'
        else:
            self.current_input = ""
            return True, 'invalid_admin'
    
    def add_key(self, key):
        return self.db.add_access_key(key)
    
    def get_all_keys(self):
        return self.db.get_all_keys()
    
    def key_exists(self, key):
        return self.db.key_exists(key)  # Delegar al DatabaseManager