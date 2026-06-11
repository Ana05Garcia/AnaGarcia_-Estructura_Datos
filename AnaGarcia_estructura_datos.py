import tkinter as tk
from tkinter import messagebox
from datetime import datetime


class Tarea:

    def __init__(self, titulo, descripcion, estado, fecha):

        self.__titulo = titulo
        self.__descripcion = descripcion
        self.__estado = estado
        self.__fecha = fecha

        self.tipo = "normal"

    def mostrar(self):

        return f"{self.titulo()} - {self.estado()}"

    def __str__(self): # Método especial que convierte el objeto en texto

        return self.mostrar()

    # Métodos para poder mostrar lo encapsulado

    def titulo(self):

        return self.__titulo

    def descripcion(self):

        return self.__descripcion

    def estado(self):

        return self.__estado

    def fecha(self):

        return self.__fecha

    def completar(self):

        self.__estado = "completada"


class TareaUrgente(Tarea):

    def __init__(self, titulo, descripcion, estado, fecha):

        super().__init__(titulo, descripcion, estado, fecha)

        self.tipo = "urgente"

    def mostrar(self):

        return f"Urgente ⚠️ {self.titulo()} - {self.estado()}"


class GestorTareas:

    def __init__(self):
              
        self.lista_tareas = [] # lista donde se guardan las tareas

        self.cargar_tareas() # carga  las tareas guardadas en el archivo

    def agregar_tarea(self, tarea):


        archivo = open("tareas.txt", "a") # abre el archivo en modo agregar

        texto = (tarea.tipo + "/" + tarea.titulo() + "/" + tarea.descripcion() + "/" + tarea.estado() + "/" + tarea.fecha() + "\n")
        archivo.write(texto)

        archivo.close()

    def guardar_tareas(self):

        archivo = open("tareas.txt", "w") 

        for tarea in self.lista_tareas: # Recorre todas las tareas

            # convierte cada tarea en texto
            texto = ( tarea.tipo + "/" + tarea.titulo() + "/" +tarea.descripcion() + "/" +tarea.estado() + "/" + tarea.fecha() + "\n")

            archivo.write(texto)

        archivo.close()

    def cargar_tareas(self):

        try:

            archivo = open("tareas.txt", "r")

            lineas = archivo.readlines() # readlines---> una funcion que Lee todas las líneas del archivo

            for linea in lineas: # recorre cada línea

                linea = linea.replace("\n", "") # elimina el salto de línea

                datos = [] #lista donde se guardan los datos

                palabra = "" #variable para formar palabras

                for letra in linea: #Recorre letra por letra

                    if letra != "/": 

                        palabra = palabra + letra # Va formando la palabra
 
                    else:

                        datos.append(palabra)# Guarda la última palabra formada

                        palabra = ""

                datos.append(palabra)

                
                # se guarda cada dato en variables segun su posicion
                tipo = datos[0]
                titulo = datos[1]
                descripcion = datos[2]
                estado = datos[3]
                fecha = datos[4]

                if tipo == "urgente":

                    tarea = TareaUrgente(titulo,descripcion,estado,fecha)

                else:
                    tarea = Tarea(titulo, descripcion, estado, fecha)

                  

                self.lista_tareas.append(tarea)

            archivo.close()

        except:

            pass

    def eliminar_tarea(self, ubicacion):

        del self.lista_tareas[ubicacion] # Elimina la tarea de la posición indicada

        self.guardar_tareas()


gestor = GestorTareas() #se crea el objeto


# FUNCIONES

def actualizar_lista(): # Función para actualizar el Listbox

    lista.delete(0, tk.END) # Borra todos los elementos de la lista 
    posicion = 0

    for tarea in gestor.lista_tareas: # Recorre todas las tareas

        lista.insert(posicion, tarea.mostrar()) # Inserta la tarea en el listbox

        posicion = posicion + 1 # Aumenta la posición


def agregar_tarea():

    titulo = entry_tarea.get()

    descripcion = descripcion_tarea.get()

    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if titulo == "" or descripcion == "":

        messagebox.showerror("Error","Completa todos los campos")

        return

    elif check_urgente.get() == 1:

        tarea = TareaUrgente(titulo,descripcion,"pendiente",fecha_actual)

    else:

        tarea = Tarea(titulo,descripcion, "pendiente", fecha_actual)

    gestor.agregar_tarea(tarea)

    actualizar_lista()

    entry_tarea.delete(0, tk.END)

    descripcion_tarea.delete(0, tk.END)

    messagebox.showinfo("Gestor","Tarea agregada")


def eliminar_tarea():

    seleccion = lista.curselection() #se obtiene la selección del Listbox con curselection que sirve para para saber qué elemento seleccionó el usuario en la interfaz
    if seleccion == ():

        messagebox.showerror("Error", "Selecciona una tarea")

        return
    ubicacion = seleccion[0]# Obtiene la posición seleccionada gracias al curselection
    gestor.eliminar_tarea(ubicacion) #Obtiene el texto de esa posición y la elimina
    actualizar_lista()
    messagebox.showinfo("Eliminada", "Se eliminó la tarea")


def completar_tarea():

    seleccion = lista.curselection() #tuve que investigar sobre curseselection--->es una funcion que Dice qué elemento seleccionó el usuario y su ubicacion
    if seleccion == ():

        messagebox.showerror("Error", "Selecciona una tarea")

        return
    ubicacion = seleccion[0]  # Obtiene la posición seleccionada gracias al curselection
    gestor.lista_tareas[ubicacion].completar() # Completa la tarea
    gestor.guardar_tareas()

    actualizar_lista()

    messagebox.showinfo("Completada", "La tarea fue completada")

# VENTANA

ventana = tk.Tk()

ventana.title("Gestor de tareas")
ventana.config(bg="#424242", bd=20, relief="solid")

ventana.geometry("500x400")


tk.Label( ventana,text="Tarea", font=("Arial", 12),bg="#424242",fg="#FFFFFF").pack(pady=2)

entry_tarea = tk.Entry( ventana, width=40)

entry_tarea.pack(pady=2)

 
tk.Label( ventana, text="Descripcion",font=("Arial", 12),bg="#424242",fg="#FFFFFF").pack(pady=2)

descripcion_tarea = tk.Entry(ventana,width=40)

descripcion_tarea.pack(pady=2)


check_urgente = tk.IntVar()

tk.Checkbutton(ventana,text="Urgente",variable=check_urgente,bg="#9B9999").pack(pady=5)


boton_agregar = tk.Button(ventana,text="Agregar tarea", command=agregar_tarea,bg="#38647E")

boton_agregar.pack(pady=5)


boton_completar = tk.Button( ventana,text="Completar", command=completar_tarea,bg="#487E38")

boton_completar.pack(pady=5)


boton_eliminar = tk.Button( ventana, text="Eliminar",command=eliminar_tarea,bg="#7E3838")

boton_eliminar.pack(pady=5)


lista = tk.Listbox(ventana, width=50)

lista.pack(pady=10)


actualizar_lista()

ventana.mainloop()