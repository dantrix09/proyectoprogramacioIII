import customtkinter as ctk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from proyectoprogramacioniii import insertar_datos_mantenimiento

class MantenimientoGUI:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.conn = sqlite3.connect('basededatosclinicas.db')
        self.cursor = self.conn.cursor()
        self.tecnicos_validos = []

    def mostrar_interfaz_registro(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        frame_titulo = ctk.CTkFrame(self.parent)
        frame_titulo.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(frame_titulo, text="GESTIÓN DE MANTENIMIENTOS - Programar Servicio", 
                     font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        frame_form = ctk.CTkFrame(self.parent)
        frame_form.pack(padx=20, pady=10, fill="both", expand=True)
        
        ctk.CTkLabel(frame_form, text="ID del Equipo Médico:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_equipo_id = ctk.CTkEntry(frame_form, width=300)
        self.entry_equipo_id.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame_form, text="Tipo de Mantenimiento:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_tipo = ctk.CTkEntry(frame_form, width=300)
        self.entry_tipo.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame_form, text="Descripción:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_desc = ctk.CTkEntry(frame_form, width=300)
        self.entry_desc.grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame_form, text="Fecha Programada (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.entry_fecha = ctk.CTkEntry(frame_form, width=300)
        self.entry_fecha.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entry_fecha.grid(row=3, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame_form, text="Técnico Encargado:").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        
        frame_tecnico = ctk.CTkFrame(frame_form)
        frame_tecnico.grid(row=4, column=1, padx=10, pady=10, sticky="ew")
        
        self.combo_tecnico = ctk.CTkComboBox(frame_tecnico, width=220, state="readonly")
        self.combo_tecnico.pack(side="left", fill="x", expand=True)
        
        btn_refresh = ctk.CTkButton(frame_tecnico, text="↻", width=40, command=self.cargar_tecnicos)
        btn_refresh.pack(side="left", padx=5)

        frame_botones = ctk.CTkFrame(frame_form)
        frame_botones.grid(row=5, column=0, columnspan=2, pady=20)

        ctk.CTkButton(frame_botones, text="Registrar Mantenimiento", 
                      command=self.guardar_mantenimiento,
                      fg_color="#2E8B57", hover_color="#228B22").pack(side="left", padx=10)
        
        ctk.CTkButton(frame_botones, text="Ver Lista Mantenimientos", 
                      command=self.ver_lista_mantenimientos).pack(side="left", padx=10)

        self.cargar_tecnicos()

    def cargar_tecnicos(self):
        try:
            query = """
            SELECT id, nombre_completo, rol 
            FROM usuarios 
            WHERE LOWER(rol) = 'tecnico' AND activo = 1
            ORDER BY nombre_completo
            """
            self.cursor.execute(query)
            tecnicos = self.cursor.fetchall()
            self.tecnicos_validos = tecnicos
            
            if not tecnicos:
                self.combo_tecnico.set("No hay técnicos registrados")
                self.combo_tecnico.configure(values=[])
            else:
                opciones = [f"{t[0]} - {t[1]}" for t in tecnicos]
                self.combo_tecnico.configure(values=opciones)
                self.combo_tecnico.set(opciones[0])
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar técnicos: {e}")

    def guardar_mantenimiento(self):
        try:
            equipo_str = self.entry_equipo_id.get().strip()
            tipo = self.entry_tipo.get().strip()
            desc = self.entry_desc.get().strip()
            fecha = self.entry_fecha.get().strip()
            tecnico_str = self.combo_tecnico.get()

            if not all([equipo_str, tipo, desc, fecha, tecnico_str]):
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            try:
                equipo_id = int(equipo_str)
                tecnico_id = int(tecnico_str.split(" - ")[0])
            except:
                messagebox.showerror("Error", "Seleccione un técnico válido y asegurese que el ID de equipo sea numérico.")
                return

            self.cursor.execute("SELECT id FROM equipos_medicos WHERE id=?", (equipo_id,))
            if not self.cursor.fetchone():
                messagebox.showerror("Error", f"No existe el equipo médico con ID {equipo_id}")
                return

            id_mant = insertar_datos_mantenimiento(equipo_id, tipo, desc, datetime.strptime(fecha, "%Y-%m-%d").date(), tecnico_id)
            
            messagebox.showinfo("Éxito", f"Mantenimiento programado correctamente.\nID Registro: {id_mant}")
            
            self.entry_desc.delete(0, 'end')
            self.entry_tipo.delete(0, 'end')

        except ValueError:
             messagebox.showerror("Error", "Formato de fecha incorrecto. Use YYYY-MM-DD")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {e}")

    def ver_lista_mantenimientos(self):
        vista = VerMantenimientosGUI(self.parent)
        vista.mostrar_tabla()


class VerMantenimientosGUI:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.conn = sqlite3.connect('basededatosclinicas.db')
        self.cursor = self.conn.cursor()

    def mostrar_tabla(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

        frame_top = ctk.CTkFrame(self.parent)
        frame_top.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(frame_top, text="< Volver a Registro", width=120, 
                      command=lambda: MantenimientoGUI(self.parent).mostrar_interfaz_registro()).pack(side="left", padx=10)
        
        ctk.CTkLabel(frame_top, text="LISTADO DE MANTENIMIENTOS", 
                     font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=20)

        frame_tabla = ctk.CTkFrame(self.parent)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("ID", "Equipo", "Tipo", "Descripción", "Fecha", "Encargado", "Estado")
        tree = ttk.Treeview(frame_tabla, columns=columns, show="headings")
        
        tree.heading("ID", text="ID")
        tree.column("ID", width=30)
        tree.heading("Equipo", text="Equipo (ID)")
        tree.column("Equipo", width=80)
        tree.heading("Tipo", text="Tipo")
        tree.column("Tipo", width=100)
        tree.heading("Descripción", text="Descripción")
        tree.column("Descripción", width=150)
        tree.heading("Fecha", text="Fecha Programada")
        tree.column("Fecha", width=100)
        tree.heading("Encargado", text="Técnico")
        tree.column("Encargado", width=100)
        tree.heading("Estado", text="Estado")
        tree.column("Estado", width=80)

        tree.pack(fill="both", expand=True)

        try:
            query = """
            SELECT m.id, m.equipo_id, m.tipo_mantenimiento, m.descripcion, m.fecha_programada, u.nombre_completo, m.estado
            FROM mantenimientos m
            LEFT JOIN usuarios u ON m.encargado_id = u.id
            ORDER BY m.fecha_programada DESC
            """
            self.cursor.execute(query)
            filas = self.cursor.fetchall()
            
            for fila in filas:
                tree.insert("", "end", values=fila)
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la lista: {e}")