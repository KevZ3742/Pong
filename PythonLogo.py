import turtle

trtle = turtle.Turtle()
screen = turtle.Screen()
screen.bgcolor("black")
trtle.speed(10)
trtle.pensize(2)
trtle.pencolor("white")

def sCurve():
    for i in range(90):
        trtle.left(1)
        trtle.forward(1)

def rCurve():
    for i in range(90):
        trtle.right(1)
        trtle.forward(1)

def lCurve1():
    sCurve()
    trtle.forward(80)
    sCurve()

def lCurve2():
    sCurve()
    trtle.forward(90)
    sCurve()

def half():
    trtle.forward(50)
    sCurve()
    trtle.forward(90)
    lCurve1()
    trtle.forward(40)
    trtle.left(90)
    trtle.forward(80)
    trtle.right(90)
    trtle.forward(10)
    trtle.right(90)
    trtle.forward(120) #on test
    lCurve2()
    trtle.forward(30)
    trtle.left(90)
    trtle.forward(50)
    rCurve()
    trtle.forward(40)
    trtle.end_fill()

def getPos():
    trtle.penup()
    trtle.forward(20)
    trtle.right(90)
    trtle.forward(10)
    trtle.right(90)
    trtle.pendown()

def eye1():
    trtle.penup()
    trtle.right(90)
    trtle.forward(160)
    trtle.left(90)
    trtle.forward(70)
    trtle.pencolor("black")
    trtle.dot(35)

def eye2():
    trtle.left(90)
    trtle.penup()
    trtle.forward(310)
    trtle.left(90)
    trtle.forward(120)
    trtle.pendown()

    trtle.dot(35)

trtle.fillcolor("#306998")
trtle.begin_fill()
half()
trtle.end_fill()
getPos()
trtle.fillcolor("#FFD43B")
trtle.begin_fill()
half()
trtle.end_fill()

eye1()
eye2()

turtle.mainloop()