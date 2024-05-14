import tkinter as tk
from tkinter import simpledialog, Canvas, Button, Tk, PhotoImage
from reportlab.pdfgen import canvas as pdf_canvas
from PIL import Image
import os

# Solicitar nombre y número de empleado
def solicitar_datos():
    root = tk.Tk()
    root.withdraw()  # Ocultamos la ventana principal de Tkinter
    nombre = simpledialog.askstring("Input", "Ingrese su nombre completo:")
    num_empleado = simpledialog.askstring("Input", "Ingrese su número de empleado:")
    root.destroy()
    return nombre, num_empleado

# Generar el archivo PDF inicial
def generar_pdf(nombre, num_empleado):
    c = pdf_canvas.Canvas(f"{num_empleado}.pdf")
    c.drawString(100, 750, f"Yo, {nombre}, acepto los términos.")
    c.save()

# Clase para la interfaz de firma
class PaintApp:
    def __init__(self, nombre, num_empleado):
        self.nombre = nombre
        self.num_empleado = num_empleado
        self.root = Tk()
        self.c = Canvas(self.root, bg='white', width=600, height=200)
        self.c.pack()
        self.image1 = PhotoImage(width=600, height=200)
        self.c.create_image((300, 100), image=self.image1, state="normal")
        self.c.bind("<B1-Motion>", self.paint)
        Button(self.root, text="Guardar", command=self.guardar_firma).pack()
        Button(self.root, text="Borrar", command=self.limpiar_canvas).pack()

    def paint(self, event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        self.c.create_oval(x1, y1, x2, y2, fill="black", width=5)
        self.draw(event.x, event.y)

    def draw(self, x, y):
        self.image1.put("black", (x, y))

    def guardar_firma(self):
        filename = f"firma_{self.num_empleado}.png"
        self.image1.write(filename, format="png")
        self.agregar_firma_a_pdf(filename)
        os.remove(filename)  # Elimina la imagen de la firma después de usarla

    def limpiar_canvas(self):
        self.c.delete("all")

    def agregar_firma_a_pdf(self, firma):
        firma_imagen = Image.open(firma)
        firma_imagen.load()  # Asegúrate de que la imagen se carga correctamente
        firma_imagen.save(f"firma_{self.num_empleado}_final.png", 'PNG', quality=95, optimize=True)

        c = pdf_canvas.Canvas(f"{self.num_empleado}.pdf")
        c.drawString(100, 750, f"Yo, {self.nombre}, acepto los términos.")
        c.drawImage(f"firma_{self.num_empleado}_final.png", 100, 500, width=200, height=100)  # Ajusta las dimensiones según sea necesario
        c.save()

        os.remove(f"{self.num_empleado}.pdf")  # Elimina el PDF base
        os.remove(f"firma_{self.num_empleado}_final.png")  # Elimina la imagen final de la firma

        self.root.destroy()

if __name__ == "__main__":
    nombre, num_empleado = solicitar_datos()
    generar_pdf(nombre, num_empleado)
    app = PaintApp(nombre, num_empleado)
    app.root.mainloop()
