from tkinter import Tk, Canvas
import random

def leftKey(event):
    global direction
    direction='left'
def rightKey(event):
    global direction
    direction='right'
def upKey(event):
    global direction
    direction='up'
def downKey(event):
    global direction
    direction='down'

def set_window_dimensions(w,h):
    window=Tk()
    window.title("Snake Game")
    screenW=window.winfo_screenwidth()
    screenH=window.winfo_screenheight()
    centerX=int(screenW/2-w/2) #startXCoord
    centerY=int(screenH/2-h/2) #startYCoord
    window.geometry(f'{w}x{h}+{centerX}+{centerY}')
    return window

def placeFood():
    global food,food_x,food_y
    food=canvas.create_rectangle(0,0,40,40,fill='red')
    food_x=random.randint(0,width-40)
    food_y=random.randint(0,height-40)
    canvas.move(food,food_x,food_y)

def init_snake():
    global head,body
    body=canvas.create_rectangle(-100,-100,-60,-60,fill='grey')
    head=canvas.create_rectangle(-100,-100,-60,-60,fill='white')
    snake.append(head)

def move_food():
    global food,food_x,food_y
    canvas.move(food,(food_x*(-1)),(food_y*(-1)))   #moves back to original starting position
    food_x=random.randint(0,width-40)
    food_y=random.randint(0,height-40)
    canvas.move(food,food_x,food_y)

def overlapping(a,b):
    if a[0]<b[2] and a[2]>b[0] and a[1]<b[3] and a[3]>b[1]:
        return True
    return False

def move_snake():
    global positions,snake,direction,score
    canvas.pack()
    positions=[]

    head_coords=canvas.coords(snake[0])
    positions.append(head_coords)
    print(positions)
    if head_coords[2]>=550:
        canvas.coords(snake[0],0,head_coords[1],40,head_coords[3])
    elif head_coords[0]<=0:
        canvas.coords(snake[0],510,head_coords[1],550,head_coords[3])
    #head_coords=canvas.coords(snake[0])
    elif head_coords[3]>=550:
        canvas.coords(snake[0],head_coords[0],0,head_coords[2],40)
    elif head_coords[1]<=0:
        canvas.coords(snake[0],head_coords[0],510,head_coords[2],550)

    if direction=='left':
        canvas.move(snake[0],-40,0)
    elif direction=='right':
        canvas.move(snake[0],40,0)
    elif direction=='up':
        canvas.move(snake[0],0,-40)
    elif direction=='down':
        canvas.move(snake[0],0,40)

    positions.clear()
    head_coords=canvas.coords(snake[0])
    food_coords=canvas.coords(food)
    positions.append(head_coords)  
    if overlapping(head_coords,food_coords):
        move_food()
        score+=1
        canvas.itemconfigure(scoreText,text=f'Score: {score}')

    window.after(1000,move_snake)
    




width=550
height=550

window=set_window_dimensions(width,height)
canvas=Canvas(window,width=width,height=height,bg='black')
snake=[]
snake_size=40
score=0

init_snake()

scoreText=canvas.create_text(70,20,text=f'Score: {score}',fill='white',font=('Helvetica','20','bold'))
canvas.bind('<Left>',leftKey)
canvas.bind('<Right>',rightKey)
canvas.bind('<Up>',upKey)
canvas.bind('<Down>',downKey)
canvas.focus_set()

direction='right'

placeFood()

move_snake()

window.mainloop()