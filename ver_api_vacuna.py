import customtkinter as ctk
from tkinter import ttk, messagebox
import sqlite3

class VerAplicacionesVacunaGUI:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.conn = sqlite3.connect('basededatosclinicas.db')
        self.cursor = self.conn.cursor()

    def mostrar_interfaz_aplicaciones(self):
        self.limpiar_parent()
        
        frame_titulo = ctk.CTkFrame(self.parent)
        frame_titulo.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(frame_titulo, 
                    text="VACUNAS APLICADAS - Historial de Dosis Administradas",
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        frame_controles = ctk.CTkFrame(self.parent)
        frame_controles.pack(fill="x", padx=20, pady=10)
        
        btn_actualizar = ctk.CTkButton(frame_controles, text="Actualizar Lista",
                                     command=self.actualizar_lista)
        btn_actualizar.pack(side="left", padx=10)
        
        btn_exportar = ctk.CTkButton(frame_controles, text="Estadísticas",
                                   command=self.mostrar_estadisticas)
        btn_exportar.pack(side="left", padx=10)
        
        frame_tabla = ctk.CTkFrame(self.parent)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.tree = ttk.Treeview(frame_tabla, 
                               columns=("ID", "Clinica", "Vacuna", "Lote", "Cantidad", "Comunidad", "Paciente", "Responsable", "Fecha"),
                               show="headings", height=20)
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Clinica", text="Clínica")
        self.tree.heading("Vacuna", text="Vacuna")
        self.tree.heading("Lote", text="Lote")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Comunidad", text="Comunidad")
        self.tree.heading("Paciente", text="Paciente")
        self.tree.heading("Responsable", text="Responsable")
        self.tree.heading("Fecha", text="Fecha Aplicación")
        
        self.tree.column("ID", width=50)
        self.tree.column("Clinica", width=120)
        self.tree.column("Vacuna", width=120)
        self.tree.column("Lote", width=100)
        self.tree.column("Cantidad", width=80)
        self.tree.column("Comunidad", width=120)
        self.tree.column("Paciente", width=120)
        self.tree.column("Responsable", width=120)
        self.tree.column("Fecha", width=150)
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.cargar_aplicaciones()

    def cargar_aplicaciones(self):
        """Carga las aplicaciones de vacunas desde la base de datos"""
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            query = """
            SELECT 
                av.id,
                c.nombre as clinica,
                v.tipo as vacuna,
                av.lote,
                av.cantidad,
                av.comunidad,
                av.paciente_identificacion,
                u.nombre_completo as responsable,
                av.fecha_aplicacion
            FROM aplicaciones_vacuna av
            JOIN clinicas c ON av.clinica_id = c.id
            JOIN vacunas v ON av.vacuna_id = v.id
            JOIN usuarios u ON av.responsable_id = u.id
            ORDER BY av.fecha_aplicacion DESC
            """
            
            self.cursor.execute(query)
            aplicaciones = self.cursor.fetchall()
            
            if not aplicaciones:
                frame_vacio = ctk.CTkFrame(self.parent)
                frame_vacio.pack(fill="both", expand=True, padx=20, pady=20)
                ctk.CTkLabel(frame_vacio, text="No hay aplicaciones de vacunas registradas", 
                           font=ctk.CTkFont(size=14)).pack(expand=True)
                return
            
            for aplicacion in aplicaciones:
                self.tree.insert("", "end", values=aplicacion)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar aplicaciones: {str(e)}")

    def actualizar_lista(self):
        """Actualiza la lista de aplicaciones"""
        self.cargar_aplicaciones()
        messagebox.showinfo("Actualizado", "Lista de aplicaciones actualizada")

    def mostrar_estadisticas(self):
        """Muestra estadísticas de las aplicaciones"""
        try:
            query_total = "SELECT COUNT(*) as total, SUM(cantidad) as total_dosis FROM aplicaciones_vacuna"
            self.cursor.execute(query_total)
            totales = self.cursor.fetchone()
            
            query_por_vacuna = """
            SELECT v.tipo, COUNT(*) as aplicaciones, SUM(av.cantidad) as dosis
            FROM aplicaciones_vacuna av
            JOIN vacunas v ON av.vacuna_id = v.id
            GROUP BY v.tipo
            ORDER BY dosis DESC
            """
            self.cursor.execute(query_por_vacuna)
            por_vacuna = self.cursor.fetchall()
            
            query_por_comunidad = """
            SELECT comunidad, COUNT(*) as aplicaciones, SUM(cantidad) as dosis
            FROM aplicaciones_vacuna
            GROUP BY comunidad
            ORDER BY dosis DESC
            LIMIT 10
            """
            self.cursor.execute(query_por_comunidad)
            por_comunidad = self.cursor.fetchall()
            
            self.mostrar_ventana_estadisticas(totales, por_vacuna, por_comunidad)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar estadísticas: {str(e)}")

    def mostrar_ventana_estadisticas(self, totales, por_vacuna, por_comunidad):
        """Muestra una ventana con las estadísticas"""
        ventana = ctk.CTkToplevel(self.parent)
        ventana.title("Estadísticas de Vacunación")
        ventana.geometry("600x500")
        ventana.transient(self.parent)
        ventana.grab_set()
        
        frame_principal = ctk.CTkFrame(ventana)
        frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(frame_principal, text="ESTADÍSTICAS DE VACUNACIÓN",
                   font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        frame_totales = ctk.CTkFrame(frame_principal)
        frame_totales.pack(fill="x", padx=10, pady=10)
        
        total_aplicaciones, total_dosis = totales
        ctk.CTkLabel(frame_totales, text=f"Total de aplicaciones: {total_aplicaciones}",
                   font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        ctk.CTkLabel(frame_totales, text=f"Total de dosis aplicadas: {total_dosis if total_dosis else 0}",
                   font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        
        frame_vacunas = ctk.CTkFrame(frame_principal)
        frame_vacunas.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(frame_vacunas, text="Por Tipo de Vacuna:",
                   font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        
        for vacuna in por_vacuna:
            tipo, aplicaciones, dosis = vacuna
            texto = f"  {tipo}: {aplicaciones} aplicaciones, {dosis} dosis"
            ctk.CTkLabel(frame_vacunas, text=texto).pack(anchor="w")
        
        frame_comunidades = ctk.CTkFrame(frame_principal)
        frame_comunidades.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(frame_comunidades, text="Top 10 Comunidades:",
                   font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        
        for comunidad in por_comunidad:
            nombre, aplicaciones, dosis = comunidad
            texto = f"  {nombre}: {aplicaciones} aplicaciones, {dosis} dosis"
            ctk.CTkLabel(frame_comunidades, text=texto).pack(anchor="w")
        
        btn_cerrar = ctk.CTkButton(frame_principal, text="Cerrar",
                                 command=ventana.destroy)
        btn_cerrar.pack(pady=10)

    def limpiar_parent(self):
        """Limpia el frame padre"""
        for widget in self.parent.winfo_children():
            widget.destroy()