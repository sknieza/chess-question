import sys

# dictionary for conversion of coordinates from chess notation to python index
conversion = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7,
    "1": 7,
    "2": 6,
    "3": 5,
    "4": 4,
    "5": 3,
    "6": 2,
    "7": 1,
    "8": 0,
}

# dictionary for deconversion from evaluation function output
convert_x = {
    0: "a",
    1: "b",
    2: "c",
    3: "d",
    4: "e",
    5: "f",
    6: "g",
    7: "h",
}

# dictionary for deconversion from evaluation function output
convert_y = {
    0: "8",
    1: "7",
    2: "6",
    3: "5",
    4: "4",
    5: "3",
    6: "2",
    7: "1",
}

# dictionary to store black piece inputs for evaluation and output
b_inputs = {}


def main():
    """In main() function we accept white piece input in format 'pawn a5', corresponding to chess rules (e.g., a-h, 1-8)
    We then proceed with black piece input until up to 16 pieces are added or function is terminated with entering 'done'
    Based on white figure (pawn and rook allowed), we evaluate which balck figures can be taken and print them.
    """

    # initial board status (empty sequence(-s)
    board_state = get_new_board_state()

    print(
        "Welcome to a chess question game. This program will answer if the placed white chess piece \
    will be able to take any of the placed black pieces. For this version of the program, you can choose to \
    play with either a pawn or a rook."
    )

    # initial function, asking for user input of a white piece
    figure_placement = input(
        "Enter your figure (pawn or rook) and its square (e.g. rook c6): "
    ).strip()
    w_move = piece_coordinates(figure_placement)
    adjusted_w = converter(w_move)
    # should return three-value list: figure name, transformed coords (a8 -> 0,0; d5 -> 3,3 and etc.)
    board_state = place_white_piece(
        board_state, adjusted_w
    )  # func updates board_state with user input

    # function that asks user to input 1-16 black pieces
    board_state = places_black_pieces(
        board_state
    )  # func that returns a sequence with final board config
    print("All figures successfully placed!")
    print_board(board_state)

    if w_move[0] == "pawn":
        checked_pieces = pawn_moves(board_state, adjusted_w)
        deconvert(b_inputs, checked_pieces)
    elif w_move[0] == "rook":
        checked_pieces = rook_moves(board_state, adjusted_w)
        deconvert(b_inputs, checked_pieces)
    else:
        pass


def get_new_board_state():  # initial function with empty e.g. list of lists
    """Chess board x-axis is (a-h), y-axis is (1-8)
    This means that for our purpose we'll need a converter, where
    input alpha character takes index (0-7), num character takes (7-0)
    and the logic is inversed as list indexing starts with y, not x
    e.g. a5 = input[3][0]; g3 = input[5][6] etc. This is done with converter()
    """

    return [
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
    ]


def piece_coordinates(figure_placement):
    """returns three-value list of transformed coordinates"""
    figure_square = figure_placement.split()
    w_piece = figure_square[0]
    temp1 = figure_square[1]
    w_coordinates = list(temp1)
    x_coordinate = w_coordinates[0]
    y_coordinate = w_coordinates[1]
    move = [w_piece, x_coordinate, y_coordinate]
    return move


def converter(move):
    """returns three-value list of coordinates as indices"""
    # move = [piece, alpha, num]
    move[1] = conversion.get(move[1])
    move[2] = conversion.get(move[2])
    return move


def place_white_piece(board_state, w_move):
    """returns returns updated board state with white piece placement"""
    x_coordinate = w_move[1]
    y_coordinate = w_move[2]
    if w_move[0] == "rook":
        marker = "R"
    elif w_move[0] == "pawn":
        marker = "P"
    else:
        pass
    board_state[y_coordinate][x_coordinate] = marker
    return board_state


def places_black_pieces(board_state):
    """initializes looped placement of 1-16 black pieces"""
    count = 0
    while count < 16:
        try:
            b_move = input(
                "Enter coordinates of 1 to 16 black pieces, or enter 'done' when finished: "
            ).strip()
            if count > 0:
                if b_move == "done":
                    break
                else:
                    pass
            if count == 0:
                if b_move == "done":
                    raise ValueError
                else:
                    pass
            place_black = piece_coordinates(b_move)
            b_split = b_move.split()
            b_inputs.update({b_split[1]: b_split[0]})
            coordinates = converter(place_black)  # smh prints the same as place_black
            if not check_occupancy(board_state, coordinates):
                # move = [piece, alpha, num]
                x_coordinate = coordinates[1]
                y_coordinate = coordinates[2]
                marker = "B"
                board_state[y_coordinate][x_coordinate] = marker
                print(f"Successfully added black {place_black[0]} at {b_move[-2:]}")
                count += 1
            else:
                raise ValueError
        except ValueError:
            print("'Done' entered too early or the square is already taken!")
            continue

    return board_state


def check_occupancy(board_state, piece_coordinates):
    """function used in places_black_pieces() to check if the square is free"""
    x_coordinate = piece_coordinates[1]
    y_coordinate = piece_coordinates[2]
    square = board_state[y_coordinate][x_coordinate]
    return square.isalpha()


def pawn_moves(board_state, adjusted_w):
    """checks if pawn can take any black figures; appends them to list"""
    checked_pieces = []
    # move = [piece, alpha, num]
    # adjusted_w = [piece, x, y]
    temp_x = adjusted_w[1]  # int
    temp_y = adjusted_w[2]  # int
    try:
        if board_state[(temp_y) - 1][(temp_x) - 1] == "B":
            piece_1 = []
            piece_1.append((temp_x) - 1)
            piece_1.append((temp_y) - 1)
            checked_pieces.append(piece_1)
    except IndexError:
        pass
    try:
        if board_state[(temp_y) - 1][(temp_x) + 1] == "B":
            piece_2 = []
            piece_2.append((temp_x) + 1)
            piece_2.append((temp_y) - 1)
            checked_pieces.append(piece_2)
    except IndexError:
        pass
    return checked_pieces


def rook_moves(board_state, adjusted_w):
    """checks if rook can take any black figures; appends them to list"""
    checked_pieces = []
    temp_x = adjusted_w[1]  # int
    temp_y = adjusted_w[2]  # int

    # Upwards y-axis
    for i in range(1, 8):
        new_y = temp_y - i
        if new_y < 0:  # Ensure we are within the board
            break
        if board_state[new_y][temp_x] == "B":
            checked_pieces.append([temp_x, new_y])
            break
        elif board_state[new_y][temp_x] != " ":  # Assuming " " is an empty square
            break

    # Downwards y-axis
    for i in range(1, 8):
        new_y = temp_y + i
        if new_y > 7:  # Ensure we are within the board
            break
        if board_state[new_y][temp_x] == "B":
            checked_pieces.append([temp_x, new_y])
            break
        elif board_state[new_y][temp_x] != " ":  # Assuming " " is an empty square
            break

    # Right-hand x-axis
    for i in range(1, 8):
        new_x = temp_x + i
        if new_x > 7:  # Ensure we are within the board
            break
        if board_state[temp_y][new_x] == "B":
            checked_pieces.append([new_x, temp_y])
            break
        elif board_state[temp_y][new_x] != " ":  # Assuming " " is an empty square
            break

    # Left-hand x-axis
    for i in range(1, 8):
        new_x = temp_x - i
        if new_x < 0:  # Ensure we are within the board
            break
        if board_state[temp_y][new_x] == "B":
            checked_pieces.append([new_x, temp_y])
            break
        elif board_state[temp_y][new_x] != " ":  # Assuming " " is an empty square
            break

    return checked_pieces


def print_board(board_state):
    """board printer for visualizing the board state"""
    for row in board_state:
        print(row)


def deconvert(b_inputs, checked_pieces):
    """reconverts indices to a proper chess input format"""
    de_coordinates = []
    for i in checked_pieces:
        x = convert_x.get(i[0])
        y = convert_y.get(i[1])
        xy = x + y
        de_coordinates.append(xy)
    for w in de_coordinates:
        piece = b_inputs.get(w)
        print(f"White piece can take {piece} {w}")


main()
