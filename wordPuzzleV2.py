import random

alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def displayGrid():
    global grid,gridSize
    for i in range(gridSize):
        print('_'.join(grid[i]))

def getWords(gridSize):
    global myWords
    #reads all words in the file
    allWords=list(open('EnglishWords.txt'))
    for i in range(5):
        while True:
            #gets a valid word from the list
            newWord=random.choice(allWords).upper().strip()
            if (newWord not in myWords) and len(newWord)<gridSize:
                break    
        myWords.append(newWord)

#ititalisation of grid size, list of words, grid, and the possible directions a word can be placed
#might extend directions to 'verticalLeftUp','verticalRightDown',etc
gridSize=20
myWords=[]
getWords(gridSize)
grid=[['_' for i in range(gridSize)]for j in range(gridSize)]
directions=['up','down','left','right']


def placeWords():
    #loops for each word in the list of valid words
    for word in myWords:
        wordLength=len(word)
        #the word has not been placed 
        placed=False
        while not placed:
            #choose a direction
            direction=random.choice(directions)
            if direction=="down":
                #the steps are used to specify the direction of the next letter to be placed
                rowStep=1
                colStep=0
            elif direction=="up":
                rowStep=-1
                colStep=0
            elif direction=="left":
                rowStep=0
                colStep=-1
            elif direction=="right":
                rowStep=0
                colStep=1
            #generate a random start position
            colStart=random.randint(0,gridSize)
            rowStart=random.randint(0,gridSize)
            #specify where the end position is to ensure it is valid
            colEnd=colStart+wordLength*colStep
            rowEnd=rowStart+wordLength*rowStep
            #check that the end position is valid
            #if not it will try the while loop again to regenerate a start and end position
            if rowEnd<0 or rowEnd >= gridSize: continue
            if colEnd<0 or colEnd >= gridSize: continue
            #neither of the if statements were run so it has NOT failed
            failed=False
            #loop for each character in the word and check if the entire word can be inserted before actually inserting it
            for i in range(wordLength):
                character=word[i]
                #location of current character insertion point
                newColStart=colStart+i*colStep
                newRowStart=rowStart+i*rowStep
                #if the location is occupied by a different character we fail which re-loops the while again
                if grid[newRowStart][newColStart]!='_' and grid[newRowStart][newColStart]!=character:
                    failed=True
                    break

            if failed:
                continue
            else:
                #word can be inserted successfully
                for i in range(wordLength):
                    character=word[i]
                    #get insertion point
                    newColStart=colStart+i*colStep
                    newRowStart=rowStart+i*rowStep
                    #insert the character
                    grid[newRowStart][newColStart]=character
                #word has been placed 
                placed=True

placeWords()
displayGrid()

#fill out the rest of the characters
for i in range(gridSize):
    for j in range(gridSize):
        if grid[i][j]=='_':
            grid[i][j]=alphabet[random.randint(0,25)]

displayGrid()