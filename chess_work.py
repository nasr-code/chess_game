chess_table = [[1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000],
               [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000],
               [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000],
               [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000],
               [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000],
               [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000],
               [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000],
               [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000],]

WHITE_ROOKS = {'wR': [[0, 0], [0, 7]]}
WHITE_BISHOPS = {'wB':[[0, 2], [0, 5]]}
WHITE_KNIGHTS = {'wN':[[0, 1], [0, 6]]}
WHITE_QUEEN = {'wQ':[[0, 3]]}
WHITE_KING = {'wK':[[0, 4]]}
WHITE_PAWNS = {'wP':[[1,0], [1,1], [1,2], [1,3], [1,4], [1,5], [1,6], [1,7]]}

BLACK_ROOKS = {'bR':[[7, 0], [7, 7]]}
BLACK_BISHOPS = {'bB':[[7, 2], [7, 5]]}
BLACK_KNIGHTS = {'bN':[[7, 1], [7, 6]]}
BLACK_QUEEN = {'bQ':[[7, 3]]}
BLACK_KING = {'bK':[[7, 4]]}
BLACK_PAWNS = {'bP':[[6,0], [6,1], [6,2], [6,3], [6,4], [6,5], [6,6], [6,7]]}

WHITE = [WHITE_PAWNS,WHITE_ROOKS,WHITE_BISHOPS,WHITE_KNIGHTS,WHITE_QUEEN,WHITE_KING]
BLACK = [BLACK_PAWNS,BLACK_ROOKS,BLACK_BISHOPS,BLACK_KNIGHTS,BLACK_QUEEN,BLACK_KING]

COLORS = ['w','b']

WHITE_dict = {}
for i in WHITE:
    for key in i:
        WHITE_dict[key] = i[key]

BLACK_dict = {}
for i in BLACK:
    for key in i:
        BLACK_dict[key] = i[key]

all_in_one = {'w' : WHITE_dict, 'b':BLACK_dict}

for key in WHITE_dict:
    for j in range(len(WHITE_dict[key])):
        xcor = WHITE_dict[key][j][0]
        ycor = WHITE_dict[key][j][1]
        chess_table[xcor][ycor] = key

for key in BLACK_dict:
    for j in range(len(BLACK_dict[key])):
        xcor = BLACK_dict[key][j][0]
        ycor = BLACK_dict[key][j][1]
        chess_table[xcor][ycor] = key

def print_table(table):
    for i in range(len(table)-1,-1,-1):
        print(table[i])
    print("\n")


def check_path_for_Knight(color,line,row):
    elements = [-2, -1, 1, 2]
    possible_places = []
    for i in elements:
        for j in elements:
            if abs(i) != abs(j):
                if line + i < 8 and line + i > -1 and row + j < 8 and row + j > -1:
                    if not (chess_table[line + i][row + j] in all_in_one[color]):
                        print("x: {}, y: {}".format(line + i, row + j))
                        possible_places.append([line + i, row + j])
                        print(chess_table[line + i][row + j])
    return possible_places

def check_straight_line(direction,color,line,row):
    other_color = COLORS[COLORS.index(color)-1]
    possible_places = []
    ranges = {"down":list(range(1,8)),"right": list(range(1,8)),
             "up": list(range(-1,-8,-1)),"left": list(range(-1,-8,-1))}
    if direction == "up" or direction == "down":
        for n in ranges[direction]:
            if line + n < 8 and line + n>-1:
                if chess_table[line + n][row] in all_in_one[color]:
                    break
                elif chess_table[line + n][row] in all_in_one[other_color]:
                    possible_places.append([line + n, row])
                    break
                else:
                    possible_places.append([line + n, row])
    if direction == "left" or direction == "right":
        for n in ranges[direction]:
            if row + n < 8 and row + n>-1:
                if chess_table[line][row + n] in all_in_one[color]:
                    break
                elif chess_table[line][row + n] in all_in_one[other_color]:
                    possible_places.append([line][row + n])
                    break
                else:
                    possible_places.append([line, row + n])
    return possible_places


def check_path_for_ROOK(color,line,row):
    all_possible_places = []
    all_possible_places.append(check_straight_line("up", color, line, row))
    #print("up: {}".format(all_possible_places[0]))
    all_possible_places.append(check_straight_line("down", color, line, row))
    #print("down: {}".format(all_possible_places[1]))
    all_possible_places.append(check_straight_line("left", color, line, row))
    #print("left: {}".format(all_possible_places[2]))
    all_possible_places.append(check_straight_line("right", color, line, row))
    #print("right: {}".format(all_possible_places[3]))

    return all_possible_places

def check_diagonal_line(direction,color,line,row):
    other_color = COLORS[COLORS.index(color) - 1]
    ranges = {"up-left":[list(range(-1,-8,-1)),list(range(-1,-8,-1))],
              "up-right":[list(range(-1,-8,-1)),list(list(range(1,8)))],
              "down-left":[list(list(range(1,8))),list(range(-1,-8,-1))],
              "down-right":[list(list(range(1,8))),list(list(range(1,8)))]}
    possible_places = []
    for i in range(8):
        l = ranges[direction][0][i]
        r = ranges[direction][1][i]
        if line + l< 8 and row + r <8:
            if chess_table[line+l][row+r] in all_in_one[color]:
                break
            elif chess_table[line+l][row+r] in all_in_one[other_color]:
                possible_places.append([line+l,row+r])
                break
            else:
                possible_places.append([line + l, row + r])

    return possible_places

def check_path_for_bishop(color,line,row):
    ranges = ["up-left", "up-right", "down-left", "down-right"]
    all_possible_moves = []

    for i in ranges:
        all_possible_moves.append(check_diagonal_line(i,color,line,row))
        #print(all_possible_moves[len(all_possible_moves)-1])

    return all_possible_moves

def check_path_for_queen(color,line,row):
    all_possible_moves = []
    all_possible_moves.append(check_path_for_ROOK(color,line,row))
    all_possible_moves.append(check_path_for_bishop(color,line,row))
    return all_possible_moves

def check_path_for_pawn(color,line,row):
    possible_moves = []
    other_color = COLORS[COLORS.index(color) - 1]
    step = 1
    if color == "b":
        step = -1

    if chess_table[line+step][row]==1000:
        possible_moves.append([line + step, row])
        if color == "w" and line == 1:
            possible_moves.append([line+2,row])
        elif color == "b" and line == 6:
            possible_moves.append([line - 2, row])

    if row-1>-1 and row+1<8:
        if chess_table[line + step][row - 1] in all_in_one[other_color]:
            possible_moves.append([line + step,row - 1])
        if chess_table[line + step][row + 1] in all_in_one[other_color]:
            possible_moves.append([line + step, row + 1])
    print(chess_table)
    return possible_moves


def check_path_for_king(color,line,row):
    other_color = COLORS[COLORS.index(color) - 1]
    ranges = [[line+1,row],[line+1,row+1],[line+1,row-1],
              [line,row+1],[line,row-1],[line-1,row+1],[line-1,row],[line-1,row-1]]
    possible_moves = []
    for i in ranges:
        if i[0]<8 and i[1]<8:
            if chess_table[i[0]][i[1]] in all_in_one[other_color] or chess_table[i[0]][i[1]]==1000:
                possible_moves.append([i[0],i[1]])
    return possible_moves

#for i in all_in_one:
#    for j in all_in_one[i]:
#        for h in all_in_one[i][j]:
#            chess_table[h[0]][h[1]] = j
#
#for i in chess_table:
#    print(i)