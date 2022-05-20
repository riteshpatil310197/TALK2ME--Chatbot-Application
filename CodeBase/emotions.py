import cv2
import numpy as np
from keras.models import load_model
from statistics import mode
from utils.inference import detect_faces
from utils.inference import draw_text
from utils.inference import draw_bounding_box
from utils.inference import apply_offsets
from utils.inference import load_detection_model
from utils.preprocessor import preprocess_input

import time

from tkinter import *

top = Tk()

global get_name
get_name = 5

time.sleep(1)

def Register():
    def Update():
        get_name = 1
        p = username.get()
        print(p)
        top.destroy()
        
    top.geometry("400x300")
    top.configure(background="#ffff8f")

    label2 = Label(top, text="Register your name")
    label2.configure(background="#ffff8f")
    label2.config(font=("Courier", 15))
    label2.place(x = 55,y=50,height=70, width=300)

    username = StringVar() 
    passEntry = Entry(top, textvariable=username)
    passEntry.place(x =145,y=150,height=40, width=120)

    B7 = Button(top, text = "Register", command = Update)
    B7.place(x = 145,y = 220,height=40, width=120)
    B7.configure(background="#ffff8f")
    top.mainloop()

Register()
    
while True:
    if(get_name==5):
#        print('ZAL ki mg')
        break

#print('Zalay')
    




# parameters for loading data and images
emotion_model_path = './models/emotion_model.hdf5'
emotion_labels = {0:'angry',1:'disgust',2:'fear',3:'happy',4:'sad',5:'surprise',6:'neutral'}

# hyper-parameters for bounding boxes shape
frame_window = 10
emotion_offsets = (20, 40)

# loading models
face_cascade = cv2.CascadeClassifier('./models/haarcascade_frontalface_default.xml')
emotion_classifier = load_model(emotion_model_path)

# getting input model shapes for inference
emotion_target_size = emotion_classifier.input_shape[1:3]

# starting lists for calculating modes
emotion_window = []

# starting video streaming

cv2.namedWindow('Emotion Detection')
video_capture = cv2.VideoCapture(0)

cap = cv2.VideoCapture(0) # Webcam source


emotion_mode = []
while cap.isOpened(): # True:
    ret, bgr_image = cap.read()

    #bgr_image = video_capture.read()[1]

    gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
    rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)

    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5,
			minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

    for face_coordinates in faces:

        x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
        gray_face = gray_image[y1:y2, x1:x2]
        try:
            gray_face = cv2.resize(gray_face, (emotion_target_size))
        except:
            continue

        gray_face = preprocess_input(gray_face, True)
        gray_face = np.expand_dims(gray_face, 0)
        gray_face = np.expand_dims(gray_face, -1)
        emotion_prediction = emotion_classifier.predict(gray_face)
        emotion_probability = np.max(emotion_prediction)
        emotion_label_arg = np.argmax(emotion_prediction)
        emotion_text = emotion_labels[emotion_label_arg]
        emotion_window.append(emotion_text)

        
        if len(emotion_window) > frame_window:
            emotion_window.pop(0)
        try:
            emotion_mode = mode(emotion_window)
        except:

            continue

        color = np.asarray((255, 255, 255))
        
        color = color.astype(int)
        color = color.tolist()

        draw_bounding_box(face_coordinates, rgb_image, color)
        draw_text(face_coordinates, rgb_image, emotion_mode,
                  color, 0, -45, 1, 1)
        print(emotion_mode)
        
    bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
    cv2.imshow('Emotion Detection', bgr_image)
    if(emotion_mode=='angry' or emotion_mode == 'sad'):
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


from tkinter import *
import time
from pygame import mixer
from textblob import TextBlob

import random


window = Tk()
frame = Frame(window, width=800, height=700)
frame.configure(background="#ffff8f")

##C = Canvas(window, bg="blue", height=250, width=300)
##filename = PhotoImage(file = "BLDC_Result.png")
##background_label = Label(window, image=filename)
##background_label.place(x=0, y=0, relwidth=1, relheight=1)

input_user = StringVar()
input_field = Entry(window, text=input_user)
input_field.pack(side=BOTTOM, fill=X)

global msg_num
msg_num = 0

def enter_pressed(event):
    global msg_num
    if(msg_num==0):
        input_get = input_field.get()
        print(input_get)
        label = Label(frame, text=input_get)
        label.config(fg="#0000ff")
        label.config(bg="#ffff8f")
        input_user.set('')
        label.pack()
        frame.update()
        time.sleep(1)
        input_get = input_field.get()
        print(input_get)
        label = Label(frame, text="Just Relax..!! I am Having Coffee..!! Would you like to have it..!!")
        label.config(fg="#ff0000")
        label.config(bg="#ffff8f")
        input_user.set('')
        label.pack()



    if(msg_num==1):
        
        input_get = input_field.get()
        print(input_get)
        p = 0
        if(input_get.find('no')!=-1):
            P = 0
        elif(input_get.find('not')!=-1):
            P = 0
        elif(input_get.find('nothing')!=-1):
            P = 0
        elif(input_get.find('don\'t')!=-1):
            P = 0
        elif(input_get.find('nope')!=-1):
            P = 0
        else:
            P = 1

        if(P == 0):
            label = Label(frame, text=input_get)
            label.config(fg="#0000ff")
            label.config(bg="#ffff8f")
            input_user.set('')
            label.pack()
            frame.update()
            time.sleep(1)
            input_get = input_field.get()
            print(input_get)
            label = Label(frame, text="Okay.. Then Let's have a talk . . . ! !")
            label.config(fg="#ff0000")
            label.config(bg="#ffff8f")
            input_user.set('')
            label.pack()
            frame.update()
        else:
            label = Label(frame, text=input_get)
            label.config(fg="#0000ff")
            label.config(bg="#ffff8f")
            input_user.set('')
            label.pack()
            frame.update()
            time.sleep(1)
            input_get = input_field.get()
            print(input_get)
            label = Label(frame, text="Then you can have it outside your office,hahaha . . ! !")
            label.config(fg="#ff0000")
            label.config(bg="#ffff8f")
            input_user.set('')
            label.pack()
            frame.update()

        input_get = input_field.get()
        print(input_get)
        label = Label(frame, text="Do u like party songs? I just love those . . . !")
        label.config(fg="#ff0000")
        label.config(bg="#ffff8f")
        input_user.set('')
        label.pack()
        frame.update()
######        mixer.init()
######        mixer.music.load('A.mp3')
######        mixer.music.play()

#############################################################################################################
    if(msg_num==2):
        input_get = input_field.get()
        print(input_get)
        p = 0
        if(input_get.find('no')!=-1):
            P = 0
        elif(input_get.find('not')!=-1):
            P = 0
        elif(input_get.find('nothing')!=-1):
            P = 0
        elif(input_get.find('don\'t')!=-1):
            P = 0
        elif(input_get.find('nope')!=-1):
            P = 0
        else:
            P = 1

        if(P == 0):
            label = Label(frame, text=input_get)
            label.config(fg="#0000ff")
            label.config(bg="#ffff8f")
            input_user.set('')
            label.pack()
            frame.update()
            time.sleep(1)
            input_get = input_field.get()
            print(input_get)
            label = Label(frame, text="Then let me play a good song for you.")
            label.config(fg="#ff0000")
            label.config(bg="#ffff8f")
            input_user.set('')
            label.pack()
            frame.update()
            song = str(random.randint(1,10))+'.mp3' # Random Song (just change number range according to song mood)
            print(song)
####            mixer.init()
####            mixer.music.load(song)
####            mixer.music.play()

        else:
            label = Label(frame, text=input_get)
            label.config(fg="#0000ff")
            label.config(bg="#ffff8f")
            input_user.set('')
            label.pack()
            frame.update()
            time.sleep(1)
            input_get = input_field.get()
            print(input_get)
            label = Label(frame, text="Then we should have met earlier than this. .")
            label.config(fg="#ff0000")
            label.config(bg="#ffff8f")
            input_user.set('')
            label.pack()
            frame.update()
            song = str(random.randint(1,10))+'.mp3' # Random Song (just change number range according to song mood)
            print(song)
######            mixer.init()
######            mixer.music.load(song)
######            mixer.music.play()
        label = Label(frame, text="It appears to me that u are sad today.Is it the case ?")
        label.config(fg="#ff0000")
        label.config(bg="#ffff8f")
        input_user.set('')
        label.pack()
        frame.update()

##############################################################################################################
    if(msg_num==3):
        input_get = input_field.get()
        print(input_get)
        label = Label(frame, text=input_get)
        label.config(fg="#0000ff")
        label.config(bg="#ffff8f")
        input_user.set('')
        label.pack()
        frame.update()
        time.sleep(1)
        p = 0
        if(input_get.find('no')!=-1):
            P = 0
        elif(input_get.find('not')!=-1):
            P = 0
        elif(input_get.find('nothing')!=-1):
            P = 0
        elif(input_get.find('don\'t')!=-1):
            P = 0
        elif(input_get.find('nope')!=-1):
            P = 0
        else:
            P = 1

        if(P == 1):
            label = Label(frame, text="Lets hear a joke :")
            label.config(fg="#0000ff")
            label.config(bg="#ffff8f")
            input_user.set('')
            label.pack()
            frame.update()
            time.sleep(1)

            num = random.randint(0,1) # change range as per number of jokes you have
            if(num==0):
                label = Label(frame, text="A man asks a farmer near a field, “Sorry sir, would you mind if I crossed your field instead of going around it? ")
                label.config(fg="#ff0000")
                label.config(bg="#ffff8f")
                input_user.set('')
                label.pack()
                frame.update()
                label = Label(frame, text="You see, I have to catch the 4:23 train.” The farmer says, “Sure, go right ahead. And if my bull sees you, you’ll even catch the 4:11 one.")
            elif(num==1):
                label = Label(frame, text="A teacher is talking to a student....  Teacher: Did your father help your with your homework? .... Student: No, he did it all by himself.")
            label.config(fg="#ff0000")
            label.config(bg="#ffff8f")
            input_user.set('')
            label.pack()
            frame.update()
            
        else:
            label = Label(frame, text=input_get)
            label.config(fg="#0000ff")
            label.config(bg="#ffff8f")
            input_user.set('')
            label.pack()
            frame.update()
            time.sleep(1)
            input_get = input_field.get()
            print(input_get)
            label = Label(frame, text="Good good,man should be happy all the time . .")
            label.config(fg="#ff0000")
            label.config(bg="#ffff8f")
            input_user.set('')
            label.pack()
            frame.update()


        label = Label(frame, text="Shall i take your leave . . ?")
        label.config(fg="#ff0000")
        label.config(bg="#ffff8f")
        input_user.set('')
        label.pack()
        frame.update()

        #############################################################################################################
##############################################################################################################
    if(msg_num==4):
        input_get = input_field.get()
        print(input_get)
        label = Label(frame, text=input_get)
        label.config(fg="#0000ff")
        label.config(bg="#ffff8f")
        input_user.set('')
        label.pack()
        frame.update()
        time.sleep(1)
        p = 0
        if(input_get.find('no')!=-1):
            P = 0
        elif(input_get.find('not')!=-1):
            P = 0
        elif(input_get.find('nothing')!=-1):
            P = 0
        elif(input_get.find('don\'t')!=-1):
            P = 0
        elif(input_get.find('nope')!=-1):
            P = 0
        else:
            P = 1

        if(P == 1):
            input_get = input_field.get()
            print(input_get)
            num = random.randint(0,2) # change range as per number of jokes you have
            if(num==0):
                label = Label(frame, text=" It was nice talking to you!! Be Happy...Bye Bye...")
            elif(num==1):
                label = Label(frame, text=" Have a good time bye")
            elif(num==2):
                label = Label(frame, text=" Hasta la vista...Be happy!!")

            label.config(fg="#ff0000")
            label.config(bg="#ffff8f")
            input_user.set('')
            label.pack()
            frame.update()
            
        else:
            input_get = input_field.get()
            print(input_get)
            label = Label(frame, text="Is there anything else you would like to share?")
            label.config(fg="#ff0000")
            label.config(bg="#ffff8f")
            input_user.set('')
            label.pack()
            frame.update()

        label = Label(frame, text="How was your day? was it good or bad?")
        label.config(fg="#ff0000")
        label.config(bg="#ffff8f")
        input_user.set('')
        label.pack()
        frame.update()


#############################################
##############################################################################################################
    if(msg_num==5):
        input_get = input_field.get()
        print(input_get)
        label = Label(frame, text=input_get)
        label.config(fg="#0000ff")
        label.config(bg="#ffff8f")
        input_user.set('')
        label.pack()
        frame.update()
        time.sleep(1)
        p = 0
        if(input_get.find('very bad')!=-1):
            P = 0
        elif(input_get.find('poor')!=-1):
            P = 0
        elif(input_get.find('worst')!=-1):
            P = 0
        elif(input_get.find('bad')!=-1):
            P = 0
        elif(input_get.find('nope')!=-1):
            P = 0
        else:
            P = 1

        if(P == 1):
            input_get = input_field.get()
            print(input_get)
            num = random.randint(0,2) # change range as per number of jokes you have
            if(num==0):
                label = Label(frame, text=" Thats nice")
            elif(num==1):
                label = Label(frame, text="ohh great")
            elif(num==2):
                label = Label(frame, text="well good for you")

            label.config(fg="#ff0000")
            label.config(bg="#ffff8f")
            input_user.set('')
            label.pack()
            frame.update()
            
        else:
           
            input_get = input_field.get()
            print(input_get)
            label = Label(frame, text="ohh..!! lets meditate for some time....it will help you calm your mind...open your youtube and play om meditation which will help you.")
            label.config(fg="#ff0000")
            label.config(bg="#ffff8f")
            input_user.set('')
            label.pack()
            frame.update()

        label = Label(frame, text="Can i recommend you to watch something?")
        label.config(fg="#ff0000")
        label.config(bg="#ffff8f")
        input_user.set('')
        label.pack()
        frame.update()



        #############################################################################################################
##############################################################################################################
    if(msg_num==6):
        input_get = input_field.get()
        print(input_get)
        label = Label(frame, text=input_get)
        label.config(fg="#0000ff")
        label.config(bg="#ffff8f")
        input_user.set('')
        label.pack()
        frame.update()
        time.sleep(1)
        input_get = input_field.get()
        print(input_get)
        p = 0
        if(input_get.find('no')!=-1):
            P = 0
        elif(input_get.find('not')!=-1):
            P = 0
        elif(input_get.find('nothing')!=-1):
            P = 0
        elif(input_get.find('don\'t')!=-1):
            P = 0
        elif(input_get.find('nope')!=-1):
            P = 0
        else:
            P = 1

        if(P == 1):
            input_get = input_field.get()
            print(input_get)
            num = random.randint(0,2) # change range as per number of jokes you have
            if(num==0):
                label = Label(frame, text=" You can watch the series known as \"FRIENDS\" which has been proven usefull for many youngesters to say goodbye to their sadness")
            elif(num==1):
                label = Label(frame, text=" you can watch the ellen show its a great inspirational and comedy show")
            elif(num==2):
                label = Label(frame, text=" you can watch commedy nights with kapil Im sure it will make you laugh a lot")

            label.config(fg="#ff0000")
            label.config(bg="#ffff8f")
            input_user.set('')
            label.pack()
            frame.update()
            
        else:
            label = Label(frame, text=input_get)
            label.config(fg="#0000ff")
            label.config(bg="#ffff8f")
            input_user.set('')
            label.pack()
            frame.update()
            time.sleep(1)
            input_get = input_field.get()
            print(input_get)
            label = Label(frame, text="okay!!Shall i take your leave ?")
            label.config(fg="#ff0000")
            label.config(bg="#ffff8f")
            input_user.set('')
            label.pack()
            frame.update()

        label = Label(frame, text="Are you feeling sick?")
        label.config(fg="#ff0000")
        label.config(bg="#ffff8f")
        input_user.set('')
        label.pack()
        frame.update()



        #############################################################################################################
##############################################################################################################
    if(msg_num==7):
        input_get = input_field.get()
        print(input_get)
        label = Label(frame, text=input_get)
        label.config(fg="#0000ff")
        label.config(bg="#ffff8f")
        input_user.set('')
        label.pack()
        frame.update()
        time.sleep(1)
        p = 0
        if(input_get.find('no')!=-1):
            P = 0
        elif(input_get.find('not')!=-1):
            P = 0
        elif(input_get.find('nothing')!=-1):
            P = 0
        elif(input_get.find('don\'t')!=-1):
            P = 0
        elif(input_get.find('nope')!=-1):
            P = 0
        else:
            P = 1

        if(P == 1):
            num = random.randint(0,1) # change range as per number of jokes you have
            if(num==0):
                label = Label(frame, text=" You should go to your nearest hospital and consult a doctor")
            elif(num==1):
                label = Label(frame, text=" You should call your family and tell them to take you to the hospital.")
        
            label.config(fg="#ff0000")
            label.config(bg="#ffff8f")
            input_user.set('')
            label.pack()
            frame.update()
            
        else:
            num = random.randint(0,1) # change range as per number of jokes you have
            if(num==0):
                label = Label(frame, text="thats fine then")
            elif(num==1):
                label = Label(frame, text="okay thats nice")
            label.config(fg="#ff0000")
            label.config(bg="#ffff8f")
            input_user.set('')
            label.pack()
            frame.update()

        label = Label(frame, text="I love to sing in my free time what do you like to do?")
        label.config(fg="#ff0000")
        label.config(bg="#ffff8f")
        input_user.set('')
        label.pack()
        frame.update()



        #############################################################################################################
##############################################################################################################
    if(msg_num==8):
        input_get = input_field.get()
        print(input_get)

        label = Label(frame, text=input_get)
        label.config(fg="#0000ff")
        label.config(bg="#ffff8f")
        input_user.set('')
        label.pack()
        frame.update()
        time.sleep(1)
##
        num = random.randint(0,2) # change range as per number of jokes you have
        if(num==0):
            label = Label(frame, text=" oh thats nice!!")
        elif(num==1):
            label = Label(frame, text=" amazing!!")
        elif(num==2):
            label = Label(frame, text="nice hobby")
    
        label.config(fg="#ff0000")
        label.config(bg="#ffff8f")
        input_user.set('')
        label.pack()
        frame.update()
        
        label = Label(frame, text="I hope your mood has been changed..So let's start the work again... !! Ba Bye .. !!")
        label.config(fg="#ff0000")
        label.config(bg="#ffff8f")
        input_user.set('')
        label.pack()
        frame.update()



    msg_num = msg_num + 1
    return "break"


def chatting():
    
    frame.pack_propagate(False) # prevent frame to resize to the labels size
    input_field.bind("<Return>", enter_pressed)
    frame.pack()
    name = ""
    input_get = input_field.get()
    print(input_get)
    label = Label(frame, text="Hello")
    label.config(fg="#ff0000")
    label.config(bg="#ffff8f")
    input_user.set('')
    label.pack()
    window.mainloop()


chatting()



