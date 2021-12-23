import random 
import numpy as np


cloneMatricies = {
    "cloneMatrix" : [[1,1],[1,0],[1,-1],[0,1],[0,-1],[-1,1],[-1,0],[-1,-1]],
    "topcloneMatrix" : [[0,-1],[0,1],[1,-1],[1,0],[1,1]],
    "leftcloneMatrix": [[-1,0],[-1,1],[0,1],[1,0],[1,1]],
    "tlccloneMatrix": [[0,1],[1,0],[1,1]]
}

def printboard(board,xaxis):
    n = 1
    print ("\n"+xaxis)
    for i in board:
        print(f"{n} {i} {n}")
        n += 1
    print (xaxis+"\n")


def board (height,width):
    map = []
    for i in range(height):
        array = []
        for j in range(width):
            array.append(" ")
        map.append(array)
    return np.array(map)


def mapgenerate (height, width, bombs):
    map = []
    for i in range(height):
        array = []
        for j in range(width):
            array.append(0)
        map.append(array)
    
    bombsCoordinate = random.sample(range(height*width), bombs)
    bombsLocation = []
    for i in bombsCoordinate:
        bomby = i//width
        bombx = i%width
        map[bomby][bombx] = "B"
        bombsLocation.append([bomby,bombx])

    for i in bombsLocation:
        if i[0]+i[1] == 0:
            for j in cloneMatricies["tlccloneMatrix"]:
                try:
                    if map[i[0]+j[0]][i[1]+j[1]] != "B":
                        map[i[0]+j[0]][i[1]+j[1]] += 1
                except:
                    continue
        elif i[0] == 0 and i[1] != 0:
            for j in cloneMatricies["topcloneMatrix"]:
                try:
                    if map[i[0]+j[0]][i[1]+j[1]] != "B":
                        map[i[0]+j[0]][i[1]+j[1]] += 1
                except:
                    continue
        elif i[1]==0 and i[0] != 0:
            for j in cloneMatricies["leftcloneMatrix"]:
                try:
                    if map[i[0]+j[0]][i[1]+j[1]] != "B":
                        map[i[0]+j[0]][i[1]+j[1]] += 1
                except:
                    continue
        else:
            for j in cloneMatricies["cloneMatrix"]:
                try:
                    if map[i[0]+j[0]][i[1]+j[1]] != "B":
                        map[i[0]+j[0]][i[1]+j[1]] += 1
                except:
                    continue

    formattedMap = np.array(map)
    return (formattedMap,bombsCoordinate.sort())


def zerosearch(solution, coordinate, board):
    y, x = coordinate[0]-1, coordinate[1]-1
    if y+x == 0:
        for i in cloneMatricies["tlccloneMatrix"]:
            try: 
                if int(solution[y+i[0]][x+i[1]]) == 0 and str(board[y+i[0]][x+i[1]]) == " ":
                    board [y+i[0]][x+i[1]] = 0
                    board = zerosearch(solution,[y+i[0]+1,x+i[1]+1],board)
                elif int(solution [y+i[0]][x+i[1]]) > 0:
                    board [y+i[0]][x+i[1]] = solution[y+i[0]][x+i[1]]
                else:
                    continue
            except:
                continue
    elif y == 0 and x != 0: 
        for i in cloneMatricies["topcloneMatrix"]:
            try: 
                if int(solution[y+i[0]][x+i[1]]) == 0 and str(board[y+i[0]][x+i[1]]) == " ":
                    board [y+i[0]][x+i[1]] = 0
                    board = zerosearch(solution,[y+i[0]+1,x+i[1]+1],board)
                elif int(solution [y+i[0]][x+i[1]]) > 0:
                    board [y+i[0]][x+i[1]] = solution[y+i[0]][x+i[1]]
                else:
                    continue
            except:
                continue
    elif y != 0 and x == 0: 
        for i in cloneMatricies["leftcloneMatrix"]:
            try: 
                if int(solution[y+i[0]][x+i[1]]) == 0 and str(board[y+i[0]][x+i[1]]) == " ":
                    board [y+i[0]][x+i[1]] = 0
                    board = zerosearch(solution,[y+i[0]+1,x+i[1]+1],board)
                elif int(solution [y+i[0]][x+i[1]]) > 0:
                    board [y+i[0]][x+i[1]] = solution[y+i[0]][x+i[1]]
                else:
                    continue
            except:
                continue
    else: 
        for i in cloneMatricies["cloneMatrix"]:
            try: 
                if int(solution[y+i[0]][x+i[1]]) == 0 and str(board[y+i[0]][x+i[1]]) == " ":
                    board [y+i[0]][x+i[1]] = 0
                    board = zerosearch(solution,[y+i[0]+1,x+i[1]+1],board)
                elif int(solution [y+i[0]][x+i[1]]) > 0:
                    board [y+i[0]][x+i[1]] = solution[y+i[0]][x+i[1]]
                else:
                    continue
            except:
                continue
    return board

            
while 1: 
    try:
        boardsize = input("How big is your board? (height,width,#bombs) (min: 2,2,1; max 9,9,81) (suggested: 9,9,10)\n")
        if boardsize == "end":
            "GG! Thanks for playing!"
            break
        else:
            dimensions = boardsize.split(",")
            if (int(dimensions[0])*int(dimensions[1]))<int(dimensions[2]):
                raise Exception
            elif int(dimensions[0])<=1 or int(dimensions[1])<=1:
                raise Exception
            elif int(dimensions[0])>9 or int(dimensions[1])>9:
                raise Exception
            else:
                height, width, bombs = int(dimensions[0]), int(dimensions[1]), int(dimensions[2])
                break
    except:
        print ("Format Error: Invalid dimensions or #Bombs \n")


columns = "123456789"
draftxaxis = []
for i in range(width):
    draftxaxis.append(columns[i])

xaxis = "    "+"   ".join(draftxaxis)

if boardsize != "end":
    [solution, bombsCoordinate] = mapgenerate (height, width, bombs) 
    board = board(height,width)
    printboard(board,xaxis)


    while True:
        #this part checks how many flags you have and see if you got the solution right
        flags = []
        flagcounter = 0
        for i in enumerate(board):
            for j in enumerate(i[1]):
                if j[1] == 'f':
                    flagcounter += 1
                    flags.append(i[0]*j[0])
                elif j[1] == " ":
                    flags.append(i[0]*j[0])
        if len(flags) == bombs:
            if flags.sort() == bombsCoordinate:
                print("GG! You Win!")
                break 
        elif flagcounter>bombs:
            print("Watch out! You've flagged more times than there are bombs!!")
        else:
            print(f"There are {bombs-flagcounter} bombs left.")



        choice = input('What block would you like to break?(format: yx; top left is "11" for ex; fyx to flag; input "end" to end; "solution" to see solution + end)')            
        if choice == "end":
            print("GG! Thanks for playing!")
            break
        elif choice == "solution":
            printboard(solution,xaxis)
            print("GG! Thanks for playing!")
            break
        elif len(choice)>2 and choice[0]!="f":
            try:
                n = 0
                points = choice.split()
                for i in points:
                    y,x = int(i[0]), int(i[1])
                    if solution[y-1,x-1] == "B":
                        n+=1
                        board[y-1,x-1] = solution[y-1,x-1]
                    elif int(solution[y-1,x-1]) == 0:
                        board[y-1,x-1] = solution[y-1,x-1]
                        board = zerosearch(solution,[int(y),int(x)],board)
                    else:
                        board[y-1,x-1] = solution[y-1,x-1]
                printboard(board,xaxis)
                if n>0:
                    print("GG, you fucked! Thanks for playing!")
                    break
            except:
                print ("Format Error: Invalid dimensions\n")
        else:
            try:
                if choice[0] == "f" and len(choice)==3:
                    board[int(choice[1])-1,int(choice[2])-1] = "f"
                elif choice[0] == "f" and len(choice)>3:
                    flags = choice.split()
                    board[int(choice[1])-1,int(choice[2])-1] = "f"
                    for i in enumerate(flags):
                        if i[0] != 0:
                            board[int(i[1][0])-1,int(i[1][1])-1] = "f"
                else:
                    y,x = int(choice[0]), int(choice[1])
                    if solution[y-1,x-1] == "B":
                        board[y-1,x-1] = "B"
                        print("GG, you fucked! Thanks for playing!")
                        break
                    elif solution[y-1,x-1] == "0":
                        board[y-1,x-1] = solution[y-1,x-1]
                        board = zerosearch(solution,[int(y),int(x)],board)
                    else: 
                        board[y-1,x-1] = solution[y-1,x-1]
            except:
                print ("Format Error: Invalid dimensions\n")
            finally:
                printboard(board,xaxis)

