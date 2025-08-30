import turtle   #importing library
my_wn = turtle.Screen()
my_wn.bgcolor("light blue") #screen background color
my_wn.title("Turtle")
my_pen = turtle.Turtle()
size = 0
while True: #iterate loop
    for i in range(4):
        my_pen.fd(size + 1)
        my_pen.left(90)
        size = size - 5
    size = size + 1
