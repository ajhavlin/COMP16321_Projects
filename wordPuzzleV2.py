import random

alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def displayGrid():
    global grid,gridSize
    for i in range(gridSize):
        print('_'.join(grid[i]))

def getWords(gridSize):
    global myWords
    allWords=list(open('EnglishWords.txt'))
    for i in range(5):
        while True:
            newWord=random.choice(allWords).upper().strip()
            if (newWord not in myWords) and len(newWord)<gridSize:
                break    
        myWords.append(newWord)

gridSize=20
myWords=[]
getWords(gridSize)
grid=[['_' for i in range(gridSize)]for j in range(gridSize)]
directions=['up','down','left','right']

def placeWords():
    for word in myWords:
        wordLength=len(word)

        placed=False
        while not placed:

            direction=random.choice(directions)
            if direction=="down":
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
            colStart=random.randint(0,gridSize)
            rowStart=random.randint(0,gridSize)

            colEnd=colStart+wordLength*colStep
            rowEnd=rowStart+wordLength*rowStep

            if rowEnd<0 or rowEnd >= gridSize: continue
            if colEnd<0 or colEnd >= gridSize: continue

            failed=False

            for i in range(wordLength):
                character=word[i]
                newColStart=colStart+i*colStep
                newRowStart=rowStart+i*rowStep

                if grid[newRowStart][newColStart]!='_' and grid[newRowStart][newColStart]!=character:
                    failed=True
                    break

            if failed:
                continue
            else:
                for i in range(wordLength):
                    character=word[i]

                    newColStart=colStart+i*colStep
                    newRowStart=rowStart+i*rowStep

                    grid[newRowStart][newColStart]=character
                placed=True

placeWords()
displayGrid()

for i in range(gridSize):
    for j in range(gridSize):
        if grid[i][j]=='_':
            grid[i][j]=alphabet[random.randint(0,25)]

displayGrid()