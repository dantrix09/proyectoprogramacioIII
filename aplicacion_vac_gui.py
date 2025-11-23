import customtkinter as ctk
from tkinter import ttk, messagebox
import sqlite3
from proyectoprogramacioniii import insertar_datos_aplicacion_vacuna

class AplicacionVacunaGUI:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.conn = sqlite3.connect('basededatosclinicas.db')
        self.cursor = self.conn.cursor()
        self.usuarios_validos = []

    def mostrar_interfaz_aplicacion_vacuna(self):
        # Limpiar el frame antes de mostrar el formulario
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        frame_titulo = ctk.CTkFrame(self.parent)
        frame_titulo.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(frame_titulo, 
                     text="APLICACIÓN DE VACUNAS - Registro de Dosis Aplicadas",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        frame_form = ctk.CTkFrame(self.parent)
        frame_form.pack(padx=20, pady=10, fill="both", expand=True)
        
        # --- CAMPOS DEL FORMULARIO ---
        
        label_clinica_id = ctk.CTkLabel(frame_form, text="ID de la Clínica:")
        label_clinica_id.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_clinica_id = ctk.CTkEntry(frame_form, width=300)
        self.entry_clinica_id.grid(row=0, column=1, padx=10, pady=10)
        
        label_vacuna_id = ctk.CTkLabel(frame_form, text="ID de la Vacuna:")
        label_vacuna_id.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_vacuna_id = ctk.CTkEntry(frame_form, width=300)
        self.entry_vacuna_id.grid(row=1, column=1, padx=10, pady=10)
        
        label_lote = ctk.CTkLabel(frame_form, text="Lote de la Vacuna:")
        label_lote.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_lote = ctk.CTkEntry(frame_form, width=300)
        self.entry_lote.grid(row=2, column=1, padx=10, pady=10)
        
        label_cantidad = ctk.CTkLabel(frame_form, text="Cantidad Aplicada:")
        label_cantidad.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.entry_cantidad = ctk.CTkEntry(frame_form, width=300)
        self.entry_cantidad.grid(row=3, column=1, padx=10, pady=10)
        
        label_comunidad = ctk.CTkLabel(frame_form, text="Comunidad:")
        label_comunidad.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.entry_comunidad = ctk.CTkEntry(frame_form, width=300)
        self.entry_comunidad.grid(row=4, column=1, padx=10, pady=10)
        
        label_paciente_id = ctk.CTkLabel(frame_form, text="Identificación Paciente:")
        label_paciente_id.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.entry_paciente_id = ctk.CTkEntry(frame_form, width=300)
        self.entry_paciente_id.grid(row=5, column=1, padx=10, pady=10)
        
        # SELECCIÓN DE RESPONSABLE (SOLO MÉDICOS)
        label_responsable_id = ctk.CTkLabel(frame_form, text="Médico Responsable:")
        label_responsable_id.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        
        frame_responsable = ctk.CTkFrame(frame_form)
        frame_responsable.grid(row=6, column=1, padx=10, pady=10, sticky="ew")
        
        self.combo_responsable = ctk.CTkComboBox(frame_responsable, width=220, state="readonly")
        self.combo_responsable.pack(side="left", fill="x", expand=True)
        
        btn_actualizar_responsables = ctk.CTkButton(frame_responsable, text="↻", width=40,
                                                  command=self.cargar_usuarios_validos)
        btn_actualizar_responsables.pack(side="left", padx=5)
        
        label_evidencia = ctk.CTkLabel(frame_form, text="Evidencia o Firma:")
        label_evidencia.grid(row=7, column=0, padx=10, pady=10, sticky="w")
        self.entry_evidencia = ctk.CTkEntry(frame_form, width=300)
        self.entry_evidencia.grid(row=7, column=1, padx=10, pady=10)
        
        # BOTONES
        frame_botones = ctk.CTkFrame(frame_form)
        frame_botones.grid(row=8, column=0, columnspan=2, pady=20)
        
        btn_guardar = ctk.CTkButton(frame_botones, text="Registrar Aplicación", 
                                  command=self.guardar_aplicacion_vacuna,
                                  fg_color="#2E8B57", hover_color="#228B22")
        btn_guardar.pack(side="left", padx=10)
        
        btn_ver_aplicaciones = ctk.CTkButton(frame_botones, text="Ver Aplicaciones",
                                           command=self.ver_aplicaciones_existentes)
        btn_ver_aplicaciones.pack(side="left", padx=10)
        
        # Cargar lista inicial
        self.cargar_usuarios_validos()

    def cargar_usuarios_validos(self):
        try:
            # --- FILTRO ESTRICTO: SOLO MÉDICOS ---
            query = """
            SELECT id, username, nombre_completo, rol 
            FROM usuarios 
            WHERE LOWER(rol) = 'medico' AND activo = 1
            ORDER BY nombre_completo
            """
            
            self.cursor.execute(query)
            usuarios = self.cursor.fetchall()
            self.usuarios_validos = usuarios
            
            if not usuarios:
                self.combo_responsable.configure(values=["No hay médicos disponibles"])
                self.combo_responsable.set("No hay médicos disponibles")
                return
            
            opciones = []
            for usuario in usuarios:
                id_usuario, username, nombre_completo, rol = usuario
                opcion = f"{id_usuario} - {nombre_completo}"
                opciones.append(opcion)
            
            self.combo_responsable.configure(values=opciones)
            if opciones:
                self.combo_responsable.set(opciones[0])
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar médicos: {str(e)}")

    def obtener_id_responsable_seleccionado(self):
        try:
            seleccion = self.combo_responsable.get()
            if seleccion and " - " in seleccion:
                return int(seleccion.split(" - ")[0])
            return None
        except:
            return None

    def guardar_aplicacion_vacuna(self):
        try:
            # Obtener datos
            clinica_id_str = self.entry_clinica_id.get().strip()
            vacuna_id_str = self.entry_vacuna_id.get().strip()
            lote = self.entry_lote.get().strip()
            cantidad_str = self.entry_cantidad.get().strip()
            comunidad = self.entry_comunidad.get().strip()
            paciente_id = self.entry_paciente_id.get().strip()
            evidencia = self.entry_evidencia.get().strip()
            
            responsable_id = self.obtener_id_responsable_seleccionado()
            
            # Validaciones básicas
            if not all([clinica_id_str, vacuna_id_str, lote, cantidad_str, comunidad, paciente_id]):
                messagebox.showerror("Error", "Complete todos los campos obligatorios")
                return
            
            if not responsable_id:
                messagebox.showerror("Error", "Seleccione un médico responsable válido")
                return
            
            # Validar tipos
            try:
                clinica_id = int(clinica_id_str)
                vacuna_id = int(vacuna_id_str)
                cantidad = int(cantidad_str)
                if cantidad <= 0: raise ValueError
            except:
                messagebox.showerror("Error", "IDs y Cantidad deben ser números positivos")
                return
            
            # Validar Clínica
            self.cursor.execute("SELECT id FROM clinicas WHERE id = ?", (clinica_id,))
            if not self.cursor.fetchone():
                messagebox.showerror("Error", f"No existe clínica con ID: {clinica_id}")
                return

            # Validar ROL (Doble seguridad)
            self.cursor.execute("SELECT rol FROM usuarios WHERE id = ?", (responsable_id,))
            user_data = self.cursor.fetchone()
            if not user_data or user_data[0].lower() != 'medico':
                messagebox.showerror("Error", "El responsable seleccionado NO tiene permisos de Médico.")
                return
            
            # Validar Stock Vacuna
            self.cursor.execute("SELECT id, cantidad FROM vacunas WHERE id = ?", (vacuna_id,))
            res_vacuna = self.cursor.fetchone()
            if not res_vacuna:
                messagebox.showerror("Error", f"No existe vacuna con ID: {vacuna_id}")
                return
            
            stock_actual = res_vacuna[1]
            if cantidad > stock_actual:
                messagebox.showerror("Error", f"Stock insuficiente. Disponible: {stock_actual}")
                return
            
            # GUARDAR
            aplicacion_id = insertar_datos_aplicacion_vacuna(
                clinica_id, vacuna_id, lote, cantidad, comunidad, 
                paciente_id, responsable_id, evidencia if evidencia else "S/E"
            )
            
            # Descontar Stock
            self.cursor.execute("UPDATE vacunas SET cantidad = cantidad - ? WHERE id = ?", (cantidad, vacuna_id))
            self.conn.commit()
            
            messagebox.showinfo("Éxito", f"Aplicación registrada (ID: {aplicacion_id}).\nStock actualizado.")
            
            # Limpiar campos
            self.entry_cantidad.delete(0, 'end')
            self.entry_paciente_id.delete(0, 'end')
            self.entry_evidencia.delete(0, 'end')
            
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Error", f"Error crítico: {str(e)}")

    def ver_aplicaciones_existentes(self):
        from ver_api_vacuna import VerAplicacionesVacunaGUI
        vista = VerAplicacionesVacunaGUI(self.parent)
        vista.mostrar_interfaz_aplicaciones()