import tkinter as tk
from tkinter import messagebox
window=tk.Tk()
window.title=("my window")
#set size
#window.geometry('300x300')
windowWidth=300
windowHeight=300
##get screen dimension
screenWidth=window.winfo_screenwidth()
screenHeight=window.winfo_screenheight()
##find center
centerX=int(screenWidth/2 - windowWidth / 2)
centerY=int(screenHeight/2 - windowHeight / 2)
##set position and size
window.geometry(f'{windowWidth}x{windowHeight}+{centerX}+{centerY}')
window.resizable(False,False)
#window.minsize(minWidth,minHeight)
#window.maxsize(maxWidth,maxHeight)

#preload images
myButton=tk.PhotoImage(file='myButton.png')
myButtonP1=tk.PhotoImage(file='myButtonP1.png')
myButtonP2=tk.PhotoImage(file='myButtonP2.png')
winner=tk.PhotoImage(file='winner.png')

#functions
def createButtons():
    for i in range(3):
        for j in range(3):
            n=j+3*i
            newButton=tk.Button(image=myButton,width=100,height=100,command=lambda button_number=n+1: handle_button_click(button_number))
            squares[n]=newButton
            squares[n].place(x=j*100,y=i*100)
    print(squares)

def handle_button_click(button_number):
    global turn
    #print(button_number)
    #print(squares[button_number-1].cget('image'),myButton)
    if str(squares[button_number-1].cget('image'))==str(myButton):
        if turn=='r':
            squares[button_number-1].config(image=myButtonP1)
            turn='g'
            player1Moves.add(button_number)
        elif turn=='g':
            squares[button_number-1].config(image=myButtonP2)
            turn='r'
            player2Moves.add(button_number)
    else:
        #print('This square has already been selected, try again')
        messagebox.showinfo('Try again','This square has already been selected')
    for pos in winningPositions:
        if pos[0] in player1Moves and pos[1] in player1Moves and pos[2] in player1Moves:
            winButton=tk.Label(window,image=winner,width=300,height=100)
            winButton.grid(pady=70)
            messagebox.showinfo('The End','Red Player Wins')
            window.quit()
            break
        elif pos[0] in player2Moves and pos[1] in player2Moves and pos[2] in player2Moves:
            winButton=tk.Label(window,image=winner,width=300,height=100)
            winButton.grid(pady=70)
            messagebox.showinfo('The End','Green Player Wins')
            window.quit()
            break
#main
squares=[None for i in range(9)]
createButtons()
print(squares)
turn='r'
player1Moves=set()
player2Moves=set()
winningPositions=[[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9],[1,5,9],[3,5,7]]

window.mainloop()
