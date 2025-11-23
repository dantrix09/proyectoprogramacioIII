import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import random

class ControlTemperatura:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.conn = sqlite3.connect('basededatosclinicas.db')
        self.cursor = self.conn.cursor()
        self.alertas_activas = {}

    def limpiar_parent(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

    def mostrar_interfaz_temperatura(self):
        self.limpiar_parent()
        
        # Título
        frame_titulo = ctk.CTkFrame(self.parent)
        frame_titulo.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(frame_titulo, 
                    text="CONTROL DE CADENA DE FRÍO - Monitoreo en Tiempo Real",
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        # BOTÓN REDONDO DE CHEQUEO RÁPIDO
        frame_chequeo = ctk.CTkFrame(self.parent)
        frame_chequeo.pack(fill="x", padx=20, pady=15)
        
        btn_chequeo = ctk.CTkButton(
            frame_chequeo, 
            text="CHEQUEO\nRÁPIDO", 
            command=self.chequeo_rapido_temperatura,
            fg_color="#2b5b84", 
            hover_color="#1e4160",
            width=80,
            height=80,
            corner_radius=40,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        btn_chequeo.pack(pady=10)
        
        # Botones de control
        frame_controles = ctk.CTkFrame(self.parent)
        frame_controles.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(frame_controles, text="Simular Lectura de Temperatura",
                     command=self.simular_lectura_temperatura).pack(side="left", padx=5)
        
        ctk.CTkButton(frame_controles, text="Verificar Estado Actual",
                     command=self.verificar_estado_actual).pack(side="left", padx=5)
        
        ctk.CTkButton(frame_controles, text="Revisar Alertas de Temperatura",
                     command=self.revisar_alertas_temperatura).pack(side="left", padx=5)
        
        # Frame para el historial
        self.frame_estado = ctk.CTkFrame(self.parent)
        self.frame_estado.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.mostrar_estado_actual()

    def mostrar_estado_actual(self):
        try:
            for widget in self.frame_estado.winfo_children():
                widget.destroy()
                
            query = """
            SELECT c.nombre, e.numero_serie, rt.temperatura, rt.fecha_registro
            FROM registros_temperatura rt
            JOIN clinicas c ON rt.clinica_id = c.id
            JOIN equipos_medicos e ON rt.equipo_id = e.id
            ORDER BY rt.fecha_registro DESC LIMIT 10
            """
            self.cursor.execute(query)
            lecturas = self.cursor.fetchall()
            
            if not lecturas:
                ctk.CTkLabel(self.frame_estado, text="No hay lecturas de temperatura disponibles").pack(pady=20)
                return
            
            ctk.CTkLabel(self.frame_estado, text="ÚLTIMAS LECTURAS DE TEMPERATURA", 
                        font=ctk.CTkFont(weight="bold")).pack(pady=10)
            
            for lectura in lecturas:
                nombre, serie, temp, fecha = lectura
                color = "red" if temp < 2 or temp > 8 else "green"
                
                frame_lectura = ctk.CTkFrame(self.frame_estado)
                frame_lectura.pack(fill="x", padx=10, pady=2)
                
                texto = f"{nombre} - {serie}: {temp}°C - {fecha}"
                ctk.CTkLabel(frame_lectura, text=texto, text_color=color).pack(pady=5)
                
        except Exception as e:
            ctk.CTkLabel(self.frame_estado, text=f"Error al cargar estado: {str(e)}").pack(pady=20)

    def chequeo_rapido_temperatura(self):
        try:
            query = """
            SELECT c.nombre, e.numero_serie, rt.temperatura, rt.fecha_registro
            FROM registros_temperatura rt
            JOIN clinicas c ON rt.clinica_id = c.id
            JOIN equipos_medicos e ON rt.equipo_id = e.id
            WHERE rt.fecha_registro >= datetime('now', '-2 hours')
            ORDER BY rt.fecha_registro DESC
            """
            self.cursor.execute(query)
            lecturas = self.cursor.fetchall()
            
            if not lecturas:
                messagebox.showinfo("Chequeo Rápido", "No hay lecturas recientes de temperatura")
                return
            
            equipos_criticos = {}
            
            for lectura in lecturas:
                nombre, serie, temp, fecha_str = lectura
                clave = f"{nombre}_{serie}"
                
                fecha_lectura = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S')
                tiempo_transcurrido = (datetime.now() - fecha_lectura).total_seconds() / 60
                
                if temp < 2 or temp > 8:
                    if clave not in equipos_criticos:
                        equipos_criticos[clave] = {
                            'nombre': nombre,
                            'serie': serie,
                            'temperatura': temp,
                            'tiempo_fuera_rango': tiempo_transcurrido,
                            'fecha_lectura': fecha_str
                        }
            
            if equipos_criticos:
                reporte = "EQUIPOS CON TEMPERATURA FUERA DE RANGO:\n\n"
                alertas_rojas = 0
                
                for equipo in equipos_criticos.values():
                    tiempo = equipo['tiempo_fuera_rango']
                    estado_alerta = "ALERTA ROJA" if tiempo >= 15 else f"Advertencia ({tiempo:.1f} min)"
                    
                    if tiempo >= 15:
                        alertas_rojas += 1
                    
                    reporte += f"• {equipo['nombre']} - {equipo['serie']}\n"
                    reporte += f"  Temperatura: {equipo['temperatura']}°C\n"
                    reporte += f"  Estado: {estado_alerta}\n\n"
                
                if alertas_rojas > 0:
                    messagebox.showwarning("Chequeo Rápido - ALERTA", reporte)
                else:
                    messagebox.showwarning("Chequeo Rápido - Advertencia", reporte)
            else:
                messagebox.showinfo("Chequeo Rápido", "Todos los equipos están en rango normal")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error en chequeo rápido: {str(e)}")

    def simular_lectura_temperatura(self):
        try:
            self.cursor.execute("SELECT id, clinica_id FROM equipos_medicos ORDER BY RANDOM() LIMIT 1")
            equipo = self.cursor.fetchone()
            
            if not equipo:
                messagebox.showerror("Error", "No hay equipos médicos registrados")
                return
                
            equipo_id, clinica_id = equipo
            temperatura = round(random.uniform(0, 10), 1)
            
            query = """
            INSERT INTO registros_temperatura (clinica_id, equipo_id, temperatura, latitud, longitud, fuente)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(query, (clinica_id, equipo_id, temperatura, 0.0, 0.0, "simulacion"))
            self.conn.commit()
            
            messagebox.showinfo("Simulación", f"Lectura simulada: {temperatura}°C")
            self.mostrar_estado_actual()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en simulación: {str(e)}")

    def verificar_estado_actual(self):
        self.mostrar_estado_actual()

    def revisar_alertas_temperatura(self):
        try:
            query = """
            SELECT tipo, mensaje, severidad FROM alertas 
            WHERE leida = 0 AND tipo LIKE '%temperatura%'
            ORDER BY fecha_creacion DESC
            """
            self.cursor.execute(query)
            alertas = self.cursor.fetchall()
            
            if not alertas:
                messagebox.showinfo("Alertas", "No hay alertas de temperatura activas")
                return
            
            reporte = "ALERTAS DE TEMPERATURA ACTIVAS:\n\n"
            for alerta in alertas:
                tipo, mensaje, severidad = alerta
                reporte += f"• {tipo}: {mensaje} ({severidad})\n"
            
            messagebox.showwarning("Alertas Activas", reporte)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al revisar alertas: {str(e)}")