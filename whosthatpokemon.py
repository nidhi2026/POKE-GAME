# WHO'S THAT POKEMON --> ARE YOU READY TO TEST YOUR POKEMON SKILLS !

# Imports here
import requests
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO
import pandas as pd
import random

# Accessing poke-data
pokemondb = pd.read_csv('poke_db.csv')
pokemon=[]

for i in range(15):
    pokemon.append(pokemondb.loc[random.randint(0,999)])

HEIGHT,WIDTH=700,800
SCORE = 0

# Creating gui
root = tk.Tk()
root.title("who's that pokemon?")
screen_width = root.winfo_screenwidth()  
screen_height = root.winfo_screenheight() 
x = (screen_width/2) - (WIDTH/2)
y = (screen_height/2) - (HEIGHT/2)

root.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, x, y))

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

# End Frame
def end_frame(score):
    global wtp_img, pokemon
    pokemon=[]
    for i in range(15):
        pokemon.append(pokemondb.loc[random.randint(0,999)])

    exit_frame = tk.Frame(root, bg='#800000')
    exit_frame.place(relwidth=1,relheight=1)

    wtp_img = tk.PhotoImage(file='wtp.png')
    wtp_logo = tk.Label(exit_frame, image=wtp_img, bg='#800000')
    wtp_logo.place(relx=0,rely=0,relheight=4/7,relwidth=1)

    high_score = tk.Label(exit_frame, text="Total Score: {}".format(score),font=('Raleway',50), bg='#ff9999',border=50,borderwidth=50)
    high_score.place(relx=0.5/4,rely=4/7,relheight=1.5/7,relwidth=3/4)

    play_again = tk.Button(exit_frame, text='Play Again',command = lambda: load_frame1(0),font=('Raleway',25), bg='#35bebe', fg='#000000', activebackground='#004b48', cursor='hand2',activeforeground='#ffffff', border=10, borderwidth=10, padx=10)
    play_again.place(relx=0.5/4,rely=5.5/7,relheight=1.45/7,relwidth=3/4)

# Welcome Frame
def load_frame1(ind):
    global wtp_img
    welcome_frame = tk.Frame(root, bg='#800000')
    welcome_frame.place(relwidth=1,relheight=1)

    wtp_img = tk.PhotoImage(file='wtp.png')
    wtp_logo = tk.Label(welcome_frame, image=wtp_img, bg='#800000')
    wtp_logo.place(relx=0,rely=0,relheight=4/7,relwidth=1)
    text_btn = 'Next Level'
    if(ind==0): text_btn = 'Play Again'
    play_button = tk.Button(welcome_frame, text=text_btn,command=lambda: load_frame2(ind+1,0),font=('Raleway',54), bg='#35bebe', fg='#000000', activebackground='#004b48', cursor='hand2',activeforeground='#ffffff', border=25, borderwidth=45, padx=15)
    play_button.place(relx=0.5/4,rely=4.5/7,relheight=1/4,relwidth=3/4)

# Check Answer
def check_answer(name_input,ind,status_label,score_label,submit_button,score):
    global SCORE
    if((name_input.get()).lower()==(pokemon[ind]['name']).lower() or ((pokemon[ind]['name']).lower().split('-')[0]==(name_input.get()).lower())):
        status_label.config(text='Status: correct',bg='#1aff1a')
        score+=10
        score_label.config(text='Score: {}'.format(score))
    else:
        status_label.config(text='Status: wrong {}'.format(pokemon[ind]['name']),bg='#ff0000')
    if(ind==14): 
        SCORE+=(score)
        submit_button.config(text='Completed',command = lambda: end_frame(SCORE))
    elif((ind+1)%5!=0): 
        submit_button.config(text='Next',command=lambda: load_frame2(ind+1,score))
    else: 
        submit_button.config(text='Finish',command = lambda: load_frame1(ind))
        SCORE+=(score)


# Play Frame
def load_frame2(ind,score):
    global pokemon_images
    poke_frame = tk.Frame(root, bg="#32bebe")
    poke_frame.place(relwidth=1,relheight=1)

    poke_label = tk.Label(poke_frame, text = "Who's That Pokemon !",font=('Raleway',int((root.winfo_screenheight())*0.055)),bg="#800000",fg="#ffffff",)
    poke_label.place(relx=0,rely=0,relwidth=1,relheight=(190/700))


    sep_line = tk.Frame(poke_frame, bg='#000000')
    sep_line.place(relx=0,rely=190/700,relheight=35/700,relwidth=1)

    if((ind+1)%5==0): level = (ind+1)//5
    else: level = ind//5 + 1
    score_label = tk.Label(sep_line, fg='#ffffff', bg='#000000',text='Level: {}  Score: {}'.format(level, score), font=('Raleway',25))
    status=''
    score_label.place(relheight=0.9,relwidth=0.45)
    status_label = tk.Label(sep_line, fg='#ffffff', bg='#000000', text='Status: {}'.format(status), font=('Raleway',25))
    status_label.place(relx=0.4,relheight=1,relwidth=0.6)


    image_url = pokemon[ind]['img']
    response_img = requests.get(image_url)
    image = Image.open(BytesIO(response_img.content))
    pokemon_images = ImageTk.PhotoImage(image)
    poke_img = tk.Label(poke_frame, image=pokemon_images)
    poke_img.place(relx=0,rely=225/700,relheight=475/700,relwidth=475/800)

    info_frame = tk.Frame(poke_frame)
    info_frame.place(relx=475/800,rely=225/700,relheight=475/700, relwidth=325/800)

    name_input = tk.Entry(info_frame, font=('Raleway',25),bg='#800000',fg='#ffffff',insertbackground='#ffffff')
    name_input.place(relx=0,rely=0,relheight=75/475,relwidth=1)

    submit_button = tk.Button(info_frame,text='Submit',command = lambda: check_answer(name_input,ind,status_label,score_label,submit_button,score),font=('Raleway',20),bg='#400000',fg='#ffffff', activebackground='#600000', activeforeground='#ffffff', border=1, borderwidth=1, padx=15,pady=5)
    submit_button.place(relx=0,rely=75/475,relheight=50/475,relwidth=1)

    types_label = tk.Label(info_frame, font=('Raleway',30),text='Types')
    types_label.place(relx=0,rely=125/475,relheight=50/475,relwidth=1)

    types_info = tk.Label(info_frame, font=('Raleway',20),text='\n'.join((pokemon[ind]['type']).replace('[','').replace(']','').replace('\'', '').split(', ')),bg='#800000',fg='#ffffff',anchor='center')
    types_info.place(relx=0,rely=175/475,relheight=130/475,relwidth=1)

    moves_label = tk.Label(info_frame, font=('Raleway',30),text='Moves')
    moves_label.place(relx=0,rely=305/475,relheight=50/475,relwidth=1)

    moves_info = tk.Label(info_frame, font=('Raleway',15),text='\n'.join((pokemon[ind]['moves']).replace('[','').replace(']','').replace('\'', '').split(', ')),bg='#800000',fg='#ffffff',anchor='center')
    moves_info.place(relx=0,rely=355/475,relheight=120/475,relwidth=1)
        

# Welcome Frame
welcome_frame = tk.Frame(root, bg='#800000')
welcome_frame.place(relwidth=1,relheight=1)

wtp_img = tk.PhotoImage(file='wtp.png')
wtp_logo = tk.Label(welcome_frame, image=wtp_img, bg='#800000')
wtp_logo.place(relx=0,rely=0,relheight=4/7,relwidth=1)

play_button = tk.Button(welcome_frame, text='Play', font=('Raleway',54), bg='#35bebe', fg='#000000', activebackground='#004b48', cursor='hand2',activeforeground='#ffffff', border=25, borderwidth=45, padx=15,command=lambda: load_frame2(0,0))
play_button.place(relx=1/4,rely=4.5/7,relheight=1/4,relwidth=2/4)

root.mainloop()