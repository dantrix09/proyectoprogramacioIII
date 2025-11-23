import customtkinter as ctk
from tkinter import messagebox

class InterfazRoles:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.rol_actual = "Operador"
        
    def mostrar_interfaz_roles(self):
        frame_rol = ctk.CTkFrame(self.parent)
        frame_rol.pack(padx=20, pady=10, fill="x")
        
        ctk.CTkLabel(frame_rol, text="Seleccionar Rol:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=10)
        
        self.combo_rol = ctk.CTkComboBox(frame_rol, 
                                       values=["Operador", "Coordinador", "Administrador"],
                                       command=self.cambiar_rol)
        self.combo_rol.pack(side="left", padx=10)
        self.combo_rol.set(self.rol_actual)
        
        self.frame_funcionalidades = ctk.CTkFrame(self.parent)
        self.frame_funcionalidades.pack(padx=20, pady=10, fill="both", expand=True)
        
        self.mostrar_funcionalidades_rol()
    
    
    def cambiar_rol(self, rol_seleccionado):
        self.rol_actual = rol_seleccionado
        self.mostrar_funcionalidades_rol()
        messagebox.showinfo("Rol Cambiado", f"Ahora está actuando como: {self.rol_actual}")
    
    def mostrar_funcionalidades_rol(self):
        for widget in self.frame_funcionalidades.winfo_children():
            widget.destroy()
        
        if self.rol_actual == "Operador":
            self.mostrar_interfaz_operador()
        elif self.rol_actual == "Coordinador":
            self.mostrar_interfaz_coordinador()
        elif self.rol_actual == "Administrador":
            self.mostrar_interfaz_administrador()
    
    def mostrar_interfaz_operador(self):
        ctk.CTkLabel(self.frame_funcionalidades, 
                    text="OPERADOR DE CLÍNICA MÓVIL - Guardián de la Cadena de Frío",
                    font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        funciones = [
            "Registrar ruta diaria (ubicación, comunidad, distancia)",
            "Monitorear temperatura de equipos cada 2 horas", 
            "Registrar uso de vacunas y medicamentos",
            "Reportar fallas técnicas"
        ]
        
        for funcion in funciones:
            frame_func = ctk.CTkFrame(self.frame_funcionalidades)
            frame_func.pack(padx=20, pady=5, fill="x")
            ctk.CTkLabel(frame_func, text=f"• {funcion}").pack(pady=2)
        
        frame_botones = ctk.CTkFrame(self.frame_funcionalidades)
        frame_botones.pack(pady=20)
        
        ctk.CTkButton(frame_botones, text="Registrar Ruta", 
                     command=self.registrar_ruta).grid(row=0, column=0, padx=5)
        ctk.CTkButton(frame_botones, text="Control Temperatura", 
                     command=self.control_temperatura).grid(row=0, column=1, padx=5)
        ctk.CTkButton(frame_botones, text="Reportar Falla", 
                     command=self.reportar_falla).grid(row=0, column=2, padx=5)
    
    def mostrar_interfaz_coordinador(self):
        ctk.CTkLabel(self.frame_funcionalidades, 
                    text="COORDINADOR LOGÍSTICO - Cerebro Logístico",
                    font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        funciones = [
            "Gestionar inventario de vacunas y medicamentos",
            "Asignar rutas según necesidad y disponibilidad", 
            "Programar mantenimientos de equipos",
            "Generar alertas automáticas"
        ]
        
        for funcion in funciones:
            frame_func = ctk.CTkFrame(self.frame_funcionalidades)
            frame_func.pack(padx=20, pady=5, fill="x")
            ctk.CTkLabel(frame_func, text=f"• {funcion}").pack(pady=2)
        
        frame_botones = ctk.CTkFrame(self.frame_funcionalidades)
        frame_botones.pack(pady=20)
        
        ctk.CTkButton(frame_botones, text="Gestionar Inventario", 
                     command=self.gestionar_inventario).grid(row=0, column=0, padx=5)
        ctk.CTkButton(frame_botones, text="Asignar Rutas", 
                     command=self.asignar_rutas).grid(row=0, column=1, padx=5)
        ctk.CTkButton(frame_botones, text="Programar Mantenimiento", 
                     command=self.programar_mantenimiento).grid(row=0, column=2, padx=5)
    
    def mostrar_interfaz_administrador(self):
        ctk.CTkLabel(self.frame_funcionalidades, 
                    text="ADMINISTRADOR DE SALUD PÚBLICA - Responsable Legal y Técnico",
                    font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        funciones = [
            "Definir políticas de cobertura",
            "Generar reportes de impacto", 
            "Exportar informes para Ministerio de Salud",
            "Auditar todas las acciones del sistema"
        ]
        
        for funcion in funciones:
            frame_func = ctk.CTkFrame(self.frame_funcionalidades)
            frame_func.pack(padx=20, pady=5, fill="x")
            ctk.CTkLabel(frame_func, text=f"• {funcion}").pack(pady=2)
        
        frame_botones = ctk.CTkFrame(self.frame_funcionalidades)
        frame_botones.pack(pady=20)
        
        ctk.CTkButton(frame_botones, text="Generar Reportes", 
                     command=self.generar_reportes).grid(row=0, column=0, padx=5)
        ctk.CTkButton(frame_botones, text="Ver Auditoría", 
                     command=self.ver_auditoria).grid(row=0, column=1, padx=5)
        ctk.CTkButton(frame_botones, text="Políticas Cobertura", 
                     command=self.politicas_cobertura).grid(row=0, column=2, padx=5)
    
    def registrar_ruta(self):
        messagebox.showinfo("Operador", "Función: Registrar ruta diaria")
    
    def control_temperatura(self):
        messagebox.showinfo("Operador", "Función: Control de temperatura de equipos")
    
    def reportar_falla(self):
        messagebox.showinfo("Operador", "Función: Reportar fallas técnicas")
    
    def gestionar_inventario(self):
        messagebox.showinfo("Coordinador", "Función: Gestionar inventario de vacunas")
    
    def asignar_rutas(self):
        messagebox.showinfo("Coordinador", "Función: Asignar rutas automáticamente")
    
    def programar_mantenimiento(self):
        messagebox.showinfo("Coordinador", "Función: Programar mantenimientos")
    
    def generar_reportes(self):
        messagebox.showinfo("Administrador", "Función: Generar reportes de impacto")
    
    def ver_auditoria(self):
        messagebox.showinfo("Administrador", "Función: Ver auditoría del sistema")
    
    def politicas_cobertura(self):
        messagebox.showinfo("Administrador", "Función: Definir políticas de cobertura")