# Snake game by Gabe Holmes
# Just a fun 1 hour project, replicating the classic game of snake


from graphics import *
import random


# Board should have 17 columns and 16 rows
# With a 30 pixel buffer at top for score and everything
def draw_board(window, num_rows, num_cols, size_of_square, top_buffer, boarder_buffer):
    window.setBackground('black')
    # Draw horizontal lines
    for row in range(num_rows + 1):
        line = Line(Point(12, (row * size_of_square) + top_buffer),
                    Point(num_cols * size_of_square + 12, (row * size_of_square) + top_buffer))
        line.draw(window)

    # Draw vertical lines
    for col in range(num_cols + 1):
        line = Line(Point(col * size_of_square + 12, top_buffer),
                    Point(col * size_of_square + 12, num_rows * size_of_square + top_buffer))
        line.draw(window)

    # Create the squares squares other methods will use
    # squares ia a 2d array of a tuple of ((Rectangle, isSnake), (row, col)) where Rectangle is used for graphics
    # and (row, col) is used for coordinates, and isSnake is used to determine if this square is a snake
    squares = [x[:] for x in [[(Rectangle(Point(0, 0), Point(0, 0)), False, False)] * num_cols] * num_rows]
    for row in range(num_rows):
        for col in range(num_cols):
            squares[row][col] = \
                (Rectangle(Point(col * size_of_square + boarder_buffer, row * size_of_square + top_buffer),
                           Point((col + 1) * size_of_square + boarder_buffer,
                                 (row + 1) * size_of_square + top_buffer)), False, False)
            if (col + row) % 2 == 0:
                squares[row][col][0].setFill(color_rgb(60, 146, 0))
            else:
                squares[row][col][0].setFill(color_rgb(73, 182, 0))
            squares[row][col][0].draw(window)
    return squares


# Removes the end of the snake and adds it to the front
def chop_and_add(snake_list, squares, direction, num_rows, num_cols, apple_spots):
    currRow, currCol = snake_list[-1]
    targetRow = currRow + direction[0]
    targetCol = currCol + direction[1]
    try:
        ate_apple = squares[targetRow][targetCol][2]
    except IndexError:
        # The target is out of bounds, so return
        return True

    # Now check if the target was a snake, or out of bounds
    # if so then indicate the game is over
    if 0 > targetRow or targetRow >= num_rows \
            or 0 > targetCol or targetCol >= num_cols:
        return True
    elif squares[targetRow][targetCol][1]:
        return True

    # If an apple was ate, dont pop the element only get the contents
    # since we keep that square as a snake square
    if ate_apple:
        lastRow, lastCol = snake_list[0]
    else:
        lastRow, lastCol = snake_list.pop(0)
        apple_spots.append((lastRow, lastCol))
        squares[lastRow][lastCol] = (squares[lastRow][lastCol][0], False, False)

    # Draw ground green again if an apple was not ate
    if not ate_apple:
        if (lastRow + lastCol) % 2 == 0:
            squares[lastRow][lastCol][0].setFill(color_rgb(60, 146, 0))
        else:
            squares[lastRow][lastCol][0].setFill(color_rgb(73, 182, 0))

    # The target index is not a snake or out of bounds, can update squares and snake_list
    snake_list.append((targetRow, targetCol))
    apple_spots.remove((targetRow, targetCol))

    squares[targetRow][targetCol][0].setFill('blue')
    squares[targetRow][targetCol] = (squares[targetRow][targetCol][0], True, False)

    # Add an apple to a random spot
    if ate_apple:
        randRow, randCol = random.choice(apple_spots)
        squares[randRow][randCol] = (squares[randRow][randCol][0], False, True)
        squares[randRow][randCol][0].setFill('red')


# win will be the window, while squares will be the 2d array containing
# info about each square
# plays the game
def play_game(win, squares, num_rows, num_cols):
    text = Text(Point(win.getWidth() / 2, 10), 'Playing')
    text.setFill('white')
    text.draw(win)
    # Start the snake occupying squares (7,9) and (8,9)
    squares[7][5] = (squares[7][5][0], True, False)
    squares[7][5][0].setFill('blue')
    squares[7][6] = (squares[7][6][0], True, False)
    squares[7][6][0].setFill('blue')

    # and an apple at (2,3)
    squares[2][3] = (squares[2][3][0], False, True)
    squares[2][3][0].setFill('red')
    # List of tuples representing snake segments
    # list[0] has been the for the longest
    snake_list = [(7, 5), (7, 6)]

    apple_spots = []
    for x in range(num_rows):
        for y in range(num_cols):
            apple_spots.append((x, y))
    apple_spots.remove((7, 5))
    apple_spots.remove((7, 6))

    loop_count = 0
    win.getMouse()
    direction = (0, 1)
    while True:
        keyStroke = win.checkKey()
        text.setText(text.getText() + keyStroke)
        directions = {'d': (0, 1), 'Right': (0, 1), 'w': (-1, 0), 'Up': (-1, 0),
                      'a': (0, -1), 'Left': (0, -1), 's': (1, 0), 'Down': (1, 0)}
        if keyStroke in directions:
            direction = directions[keyStroke]
            text.setText(str(direction))

        # Only move the snake every 10 loops, used to adjust tik rate
        if loop_count % 2 == 0:
            if chop_and_add(snake_list, squares, direction, num_rows, num_cols, apple_spots):
                text.setText('Lost')
                break
        loop_count += 1


def main():
    num_rows = 16
    num_cols = 17
    size_of_square = 25
    top_buffer = 30  # The size of the strip at the top to display information
    boarder_buffer = 12  # The padding around the left right

    window_width = num_cols * size_of_square + (boarder_buffer * 2)
    window_height = num_rows * size_of_square + (boarder_buffer * 3)

    win = GraphWin('Snake Game', window_width, window_height)
    squares = draw_board(win, num_rows, num_cols, size_of_square, top_buffer, boarder_buffer)

    play_game(win, squares, num_rows, num_cols)

    win.getMouse()


if __name__ == '__main__':
    main()
