import sqlite3
from proyectoprogramacioniii import *

class ClinicaMovilGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema Clinicas Moviles")
        self.geometry("1000x600")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.crear_sidebar()
        self.crear_main_content()
        

    def mostrar_roles(self):
        self.limpiar_main_frame()
        self.titulo_main.configure(text="Sistema de Gestión por Roles")
    
        from gui_roles import InterfazRoles
        interfaz_roles = InterfazRoles(self.main_frame)
        interfaz_roles.mostrar_interfaz_roles()

    def crear_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=180)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.titulo_sidebar = ctk.CTkLabel(self.sidebar_frame, text="CLINICAS MOVILES", font=ctk.CTkFont(weight="bold"))
        self.titulo_sidebar.pack(pady=20)
        
        self.btn_registrar_clinica = ctk.CTkButton(self.sidebar_frame, text="Registrar Clinica", command=self.mostrar_registro_clinica)
        self.btn_registrar_clinica.pack(pady=5)
        
        self.btn_ver_clinicas = ctk.CTkButton(self.sidebar_frame, text="Ver Clinicas", command=self.mostrar_clinicas)
        self.btn_ver_clinicas.pack(pady=5)
        
        self.btn_temperatura = ctk.CTkButton(self.sidebar_frame, text="Control Temperatura", command=self.mostrar_temperatura)
        self.btn_temperatura.pack(pady=5)
        
        self.btn_vacunas = ctk.CTkButton(self.sidebar_frame, text="Gestion Vacunas", command=self.mostrar_vacunas)
        self.btn_vacunas.pack(pady=5)
        
        self.btn_rutas = ctk.CTkButton(self.sidebar_frame, text="Gestion Rutas", command=self.mostrar_rutas)
        self.btn_rutas.pack(pady=5)
        
        self.btn_alertas = ctk.CTkButton(self.sidebar_frame, text="Sistema Alertas", command=self.mostrar_alertas)
        self.btn_alertas.pack(pady=5)
        
        self.btn_roles = ctk.CTkButton(self.sidebar_frame, text="Sistema de Roles", command=self.mostrar_roles)
        self.btn_roles.pack(pady=5)

    def crear_main_content(self):
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        self.titulo_main = ctk.CTkLabel(self.main_frame, text="Sistema de Gestion de Clinicas Moviles", font=ctk.CTkFont(size=16, weight="bold"))
        self.titulo_main.grid(row=0, column=0, padx=20, pady=20)
        
        self.mostrar_inicio()
        
    def mostrar_inicio(self):
        self.limpiar_main_frame()
        
        frame_info = ctk.CTkFrame(self.main_frame)
        frame_info.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        cursor.execute("SELECT COUNT(*) FROM clinicas")
        total_clinicas = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM vacunas")
        total_vacunas = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM alertas WHERE leida = 0")
        alertas_pendientes = cursor.fetchone()[0]
        
        info_text = f"""
        Sistema de Gestion de Clinicas Moviles
        
        Clinicas registradas: {total_clinicas}
        Vacunas en inventario: {total_vacunas}
        Alertas pendientes: {alertas_pendientes}
        
        Seleccione una opcion del menu lateral.
        """
        
        label_info = ctk.CTkLabel(frame_info, text=info_text, justify="left")
        label_info.pack(pady=50)
        
    def mostrar_registro_clinica(self):
        self.limpiar_main_frame()
        self.titulo_main.configure(text="Registro de Nueva Clinica")
        
        frame_form = ctk.CTkFrame(self.main_frame)
        frame_form.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        label_nombre = ctk.CTkLabel(frame_form, text="Nombre:")
        label_nombre.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_nombre = ctk.CTkEntry(frame_form, width=300)
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=10)
        
        label_ubicacion = ctk.CTkLabel(frame_form, text="Ubicacion Base:")
        label_ubicacion.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_ubicacion = ctk.CTkEntry(frame_form, width=300)
        self.entry_ubicacion.grid(row=1, column=1, padx=10, pady=10)
        
        label_latitud = ctk.CTkLabel(frame_form, text="Latitud:")
        label_latitud.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_latitud = ctk.CTkEntry(frame_form, width=300)
        self.entry_latitud.grid(row=2, column=1, padx=10, pady=10)
        
        label_longitud = ctk.CTkLabel(frame_form, text="Longitud:")
        label_longitud.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.entry_longitud = ctk.CTkEntry(frame_form, width=300)
        self.entry_longitud.grid(row=3, column=1, padx=10, pady=10)
        
        btn_guardar = ctk.CTkButton(frame_form, text="Registrar Clinica", command=self.guardar_clinica)
        btn_guardar.grid(row=4, column=0, columnspan=2, pady=20)
        
    def guardar_clinica(self):
        nombre = self.entry_nombre.get()
        ubicacion = self.entry_ubicacion.get()
        latitud = self.entry_latitud.get()
        longitud = self.entry_longitud.get()
        
        if nombre and ubicacion and latitud and longitud:
            try:
                insertar_datos_clnica(nombre, ubicacion, float(latitud), float(longitud))
                messagebox.showinfo("Exito", "Clinica registrada correctamente")
                self.entry_nombre.delete(0, 'end')
                self.entry_ubicacion.delete(0, 'end')
                self.entry_latitud.delete(0, 'end')
                self.entry_longitud.delete(0, 'end')
            except ValueError:
                messagebox.showerror("Error", "Latitud y Longitud deben ser numeros validos")
        else:
            messagebox.showerror("Error", "Complete todos los campos")
            
    def mostrar_clinicas(self):
        self.limpiar_main_frame()
        self.titulo_main.configure(text="Clinicas Registradas")
        
        frame_tabla = ctk.CTkFrame(self.main_frame)
        frame_tabla.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        cursor.execute("SELECT id, nombre, ubicacion_base, latitud, longitud FROM clinicas")
        clinicas = cursor.fetchall()
        
        tree = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "Ubicacion", "Latitud", "Longitud"), show="headings", height=15)
        
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Ubicacion", text="Ubicacion")
        tree.heading("Latitud", text="Latitud")
        tree.heading("Longitud", text="Longitud")
        
        tree.column("ID", width=50)
        tree.column("Nombre", width=200)
        tree.column("Ubicacion", width=150)
        tree.column("Latitud", width=100)
        tree.column("Longitud", width=100)
        
        for clinica in clinicas:
            tree.insert("", "end", values=clinica)
        
        tree.pack(padx=10, pady=10, fill="both", expand=True)
        
    def mostrar_temperatura(self):
        self.limpiar_main_frame()
        self.titulo_main.configure(text="Control de Temperatura")
        
        frame_temp = ctk.CTkFrame(self.main_frame)
        frame_temp.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        label_titulo = ctk.CTkLabel(frame_temp, text="Registros de Temperatura", font=ctk.CTkFont(weight="bold"))
        label_titulo.pack(pady=10)
        
        cursor.execute("""
            SELECT c.nombre, rt.temperatura, rt.fecha_registro 
            FROM registros_temperatura rt 
            JOIN clinicas c ON rt.clinica_id = c.id 
            ORDER BY rt.fecha_registro DESC LIMIT 10
        """)
        registros = cursor.fetchall()
        
        for registro in registros:
            frame_reg = ctk.CTkFrame(frame_temp)
            frame_reg.pack(padx=20, pady=2, fill="x")
            label_reg = ctk.CTkLabel(frame_reg, text=f"{registro[0]}: {registro[1]}C - {registro[2]}")
            label_reg.pack(pady=2)
            
    def mostrar_vacunas(self):
        self.limpiar_main_frame()
        self.titulo_main.configure(text="Gestion de Vacunas")
        
        frame_vacunas = ctk.CTkFrame(self.main_frame)
        frame_vacunas.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        cursor.execute("SELECT lote, tipo, cantidad, fecha_vencimiento FROM vacunas")
        vacunas = cursor.fetchall()
        
        tree = ttk.Treeview(frame_vacunas, columns=("Lote", "Tipo", "Cantidad", "Vencimiento"), show="headings", height=15)
        
        tree.heading("Lote", text="Lote")
        tree.heading("Tipo", text="Tipo")
        tree.heading("Cantidad", text="Cantidad")
        tree.heading("Vencimiento", text="Vencimiento")
        
        for vacuna in vacunas:
            tree.insert("", "end", values=vacuna)
        
        tree.pack(padx=10, pady=10, fill="both", expand=True)
        
    def mostrar_rutas(self):
        self.limpiar_main_frame()
        self.titulo_main.configure(text="Gestion de Rutas")
        
        frame_rutas = ctk.CTkFrame(self.main_frame)
        frame_rutas.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        cursor.execute("SELECT c.nombre, r.comunidad, r.distancia_km, r.fecha FROM rutas r JOIN clinicas c ON r.clinica_id = c.id")
        rutas = cursor.fetchall()
        
        tree = ttk.Treeview(frame_rutas, columns=("Clinica", "Comunidad", "Distancia", "Fecha"), show="headings", height=15)
        
        tree.heading("Clinica", text="Clinica")
        tree.heading("Comunidad", text="Comunidad")
        tree.heading("Distancia", text="Distancia (km)")
        tree.heading("Fecha", text="Fecha")
        
        for ruta in rutas:
            tree.insert("", "end", values=ruta)
        
        tree.pack(padx=10, pady=10, fill="both", expand=True)
        
    def mostrar_alertas(self):
        self.limpiar_main_frame()
        self.titulo_main.configure(text="Sistema de Alertas")
        
        frame_alertas = ctk.CTkFrame(self.main_frame)
        frame_alertas.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        cursor.execute("SELECT tipo, mensaje, severidad, fecha_creacion FROM alertas ORDER BY fecha_creacion DESC")
        alertas = cursor.fetchall()
        
        for alerta in alertas:
            frame_alert = ctk.CTkFrame(frame_alertas)
            frame_alert.pack(padx=20, pady=5, fill="x")
            
            color = "red" if alerta[2] == "alta" else "orange"
            label_alert = ctk.CTkLabel(frame_alert, text=f"{alerta[0]}: {alerta[1]} - {alerta[3]}", text_color=color)
            label_alert.pack(pady=2)
            
    def limpiar_main_frame(self):
        for widget in self.main_frame.winfo_children():
            if widget != self.titulo_main:
                widget.destroy()

if __name__ == "__main__":
    app = ClinicaMovilGUI()
    app.mainloop()

def mostrar_roles(self):
    self.limpiar_main_frame()
    self.titulo_main.configure(text="Sistema de Gestión por Roles")
    
    from gui_roles import InterfazRoles
    interfaz_roles = InterfazRoles(self.main_frame)
    interfaz_roles.mostrar_interfaz_roles()