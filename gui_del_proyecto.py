import customtkinter as ctk
from tkinter import ttk, messagebox
import sqlite3
from proyectoprogramacioniii import *
from control_temp import ControlTemperatura
from auditoria_gui import AuditoriaGUI

class ClinicaMovilGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema Clinicas Moviles")
        self.geometry("1000x600")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.conn = sqlite3.connect('basededatosclinicas.db')
        self.cursor = self.conn.cursor()
        
        self.crear_sidebar()
        self.crear_main_content()

    def crear_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=180)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.titulo_sidebar = ctk.CTkLabel(self.sidebar_frame, text="CLINICAS MOVILES", 
                                         font=ctk.CTkFont(weight="bold", size=14))
        self.titulo_sidebar.pack(pady=20)
        
        label_registros = ctk.CTkLabel(self.sidebar_frame, text="REGISTROS", 
                                     font=ctk.CTkFont(weight="bold"))
        label_registros.pack(pady=(10,5))
        
        self.btn_registrar_clinica = ctk.CTkButton(self.sidebar_frame, text="Registrar Clinica", 
                                                 command=self.mostrar_registro_clinica)
        self.btn_registrar_clinica.pack(pady=2, padx=10, fill="x")
        
        self.btn_registrar_usuario = ctk.CTkButton(self.sidebar_frame, text="Registrar Usuario", 
                                                 command=self.mostrar_registro_usuario)
        self.btn_registrar_usuario.pack(pady=2, padx=10, fill="x")
        
        self.btn_registrar_equipo = ctk.CTkButton(self.sidebar_frame, text="Registrar Equipo", 
                                                command=self.mostrar_registro_equipo)
        self.btn_registrar_equipo.pack(pady=2, padx=10, fill="x")
        
        self.btn_registrar_vacuna = ctk.CTkButton(self.sidebar_frame, text="Registrar Vacuna", 
                                                command=self.mostrar_registro_vacuna)
        self.btn_registrar_vacuna.pack(pady=2, padx=10, fill="x")
        
        self.btn_registrar_ruta = ctk.CTkButton(self.sidebar_frame, text="Registrar Ruta", 
                                              command=self.mostrar_registro_ruta)
        self.btn_registrar_ruta.pack(pady=2, padx=10, fill="x")
        
        label_consultas = ctk.CTkLabel(self.sidebar_frame, text="CONSULTAS", 
                                     font=ctk.CTkFont(weight="bold"))
        label_consultas.pack(pady=(15,5))
        
        self.btn_ver_clinicas = ctk.CTkButton(self.sidebar_frame, text="Ver Clinicas", 
                                            command=self.mostrar_clinicas)
        self.btn_ver_clinicas.pack(pady=2, padx=10, fill="x")
        
        self.btn_ver_usuarios = ctk.CTkButton(self.sidebar_frame, text="Ver Usuarios", 
                                            command=self.mostrar_usuarios)
        self.btn_ver_usuarios.pack(pady=2, padx=10, fill="x")
        
        self.btn_ver_equipos = ctk.CTkButton(self.sidebar_frame, text="Ver Equipos", 
                                           command=self.mostrar_equipos)
        self.btn_ver_equipos.pack(pady=2, padx=10, fill="x")
        
        self.btn_temperatura = ctk.CTkButton(self.sidebar_frame, text="Control Temperatura", 
                                           command=self.mostrar_temperatura_gui)
        self.btn_temperatura.pack(pady=2, padx=10, fill="x")
        
        self.btn_vacunas = ctk.CTkButton(self.sidebar_frame, text="Gestion Vacunas", 
                                       command=self.mostrar_vacunas)
        self.btn_vacunas.pack(pady=2, padx=10, fill="x")
        
        self.btn_rutas = ctk.CTkButton(self.sidebar_frame, text="Gestion Rutas", 
                                     command=self.mostrar_rutas)
        self.btn_rutas.pack(pady=2, padx=10, fill="x")
        
        self.btn_alertas = ctk.CTkButton(self.sidebar_frame, text="Sistema Alertas", 
                                       command=self.mostrar_alertas)
        self.btn_alertas.pack(pady=2, padx=10, fill="x")
        
        self.btn_auditoria = ctk.CTkButton(self.sidebar_frame, text="Agregar Auditoria", 
                                         command=self.mostrar_auditoria_gui,
                                         fg_color="#8B4513", hover_color="#A0522D")
        self.btn_auditoria.pack(pady=2, padx=10, fill="x")

    def crear_main_content(self):
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        self.titulo_main = ctk.CTkLabel(self.main_frame, text="Sistema de Gestion de Clinicas Moviles", 
                                      font=ctk.CTkFont(size=16, weight="bold"))
        self.titulo_main.grid(row=0, column=0, padx=20, pady=20)
        
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        self.mostrar_inicio()

    def mostrar_inicio(self):
        self.limpiar_content_frame()
        
        total_clinicas = self.obtener_total_clinicas()
        total_vacunas = self.obtener_total_vacunas()
        total_alertas = self.obtener_total_alertas()
        total_usuarios = self.obtener_total_usuarios()
        total_equipos = self.obtener_total_equipos()
        
        frame_info = ctk.CTkFrame(self.content_frame)
        frame_info.pack(expand=True, fill="both", padx=50, pady=50)
        
        label_titulo = ctk.CTkLabel(frame_info, text="PANEL PRINCIPAL", 
                                  font=ctk.CTkFont(size=18, weight="bold"))
        label_titulo.pack(pady=20)
        
        info_text = f"""
        Sistema de Gestion de Clinicas Moviles
        
        Clinicas registradas: {total_clinicas}
        Usuarios en sistema: {total_usuarios}
        Equipos medicos: {total_equipos}
        Vacunas en inventario: {total_vacunas}
        Alertas pendientes: {total_alertas}
        
        Seleccione una opcion del menu lateral para comenzar.
        """
        
        label_info = ctk.CTkLabel(frame_info, text=info_text, justify="center",
                                font=ctk.CTkFont(size=14))
        label_info.pack(pady=30)

    def obtener_total_clinicas(self):
        self.cursor.execute("SELECT COUNT(*) FROM clinicas")
        return self.cursor.fetchone()[0]
    
    def obtener_total_vacunas(self):
        self.cursor.execute("SELECT COUNT(*) FROM vacunas")
        return self.cursor.fetchone()[0]
    
    def obtener_total_alertas(self):
        self.cursor.execute("SELECT COUNT(*) FROM alertas WHERE leida = 0")
        return self.cursor.fetchone()[0]
    
    def obtener_total_usuarios(self):
        self.cursor.execute("SELECT COUNT(*) FROM usuarios")
        return self.cursor.fetchone()[0]
    
    def obtener_total_equipos(self):
        self.cursor.execute("SELECT COUNT(*) FROM equipos_medicos")
        return self.cursor.fetchone()[0]

    def limpiar_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

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

    def mostrar_registro_usuario(self):
        self.limpiar_content_frame()
        self.titulo_main.configure(text="Registro de Nuevo Usuario")
        
        frame_form = ctk.CTkFrame(self.content_frame)
        frame_form.pack(padx=20, pady=10, fill="both", expand=True)
        
        label_username = ctk.CTkLabel(frame_form, text="Username:")
        label_username.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        entry_username = ctk.CTkEntry(frame_form, width=300)
        entry_username.grid(row=0, column=1, padx=10, pady=10)
        
        label_nombre_completo = ctk.CTkLabel(frame_form, text="Nombre Completo:")
        label_nombre_completo.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        entry_nombre_completo = ctk.CTkEntry(frame_form, width=300)
        entry_nombre_completo.grid(row=1, column=1, padx=10, pady=10)
        
        label_correo = ctk.CTkLabel(frame_form, text="Correo:")
        label_correo.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        entry_correo = ctk.CTkEntry(frame_form, width=300)
        entry_correo.grid(row=2, column=1, padx=10, pady=10)
        
        label_rol = ctk.CTkLabel(frame_form, text="Rol:")
        label_rol.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        combo_rol = ctk.CTkComboBox(frame_form, values=["admin", "medico", "mantenimiento"], width=300)
        combo_rol.grid(row=3, column=1, padx=10, pady=10)
        combo_rol.set("medico")
        
        def guardar_usuario():
            username = entry_username.get()
            nombre_completo = entry_nombre_completo.get()
            correo = entry_correo.get()
            rol = combo_rol.get()
            
            if username and nombre_completo and correo and rol:
                try:
                    insertar_datos_usuario(username, nombre_completo, correo, rol)
                    messagebox.showinfo("Exito", "Usuario registrado correctamente")
                    entry_username.delete(0, 'end')
                    entry_nombre_completo.delete(0, 'end')
                    entry_correo.delete(0, 'end')
                    combo_rol.set("medico")
                except Exception as e:
                    messagebox.showerror("Error", f"Error al registrar usuario: {str(e)}")
            else:
                messagebox.showerror("Error", "Complete todos los campos")
        
        btn_guardar = ctk.CTkButton(frame_form, text="Registrar Usuario", command=guardar_usuario)
        btn_guardar.grid(row=4, column=0, columnspan=2, pady=20)

    def mostrar_registro_equipo(self):
        self.limpiar_content_frame()
        self.titulo_main.configure(text="Registro de Nuevo Equipo Medico")
        
        frame_form = ctk.CTkFrame(self.content_frame)
        frame_form.pack(padx=20, pady=10, fill="both", expand=True)
        
        label_tipo = ctk.CTkLabel(frame_form, text="Tipo:")
        label_tipo.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        entry_tipo = ctk.CTkEntry(frame_form, width=300)
        entry_tipo.grid(row=0, column=1, padx=10, pady=10)
        
        label_modelo = ctk.CTkLabel(frame_form, text="Modelo:")
        label_modelo.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        entry_modelo = ctk.CTkEntry(frame_form, width=300)
        entry_modelo.grid(row=1, column=1, padx=10, pady=10)
        
        label_serie = ctk.CTkLabel(frame_form, text="Numero de Serie:")
        label_serie.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        entry_serie = ctk.CTkEntry(frame_form, width=300)
        entry_serie.grid(row=2, column=1, padx=10, pady=10)
        
        label_capacidad = ctk.CTkLabel(frame_form, text="Capacidad (litros):")
        label_capacidad.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        entry_capacidad = ctk.CTkEntry(frame_form, width=300)
        entry_capacidad.grid(row=3, column=1, padx=10, pady=10)
        
        label_clinica_id = ctk.CTkLabel(frame_form, text="ID Clinica:")
        label_clinica_id.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        entry_clinica_id = ctk.CTkEntry(frame_form, width=300)
        entry_clinica_id.grid(row=4, column=1, padx=10, pady=10)
        
        def guardar_equipo():
            tipo = entry_tipo.get()
            modelo = entry_modelo.get()
            numero_serie = entry_serie.get()
            capacidad_str = entry_capacidad.get()
            clinica_id_str = entry_clinica_id.get()
            
            if tipo and modelo and numero_serie and capacidad_str and clinica_id_str:
                try:
                    capacidad = float(capacidad_str)
                    clinica_id = int(clinica_id_str)
                    
                    insertar_datos_equipo_medico(tipo, modelo, numero_serie, clinica_id, capacidad)
                    messagebox.showinfo("Exito", "Equipo medico registrado correctamente")
                    entry_tipo.delete(0, 'end')
                    entry_modelo.delete(0, 'end')
                    entry_serie.delete(0, 'end')
                    entry_capacidad.delete(0, 'end')
                    entry_clinica_id.delete(0, 'end')
                except ValueError:
                    messagebox.showerror("Error", "Capacidad y ID Clinica deben ser numeros validos")
                except Exception as e:
                    messagebox.showerror("Error", f"Error al registrar equipo: {str(e)}")
            else:
                messagebox.showerror("Error", "Complete todos los campos")
        
        btn_guardar = ctk.CTkButton(frame_form, text="Registrar Equipo", command=guardar_equipo)
        btn_guardar.grid(row=5, column=0, columnspan=2, pady=20)

    def mostrar_registro_vacuna(self):
        self.limpiar_content_frame()
        self.titulo_main.configure(text="Registro de Nueva Vacuna")
        
        frame_form = ctk.CTkFrame(self.content_frame)
        frame_form.pack(padx=20, pady=10, fill="both", expand=True)
        
        label_lote = ctk.CTkLabel(frame_form, text="Lote:")
        label_lote.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        entry_lote = ctk.CTkEntry(frame_form, width=300)
        entry_lote.grid(row=0, column=1, padx=10, pady=10)
        
        label_tipo = ctk.CTkLabel(frame_form, text="Tipo:")
        label_tipo.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        entry_tipo = ctk.CTkEntry(frame_form, width=300)
        entry_tipo.grid(row=1, column=1, padx=10, pady=10)
        
        label_cantidad = ctk.CTkLabel(frame_form, text="Cantidad:")
        label_cantidad.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        entry_cantidad = ctk.CTkEntry(frame_form, width=300)
        entry_cantidad.grid(row=2, column=1, padx=10, pady=10)
        
        label_temp_min = ctk.CTkLabel(frame_form, text="Temp. Minima:")
        label_temp_min.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        entry_temp_min = ctk.CTkEntry(frame_form, width=300)
        entry_temp_min.grid(row=3, column=1, padx=10, pady=10)
        
        label_temp_max = ctk.CTkLabel(frame_form, text="Temp. Maxima:")
        label_temp_max.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        entry_temp_max = ctk.CTkEntry(frame_form, width=300)
        entry_temp_max.grid(row=4, column=1, padx=10, pady=10)
        
        label_vencimiento = ctk.CTkLabel(frame_form, text="Fecha Vencimiento (YYYY-MM-DD):")
        label_vencimiento.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        entry_vencimiento = ctk.CTkEntry(frame_form, width=300)
        entry_vencimiento.grid(row=5, column=1, padx=10, pady=10)
        
        label_clinica_id = ctk.CTkLabel(frame_form, text="ID Clinica:")
        label_clinica_id.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        entry_clinica_id = ctk.CTkEntry(frame_form, width=300)
        entry_clinica_id.grid(row=6, column=1, padx=10, pady=10)
        
        def guardar_vacuna():
            try:
                lote = entry_lote.get()
                tipo = entry_tipo.get()
                cantidad = int(entry_cantidad.get())
                temp_min = float(entry_temp_min.get())
                temp_max = float(entry_temp_max.get())
                fecha_vencimiento = entry_vencimiento.get()
                clinica_id = int(entry_clinica_id.get())
                
                if lote and tipo and fecha_vencimiento:
                    insertar_datos_vacuna(lote, tipo, cantidad, temp_min, temp_max, fecha_vencimiento, clinica_id)
                    messagebox.showinfo("Exito", "Vacuna registrada correctamente")
                    entry_lote.delete(0, 'end')
                    entry_tipo.delete(0, 'end')
                    entry_cantidad.delete(0, 'end')
                    entry_temp_min.delete(0, 'end')
                    entry_temp_max.delete(0, 'end')
                    entry_vencimiento.delete(0, 'end')
                    entry_clinica_id.delete(0, 'end')
                else:
                    messagebox.showerror("Error", "Complete todos los campos")
            except ValueError:
                messagebox.showerror("Error", "Verifique que los valores numericos sean correctos")
            except Exception as e:
                messagebox.showerror("Error", f"Error al registrar vacuna: {str(e)}")
        
        btn_guardar = ctk.CTkButton(frame_form, text="Registrar Vacuna", command=guardar_vacuna)
        btn_guardar.grid(row=7, column=0, columnspan=2, pady=20)

    def mostrar_registro_ruta(self):
        self.limpiar_content_frame()
        self.titulo_main.configure(text="Registro de Nueva Ruta")
        
        frame_form = ctk.CTkFrame(self.content_frame)
        frame_form.pack(padx=20, pady=10, fill="both", expand=True)
        
        label_clinica_id = ctk.CTkLabel(frame_form, text="ID Clinica:")
        label_clinica_id.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        entry_clinica_id = ctk.CTkEntry(frame_form, width=300)
        entry_clinica_id.grid(row=0, column=1, padx=10, pady=10)
        
        label_comunidad = ctk.CTkLabel(frame_form, text="Comunidad:")
        label_comunidad.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        entry_comunidad = ctk.CTkEntry(frame_form, width=300)
        entry_comunidad.grid(row=1, column=1, padx=10, pady=10)
        
        label_fecha = ctk.CTkLabel(frame_form, text="Fecha (YYYY-MM-DD):")
        label_fecha.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        entry_fecha = ctk.CTkEntry(frame_form, width=300)
        entry_fecha.grid(row=2, column=1, padx=10, pady=10)
        
        label_distancia = ctk.CTkLabel(frame_form, text="Distancia (km):")
        label_distancia.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        entry_distancia = ctk.CTkEntry(frame_form, width=300)
        entry_distancia.grid(row=3, column=1, padx=10, pady=10)
        
        def guardar_ruta():
            try:
                clinica_id = int(entry_clinica_id.get())
                comunidad = entry_comunidad.get()
                fecha = entry_fecha.get()
                distancia = float(entry_distancia.get())
                
                if comunidad and fecha:
                    insertar_datos_ruta(clinica_id, comunidad, fecha, distancia)
                    messagebox.showinfo("Exito", "Ruta registrada correctamente")
                    entry_clinica_id.delete(0, 'end')
                    entry_comunidad.delete(0, 'end')
                    entry_fecha.delete(0, 'end')
                    entry_distancia.delete(0, 'end')
                else:
                    messagebox.showerror("Error", "Complete todos los campos")
            except ValueError:
                messagebox.showerror("Error", "Verifique que los valores numericos sean correctos")
            except Exception as e:
                messagebox.showerror("Error", f"Error al registrar ruta: {str(e)}")
        
        btn_guardar = ctk.CTkButton(frame_form, text="Registrar Ruta", command=guardar_ruta)
        btn_guardar.grid(row=4, column=0, columnspan=2, pady=20)

    def mostrar_clinicas(self):
        self.limpiar_content_frame()
        self.titulo_main.configure(text="Clinicas Registradas")
        
        self.cursor.execute("SELECT id, nombre, ubicacion_base, latitud, longitud FROM clinicas")
        clinicas = self.cursor.fetchall()
        
        frame_tabla = ctk.CTkFrame(self.content_frame)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)
        
        tree = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "Ubicacion", "Latitud", "Longitud"), 
                          show="headings", height=15)
        
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
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        for clinica in clinicas:
            tree.insert("", "end", values=clinica)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def mostrar_usuarios(self):
        self.limpiar_content_frame()
        self.titulo_main.configure(text="Usuarios Registrados")
        
        self.cursor.execute("SELECT id, username, nombre_completo, correo, rol FROM usuarios")
        usuarios = self.cursor.fetchall()
        
        frame_tabla = ctk.CTkFrame(self.content_frame)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)
        
        tree = ttk.Treeview(frame_tabla, columns=("ID", "Username", "Nombre", "Correo", "Rol"), 
                          show="headings", height=15)
        
        tree.heading("ID", text="ID")
        tree.heading("Username", text="Username")
        tree.heading("Nombre", text="Nombre Completo")
        tree.heading("Correo", text="Correo")
        tree.heading("Rol", text="Rol")
        
        tree.column("ID", width=50)
        tree.column("Username", width=120)
        tree.column("Nombre", width=200)
        tree.column("Correo", width=150)
        tree.column("Rol", width=100)
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        for usuario in usuarios:
            tree.insert("", "end", values=usuario)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def mostrar_equipos(self):
        self.limpiar_content_frame()
        self.titulo_main.configure(text="Equipos Medicos Registrados")
        
        self.cursor.execute("""
            SELECT e.id, e.tipo, e.modelo, e.numero_serie, e.capacidad_litros, c.nombre 
            FROM equipos_medicos e 
            LEFT JOIN clinicas c ON e.clinica_id = c.id
        """)
        equipos = self.cursor.fetchall()
        
        frame_tabla = ctk.CTkFrame(self.content_frame)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)
        
        tree = ttk.Treeview(frame_tabla, columns=("ID", "Tipo", "Modelo", "Serie", "Capacidad", "Clinica"), 
                          show="headings", height=15)
        
        tree.heading("ID", text="ID")
        tree.heading("Tipo", text="Tipo")
        tree.heading("Modelo", text="Modelo")
        tree.heading("Serie", text="Numero Serie")
        tree.heading("Capacidad", text="Capacidad (L)")
        tree.heading("Clinica", text="Clinica")
        
        tree.column("ID", width=50)
        tree.column("Tipo", width=120)
        tree.column("Modelo", width=120)
        tree.column("Serie", width=120)
        tree.column("Capacidad", width=100)
        tree.column("Clinica", width=150)
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        for equipo in equipos:
            tree.insert("", "end", values=equipo)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def mostrar_temperatura_gui(self):
        self.limpiar_content_frame()
        self.titulo_main.configure(text="Control de Cadena de Frio")
        
        control_temp = ControlTemperatura(self.content_frame)
        control_temp.mostrar_interfaz_temperatura()
        
    def mostrar_vacunas(self):
        self.limpiar_content_frame()
        self.titulo_main.configure(text="Gestion de Vacunas")
        
        self.cursor.execute("SELECT lote, tipo, cantidad, fecha_vencimiento FROM vacunas")
        vacunas = self.cursor.fetchall()
        
        frame_tabla = ctk.CTkFrame(self.content_frame)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)
        
        tree = ttk.Treeview(frame_tabla, columns=("Lote", "Tipo", "Cantidad", "Vencimiento"), 
                          show="headings", height=15)
        
        tree.heading("Lote", text="Lote")
        tree.heading("Tipo", text="Tipo")
        tree.heading("Cantidad", text="Cantidad")
        tree.heading("Vencimiento", text="Vencimiento")
        
        tree.column("Lote", width=150)
        tree.column("Tipo", width=150)
        tree.column("Cantidad", width=100)
        tree.column("Vencimiento", width=120)
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        for vacuna in vacunas:
            tree.insert("", "end", values=vacuna)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def mostrar_rutas(self):
        self.limpiar_content_frame()
        self.titulo_main.configure(text="Gestion de Rutas")
        
        self.cursor.execute("SELECT c.nombre, r.comunidad, r.distancia_km, r.fecha FROM rutas r JOIN clinicas c ON r.clinica_id = c.id")
        rutas = self.cursor.fetchall()
        
        frame_tabla = ctk.CTkFrame(self.content_frame)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)
        
        tree = ttk.Treeview(frame_tabla, columns=("Clinica", "Comunidad", "Distancia", "Fecha"), 
                          show="headings", height=15)
        
        tree.heading("Clinica", text="Clinica")
        tree.heading("Comunidad", text="Comunidad")
        tree.heading("Distancia", text="Distancia (km)")
        tree.heading("Fecha", text="Fecha")
        
        tree.column("Clinica", width=150)
        tree.column("Comunidad", width=150)
        tree.column("Distancia", width=120)
        tree.column("Fecha", width=120)
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        for ruta in rutas:
            tree.insert("", "end", values=ruta)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def mostrar_alertas(self):
        self.limpiar_content_frame()
        self.titulo_main.configure(text="Sistema de Alertas")
        
        self.cursor.execute("SELECT tipo, mensaje, severidad, fecha_creacion FROM alertas ORDER BY fecha_creacion DESC")
        alertas = self.cursor.fetchall()
        
        frame_alertas = ctk.CTkFrame(self.content_frame)
        frame_alertas.pack(fill="both", expand=True, padx=20, pady=10)
        
        if not alertas:
            label_no_alertas = ctk.CTkLabel(frame_alertas, text="No hay alertas activas", 
                                          font=ctk.CTkFont(size=14))
            label_no_alertas.pack(pady=50)
            return
        
        for alerta in alertas:
            frame_alert = ctk.CTkFrame(frame_alertas)
            frame_alert.pack(fill="x", padx=10, pady=5)
            
            color = "red" if alerta[2] == "alta" else "orange" if alerta[2] == "media" else "yellow"
            label_alert = ctk.CTkLabel(frame_alert, 
                                     text=f"{alerta[0]}: {alerta[1]} - {alerta[3]}", 
                                     text_color=color,
                                     font=ctk.CTkFont(weight="bold"))
            label_alert.pack(pady=5)
            
    def mostrar_auditoria_gui(self):
        self.limpiar_content_frame()
        self.titulo_main.configure(text="Registro de Auditoria")
        
        auditoria_gui = AuditoriaGUI(self.content_frame)
        auditoria_gui.mostrar_interfaz_auditoria()

if __name__ == "__main__":
    app = ClinicaMovilGUI()
    app.mainloop()