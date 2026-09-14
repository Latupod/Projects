import turtle as t
from math import sqrt

screen = t.Screen()
size = 440
screen.setup(size,size)
canmovestatus = True

#chunks = [f"MapChunking\GroundFloor\Third Chunk Iteration\Ground Floor Chunk {x}.PNG" for x in range(1,50)]
#chunks = [f"MapChunking\GroundFloor\Second Chunk Iteration\Ground Floor Chunk {x}.PNG" for x in range(1,17)]
chunks = [f"plsplspls help me\plsplsplspls helm eme {x}.PNG" for x in range(1,55)]

t = t.Turtle()
t.speed("fastest")

currentchunk = 23 - 1 
t.screen.bgpic(chunks[currentchunk])

testinput = t.screen.textinput("TEST","This is just a test input it does nothing")
if testinput.lower() == "quit":
    quit()
t.penup()
t.setpos(60,-170)
t.pensize(3)

movebyd =5
t.shape("turtle")
t.pencolor("red")

def up():
    global canmovestatus
    if canmovestatus == True:
        #print("recieived up")
        t.setheading(90)
        t.fd(movebyd)
        canmovestatus = True
        checkforcollision()
    

def down():
    global canmovestatus
    if canmovestatus == True:
        #print("recieved down")
        t.setheading(270)
        t.fd(movebyd)
        checkforcollision()

def left():
    global canmovestatus
    if canmovestatus == True:
        #print("recieved left")
        t.setheading(180)
        t.fd(movebyd)
        checkforcollision()

def right():
    global canmovestatus
    if canmovestatus == True:
        #print("recieved right")
        t.setheading(0)
        t.fd(movebyd)
        checkforcollision()

def getpos():
    print(f"Turtle position: {t.pos()}")
    print(f"Turtle chunk: {currentchunk+1}")

#int(sqrt(len(chunks))) #magical square stuff

def checkforcollision():
    global currentchunk,canmovestatus
    position = t.pos()
    if position[0] >= (size/2 - 5):
        canmovestatus = False
        newchunk = (currentchunk + 1)%len(chunks)
        currentchunk = newchunk
        t.screen.bgpic(chunks[currentchunk])
        t.clear()
        t.penup()
        t.setpos(-position[0]+movebyd,position[1])
        t.pendown()
        canmovestatus = True
    if position[1] <= -(size/2 -5):
        canmovestatus = False
        newchunk = (currentchunk - 9)%len(chunks)
        currentchunk = newchunk
        t.screen.bgpic(chunks[currentchunk])
        t.clear()
        t.penup()
        t.setpos(position[0],-position[1]-movebyd)
        t.pendown()
        canmovestatus = True
    if position[0] <= -(size/2 -5):
        canmovestatus = False
        newchunk = (currentchunk - 1)%len(chunks)
        currentchunk = newchunk
        t.screen.bgpic(chunks[currentchunk])
        t.clear()
        t.penup()
        t.setpos(-position[0]-movebyd,position[1])
        t.pendown()
        canmovestatus = True
    if position[1] >= (size/2 - 5):
        canmovestatus = False
        newchunk = (currentchunk + 9)%len(chunks)
        currentchunk = newchunk
        t.screen.bgpic(chunks[currentchunk])
        t.clear()
        t.penup()
        t.setpos(position[0],-position[1]+movebyd)
        t.pendown()
        canmovestatus = True

def clearscreen():
    t.clear()

def enablemovement():
    global canmovestatus
    canmovestatus = False

def undolast():
    t.undo()

t.screen.onkeypress(up,"w")
t.screen.onkeypress(down,"s")
t.screen.onkeypress(left,"a")
t.screen.onkeypress(right,"d")
t.screen.onkeypress(getpos,"space")
t.screen.onkeypress(clearscreen,"c")
t.screen.onkeypress(undolast,"b")
# t.screen.onkeyrelease(enablemovement,"w")
# t.screen.onkeyrelease(enablemovement,"a")
# t.screen.onkeyrelease(enablemovement,"s")
# t.screen.onkeyrelease(enablemovement,"d")
t.screen.listen()
t.pendown()
t.screen.mainloop()