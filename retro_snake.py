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
    global head,snake
    head=canvas.create_rectangle(-100,-100,-60,-60,fill='white')
    snake.append(head)


def grow_snake():
    global direction,snake
    last_coords=canvas.coords(snake[len(snake)-1])
    new_body=canvas.create_rectangle(0,0,40,40,fill='#FDF3F3')
    if direction=='left':
        canvas.coords(new_body,last_coords[0]+40,last_coords[1],last_coords[2]+40,last_coords[3])
    elif direction=='right':
        canvas.coords(new_body,last_coords[0]-40,last_coords[1],last_coords[2]-40,last_coords[3])
    elif direction=='up':
        canvas.coords(new_body,last_coords[0],last_coords[1]+40,last_coords[2],last_coords[3]+40)
    elif direction=='down':
        canvas.coords(new_body,last_coords[0],last_coords[1]-40,last_coords[2],last_coords[3]-40)
    snake.append(new_body)

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
    if head_coords[2]>550:
        canvas.coords(snake[0],0,head_coords[1],40,head_coords[3])
    elif head_coords[0]<=0:
        canvas.coords(snake[0],510,head_coords[1],550,head_coords[3])
    #head_coords=canvas.coords(snake[0])
    elif head_coords[3]>550:
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
        grow_snake()
        score+=1
        canvas.itemconfigure(scoreText,text=f'Score: {score}')

    for i in range(1,len(snake)):
        if overlapping(head_coords, canvas.coords(snake[i])):
            game_over=True
            canvas.create_text(width/2,height/2,fill='white',font=('Helvetica','50','bold'),text='Game Over!')

    for i in range(1, len(snake)):
        positions.append(canvas.coords(snake[i]))
    for i in range(len(snake)-1):
        canvas.coords(snake[i+1],positions[i][0],positions[i][1],positions[i][2],positions[i][3])
    
    if 'game_over' not in locals():
        window.after(500,move_snake)
    




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