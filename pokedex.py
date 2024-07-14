import tkinter as tk
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk
import io

def fetch_pokemon_data(pokemon):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def display_pokemon(event=None):
    pokemon_name = entry.get()
    data = fetch_pokemon_data(pokemon_name)
    if data:
        clear_pokemon_info()
        name_label.config(text=f"Name: {data['name'].capitalize()}")
        types = ", ".join([t['type']['name'].capitalize() for t in data['types']])
        type_label.config(text=f"Type(s): {types}")
        weight_label.config(text=f"Weight: {data['weight']} kg")
        height_label.config(text=f"Height: {data['height']} dm")

        image_url = data['sprites']['front_default']
        if image_url:
            image_data = requests.get(image_url).content
            image = Image.open(io.BytesIO(image_data))
            image = image.resize((150, 150))  
            photo = ImageTk.PhotoImage(image)
            image_label.config(image=photo)
            image_label.image = photo  
        else:
            messagebox.showerror("Error", f"Image not found for Pokemon '{pokemon_name}'")
    else:
        messagebox.showerror("Error", f"Pokemon '{pokemon_name}' not found.")

def clear_pokemon_info():
    name_label.config(text="Name:")
    type_label.config(text="Type(s):")
    weight_label.config(text="Weight:")
    height_label.config(text="Height:")
    image_label.config(image="")

root = tk.Tk()
root.title("Pokedex")
root.geometry("400x600")
root.configure(bg="red")
root.resizable(False, False)

top_border = tk.Frame(root, bg="black", height=50)
top_border.pack(fill=tk.X)

title_label = tk.Label(top_border, text="POKEDEX", font=("Arial", 20, "bold"), fg="white", bg="black")
title_label.pack(pady=10)

frame = tk.Frame(root, width=200, height=200, bg="white")
frame.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

image_label = tk.Label(frame, bg="white")
image_label.pack(pady=10)

info_frame = tk.Frame(root, width=200, height=300, bg="white")
info_frame.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

name_label = tk.Label(info_frame, font=("Arial", 12), bg="white")
name_label.pack(pady=5)

type_label = tk.Label(info_frame, font=("Arial", 12), bg="white")
type_label.pack(pady=5)

weight_label = tk.Label(info_frame, font=("Arial", 12), bg="white")
weight_label.pack(pady=5)

height_label = tk.Label(info_frame, font=("Arial", 12), bg="white")
height_label.pack(pady=5)

canvas = tk.Canvas(root, width=50, height=50, bg="red", highlightthickness=0)
canvas.place(relx=0.95, rely=0.9, anchor=tk.SE)
canvas.create_oval(0, 0, 50, 50, fill="black")

search_frame = tk.Frame(root, bg="red", padx=10, pady=10)
search_frame.pack(side=tk.BOTTOM, fill=tk.X)

search_label = tk.Label(search_frame, text="Enter Pokemon Name or ID:", font=("Arial", 12), bg="white")
search_label.pack(side=tk.LEFT)

entry = ttk.Entry(search_frame, width=20, font=("Arial", 12))
entry.pack(side=tk.LEFT, padx=10)
entry.bind("<Return>", display_pokemon)  

root.mainloop()
