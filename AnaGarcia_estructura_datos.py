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

    def __str__(self):

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

        self.lista_tareas = []

        self.cargar_tareas()

    def agregar_tarea(self, tarea):

        self.lista_tareas.append(tarea)

        archivo = open("tareas.txt", "a")

        texto = (tarea.tipo + "/" + tarea.titulo() + "/" + tarea.descripcion() + "/" + tarea.estado() + "/" + tarea.fecha() + "\n")
        archivo.write(texto)

        archivo.close()

    def guardar_tareas(self):

        archivo = open("tareas.txt", "w")

        for tarea in self.lista_tareas:

            texto = ( tarea.tipo + "/" + tarea.titulo() + "/" +tarea.descripcion() + "/" +tarea.estado() + "/" + tarea.fecha() + "\n")

            archivo.write(texto)

        archivo.close()

    def cargar_tareas(self):

        try:

            archivo = open("tareas.txt", "r")

            lineas = archivo.readlines()

            for linea in lineas:

                linea = linea.replace("\n", "")

                datos = []

                palabra = ""

                for letra in linea:

                    if letra != "/":

                        palabra = palabra + letra

                    else:

                        datos.append(palabra)

                        palabra = ""

                datos.append(palabra)

                if len(datos) < 5:

                    continue

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

        except FileNotFoundError:

            pass

    def eliminar_tarea(self, ubicacion):

        del self.lista_tareas[ubicacion]

        self.guardar_tareas()


gestor = GestorTareas()


# FUNCIONES

def actualizar_lista():

    lista.delete(0, tk.END)

    posicion = 0

    for tarea in gestor.lista_tareas:

        lista.insert(posicion, tarea.mostrar())

        posicion = posicion + 1


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

    if len(gestor.lista_tareas) > 0:

        gestor.eliminar_tarea(0)

        actualizar_lista()

        messagebox.showinfo("Eliminada","Se eliminó la tarea")


def completar_tarea():
    
    if len(gestor.lista_tareas) > 0:

        gestor.lista_tareas[0].completar()

        gestor.guardar_tareas()

        actualizar_lista()

        messagebox.showinfo( "Completada", "La primera tarea fue completada")


# VENTANA

ventana = tk.Tk()

ventana.title("Gestor de tareas")

ventana.geometry("500x400")


tk.Label( ventana,text="Tarea", font=("Arial", 12)).pack(pady=2)

entry_tarea = tk.Entry( ventana, width=40)

entry_tarea.pack(pady=2)

 
tk.Label( ventana, text="Descripcion",font=("Arial", 12)).pack(pady=2)

descripcion_tarea = tk.Entry(ventana,width=40)

descripcion_tarea.pack(pady=2)


check_urgente = tk.IntVar()

tk.Checkbutton(ventana,text="Urgente",variable=check_urgente).pack(pady=5)


boton_agregar = tk.Button(ventana,text="Agregar tarea", command=agregar_tarea)

boton_agregar.pack(pady=5)


boton_completar = tk.Button( ventana,text="Completar", command=completar_tarea)

boton_completar.pack(pady=5)


boton_eliminar = tk.Button( ventana, text="Eliminar",command=eliminar_tarea)

boton_eliminar.pack(pady=5)


lista = tk.Listbox(ventana, width=50)

lista.pack(pady=10)


actualizar_lista()

ventana.mainloop()