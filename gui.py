from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
from WhatSend import sendwtsp
import json

FONT = "Cousine NF"


class WhatSendApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WhatSend")
        self.root.config(pady=25, padx=25)

        # Load the hospital templates from the JSON file
        with open("Public/hospital_templates.json", "r", encoding="utf-8") as json_file:
            self.hospital_data = json.load(json_file)

        self.create_widgets()

        self.templates = {}  # Dictionary to store updated templates and numbers

    def create_widgets(self):
        self.create_canvas()
        self.create_labels()
        self.create_buttons()
        self.create_entries()
        self.create_combobox()
        self.create_text_entry()

    def create_canvas(self):
        self.canvas = Canvas(width=200, height=200, highlightthickness=0)
        img = Image.open("Public/mga.jpg")
        resized_image = img.resize((200, 200))
        self.new_img = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(0, 0, anchor=NW, image=self.new_img)
        self.canvas.grid(column=0, row=0, columnspan=2)

    def create_labels(self):
        self.nombreMascota = Label(text="Nombre de Mascota", highlightthickness=0, font=(FONT, 10, "normal"))
        self.nombreMascota.grid(column=0, row=2)

        self.nWhatsApp = Label(text="# WhatsApp", highlightthickness=0, font=(FONT, 10, "normal"))
        self.nWhatsApp.grid(column=0, row=3)

        self.menuList_label = Label(text="Listado", highlightthickness=0, font=(FONT, 10, "normal"))
        self.menuList_label.grid(column=0, row=4)

    def create_buttons(self):
        self.add_button = Button(text="Agregar", width=10, font=(FONT, 10, "normal"), command=self.add_to_dictionary)
        self.add_button.grid(column=0, row=6)

        self.enviar = Button(text="Enviar", width=10, font=(FONT, 10, "normal"), command=self.send_message)
        self.enviar.grid(column=1, row=6)

    def create_entries(self):
        self.nombre_mascota = Entry(width=25)
        self.nombre_mascota.grid(column=1, row=2)
        self.nombre_mascota.focus()

        self.whatsapp_entry = Entry(width=25)
        self.whatsapp_entry.grid(column=1, row=3)
        self.whatsapp_entry.insert(0, '+52')

    def create_combobox(self):
        self.menu_listbox = Combobox(width=25, values=list(self.hospital_data.keys()))
        self.menu_listbox.grid(column=1, row=4)
        self.menu_listbox.set("Selecciona Mensaje")
        self.menu_listbox.bind("<<ComboboxSelected>>", self.update_template)

    def create_text_entry(self):
        self.selected_item_entry = Text(width=40, height=2, wrap=WORD)
        self.selected_item_entry.grid(column=0, row=5, columnspan=2)

        for widget in self.root.winfo_children():
            widget.grid_configure(pady=5)

    def update_template(self, event):
        selected_hospital = self.menu_listbox.get()
        template = self.hospital_data[selected_hospital]["template"]
        patient_name = self.nombre_mascota.get()
        updated_template = template.replace("[Nombre del Paciente]", patient_name)

        self.selected_item_entry.delete(1.0, END)
        self.selected_item_entry.insert(1.0, updated_template)

        lines = int(self.selected_item_entry.index('end-1c').split('.')[0])
        line_height = 15
        max_height = min(10, lines * line_height)
        self.selected_item_entry.config(height=max_height)

    def add_to_dictionary(self):
        selected_hospital = self.menu_listbox.get()
        updated_template = self.selected_item_entry.get(1.0, END).strip()  # Get the template
        phone_number = self.whatsapp_entry.get()  # Get the phone number

        if updated_template and phone_number:
            self.templates[selected_hospital] = {"template": updated_template, "phone": phone_number}

        # Clear the entries
        self.nombre_mascota.delete(0, END)
        self.whatsapp_entry.delete(0, END)
        self.selected_item_entry.delete(1.0, END)

    def send_message(self):
        if self.templates:
            for hospital, data in self.templates.items():
                sendwtsp(phone=data["phone"], message=data["template"])

            # Clear the dictionary after sending messages
            self.templates.clear()
        else:
            phone_number = self.whatsapp_entry.get()
            updated_template = self.selected_item_entry.get(1.0, END).strip()

            if phone_number and updated_template:
                sendwtsp(phone=phone_number, message=updated_template)

        # Clear the entries
        self.nombre_mascota.delete(0, END)
        self.whatsapp_entry.delete(0, END)
        self.selected_item_entry.delete(1.0, END)

        messagebox.showinfo("Enviado", "Mensajes enviados exitosamente.")
