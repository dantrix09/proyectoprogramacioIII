import customtkinter as ctk
from tkinter import ttk, messagebox
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
        
        # Conexión a la base de datos
        self.conn = sqlite3.connect('basededatosclinicas.db')
        self.cursor = self.conn.cursor()
        
        self.crear_sidebar()
        self.crear_main_content()
        
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
        # Frame principal
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Título que NUNCA se destruye
        self.titulo_main = ctk.CTkLabel(self.main_frame, text="Sistema de Gestion de Clinicas Moviles", 
                                      font=ctk.CTkFont(size=16, weight="bold"))
        self.titulo_main.grid(row=0, column=0, padx=20, pady=20)
        
        # Frame para contenido dinámico (esto es lo que se limpia)
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        self.mostrar_inicio()
        
    def mostrar_inicio(self):
        self.limpiar_content_frame()
        
        info_text = f"""
        Sistema de Gestion de Clinicas Moviles
        
        Clinicas registradas: {self.obtener_total_clinicas()}
        Vacunas en inventario: {self.obtener_total_vacunas()}
        Alertas pendientes: {self.obtener_total_alertas()}
        
        Seleccione una opcion del menu lateral.
        """
        
        label_info = ctk.CTkLabel(self.content_frame, text=info_text, justify="left")
        label_info.pack(pady=50)
    
    def obtener_total_clinicas(self):
        self.cursor.execute("SELECT COUNT(*) FROM clinicas")
        return self.cursor.fetchone()[0]
    
    def obtener_total_vacunas(self):
        self.cursor.execute("SELECT COUNT(*) FROM vacunas")
        return self.cursor.fetchone()[0]
    
    def obtener_total_alertas(self):
        self.cursor.execute("SELECT COUNT(*) FROM alertas WHERE leida = 0")
        return self.cursor.fetchone()[0]
        
    def mostrar_registro_clinica(self):
        self.limpiar_content_frame()
        self.titulo_main.configure(text="Registro de Nueva Clinica")
        
        frame_form = ctk.CTkFrame(self.content_frame)
        frame_form.pack(padx=20, pady=10, fill="both", expand=True)
        
        label_nombre = ctk.CTkLabel(frame_form, text="Nombre:")
        label_nombre.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        entry_nombre = ctk.CTkEntry(frame_form, width=300)
        entry_nombre.grid(row=0, column=1, padx=10, pady=10)
        
        label_ubicacion = ctk.CTkLabel(frame_form, text="Ubicacion Base:")
        label_ubicacion.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        entry_ubicacion = ctk.CTkEntry(frame_form, width=300)
        entry_ubicacion.grid(row=1, column=1, padx=10, pady=10)
        
        label_latitud = ctk.CTkLabel(frame_form, text="Latitud:")
        label_latitud.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        entry_latitud = ctk.CTkEntry(frame_form, width=300)
        entry_latitud.grid(row=2, column=1, padx=10, pady=10)
        
        label_longitud = ctk.CTkLabel(frame_form, text="Longitud:")
        label_longitud.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        entry_longitud = ctk.CTkEntry(frame_form, width=300)
        entry_longitud.grid(row=3, column=1, padx=10, pady=10)
        
        def guardar_clinica():
            nombre = entry_nombre.get()
            ubicacion = entry_ubicacion.get()
            latitud_val = entry_latitud.get()
            longitud_val = entry_longitud.get()
            
            if nombre and ubicacion and latitud_val and longitud_val:
                try:
                    insertar_datos_clnica(nombre, ubicacion, float(latitud_val), float(longitud_val))
                    messagebox.showinfo("Exito", "Clinica registrada correctamente")
                    entry_nombre.delete(0, 'end')
                    entry_ubicacion.delete(0, 'end')
                    entry_latitud.delete(0, 'end')
                    entry_longitud.delete(0, 'end')
                except ValueError:
                    messagebox.showerror("Error", "Latitud y Longitud deben ser numeros validos")
            else:
                messagebox.showerror("Error", "Complete todos los campos")
        
        btn_guardar = ctk.CTkButton(frame_form, text="Registrar Clinica", command=guardar_clinica)
        btn_guardar.grid(row=4, column=0, columnspan=2, pady=20)
            
    def mostrar_clinicas(self):
        self.limpiar_content_frame()
        self.titulo_main.configure(text="Clinicas Registradas")
        
        self.cursor.execute("SELECT id, nombre, ubicacion_base, latitud, longitud FROM clinicas")
        clinicas = self.cursor.fetchall()
        
        tree = ttk.Treeview(self.content_frame, columns=("ID", "Nombre", "Ubicacion", "Latitud", "Longitud"), show="headings", height=15)
        
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
        self.limpiar_content_frame()
        self.titulo_main.configure(text="Control de Temperatura")
        
        label_titulo = ctk.CTkLabel(self.content_frame, text="Registros de Temperatura", font=ctk.CTkFont(weight="bold"))
        label_titulo.pack(pady=10)
        
        self.cursor.execute("""
            SELECT c.nombre, rt.temperatura, rt.fecha_registro 
            FROM registros_temperatura rt 
            JOIN clinicas c ON rt.clinica_id = c.id 
            ORDER BY rt.fecha_registro DESC LIMIT 10
        """)
        registros = self.cursor.fetchall()
        
        for registro in registros:
            frame_reg = ctk.CTkFrame(self.content_frame)
            frame_reg.pack(padx=20, pady=2, fill="x")
            label_reg = ctk.CTkLabel(frame_reg, text=f"{registro[0]}: {registro[1]}C - {registro[2]}")
            label_reg.pack(pady=2)
            
    def mostrar_vacunas(self):
        self.limpiar_content_frame()
        self.titulo_main.configure(text="Gestion de Vacunas")
        
        self.cursor.execute("SELECT lote, tipo, cantidad, fecha_vencimiento FROM vacunas")
        vacunas = self.cursor.fetchall()
        
        tree = ttk.Treeview(self.content_frame, columns=("Lote", "Tipo", "Cantidad", "Vencimiento"), show="headings", height=15)
        
        tree.heading("Lote", text="Lote")
        tree.heading("Tipo", text="Tipo")
        tree.heading("Cantidad", text="Cantidad")
        tree.heading("Vencimiento", text="Vencimiento")
        
        for vacuna in vacunas:
            tree.insert("", "end", values=vacuna)
        
        tree.pack(padx=10, pady=10, fill="both", expand=True)
        
    def mostrar_rutas(self):
        self.limpiar_content_frame()
        self.titulo_main.configure(text="Gestion de Rutas")
        
        self.cursor.execute("SELECT c.nombre, r.comunidad, r.distancia_km, r.fecha FROM rutas r JOIN clinicas c ON r.clinica_id = c.id")
        rutas = self.cursor.fetchall()
        
        tree = ttk.Treeview(self.content_frame, columns=("Clinica", "Comunidad", "Distancia", "Fecha"), show="headings", height=15)
        
        tree.heading("Clinica", text="Clinica")
        tree.heading("Comunidad", text="Comunidad")
        tree.heading("Distancia", text="Distancia (km)")
        tree.heading("Fecha", text="Fecha")
        
        for ruta in rutas:
            tree.insert("", "end", values=ruta)
        
        tree.pack(padx=10, pady=10, fill="both", expand=True)
        
    def mostrar_alertas(self):
        self.limpiar_content_frame()
        self.titulo_main.configure(text="Sistema de Alertas")
        
        self.cursor.execute("SELECT tipo, mensaje, severidad, fecha_creacion FROM alertas ORDER BY fecha_creacion DESC")
        alertas = self.cursor.fetchall()
        
        for alerta in alertas:
            frame_alert = ctk.CTkFrame(self.content_frame)
            frame_alert.pack(padx=20, pady=5, fill="x")
            
            color = "red" if alerta[2] == "alta" else "orange"
            label_alert = ctk.CTkLabel(frame_alert, text=f"{alerta[0]}: {alerta[1]} - {alerta[3]}", text_color=color)
            label_alert.pack(pady=2)
    
    def mostrar_roles(self):
        self.limpiar_content_frame()
        self.titulo_main.configure(text="Sistema de Gestión por Roles")
        
        from gui_roles import InterfazRoles
        interfaz_roles = InterfazRoles(self.content_frame)
        interfaz_roles.mostrar_interfaz_roles()
            
    def limpiar_content_frame(self):
        """Limpia solo el frame de contenido, NO el título"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = ClinicaMovilGUI()
    app.mainloop()