from reportlab.pdfgen import canvas
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk
import datetime
from reportlab.lib.pagesizes import letter
import os
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
import io

def crear_pdf(nombre_archivo, firma, nombre_completo, numero_empleado, departamento, fecha, plantilla_pdf):
    # Crea un nuevo archivo PDF que servirá como lienzo para añadir los datos.
    output_pdf = nombre_archivo

    # Utiliza la plantilla existente.
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(480, 80, f"{fecha}")
    can.drawString(50, 110, f"{nombre_completo}")
    can.drawString(480, 110, f"{numero_empleado}")
    can.drawString(100, 80, f"{departamento}")
    # Asegúrate de que la ruta de la imagen de la firma sea correcta.
    firma_path = r"C:\ProduccionRpa\Sing\Control\firma.png"
    if os.path.exists(firma_path):
        can.drawImage(firma_path, 250, 30, width=150, height=60) # Ajusta según sea necesario
    can.save()

    # Mueve el lienzo al paquete de BytesIO.
    packet.seek(0)
    new_pdf = PdfReader(packet)
    # Lee la plantilla existente.
    existing_pdf = PdfReader(open(plantilla_pdf, "rb"))
    output = PdfWriter()
    
    # Agrega la página de la plantilla con los datos dibujados encima.
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)

    # Escribe el resultado en un archivo.
    outputStream = open(output_pdf, "wb")
    output.write(outputStream)
    outputStream.close()

def guardar_firma(firma, nombre_completo, numero_empleado, departamento, limpiar_campos):
    hoy = datetime.datetime.now().strftime("%Y-%m-%d")
    año = datetime.datetime.now().strftime("%Y")
    
    # Guarda la firma en la ruta especificada.
    firma.save(r"C:\ProduccionRpa\Sing\Control\firma.png")
    
    archivo_plantilla = r"C:\ProduccionRpa\Sing\Control\FOR 7.1 001 CTA_MENDELFIRMA.pdf"
    nombre_archivo_local = "documento.pdf"
    crear_pdf(nombre_archivo_local, firma, nombre_completo, numero_empleado, departamento, hoy, archivo_plantilla)
    
    nombre_archivo_especifico = fr"C:\ProduccionRpa\Sing\Resultados\{numero_empleado}_{nombre_completo}_{año}-MENDEL.pdf"
    crear_pdf(nombre_archivo_especifico, firma, nombre_completo, numero_empleado, departamento, hoy, archivo_plantilla)
    
    messagebox.showinfo("PDF generado", "El PDF ha sido generado con éxito en ambas ubicaciones.")
    limpiar_campos()

def entrada_datos():
    ventana = tk.Tk()
    ventana.title("SYSCOM - Firma Digital")
    ventana.geometry("600x400")
    ventana.configure(bg='light grey')

    customFont = ("Arial", 12)
    labelBg = "light grey"
    entryBg = "white"
    entryFg = "black"
    entryBorderWidth = 2
    entryRelief = "groove"
    entryWidth = 30

    # Nombre completo
    tk.Label(ventana, text="Nombre completo", font=customFont, bg=labelBg).pack(pady=(10,2))
    nombres = tk.Entry(ventana, font=customFont, bg=entryBg, fg=entryFg, borderwidth=entryBorderWidth, relief=entryRelief, width=entryWidth)
    nombres.pack(pady=(2,10))

    # Frame para Número de empleado y Departamento
    frame = tk.Frame(ventana, bg='light grey')
    frame.pack(pady=(10,0))

    # Número de empleado
    tk.Label(frame, text="Número de empleado", font=customFont, bg=labelBg).pack(side=tk.LEFT, padx=(0,10))
    empleado = tk.Entry(frame, font=customFont, bg=entryBg, fg=entryFg, borderwidth=entryBorderWidth, relief=entryRelief, width=10)
    empleado.pack(side=tk.LEFT, padx=(0,10))

    # Departamento
    tk.Label(frame, text="Departamento", font=customFont, bg=labelBg).pack(side=tk.LEFT, padx=(10,0))
    departamento = tk.Entry(frame, font=customFont, bg=entryBg, fg=entryFg, borderwidth=entryBorderWidth, relief=entryRelief, width=entryWidth)
    departamento.pack(side=tk.LEFT)

    canvas = tk.Canvas(ventana, width=400, height=200, bg='white')
    canvas.pack(pady=(10,0),padx=(0,0))

    firma_image = Image.new("RGB", (400, 200), 'white')
    draw = ImageDraw.Draw(firma_image)

    def pintar(event):
        x, y = event.x, event.y
        draw.ellipse((x-1, y-1, x+1, y+1), fill='blue')
        canvas.create_oval(x-1, y-1, x+1, y+1, fill='blue')

    def limpiar_firma():
        global draw
        canvas.delete("all")
        draw = ImageDraw.Draw(firma_image)

    def limpiar_campos():
        nombres.delete(0, tk.END)
        empleado.delete(0, tk.END)
        departamento.delete(0, tk.END)
        limpiar_firma()

    def finalizar_firma():
        # Guarda temporalmente la imagen de la firma para su uso.
        firma_image.save(r"C:\ProduccionRpa\Sing\Control\firma.png")
        guardar_firma(firma_image, nombres.get(), empleado.get(), departamento.get(), limpiar_campos)
        ventana.destroy()
        entrada_datos()

    boton_guardar = tk.Button(ventana, text="Guardar Firma y Generar PDF", command=finalizar_firma)
    boton_guardar.pack(pady=(10,0))

    boton_limpiar_firma = tk.Button(ventana, text="Limpiar Firma", command=limpiar_firma)
    boton_limpiar_firma.pack(pady=(5,0))

    canvas.bind("<B1-Motion>", pintar)

    ventana.mainloop()

if __name__ == "__main__":
    entrada_datos()
