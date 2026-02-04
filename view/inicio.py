import tkinter as tk
from tkinter import ttk, messagebox
from detector import iniciarDeteccion
from configuraciones.parametros import *

class appDetectarCaida:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Detección de Caídas")
        self.root.geometry("500x1100")
        self.root.configure(bg="#f0f0f0")
        
        # Centrar la ventana de la interfaz gráfica
        width = 500
        height = 1100
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Configuración de estilo
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12), background="#f0f0f0")
        style.configure("TEntry", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 12), padding=5)

        # Frame para los parámetros
        self.parametros_frame = ttk.LabelFrame(root, text="Parámetros de Detección", padding=(20, 10))
        self.parametros_frame.pack(padx=10, pady=10, fill="x")

        # Campos para los parámetros
        self.crearCamposParametros()

        # Botones
        self.boton_iniciar = ttk.Button(root, text="Iniciar Detección", command=self.comenzarDeteccion)
        self.boton_salir = ttk.Button(root, text="Salir", command=self.confirmarExit)

        # Posicionamiento de los botones
        self.boton_iniciar.pack(pady=10)
        self.boton_salir.pack(pady=10)

        # Lista para los números de destinatarios
        self.lista_numeros = []

    def crearCamposParametros(self):
        """Crea los campos de entrada para los parámetros."""
        self.umbral_caida_entry = self.crearEntradaEtiqueta("Umbral de caída:", fall_threshold)
        self.umbral_lento_entry = self.crearEntradaEtiqueta("Umbral de velocidad lenta:", slow_motion_threshold)
        self.umbral_torso_entry = self.crearEntradaEtiqueta("Umbral de inclinación de torso:", torso_inclination_threshold)
        self.umbral_pierna_entry = self.crearEntradaEtiqueta("Umbral de ángulo de pierna:", leg_angle_threshold)
        self.sala_entry = self.crearEntradaEtiqueta("Sala:", sala)
        self.email_entry = self.crearEntradaEtiqueta("Email destinatario:", destinatario_email)
        self.crearCampoNumeros(lista_numeros)  # Campo para múltiples números

    def crearEntradaEtiqueta(self, label_text, default_value):
        """Crea un widget de entrada etiquetado."""
        label = ttk.Label(self.parametros_frame, text=label_text)
        entry = ttk.Entry(self.parametros_frame)
        entry.insert(0, default_value)  # Valor predeterminado
        label.pack(fill='x', pady=5)
        entry.pack(fill='x', pady=5)
        return entry

    def crearCampoNumeros(self, default_value):
        """Crea el campo de entrada para agregar y eliminar múltiples números."""
        # Etiqueta
        label = ttk.Label(self.parametros_frame, text="Número destinatario:")
        label.pack(fill='x', pady=5)
        
        # Entrada para el número
        self.num_entry = ttk.Entry(self.parametros_frame)
        self.num_entry.insert(0, default_value)  # Valor predeterminado
        self.num_entry.pack(fill='x', pady=5)

        # Frame para los botones "Agregar" y "Eliminar"
        botones_frame = ttk.Frame(self.parametros_frame)
        botones_frame.pack(fill='x', pady=5)

        # Botón para agregar el número
        boton_agregar_numero = ttk.Button(botones_frame, text="Agregar número", command=self.agregarNumero)
        boton_agregar_numero.pack(side=tk.LEFT, padx=5)

        # Botón para eliminar el número (inicialmente oculto)
        self.boton_eliminar_numero = ttk.Button(botones_frame, text="Eliminar número", command=self.eliminarNumero)
        self.boton_eliminar_numero.pack(side=tk.LEFT, padx=5)
        self.boton_eliminar_numero.pack_forget()  # Oculta el botón inicialmente

        # Listbox para mostrar los números agregados
        self.lista_numeros_box = tk.Listbox(self.parametros_frame, height=5)
        self.lista_numeros_box.pack(fill='x', pady=5)

        # Detectar cuando se selecciona un número
        self.lista_numeros_box.bind("<<ListboxSelect>>", self.mostrarBotonEliminar)

    def mostrarBotonEliminar(self, event):
        """Muestra el botón de eliminar solo cuando hay un número seleccionado."""
        if self.lista_numeros_box.curselection():
            # Mostrar el botón cuando hay un elemento seleccionado
            self.boton_eliminar_numero.pack(side=tk.LEFT, padx=5)
        else:
            # Ocultar el botón si no hay selección
            self.boton_eliminar_numero.pack_forget()

    def eliminarNumero(self):
        """Elimina el número seleccionado de la lista."""
        seleccionado = self.lista_numeros_box.curselection()  # Obtiene la selección del Listbox
        if seleccionado:
            indice = seleccionado[0]  # El índice de la selección
            self.lista_numeros.pop(indice)  # Elimina de la lista interna
            self.lista_numeros_box.delete(indice)  # Elimina del Listbox
            self.boton_eliminar_numero.pack_forget()  # Oculta el botón después de eliminar

    def agregarNumero(self):
        """Agrega el número ingresado a la lista de números."""
        numero = self.num_entry.get().strip()
        if numero:
            self.lista_numeros.append(numero)
            self.lista_numeros_box.insert(tk.END, numero)  # Muestra el número en el Listbox
            self.num_entry.delete(0, tk.END)  # Limpia el campo de entrada

    def comenzarDeteccion(self):
        """Actualiza los parámetros y comienza la detección."""
        if self.validarInputs():
            self.actualizarParametros()
            iniciarDeteccion()

    def validarInputs(self):
        """Valida la entrada del usuario antes de iniciar la detección."""
        try:
            int(self.umbral_caida_entry.get())
            float(self.umbral_lento_entry.get())
            int(self.umbral_torso_entry.get())
            int(self.umbral_pierna_entry.get())
            if not self.lista_numeros:
                raise ValueError("Debe agregar al menos un número de destinatario.")
            return True
        except ValueError as e:
            messagebox.showerror("Error de entrada", str(e))
            return False

    def confirmarExit(self):
        """Confirma la acción de salir."""
        self.root.quit()

    def actualizarParametros(self):
        """Actualiza los parámetros según la entrada del usuario."""
        actualizarParametros(
            int(self.umbral_caida_entry.get()),
            float(self.umbral_lento_entry.get()),
            int(self.umbral_torso_entry.get()),
            int(self.umbral_pierna_entry.get()),
            self.email_entry.get(),
            self.sala_entry.get(),
            self.lista_numeros  # Envía la lista de números
        )

def inicioInterfaz():
    root = tk.Tk()
    app = appDetectarCaida(root)
    root.mainloop()
