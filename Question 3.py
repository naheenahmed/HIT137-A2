import turtle

# This function draws one "side" of the shape.
# If depth is 0, it just draws a straight line.
# Otherwise, it splits the side into 4 smaller parts with a little "bump" in the middle.
import turtle

def draw_side(my_turtle, length, depth):
    if depth == 0:
        my_turtle.forward(length)
    else:
        new_length = length / 3
        draw_side(my_turtle, new_length, depth - 1)
        my_turtle.left(60)
        draw_side(my_turtle, new_length, depth - 1)
        my_turtle.right(120)
        draw_side(my_turtle, new_length, depth - 1)
        my_turtle.left(60)
        draw_side(my_turtle, new_length, depth - 1)


def main():
    sides = int(input("How many sides for the starting shape? "))
    length = int(input("How long should each side be (pixels)? "))
    depth = int(input("How many times to repeat the pattern (recursion depth)? "))

    my_turtle = turtle.Turtle()
    my_turtle.hideturtle()   
    turtle.bgcolor("white")

    # Speed boost
    turtle.tracer(False)

    # Center polygon
    my_turtle.penup()
    my_turtle.goto(-length // 2, length // 3)
    my_turtle.pendown()

    turn_angle = 360 / sides
    for _ in range(sides):
        draw_side(my_turtle, length, depth)
        my_turtle.right(turn_angle)

#Instant render
    turtle.update()   
    turtle.done()

if __name__ == "__main__":
    main()
