import tkinter as tk
from tkinter import Canvas, Button, Label, Text, Scrollbar
from PIL import Image, ImageDraw
from keras.models import load_model
from keras.preprocessing import image as keras_image
import numpy as np
import os
import text_generation

model_personajes = load_model('./modelo_personajes_img.h5')
model_lugares = load_model('./model_lugares_img.h5')

CLASSES_PERSONAJES = {
    0: "oso",
    1: "serpiente",
    2: "leon",
    3: "raton",
    4: "cerdo",
    5: "pinguino",
    6: "conejo",
    7: "vaca",
    8: "perro",
    9: "ardilla"
    
}

CLASSES_LUGARES = {
    0: "arbol",
    1: "avion",
    2: "casa",
    3: "submarino",
    4: "torre-eiffel",
    5: "tren"
}

class DrawingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Dibuja y Predice")
        
        self.canvas1 = Canvas(master, width=250, height=250, bg="white")
        self.canvas1.pack(side=tk.LEFT)

        self.canvas2 = Canvas(master, width=250, height=250, bg="white")
        self.canvas2.pack(side=tk.RIGHT)

        self.label_result1 = Label(master, text="Resultado 1: ")
        self.label_result1.pack()

        self.label_result2 = Label(master, text="Resultado 2: ")
        self.label_result2.pack()

        self.text_output = Text(master, wrap="word", height=4, width=40)
        self.text_output.pack(padx=10, pady=10)

        self.story_text = Text(master, wrap="word", height=10, width=60)
        self.story_text.pack(padx=10, pady=10)

        self.scrollbar = Scrollbar(master, command=self.text_output.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.text_output.config(yscrollcommand=self.scrollbar.set)

        self.button_clear = Button(master, text="Borrar", command=self.clear_canvas)
        self.button_clear.pack()

        self.button_predict = Button(master, text="Predecir Dibujos", command=self.predict)
        self.button_predict.pack()

        self.button_generate_story = Button(master, text="Generar Historia", command=self.generate_story)
        self.button_generate_story.pack()

        self.image1 = Image.new("L", (200, 200), 255)
        self.draw1 = ImageDraw.Draw(self.image1)

        self.image2 = Image.new("L", (200, 200), 255)
        self.draw2 = ImageDraw.Draw(self.image2)

        self.canvas1.bind("<B1-Motion>", lambda event, canvas=self.canvas1, draw=self.draw1: self.paint(event, canvas, draw))
        self.canvas2.bind("<B1-Motion>", lambda event, canvas=self.canvas2, draw=self.draw2: self.paint(event, canvas, draw))

        # Agregar una variable para almacenar el texto generado
        self.generated_text1 = ""
        self.generated_text2 = ""
        

    def paint(self, event, canvas, draw):
        x1, y1 = int(event.x - 1), int(event.y - 1)
        x2, y2 = int(event.x + 1), int(event.y + 1)
        canvas.create_oval(x1, y1, x2, y2, fill="black", width=2)
        draw.line([x1, y1, x2, y2], fill="black", width=2)
    
    def clear_canvas(self):
        self.canvas1.delete("all")
        self.canvas2.delete("all")
        self.image1 = Image.new("L", (200, 200), 255)
        self.draw1 = ImageDraw.Draw(self.image1)
        self.image2 = Image.new("L", (200, 200), 255)
        self.draw2 = ImageDraw.Draw(self.image2)
        self.label_result1.config(text="Resultado 1: ")
        self.label_result2.config(text="Resultado 2: ")
        self.text_output.delete(1.0, "end")
        self.story_text.delete(1.0, "end")

    def preprocess_image(self, image):
    
        img = image.resize((28, 28))
        img_array = keras_image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0
        img_array = 1 - img_array 
        return img_array

    def predict(self):
        img_array1 = self.preprocess_image(self.image1)
        img_array2 = self.preprocess_image(self.image2)
        
        prediction1 = model_personajes.predict(img_array1) 
        predicted_class1 = np.argmax(prediction1)
        result1 = CLASSES_PERSONAJES.get(predicted_class1, "Desconocido")
        
        prediction2 = model_lugares.predict(img_array2) 
        predicted_class2 = np.argmax(prediction2)
        result2 = CLASSES_LUGARES.get(predicted_class2, "Desconocido")

        self.set_generated_text(result1, result2)

    def set_generated_text(self, text1, text2):
        self.generated_text1 = text1
        self.generated_text2 = text2
        self.label_result1.config(text=f"Resultado 1: {text1}")
        self.label_result2.config(text=f"Resultado 2: {text2}")
        self.text_output.delete(1.0, "end")
        self.text_output.insert("end", f"{text1}\n{text2}")

    def generate_story(self):
        result1 = self.generated_text1
        result2 = self.generated_text2
    
        # Generar la historia utilizando los resultados de las predicciones como palabras clave
        story = text_generation.generate_story(result1, result2)
    
        # Muestra la historia en el cuadro de texto dedicado
        # Show the history
        self.story_text.delete(1.0, "end")
        self.story_text.insert("end", story)

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
