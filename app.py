import speech_recognition as sr
from tkinter import *
from random import random

from gtts import gTTS
import os

from google_images_download import google_images_download

import shutil

from flask import Flask, render_template, url_for

paintappwrapper = Flask(__name__)

@paintappwrapper.route("/")
def index():
    mytext = 'Hey welcome what do you want to see'
    myaudiotext = 'Speak correctly please !!!'
    language = 'en'

    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj2 = gTTS(text=myaudiotext, lang=language, slow=False)

    myobj.save("welcome.mp3")
    myobj2.save("error.mp3")

    ListOfObjects = {'apple': 'red', 'fish': 'blue', 'leaf': 'green'}

    os.system("mpg123 welcome.mp3")
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # Speech recognition using Google Speech Recognition
    try:
        print("You said: " + r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        os.system("mpg123 error.mp3")
        exit()
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    path = './downloads/' + r.recognize_google(audio)
    destpath = './static/' + r.recognize_google(audio)
    if not os.path.exists(path):
        response = google_images_download.googleimagesdownload();
        arguments = {"keywords": r.recognize_google(audio), "limit": 10, "print_urls": True}
        paths = response.download(arguments)

    if not os.path.exists(destpath):
        shutil.copytree(path, destpath)

    imgPaths = ["", "", "", "", "", "", "", "", "", ""]
    i = 0

    newpath = './../downloads/' + r.recognize_google(audio)

    for filename in os.listdir(path):
        imgPaths[i] = r.recognize_google(audio)+'/'+filename
        i = i + 1

    return render_template('index.html', value=r.recognize_google(audio), images=imgPaths)





# class MyBackground(Widget):
#     def __init__(self, **kwargs):
#         super(MyBackground, self).__init__(**kwargs)
#         with self.canvas:
#             Window.clearcolor = (0, 0, 0, 0)
#             object = r.recognize_google(audio);
#
#             if object.lower() in ListOfObjects :
#
#                 self.bg = Rectangle(source=object+'e'+'.gif', size=(300, 300), pos=(100, 100))
#                 self.bg = Rectangle(source=object+'Sample'+'.gif', size=(300, 300), pos=(1000, 100))
#                 self.bg = Rectangle(source=object+'.gif', size=(300, 300), pos=(550, 100))
#
#             else:
#                 self.bg = Rectangle(source='photo.gif', size=(500, 300), pos=(490, 100))
#
#             path = './downloads/'+object
#             if not os.path.exists(path + '/' + 'converted'):
#                 os.mkdir(path + '/' + 'converted')
#             skip = ["converted"]
#             for filename in os.listdir(path):
#                 if(filename in skip):
#                     continue;
#                 img = Image.open(path+'/'+filename)
#                 filename = filename.rsplit('.', 1)
#                 img.save(path+'/' + 'converted/' + filename[0] + '.gif')
#
#             newpath = path + '/' + 'converted'
#             dpos = 100;
#             for filename in os.listdir(newpath):
#                 self.bg = Rectangle(source= newpath+ '/' + filename, size=(300, 300), pos=(dpos, 500))
#                 dpos= dpos+400;
#
# class MyPaintWidget(Widget):
#
#     def on_touch_down(self, touch):
#         color = (random(), 1, 1)
#         with self.canvas:
#
#             Color(*color, mode='hsv')
#             touch.ud['line'] = Line(points=(touch.x, touch.y), width=5)
#
#     def on_touch_move(self, touch):
#         touch.ud['line'].points += [touch.x, touch.y]
#
#
#
#
# # os.system("mpg123 welcome.mp3")
# # # Record Audio
# # r = sr.Recognizer()
# # with sr.Microphone() as source:
# #     print("Say something!")
# #     audio = r.listen(source)
# #
# # # Speech recognition using Google Speech Recognition
# # try:
# #     print("You said: " + r.recognize_google(audio))
# # except sr.UnknownValueError:
# #     print("Google Speech Recognition could not understand audio")
# #     os.system("mpg123 error.mp3")
# #     exit()
# # except sr.RequestError as e:
# #     print("Could not request results from Google Speech Recognition service; {0}".format(e))
#
# class MyPaintApp(App):
#
#
#     def build(self):
#         response = google_images_download.googleimagesdownload();
#         arguments = {"keywords": r.recognize_google(audio), "limit": 3, "print_urls": True}
#
#         paths = response.download(arguments)
#
#         parent = MyBackground()
#         self.painter = MyPaintWidget()
#         clearbtn = Button(text='Clear')
#         clearbtn.bind(on_release=self.clear_canvas)
#         parent.add_widget(self.painter)
#         parent.add_widget(clearbtn)
#         savebtn = Button(text='Save',pos=(1000, 0))
#         savebtn.bind(on_release=self.save)
#         parent.add_widget(savebtn)
#         print('paint rendering')
#         return parent
#
#     def clear_canvas(self, obj):
#         self.painter.canvas.clear()
#
#     def save(self, *args):
#         im = ImageGrab.grab()
#         im.save('screenshot.png')



if __name__ == '__main__':
    paintappwrapper.run(debug=True, threaded=True)