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
        self.limpiar_parent()
        
        frame_titulo = ctk.CTkFrame(self.parent)
        frame_titulo.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(frame_titulo, 
                    text="APLICACIÓN DE VACUNAS - Registro de Dosis Aplicadas",
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        frame_form = ctk.CTkFrame(self.parent)
        frame_form.pack(padx=20, pady=10, fill="both", expand=True)
        
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
        
        label_paciente_id = ctk.CTkLabel(frame_form, text="ID del Paciente:")
        label_paciente_id.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.entry_paciente_id = ctk.CTkEntry(frame_form, width=300)
        self.entry_paciente_id.grid(row=5, column=1, padx=10, pady=10)
        
        label_responsable_id = ctk.CTkLabel(frame_form, text="Responsable:")
        label_responsable_id.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        
        frame_responsable = ctk.CTkFrame(frame_form)
        frame_responsable.grid(row=6, column=1, padx=10, pady=10, sticky="ew")
        frame_responsable.grid_columnconfigure(0, weight=1)
        
        self.combo_responsable = ctk.CTkComboBox(frame_responsable, 
                                               width=300,
                                               state="readonly")
        self.combo_responsable.grid(row=0, column=0, sticky="ew")
        
        btn_actualizar_responsables = ctk.CTkButton(frame_responsable, 
                                                  text="Actualizar",
                                                  width=80,
                                                  command=self.cargar_usuarios_validos)
        btn_actualizar_responsables.grid(row=0, column=1, padx=(10, 0))
        
        label_evidencia = ctk.CTkLabel(frame_form, text="Evidencia o Firma:")
        label_evidencia.grid(row=7, column=0, padx=10, pady=10, sticky="w")
        self.entry_evidencia = ctk.CTkEntry(frame_form, width=300)
        self.entry_evidencia.grid(row=7, column=1, padx=10, pady=10)
        
        frame_botones = ctk.CTkFrame(frame_form)
        frame_botones.grid(row=8, column=0, columnspan=2, pady=20)
        
        btn_guardar = ctk.CTkButton(frame_botones, text="Registrar Aplicación", 
                                  command=self.guardar_aplicacion_vacuna,
                                  fg_color="#2E8B57", hover_color="#228B22")
        btn_guardar.pack(side="left", padx=10)
        
        btn_limpiar = ctk.CTkButton(frame_botones, text="Limpiar Formulario",
                                  command=self.limpiar_formulario)
        btn_limpiar.pack(side="left", padx=10)
        
        btn_ver_aplicaciones = ctk.CTkButton(frame_botones, text="Ver Aplicaciones",
                                          command=self.ver_aplicaciones_existentes)
        btn_ver_aplicaciones.pack(side="left", padx=10)
        
        self.cargar_usuarios_validos()

    def cargar_usuarios_validos(self):
        try:
            query = """
            SELECT id, username, nombre_completo, rol 
            FROM usuarios 
            WHERE rol IN ('medico', 'admin') AND activo = 1
            ORDER BY nombre_completo
            """
            
            self.cursor.execute(query)
            usuarios = self.cursor.fetchall()
            
            self.usuarios_validos = usuarios
            
            if not usuarios:
                self.combo_responsable.configure(values=["No hay usuarios disponibles"])
                self.combo_responsable.set("No hay usuarios disponibles")
                return
            
            opciones = []
            for usuario in usuarios:
                id_usuario, username, nombre_completo, rol = usuario
                opcion = f"{id_usuario} - {nombre_completo} ({rol})"
                opciones.append(opcion)
            
            self.combo_responsable.configure(values=opciones)
            
            if opciones:
                self.combo_responsable.set(opciones[0])
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar usuarios: {str(e)}")

    def obtener_id_responsable_seleccionado(self):
        try:
            seleccion = self.combo_responsable.get()
            if seleccion and " - " in seleccion:
                id_responsable = int(seleccion.split(" - ")[0])
                return id_responsable
            return None
        except (ValueError, IndexError):
            return None

    def guardar_aplicacion_vacuna(self):
        try:
            clinica_id_str = self.entry_clinica_id.get().strip()
            vacuna_id_str = self.entry_vacuna_id.get().strip()
            lote = self.entry_lote.get().strip()
            cantidad_str = self.entry_cantidad.get().strip()
            comunidad = self.entry_comunidad.get().strip()
            paciente_id = self.entry_paciente_id.get().strip()
            evidencia = self.entry_evidencia.get().strip()
            
            responsable_id = self.obtener_id_responsable_seleccionado()
            
            if not all([clinica_id_str, vacuna_id_str, lote, cantidad_str, comunidad, paciente_id]):
                messagebox.showerror("Error", "Complete todos los campos obligatorios")
                return
            
            if not responsable_id:
                messagebox.showerror("Error", "Seleccione un responsable válido")
                return
            
            try:
                clinica_id = int(clinica_id_str)
                vacuna_id = int(vacuna_id_str)
                cantidad = int(cantidad_str)
            except ValueError:
                messagebox.showerror("Error", "Los IDs y cantidad deben ser números válidos")
                return
            
            self.cursor.execute("SELECT id FROM clinicas WHERE id = ?", (clinica_id,))
            if not self.cursor.fetchone():
                messagebox.showerror("Error", f"No existe una clínica con ID: {clinica_id}")
                return
            
            self.cursor.execute("SELECT id, cantidad FROM vacunas WHERE id = ?", (vacuna_id,))
            resultado_vacuna = self.cursor.fetchone()
            if not resultado_vacuna:
                messagebox.showerror("Error", f"No existe una vacuna con ID: {vacuna_id}")
                return
            
            stock_actual = resultado_vacuna[1]
            if cantidad > stock_actual:
                messagebox.showerror("Error", f"No hay suficiente stock. Stock actual: {stock_actual}, Cantidad solicitada: {cantidad}")
                return
            
            aplicacion_id = insertar_datos_aplicacion_vacuna(
                clinica_id, 
                vacuna_id, 
                lote, 
                cantidad, 
                comunidad, 
                paciente_id, 
                responsable_id, 
                evidencia if evidencia else "Registrado en sistema"
            )
            
            self.cursor.execute("UPDATE vacunas SET cantidad = cantidad - ? WHERE id = ?", (cantidad, vacuna_id))
            self.conn.commit()
            
            messagebox.showinfo("Éxito", f"Aplicación de vacuna registrada correctamente\nID: {aplicacion_id}\nStock actualizado: {stock_actual - cantidad}")
            self.limpiar_formulario()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar aplicación de vacuna: {str(e)}")

    def ver_aplicaciones_existentes(self):
        from ver_api_vacuna import VerAplicacionesVacunaGUI
        self.limpiar_parent()
        aplicaciones_gui = VerAplicacionesVacunaGUI(self.parent)
        aplicaciones_gui.mostrar_interfaz_aplicaciones()

    def limpiar_formulario(self):
        self.entry_clinica_id.delete(0, 'end')
        self.entry_vacuna_id.delete(0, 'end')
        self.entry_lote.delete(0, 'end')
        self.entry_cantidad.delete(0, 'end')
        self.entry_comunidad.delete(0, 'end')
        self.entry_paciente_id.delete(0, 'end')
        self.entry_evidencia.delete(0, 'end')
        
        if self.usuarios_validos:
            opciones = [f"{usuario[0]} - {usuario[2]} ({usuario[3]})" for usuario in self.usuarios_validos]
            if opciones:
                self.combo_responsable.set(opciones[0])

    def limpiar_parent(self):
        for widget in self.parent.winfo_children():
            widget.destroy()