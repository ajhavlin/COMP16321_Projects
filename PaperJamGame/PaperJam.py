from tkinter import Tk,Canvas,Menu,messagebox,PhotoImage
from random import randint as rand, choice

# classes -----------------------
class paper(): #the enemy class
    def __init__(self,size,damage,health,speed): 
        self.__size=size
        self.__dps=damage
        self.__health=health
        self.__speed=speed

        self.__paper=canvas.create_rectangle(0,0,self.__size*1.201,self.__size,outline= 'black', width=3,fill='white')
        paper_x=rand(250,960-self.__size) #define the region in which a paper could be spawned based on background
        paper_y=rand(0,400-self.__size)
        canvas.move(self.__paper,paper_x,paper_y)

    #setters
    def setSize(self,size):
        self.__size=size
    def setHealth(self,damageTaken):
        self.__health-=damageTaken

    #getters
    def getPaper(self):
        return self.__paper
    def getSize(self):
        return self.__size
    def getDps(self):
        return self.__dps
    def getHealth(self):
        return self.__health
    def getSpeed(self):
        return self.__speed

class printer(): #define the player class
    def __init__(self):
        self.__damage=1
        self.__health=65

    #setters
    def setDps(self,damage):
        self.__damage=damage
    def setHealth(self,health):
        self.__health=health
    
    #getters
    def getDps(self):
        return self.__damage
    def getHealth(self):
        return self.__health



# procedures -------------------------
def setWindowDimensions(w,h):
    window=Tk()
    window.title("Paper Jam")
    screenW=window.winfo_screenwidth()
    screenH=window.winfo_screenheight()
    centerX=int(screenW/2-w/2) #startXCoord
    centerY=int(screenH/2-h/2-50) #startYCoord
    window.geometry(f'{w}x{h}+{centerX}+{centerY}')
    window.resizable(False,False) #not resizable in x or y
    return window

def createScene(): #initialise the background attributes
    global scoreText, score, healthText, player, waveNumber, waveText
    canvas.create_rectangle(0,0,250,540,fill='#FFFDD0')
    canvas.create_rectangle(30,10,220,100,fill='#A5846A')
    canvas.create_rectangle(0,240,250,540,fill='#BB9059')
    canvas.create_rectangle(0,400,960,560,fill='#f0f8ff')
    scoreText=canvas.create_text(125,25,text=f'Score: {score}',fill='white',font=('Helvetica','20','bold'))
    healthText=canvas.create_text(125,55,text=f'Health: {player.getHealth()}',fill='white',font=('Helvetica','20','bold'))
    waveText=canvas.create_text(125,85,text=f'Wave Num: {waveNumber}',fill='white',font=('Helvetica','20','bold'))

    createMenu()

def createMenu():
    menuBar=Menu(window)
    window.config(menu=menuBar)

    options=Menu(menuBar,tearoff=False) #remove the dashed line

    menuBar.add_command(label='Pause',command=pauseUnpause) 
    #options.add_separator()
    options.add_command(label='Save',command=saveGame)
    #options.add_separator()
    options.add_command(label='Color Blind Mode',command=colorBlind) # configured for deuterenope
    #options.add_separator()
    options.add_command(label='Cheats',command=window.destroy) # this one will kill the program as a joke
    #options.add_separator()
    options.add_command(label='Exit',command=cheater)
    menuBar.add_cascade(label="Menu",menu=options)

def colorBlind():
    global colorBlindMode
    colorBlindMode=True

def pauseUnpause():
    global pause
    if pause==False:
        pause=True
    else:
        pause=False
        movePaper()

def bossKey(event):
    global pause
    if str(event)[1:6]=='Leave':
        pause=True
    else:
        pause=False
        movePaper()
    
def cheater():
    global player, healthText
    messagebox.showinfo('Cheats', 'Haha you thought this would give you the cheats')
    messagebox.showinfo('Cheats', 'Jk lol.')
    cheatCode=input("Enter a cheatcode or type 'help' ")
    if cheatCode=='help':
        messagebox.showinfo('Cheats', 'The codes are: "givemehealth", and "fatality"')
    elif cheatCode=='givemehealth':
        player.setHealth(1000000)
        canvas.itemconfigure(healthText,text=f'Health: {player.getHealth()}')
    elif cheatCode=='fatality':
        player.setDps(1000000)



def spawnPaper(size=40,damage=1,health=1,speed=1): #default values
    global papers, waveNumber, score, waveText

    if ((score)//10)==waveNumber: #increment waves every 10 points
        waveNumber=((score+1)//10)+1
        canvas.itemconfigure(waveText,text=f'Wave Num: {waveNumber}')

    multiplier=rand(1,min(4,waveNumber)) #update depending on the wave of enemies
    newPaper=paper(multiplier*40,multiplier,multiplier,1.5-multiplier*.28)
    papers.append(newPaper) 

def movePaper():
    global papers, player, healthText,pause, moveAgain
    if pause==False:
        for thisPaper in papers:
            canvas.pack()

            # move the paper
            distance=(thisPaper.getSpeed())*10
            pos=canvas.coords(thisPaper.getPaper())
            if (pos[0]-distance)<=250:
                canvas.coords(thisPaper.getPaper(),250,pos[1],250+thisPaper.getSize(),pos[3])
                player.setHealth(player.getHealth()-thisPaper.getDps())
                canvas.itemconfigure(healthText,text=f'Health: {player.getHealth()}')
            else:
                canvas.move(thisPaper.getPaper(),-distance,0)

            # game over!
            if player.getHealth()<=0:
                printJam=True
                canvas.after_cancel(moveAgain) # stop the loop running again
                if rand(0,1)==0: #generate a game over message
                    message=f'Oh no! The printer is jammed.\nYour Score was {score}'
                else:
                    message=f'Paper jam! Could have prevented that one.\nYour Score was {score}'

                messagebox.showinfo('Printer Jammed!', message)
                break # i had trouble figuring out that i needed this break but it is here because we dont need it to run for all papers if the player is already dead
        
                #canvas.create_text(960/2,540/3,fill='black',font=('Helvetica','50','bold'),text='Game Over!')

        if 'printJam' not in locals():
            if rand(1,6)==1: # randomly spawn new papers
                spawnPaper()
            moveAgain=canvas.after(370,movePaper) # move the paper again
        else:
            window.destroy()
            saveGame() # save game progress



def inkJet(event):
    global ink, papers, player, score, scoreText, waveNumber, colorBlindMode
    
    inkBlobCoords=[event.x-20,event.y-20,event.x+20,event.y+20]
    if colorBlindMode==False:
        colors=['blue','#38e038','red']
    else: 
        colors=['#058ed9','#ff934f','#cc2d35'] # configured colors for deuteranopia
    

    # ------------ my attempt at adding ink droplett graphics -----------
    # inkBlobCoords=[event.x-20,event.y-20,event.x+20,event.y+20]
    # colors=['Blue','Green','Red']
    # if colorBlindMode==True:
    #     inkBlobImg=PhotoImage(file=f"inkBlob{choice(colors)}Deuteranope.png")
    # else: 
    #     inkBlobImg=PhotoImage(file=f"inkBlob{choice(colors)}.png")
    # inkBlob=canvas.create_image(inkBlobCoords[0],inkBlobCoords[1], image=inkBlobImg)
    
    inkBlob=canvas.create_rectangle(inkBlobCoords[0],inkBlobCoords[1],inkBlobCoords[2],inkBlobCoords[3],fill=f'{choice(colors)}')
    
    for thisPaper in papers:
        paperCoords=canvas.coords(thisPaper.getPaper())
        if (inkBlobCoords[0]<=paperCoords[2] and inkBlobCoords[2]>=paperCoords[0]) and (inkBlobCoords[1]<=paperCoords[3] and inkBlobCoords[3]>=paperCoords[1]):
            # add damage mechanism
            if thisPaper.getHealth()<=player.getDps():
                #score is calculated by the dps of a paper object
                score+=thisPaper.getDps()
                canvas.delete(thisPaper.getPaper())
                papers.remove(thisPaper)
                canvas.itemconfigure(scoreText,text=f'Score: {score}')
            else:
                thisPaper.setHealth(player.getDps())

    #update the inkBlobs on the canvas after 2.4s
    canvas.after(2400,deleteInkBlob)
    ink.append(inkBlob)

def deleteInkBlob():
    if len(ink)>0:
        canvas.delete(ink[0])
        ink.remove(ink[0])
    


def leaderboard():
    f=open('highscores.txt','r')
    playerStats=f.readlines()
    f.close()
    highestScores=[['ABC',0],['ABC',0],['ABC',0]]
    for thisPlayersStats in playerStats: #each thisPlayerStats is stored in the format: 'ABC*score*waveNumber*player.getDps()*player.getHealth()'
        playerName=thisPlayersStats.strip().split('*')[0]
        score=int(thisPlayersStats.strip().split('*')[1])
        if highestScores[2][1]<score:
            if highestScores[1][1]<score:
                if highestScores[0][1]<score:
                    highestScores[2],highestScores[1]=highestScores[1],highestScores[0]
                    highestScores[0]=[playerName,score]
                else:
                    highestScores[2]=highestScores[1]
                    highestScores[1]=[playerName,score]
            else:
                highestScores[2]=[playerName,score]
    
    canvas.create_text(480,470,text=f'High Scores:  {highestScores[0][0]} -> {highestScores[0][1]}   {highestScores[1][0]} -> {highestScores[1][1]}   {highestScores[2][0]} -> {highestScores[2][1]} ',fill='black',font=('Helvetica','25','bold'))

def saveGame():
    global score,player,waveNumber,username
    
    newSave=f'{username}*{score}*{waveNumber}*{player.getDps()}*{player.getHealth()}'
    # save the data in the file
    f=open('highscores.txt','a')
    f.write('\n')
    f.write(newSave)
    f.close()

def loadGame():
    global player, username
    username=input("Enter your initials e.g. 'ABC' :").upper()
    while len(username)!=3 and username[0].isdigit()==False:
        username=input("Enter your initials e.g. 'ABC' :").upper()
    
    startNew=input("Would you like to start new game: 'y'")

    if startNew!='y':
        playerSaves=[]
        f=open('highscores.txt','r')
        for line in f: # each line is stored in the format: 'ABC*score*waveNumber*player.getDps()*player.getHealth()'
            thisPlayerStats=line.strip().split('*')
            playerName=thisPlayerStats[0]
            if username==playerName and int(thisPlayerStats[4])>0:
                playerSaves.append(thisPlayerStats[1::]) # gets everything but the playername
        f.close()

        player=printer() # init player class
        if playerSaves!=[]:
            for index, playerSave in enumerate(playerSaves):
                print(f'[{index}] <= Wave: {playerSave[1]}, Score: {playerSave[0]}')
            thisSave=playerSaves[int(input("Enter the index of the save you would like to load"))]
            player.setDps(thisSave[2])
            player.setHealth(thisSave[3])
            return (int(thisSave[0]),int(thisSave[1])) # score, wavenum
    else:
        return (0,1)



# main code --------------------------------------------
papers=[]
ink=[]
score,waveNumber=loadGame()
pause=False
colorBlindMode=False
#the size i want the window to be:
#windowed fullscreen was omitted due to differing screen resolutions on lab machines
width=960
height=540

window=setWindowDimensions(width,height)
canvas=Canvas(window,width=width,height=height,bg='white')
    
player=printer()

# decorate the environment 
createScene()
printerImage=PhotoImage(file="Printer.png")
canvas.create_image(125, 200, image=printerImage)
bg=PhotoImage(file="bg.png")
canvas.create_image(605, 77, image=bg)
colors=[PhotoImage(file="inkBlobBlue.png"),PhotoImage(file="inkBlobGreen.png"),PhotoImage(file="inkBlobRed.png")]
for i in range(9):
    canvas.create_image(rand(0,960),rand(440,540), image=choice(colors))
leaderboard()
canvas.pack()

spawnPaper() # let the game begin! :)
movePaper()

# mappings
canvas.bind('<Button-1>', inkJet)
canvas.bind('<Leave>', bossKey)
canvas.bind('<Enter>', bossKey)

window.mainloop()