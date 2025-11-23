import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from proyectoprogramacioniii import insertar_datos_auditoria

class AuditoriaGUI:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.conn = sqlite3.connect('basededatosclinicas.db')
        self.cursor = self.conn.cursor()

    def mostrar_interfaz_auditoria(self):
        self.limpiar_parent()
        
        frame_titulo = ctk.CTkFrame(self.parent)
        frame_titulo.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(frame_titulo, 
                    text="REGISTRO DE AUDITORÍA - Sistema de Trazabilidad",
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        frame_form = ctk.CTkFrame(self.parent)
        frame_form.pack(padx=20, pady=10, fill="both", expand=True)
        
        label_tabla = ctk.CTkLabel(frame_form, text="Tabla Afectada:")
        label_tabla.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_tabla = ctk.CTkEntry(frame_form, width=300, placeholder_text="Ej: clinicas, vacunas, equipos_medicos")
        self.entry_tabla.grid(row=0, column=1, padx=10, pady=10)
        
        label_registro_id = ctk.CTkLabel(frame_form, text="ID del Registro:")
        label_registro_id.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_registro_id = ctk.CTkEntry(frame_form, width=300, placeholder_text="Número del registro afectado")
        self.entry_registro_id.grid(row=1, column=1, padx=10, pady=10)
        
        label_accion = ctk.CTkLabel(frame_form, text="Acción:")
        label_accion.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.combo_accion = ctk.CTkComboBox(frame_form, 
                                     values=["INSERT", "UPDATE", "DELETE"],
                                     width=300)
        self.combo_accion.grid(row=2, column=1, padx=10, pady=10)
        self.combo_accion.set("INSERT")
        
        label_usuario_id = ctk.CTkLabel(frame_form, text="ID del Usuario:")
        label_usuario_id.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.entry_usuario_id = ctk.CTkEntry(frame_form, width=300, placeholder_text="ID del usuario que realizó la acción")
        self.entry_usuario_id.grid(row=3, column=1, padx=10, pady=10)
        
        label_valores_anteriores = ctk.CTkLabel(frame_form, text="Valores Anteriores:")
        label_valores_anteriores.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.entry_valores_anteriores = ctk.CTkEntry(frame_form, width=300, placeholder_text="Valores antes del cambio (JSON o texto)")
        self.entry_valores_anteriores.grid(row=4, column=1, padx=10, pady=10)
        
        label_valores_nuevos = ctk.CTkLabel(frame_form, text="Valores Nuevos:")
        label_valores_nuevos.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.entry_valores_nuevos = ctk.CTkEntry(frame_form, width=300, placeholder_text="Valores después del cambio (JSON o texto)")
        self.entry_valores_nuevos.grid(row=5, column=1, padx=10, pady=10)
        
        # Botones
        frame_botones = ctk.CTkFrame(frame_form)
        frame_botones.grid(row=6, column=0, columnspan=2, pady=20)
        
        btn_guardar = ctk.CTkButton(frame_botones, text="Registrar Auditoría", 
                                  command=self.guardar_auditoria,
                                  fg_color="#8B4513", hover_color="#A0522D")
        btn_guardar.pack(side="left", padx=10)
        
        btn_limpiar = ctk.CTkButton(frame_botones, text="Limpiar Formulario",
                                  command=self.limpiar_formulario)
        btn_limpiar.pack(side="left", padx=10)
        
        # Información de ayuda
        frame_info = ctk.CTkFrame(self.parent)
        frame_info.pack(fill="x", padx=20, pady=10)
        
        info_text = """
        Registre aquí todas las acciones importantes del sistema para mantener la trazabilidad.
        Ejemplo: Cambios en clínicas, modificaciones de inventario, actualizaciones de equipos.
        """
        ctk.CTkLabel(frame_info, text=info_text, justify="left").pack(pady=10)

    def guardar_auditoria(self):
        """Guarda un nuevo registro de auditoría"""
        try:
            tabla_afectada = self.entry_tabla.get().strip()
            registro_id_str = self.entry_registro_id.get().strip()
            accion = self.combo_accion.get()
            usuario_id_str = self.entry_usuario_id.get().strip()
            valores_anteriores = self.entry_valores_anteriores.get().strip()
            valores_nuevos = self.entry_valores_nuevos.get().strip()
            
            # Validaciones
            if not tabla_afectada:
                messagebox.showerror("Error", "La tabla afectada es obligatoria")
                return
                
            if not registro_id_str:
                messagebox.showerror("Error", "El ID del registro es obligatorio")
                return
                
            if not usuario_id_str:
                messagebox.showerror("Error", "El ID del usuario es obligatorio")
                return
            
            # Convertir IDs a enteros
            try:
                registro_id = int(registro_id_str)
                usuario_id = int(usuario_id_str)
            except ValueError:
                messagebox.showerror("Error", "Los IDs deben ser números válidos")
                return
            
            # Verificar que el usuario existe
            self.cursor.execute("SELECT id FROM usuarios WHERE id = ?", (usuario_id,))
            if not self.cursor.fetchone():
                messagebox.showerror("Error", f"No existe un usuario con ID: {usuario_id}")
                return
            
            # Insertar auditoría
            auditoria_id = insertar_datos_auditoria(
                tabla_afectada, 
                registro_id, 
                accion, 
                usuario_id, 
                valores_anteriores if valores_anteriores else "N/A", 
                valores_nuevos if valores_nuevos else "N/A"
            )
            
            messagebox.showinfo("Éxito", f"Auditoría registrada correctamente\nID: {auditoria_id}")
            self.limpiar_formulario()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar auditoría: {str(e)}")

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.entry_tabla.delete(0, 'end')
        self.entry_registro_id.delete(0, 'end')
        self.combo_accion.set("INSERT")
        self.entry_usuario_id.delete(0, 'end')
        self.entry_valores_anteriores.delete(0, 'end')
        self.entry_valores_nuevos.delete(0, 'end')

    def limpiar_parent(self):
        """Limpia el frame padre"""
        for widget in self.parent.winfo_children():
            widget.destroy()