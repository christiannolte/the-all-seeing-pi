from picamera2 import Picamera2, Preview
from gpiozero import Button
from overlay_functions import *
from time import gmtime, strftime
from guizero import App, PushButton, Text, Picture
import time
import sys
from libcamera import Transform


# Tell the next overlay button what to do
def next_overlay():
    global overlay
    overlay = next(all_overlays)
    print(overlay)
    preview_overlay(camera, overlay)

# Tell the take picture button what to do
def take_picture():
    global output
    global your_pic
    global app
    output = strftime("/home/pi/fotos/Fotobox-%Y-%m-%d_%H:%M:%S.png", gmtime())
    capture_config = camera.create_still_configuration(main={"size": (1024, 768)}, lores={"size": (1024, 768)}, display="lores")
    camera.switch_mode_and_capture_file(capture_config, output)
    camera.stop_preview()
    output_overlay(output, overlay)

    # Save a smaller gif
    size = 550, 550
    gif_img = Image.open(output)
    gif_img.thumbnail(size, Image.ANTIALIAS)
    gif_img.save(latest_photo, 'gif')

    # Set the gui picture to this picture
#    your_pic.set(latest_photo)
#    your_pic.destroy()
#    your_pic = Picture(app, latest_photo)
#    your_pic.image=latest_photo
    app.destroy()


def new_picture():
    camera.start_preview(Preview.QTGL, x=0, y=0, width=640, height=480,transform=Transform(hflip=1))
    camera.start()
    preview_overlay(camera, overlay)



# Set up buttons
next_overlay_btn = Button(23)
next_overlay_btn.when_released = next_overlay
take_pic_btn = Button(25,pull_up = True,bounce_time= None)
take_pic_btn.when_pressed = take_picture

# Set up camera (with resolution of the touchscreen)
camera = Picamera2()
camera_config_preview = camera.create_preview_configuration()
#camera_config_still = camera.create_still_configuration(main={"size": (1024, 768)}, lores={"size": (640, 480)}, display="lores")
camera.configure(camera_config_preview)
#camera.resolution = (1024, 768)
#camera.hflip = True

# Start camera preview
#camera.start_preview(Preview.QTGL, x=0, y=0, width=80, height=60,transform=Transform(hflip=1))
#camera.start()

# Set up filename
output = ""

latest_photo = '/home/pi/latest.gif'

app = App("Fotobox", 800, 480)
app.tk.attributes("-fullscreen", True)
#message = Text(app, "I spotted you!")
your_pic = Picture(app, latest_photo)
new_pic = PushButton(app, new_picture, text="Neues Bild aufnehmen")
app.display()
