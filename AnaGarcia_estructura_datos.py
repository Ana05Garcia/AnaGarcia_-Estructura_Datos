import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os

class Tarea:
    def __init__(self,titulo,descripcion,estado,fecha):
        self.__titulo = titulo
        self.__descripcion = descripcion
        self.__estado = estado
        self.__estado= "pendiente"
        self.__fecha= fecha
        self.__fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def mostrar(self):
        return f"{self.__titulo}-{self.__estado}"
    
    def __str__(self): #metodo dunder para mostrar una funcion
        return self.mostrar
    

class TareaUrgente(Tarea):
    def __init__(self, titulo, descripcion, estado, fecha,tipo):
        super().__init__(titulo, descripcion, estado, fecha)
        self.tipo = "Urgente"
    
    def mostrar(self):
        return f"Urgente⚠️ {self.__titulo}-{self.__estado}"
    

    
    

class GestorTareas:
    def __init__(self):
        self.lista_tareas= []
        self.cargar_tareas()

    def agregar_tarea(self,tarea):

        self.lista_tareas.append(tarea)
        
        archivo = open("tareas.txt","a") #a es append
        texto = ( tarea.tipo + "|" + tarea.titulo + "|" +tarea.descripcion + "|" + tarea.estado + "|" + tarea.fecha + "\n")
        archivo.write(texto)
        archivo.close()

    def guardar_tareas(self):

        # Reescribe el archivo completo
        archivo = open("tareas.txt", "w")

        for tarea in self.lista_tareas:

            archivo.write(tarea.tipo + "," + tarea.titulo + "," +tarea.descripcion + "," +tarea.estado + "," + tarea.fecha + "\n") #escribe la informacion en un archivo

        archivo.close()
     
    def cargar_tareas(self): #lo mas dificil del codigo :,I
            try:

                archivo = open("tareas.txt", "r")

                lineas = archivo.readlines() #Lee todas las líneas del archivo y las guarda en una lista (lo tuve que consultar)

                for linea in lineas: #Recorre cada línea del archivo una por una

                    linea = linea.replace("\n", "") #reemplaza los saltos de linea por un espacio en blanco

                    datos = []

                    palabra = ""

                    for letra in linea: #Recorre cada letra de la línea.

                        if letra != ",": #  si la letra no es una coma de agrega a palabra
                            palabra = palabra + letra

                        else: #  al encontrar una coma se guarda la palabra completa en la lista datos
                            datos.append(palabra)
                            palabra = ""

                    datos.append(palabra) #Guarda la palabra que queda después de la última coma.


                    #Cada posición de la lista se guarda en una variable (lo tuve que consultar un poco)
                    tipo = datos[0] # lo que esta adento de datos es la posicion de cada elemento de la lista
                    titulo = datos[1]
                    descripcion = datos[2]
                    estado = datos[3]
                    fecha = datos[4]

                    if tipo == "urgente":

                        tarea = TareaUrgente(titulo,descripcion, estado,fecha) #se crea un objeto en base a Tarea urgente

                    else:

                        tarea = Tarea( titulo,descripcion,estado,fecha) #se crea un objeto en base a la clase Tarea

                    self.lista_tareas.append(tarea)

                archivo.close()
            except:
                pass 
    
    def eliminar_tarea(self, ubicacion):  #ubicacion es la posición de la tarea que se quiere borrar.

        del self.lista_tareas[ubicacion] #del  es para eliminar elementos de una lista y asi evito hacer una lista nueva  sin el elemento borrado y un ciclo for -_-

        self.guardar_tareas() 

ventana = tk.Tk()

ventana.title("Gestor de tareas")

ventana.geometry("500x400")

                

      
        
        
        

        