import turtle as t
from math import sqrt

screen = t.Screen()
size = 600
screen.setup(size,size)
canmovestatus = True

#chunks = [f"MapChunking\GroundFloor\Third Chunk Iteration\Ground Floor Chunk {x}.PNG" for x in range(1,50)]
chunks = [f"MapChunking\GroundFloor\Second Chunk Iteration\Ground Floor Chunk {x}.PNG" for x in range(1,17)]

# chunks = [
#     "MapChunking\GroundFloor\Second Chunk Iteration\Ground Floor Chunk 1.PNG",
#     "MapChunking\GroundFloor\Second Chunk Iteration\Ground Floor Chunk 2.PNG",
#     "MapChunking\GroundFloor\Second Chunk Iteration\Ground Floor Chunk 3.PNG",
#     "MapChunking\GroundFloor\Second Chunk Iteration\Ground Floor Chunk 4.PNG",
#     "MapChunking\GroundFloor\Second Chunk Iteration\Ground Floor Chunk 5.PNG",
#     "MapChunking\GroundFloor\Second Chunk Iteration\Ground Floor Chunk 6.PNG",
#     "MapChunking\GroundFloor\Second Chunk Iteration\Ground Floor Chunk 7.PNG",
#     "MapChunking\GroundFloor\Second Chunk Iteration\Ground Floor Chunk 8.PNG",
#     "MapChunking\GroundFloor\Second Chunk Iteration\Ground Floor Chunk 9.PNG",
#     "MapChunking\GroundFloor\Second Chunk Iteration\Ground Floor Chunk 10.PNG",
#     "MapChunking\GroundFloor\Second Chunk Iteration\Ground Floor Chunk 11.PNG",
#     "MapChunking\GroundFloor\Second Chunk Iteration\Ground Floor Chunk 12.PNG",
#     "MapChunking\GroundFloor\Second Chunk Iteration\Ground Floor Chunk 13.PNG",
#     "MapChunking\GroundFloor\Second Chunk Iteration\Ground Floor Chunk 14.PNG",
#     "MapChunking\GroundFloor\Second Chunk Iteration\Ground Floor Chunk 15.PNG",
#     "MapChunking\GroundFloor\SecondChunkIteration\Ground Floor Chunk 16.PNG",
# ]

t = t.Turtle()
t.speed("fastest")

currentchunk = 7 - 1 #NB: Chunks x will be referenced for x-1 as list in python start from 0
t.screen.bgpic(chunks[currentchunk])

testinput = t.screen.textinput("TEST","This is just a test input it does nothing")
if testinput.lower() == "quit":
    quit()
t.penup()
t.setpos(-270,-275)
t.pensize(3)

# t.write("Home = ", True, align="center",font=("Arial",8,"normal"))
# t.write((0,0),True)

# t.fillcolor("yellow")
# t.begin_fill()
# for i in range(3):
#     t.fd(100)
#     t.left(120)
# t.end_fill()

# t.penup()
# t.setpos(-50,-50)
# t.write("This is a test among tests to see if I could use turtle to so called 'animate' the porgression of my navigation system as this would drastically reduce lag", True,font=("Arial",8,"normal"))
# t.home()

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
    if position[1] <= -(size/2 - 5):
        canmovestatus = False
        newchunk = (currentchunk - int(sqrt(len(chunks))))%len(chunks)
        currentchunk = newchunk
        t.screen.bgpic(chunks[currentchunk])
        t.clear()
        t.penup()
        t.setpos(position[0],-position[1]-movebyd)
        t.pendown()
        canmovestatus = True
    if position[0] <= -(size/2 - 5):
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
        newchunk = (currentchunk + int(sqrt(len(chunks))))%len(chunks)
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