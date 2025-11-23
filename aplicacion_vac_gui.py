import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from proyectoprogramacioniii import insertar_datos_aplicacion_vacuna

class AplicacionVacunaGUI:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.conn = sqlite3.connect('basededatosclinicas.db')
        self.cursor = self.conn.cursor()

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
        self.entry_clinica_id = ctk.CTkEntry(frame_form, width=300, placeholder_text="ID de la clínica donde se aplica")
        self.entry_clinica_id.grid(row=0, column=1, padx=10, pady=10)
        
        label_vacuna_id = ctk.CTkLabel(frame_form, text="ID de la Vacuna:")
        label_vacuna_id.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_vacuna_id = ctk.CTkEntry(frame_form, width=300, placeholder_text="ID de la vacuna aplicada")
        self.entry_vacuna_id.grid(row=1, column=1, padx=10, pady=10)
        
        label_lote = ctk.CTkLabel(frame_form, text="Lote de la Vacuna:")
        label_lote.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_lote = ctk.CTkEntry(frame_form, width=300, placeholder_text="Número de lote de la vacuna")
        self.entry_lote.grid(row=2, column=1, padx=10, pady=10)
        
        label_cantidad = ctk.CTkLabel(frame_form, text="Cantidad Aplicada:")
        label_cantidad.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.entry_cantidad = ctk.CTkEntry(frame_form, width=300, placeholder_text="Número de dosis aplicadas")
        self.entry_cantidad.grid(row=3, column=1, padx=10, pady=10)
        
        label_comunidad = ctk.CTkLabel(frame_form, text="Comunidad:")
        label_comunidad.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.entry_comunidad = ctk.CTkEntry(frame_form, width=300, placeholder_text="Comunidad donde se aplicó")
        self.entry_comunidad.grid(row=4, column=1, padx=10, pady=10)
        
        label_paciente_id = ctk.CTkLabel(frame_form, text="ID del Paciente:")
        label_paciente_id.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.entry_paciente_id = ctk.CTkEntry(frame_form, width=300, placeholder_text="Identificación del paciente")
        self.entry_paciente_id.grid(row=5, column=1, padx=10, pady=10)
        
        label_responsable_id = ctk.CTkLabel(frame_form, text="ID del Responsable:")
        label_responsable_id.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        self.entry_responsable_id = ctk.CTkEntry(frame_form, width=300, placeholder_text="ID del usuario que aplicó")
        self.entry_responsable_id.grid(row=6, column=1, padx=10, pady=10)
        
        label_evidencia = ctk.CTkLabel(frame_form, text="Evidencia o Firma:")
        label_evidencia.grid(row=7, column=0, padx=10, pady=10, sticky="w")
        self.entry_evidencia = ctk.CTkEntry(frame_form, width=300, placeholder_text="Descripción de evidencia o firma")
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
        
        frame_info = ctk.CTkFrame(self.parent)
        frame_info.pack(fill="x", padx=20, pady=10)
        
        info_text = """
        Registre aquí las aplicaciones de vacunas realizadas en las comunidades.
        Asegúrese de verificar la información antes de guardar.
        """
        ctk.CTkLabel(frame_info, text=info_text, justify="left").pack(pady=10)

    def guardar_aplicacion_vacuna(self):
        """Guarda un nuevo registro de aplicación de vacuna"""
        try:
            clinica_id_str = self.entry_clinica_id.get().strip()
            vacuna_id_str = self.entry_vacuna_id.get().strip()
            lote = self.entry_lote.get().strip()
            cantidad_str = self.entry_cantidad.get().strip()
            comunidad = self.entry_comunidad.get().strip()
            paciente_id = self.entry_paciente_id.get().strip()
            responsable_id_str = self.entry_responsable_id.get().strip()
            evidencia = self.entry_evidencia.get().strip()
            
            if not clinica_id_str:
                messagebox.showerror("Error", "El ID de la clínica es obligatorio")
                return
                
            if not vacuna_id_str:
                messagebox.showerror("Error", "El ID de la vacuna es obligatorio")
                return
                
            if not lote:
                messagebox.showerror("Error", "El lote de la vacuna es obligatorio")
                return
                
            if not cantidad_str:
                messagebox.showerror("Error", "La cantidad aplicada es obligatoria")
                return
                
            if not comunidad:
                messagebox.showerror("Error", "La comunidad es obligatoria")
                return
                
            if not paciente_id:
                messagebox.showerror("Error", "El ID del paciente es obligatorio")
                return
                
            if not responsable_id_str:
                messagebox.showerror("Error", "El ID del responsable es obligatorio")
                return
            
            try:
                clinica_id = int(clinica_id_str)
                vacuna_id = int(vacuna_id_str)
                cantidad = int(cantidad_str)
                responsable_id = int(responsable_id_str)
            except ValueError:
                messagebox.showerror("Error", "Los IDs y cantidad deben ser números válidos")
                return
            
            self.cursor.execute("SELECT id FROM clinicas WHERE id = ?", (clinica_id,))
            if not self.cursor.fetchone():
                messagebox.showerror("Error", f"No existe una clínica con ID: {clinica_id}")
                return
        
            self.cursor.execute("SELECT id FROM vacunas WHERE id = ?", (vacuna_id,))
            if not self.cursor.fetchone():
                messagebox.showerror("Error", f"No existe una vacuna con ID: {vacuna_id}")
                return
            
            self.cursor.execute("SELECT id FROM usuarios WHERE id = ?", (responsable_id,))
            if not self.cursor.fetchone():
                messagebox.showerror("Error", f"No existe un usuario con ID: {responsable_id}")
                return
            
            self.cursor.execute("SELECT cantidad FROM vacunas WHERE id = ?", (vacuna_id,))
            resultado = self.cursor.fetchone()
            if resultado:
                stock_actual = resultado[0]
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
            
            messagebox.showinfo("Éxito", f"Aplicación de vacuna registrada correctamente\nID: {aplicacion_id}\nStock actualizado")
            self.limpiar_formulario()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar aplicación de vacuna: {str(e)}")

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.entry_clinica_id.delete(0, 'end')
        self.entry_vacuna_id.delete(0, 'end')
        self.entry_lote.delete(0, 'end')
        self.entry_cantidad.delete(0, 'end')
        self.entry_comunidad.delete(0, 'end')
        self.entry_paciente_id.delete(0, 'end')
        self.entry_responsable_id.delete(0, 'end')
        self.entry_evidencia.delete(0, 'end')

    def limpiar_parent(self):
        """Limpia el frame padre"""
        for widget in self.parent.winfo_children():
            widget.destroy()