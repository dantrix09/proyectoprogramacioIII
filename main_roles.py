import customtkinter as ctk
from gui_roles import InterfazRoles

class AppRoles(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema de Roles - Clínicas Móviles")
        self.geometry("900x500")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Título principal
        self.titulo = ctk.CTkLabel(self, text="Sistema de Gestión por Roles - Clínicas Móviles", 
                                 font=ctk.CTkFont(size=18, weight="bold"))
        self.titulo.grid(row=0, column=0, padx=20, pady=20)
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Inicializar interfaz de roles
        self.interfaz_roles = InterfazRoles(self.main_frame)
        self.interfaz_roles.mostrar_interfaz_roles()

if __name__ == "__main__":
    app = AppRoles()
    app.mainloop()