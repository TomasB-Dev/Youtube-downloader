import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os
from pytube import YouTube
import threading
import shutil

def parse_youtube_url(url):
    query = url.split("?")[1]
    query_dict = dict(item.split("=") for item in query.split("&"))
    return query_dict["v"]

def download_video(youtube_url, quality, filename):
    try:
        yt = YouTube(youtube_url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').get_by_resolution(quality)
        # Directorio de la carpeta de descargas universal
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        # Ruta completa del archivo descargado
        destination = os.path.join(downloads_folder, filename)
        # Descargar el archivo en la carpeta de descargas universal
        stream.download(output_path=downloads_folder, filename=filename)
        messagebox.showinfo("Success", "Video downloaded successfully!")
        progress_bar["value"] = 100
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def download_audio(youtube_url, filename):
    try:
        yt = YouTube(youtube_url)
        stream = yt.streams.filter(only_audio=True).first()
        # Directorio de la carpeta de descargas universal
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        # Ruta completa del archivo descargado
        destination = os.path.join(downloads_folder, filename)
        # Descargar el archivo en la carpeta de descargas universal
        stream.download(output_path=downloads_folder, filename=filename)
        messagebox.showinfo("Success", "Audio downloaded successfully!")
        progress_bar["value"] = 100
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def start_progress_animation():
    progress_bar["value"] = 0
    animate_progress()

def animate_progress():
    if progress_bar["value"] < 80:
        progress_bar["value"] += 1
        root.after(50, animate_progress)
    else:
        root.after_cancel(animate_progress)

def on_download_click():
    global var
    url = entry_url.get()
    if url == "":
        messagebox.showwarning("Warning", "Please enter a valid YouTube URL.")
        return

    quality = quality_var.get()
    filename = filename_entry.get()

    start_progress_animation()

    if var.get() == 1:
        threading.Thread(target=download_video, args=(url, quality, filename + ".mp4")).start()
    elif var.get() == 2:
        threading.Thread(target=download_audio, args=(url, filename + ".mp3")).start()

def paste_from_clipboard():
    text = root.clipboard_get()
    entry_url.delete(0, tk.END)
    entry_url.insert(0, text)

def open_downloads_folder():
    try:
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        os.startfile(downloads_folder)  # Abre la carpeta de descargas en el explorador de archivos
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while opening the Downloads folder: {str(e)}")

root = tk.Tk()
root.title("YouTube Downloader")
root.configure(bg="#f0f0f0")
root.iconbitmap("icon.ico")

# Definir variable global var
var = tk.IntVar()

# Menú contextual para la entrada de texto
entry_menu = tk.Menu(root, tearoff=0)
entry_menu.add_command(label="Pegar", command=paste_from_clipboard)

# Función para manejar el evento del clic derecho
def entry_right_click(event):
    entry_menu.post(event.x_root, event.y_root)

# Establecer la función de manejo del clic derecho en la entrada de texto
entry_url = tk.Entry(root, bd=2)
entry_url.pack(side=tk.LEFT, padx=5, pady=5)
entry_url.bind("<Button-3>", entry_right_click)

button_paste = tk.Button(root, text="Paste", command=paste_from_clipboard, bg="#007bff", fg="white", relief="flat", padx=10)
button_paste.pack(side=tk.LEFT, pady=5)

# Ajustar el tamaño de la fuente para que coincida con el del botón de pegar
button_paste.update_idletasks()
entry_url.config(font=button_paste.cget("font"))

frame_radio = tk.Frame(root, bg="#f0f0f0")
frame_radio.pack(pady=10)

radio_video = tk.Radiobutton(frame_radio, text="Descargar Video", value=1, variable=var, bg="#f0f0f0")
radio_video.pack(side=tk.LEFT)

quality_var = tk.StringVar()
quality_var.set("720p")
quality_options = ["144p", "240p", "360p", "480p", "720p", "1080p"]
quality_dropdown = tk.OptionMenu(frame_radio, quality_var, *quality_options)
quality_dropdown.config(bg="#f0f0f0", relief="flat")
quality_dropdown.pack(side=tk.LEFT)

radio_audio = tk.Radiobutton(frame_radio, text="Descargar Audio (MP3)", value=2, variable=var, bg="#f0f0f0")
radio_audio.pack(side=tk.LEFT)

filename_frame = tk.Frame(root, bg="#f0f0f0")
filename_frame.pack(pady=(5, 20))

filename_label = tk.Label(filename_frame, text="Nombre del Archivo:", bg="#f0f0f0")
filename_label.pack(side=tk.LEFT)

filename_entry = tk.Entry(filename_frame, width=20)
filename_entry.pack(side=tk.LEFT)

button_download = tk.Button(root, text="Descargar", command=on_download_click, bg="#28a745", fg="white", relief="flat", padx=10)
button_download.pack(pady=5)

button_open_folder = tk.Button(root, text="Abrir Carpeta de Descargas", command=open_downloads_folder, bg="#007bff", fg="white", relief="flat", padx=10)
button_open_folder.pack(pady=5)

progress_frame = tk.Frame(root, bg="#f0f0f0")
progress_frame.pack(pady=10)

progress_label = tk.Label(progress_frame, text="Progreso de Descarga:", bg="#f0f0f0")
progress_label.pack(side=tk.LEFT)

progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(side=tk.LEFT)

root.mainloop()
