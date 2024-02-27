from tkinter import *
from tkinter import filedialog
from pytube import YouTube
from PIL import Image, ImageTk
import threading
import time
import sys  
import os

#i grabbed this from here
#https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

Logo = resource_path("Logo.png")

def download():
    Option = str(var.get())
    Link = str(txtfld.get())
    if Link == "":
        lbl3.config(text="Enter a URL Link")
    else:
        global save_path
        save_path = filedialog.askdirectory()
        if save_path:
            txtfld.config(state=DISABLED)  # Disable the entry widget during download
            lbl3.config(text="Download Started, Please Wait!..")
            loading_thread = threading.Thread(target=show_loading_dots)
            loading_thread.start()
            download_thread = threading.Thread(target=perform_download, args=(Option, Link))
            download_thread.start()
        else:
            lbl3.config(text="Select download location")

def perform_download(Option, Link):
    try:
        yt = YouTube(Link)
        stream = None
        if Option == "0" or Option == "1":
            stream = yt.streams.get_by_itag(18)
        elif Option == "2":
            stream = yt.streams.get_by_itag(251)
        
        if stream:
            stream.download(output_path=save_path)
            lbl3.config(text="Download Complete!")
        else:
            lbl3.config(text="Stream not available")
    except Exception as e:
        lbl3.config(text=f"Error: {str(e)}")

def show_loading_dots():
    dots = ""
    while lbl3.cget("text") == "Download Started":
        dots += "."
        if len(dots) > 3:
            dots = "."
        lbl3.config(text="Download Started" + dots)
        time.sleep(0.5)

window = Tk()
window.title('Youtube Video Grabber Powered by QichinoLTD')
window.geometry("500x300")
window.configure(bg='white')

# Background Image
image_0 = Image.open(resource_path('street.png'))
bck_pic = ImageTk.PhotoImage(image_0.resize((500,200)))
lbl = Label(image=bck_pic)
lbl.place(x=1, y=1)

lbl2 = Label(window, text="Video URL:", bg='white', fg='black', font=("System", 11))
lbl2.place(x=10, y=185)

txtfld = Entry(window, text="This is Entry Widget", bd="5", width="52")
txtfld.place(x=95, y=185)

btn = Button(window, text="Download", bg='white', fg='black', command=download)
btn.place(x=420, y=185)

var = IntVar()
R1 = Radiobutton(window, text="Download MP4", bg='white', fg='black', variable=var, value=1)
R1.place(x=120, y=210)

R2 = Radiobutton(window, text="Download MP3", bg='white', fg='black', variable=var, value=2)
R2.place(x=270, y=210)

lbl3 = Label(window, text="", bg='white', fg='black', width="40", font=("System", 11))
lbl3.place(x=100, y=240)

window.mainloop()

