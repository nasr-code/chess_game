import pygame
from sys import exit
import threading

"""
to do list
add en passant
add rook and king switching
give player option to switch pawn to something any other piece other than king
add stalemate conditions and effects
add checkmate conditions and effects
maybe add captured pieces list and visuals

"""

#######################################################################################################################################
def print_table(table):
    for i in range(len(table) - 1, -1, -1):
        print(table[i])
    print("\n")



def check_path_for_Knight(color, line, row, table):
    elements = [-2, -1, 1, 2]
    possible_places = []
    for i in elements:
        for j in elements:
            if abs(i) != abs(j):
                if line + i < 8 and line + i > -1 and row + j < 8 and row + j > -1:
                    if not (table[line + i][row + j][0] == color):#meaning the location we looking at contains a homie, but not reverses that condition
                        # print("x: {}, y: {}".format(line + i, row + j))
                        possible_places.append([line + i, row + j])
                        # print(chess_table[line + i][row + j])
                    else:
                        possible_places.append([line + i, row + j, 'ST'])  # ST for same team
    return possible_places


def check_straight_line(direction, color, line, row, table):
    other_color = COLORS[COLORS.index(color) - 1]
    possible_places = []
    ranges = {"down": list(range(1, 8)), "right": list(range(1, 8)),
              "up": list(range(-1, -8, -1)), "left": list(range(-1, -8, -1))}
    if direction == "up" or direction == "down":
        for n in ranges[direction]:
            if line + n < 8 and line + n > -1:
                if table[line + n][row][0] == color:
                    possible_places.append([line + n, row, 'ST'])  # ST for same team
                    break
                elif table[line + n][row][0] == other_color:
                    possible_places.append([line + n, row])
                    break
                else:
                    possible_places.append([line + n, row])
    if direction == "left" or direction == "right":
        for n in ranges[direction]:
            if row + n < 8 and row + n > -1:
                if table[line][row + n][0] == color:
                    possible_places.append([line, row + n, 'ST'])  # ST for same team
                    break
                elif table[line][row + n][0] == other_color:
                    possible_places.append([line, row + n])
                    break
                else:
                    possible_places.append([line, row + n])
    return possible_places


def check_path_for_ROOK(color, line, row, table):
    all_possible_places = []
    all_possible_places.append(check_straight_line("up", color, line, row, table))
    all_possible_places.append(check_straight_line("down", color, line, row, table))
    all_possible_places.append(check_straight_line("left", color, line, row, table))
    all_possible_places.append(check_straight_line("right", color, line, row, table))

    return all_possible_places


def check_diagonal_line(direction, color, line, row, table):
    other_color = COLORS[COLORS.index(color) - 1]
    ranges = {"up-left": [list(range(-1, -8, -1)), list(range(-1, -8, -1))],
              "up-right": [list(range(-1, -8, -1)), list(list(range(1, 8)))],
              "down-left": [list(list(range(1, 8))), list(range(-1, -8, -1))],
              "down-right": [list(list(range(1, 8))), list(list(range(1, 8)))]}
    possible_places = []
    for i in range(7):
        # print(ranges[direction][0])
        l = ranges[direction][0][i]
        r = ranges[direction][1][i]

        if line + l < 8 and line + l > -1 and row + r < 8 and row + r > -1:
            if table[line + l][row + r][0] == color:
                possible_places.append([line + l, row + r, 'ST'])  # ST for same team
                break
            elif table[line + l][row + r][0] == other_color:
                possible_places.append([line + l, row + r])
                break
            else:
                possible_places.append([line + l, row + r])

    return possible_places


def check_path_for_bishop(color, line, row, table):
    ranges = ["up-left", "up-right", "down-left", "down-right"]
    all_possible_moves = []

    for i in ranges:
        all_possible_moves.append(check_diagonal_line(i, color, line, row, table))
        # print(all_possible_moves[len(all_possible_moves)-1])

    return all_possible_moves


def check_path_for_queen(color, line, row, table):
    all_possible_moves = []
    all_possible_moves.append(check_path_for_ROOK(color, line, row, table))
    all_possible_moves.append(check_path_for_bishop(color, line, row, table))
    return all_possible_moves


def check_path_for_pawn(color, line, row, table):
    possible_moves = []
    other_color = COLORS[COLORS.index(color) - 1]
    step = 1
    if color == "b":
        step = -1

    if line + step > -1 and line + step < 8:
        if table[line + step][row] == '00':
            possible_moves.append([line + step, row])
            if line == 1 or line == 6:
                if table[line + 2 * step][row] == '00':
                    possible_moves.append([line + 2 * step, row])

    if line + step > -1 and line + step < 8:
        for i in [-1, 1]:
            if row + i > -1 and row + i < 8:
                if not table[line + step][row + i][0] == color:
                    possible_moves.append([line + step, row + i])
                else:
                    possible_moves.append([line + step, row + i, 'ST'])  # ST for same team



    return possible_moves


def check_path_for_king(color, line, row, table):
    other_color = COLORS[COLORS.index(color) - 1]
    ranges = [[line + 1, row], [line + 1, row + 1], [line + 1, row - 1],
              [line, row + 1], [line, row - 1], [line - 1, row + 1], [line - 1, row], [line - 1, row - 1]]
    possible_moves = []
    for i in ranges:
        if i[0] < 8 and i[0] > -1 and i[1] < 8 and i[1] > -1:
            if not table[i[0]][i[1]][0] == color:
                possible_moves.append([i[0], i[1]])

    return possible_moves


def check_path_for_piece(line, row, table, regular_mode=True):  # checks for path of pieces on the regular use
    color = table[line][row][0]  # next_move_mode is for when we are in a state to check the future move
    piece = table[line][row][1]
    possible_moves = []
    possible_moves_brushed = []
    other_color = COLORS[COLORS.index(color) - 1]
    if piece == 'P':
        step = 1 if color == 'w' else -1
        possible_moves_brushed = check_path_for_pawn(color, line, row, table)
        # filters the attack positions of the pawn if there is no enemy there
        j = 0
        while j < len(possible_moves_brushed):
            if possible_moves_brushed[j][0] == line + step:
                if possible_moves_brushed[j][1] == row - 1:
                    if table[line + step][row - 1] == '00':
                        possible_moves_brushed.pop(j)
                        j -= 1
                elif possible_moves_brushed[j][1] == row + 1:
                    if table[line + step][row + 1] == '00':
                        possible_moves_brushed.pop(j)
                        j -= 1
            j += 1

    elif piece == 'R':
        possible_moves = check_path_for_ROOK(color, line, row, table)
        for i in possible_moves:
            for j in i:
                possible_moves_brushed.append(j)

    elif piece == 'N':
        possible_moves_brushed = check_path_for_Knight(color, line, row, table)
    elif piece == 'B':
        possible_moves = check_path_for_bishop(color, line, row, table)
        for i in possible_moves:
            for j in i:
                possible_moves_brushed.append(j)

    elif piece == 'Q':
        possible_moves = check_path_for_queen(color, line, row, table)
        for i in possible_moves:
            for j in i:
                for h in j:
                    possible_moves_brushed.append(h)

    elif piece == 'K':
        possible_moves_brushed = check_path_for_king(color, line, row, table)
        cover_table = check_cover(other_color, table)
        i = 0
        while i < len(possible_moves_brushed):
            if cover_table[possible_moves_brushed[i][0]][possible_moves_brushed[i][1]] != '00':
                possible_moves_brushed.pop(i)
                i -= 1
            i += 1
    # filters the covered pieces of the piece that are on the same team during regular use
    i = 0
    if possible_moves_brushed and regular_mode == True:
        while i < len(possible_moves_brushed):
            if len(possible_moves_brushed[i]) == 3:
                if possible_moves_brushed[i][2] == 'ST':
                    possible_moves_brushed.pop(i)
                    i -= 1
            i += 1
    i = 0

    # print(possible_moves_brushed)
    return possible_moves_brushed


def check_cover(color, table):
    other_color = COLORS[COLORS.index(color) - 1]
    global all_cover
    cover_table = [['00', '00', '00', '00', '00', '00', '00', '00'],
                   ['00', '00', '00', '00', '00', '00', '00', '00'],
                   ['00', '00', '00', '00', '00', '00', '00', '00'],
                   ['00', '00', '00', '00', '00', '00', '00', '00'],
                   ['00', '00', '00', '00', '00', '00', '00', '00'],
                   ['00', '00', '00', '00', '00', '00', '00', '00'],
                   ['00', '00', '00', '00', '00', '00', '00', '00'],
                   ['00', '00', '00', '00', '00', '00', '00', '00']]
    for i in range(8):
        for j in range(8):
            if table[i][j][0] == color:
                line = i
                row = j
                if table[line][row][1] == 'K':
                    possible_moves = check_path_for_king(color, line, row, table)
                elif table[line][row][1] == 'P':
                    step = 1 if color == 'w' else -1
                    possible_moves = check_path_for_pawn(color, line, row, table)
                    h = 0
                    while h < len(possible_moves):
                        if (possible_moves[h][0] == line + 2 * step) or (
                                possible_moves[h][0] == line + step and possible_moves[h][1] == row):
                            possible_moves.pop(h)
                            h -= 1
                        h += 1
                    # print(possible_moves)
                else:
                    possible_moves = check_path_for_piece(line, row, table, False)

                if possible_moves:
                    for moves in possible_moves:
                        cover_table[moves[0]][moves[1]] = f'{color}{color}'

    # for i in range(len(all_cover[color])):
    #    print(all_cover[color][7 - i])
    return cover_table


def with_check_very_next_move(line, row, table):
    color = table[line][row][0]
    other_color = COLORS[COLORS.index(color) - 1]
    piece = table[line][row]
    for i in range(8):
        for j in range(8):
            if table[i][j]==f'{color}K':
                king_line = i
                king_row = j
                break
    possible_moves = check_path_for_piece(line, row, table)
    # filters the moves that don't take king away from a check
    # so pinned pieces and ones used to block check
    i = 0
    while i < len(possible_moves):
        dummy_chess_table = []
        for j in table:
            dummy_chess_table.append(list(j))
        dummy_chess_table[possible_moves[i][0]][possible_moves[i][1]] = piece
        dummy_chess_table[line][row] = '00'
        dummy_cover_table = check_cover(other_color, dummy_chess_table)
        if piece == f'{color}K':
            king_line = possible_moves[i][0]
            king_row = possible_moves[i][1]

        if dummy_cover_table[king_line][king_row] == f'{other_color}{other_color}':
            possible_moves.pop(i)
            i -= 1
        i += 1
    return possible_moves


#######################################################################################################################################

chess_table = [['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
               ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
               ['00', '00', '00', '00', '00', '00', '00', '00'],
               ['00', '00', '00', '00', '00', '00', '00', '00'],
               ['00', '00', '00', '00', '00', '00', '00', '00'],
               ['00', '00', '00', '00', '00', '00', '00', '00'],
               ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
               ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR']]

# chess_table =  [['00', '00', '00', '00', '00', '00', '00', '00'],
#               ['00', '00', '00', 'bP', '00', '00', '00', '00'],
#               ['00', '00', '00', '00', '00', '00', '00', '00'],
#               ['00', '00', '00', '00', '00', '00', '00', '00'],
#               ['00', 'bR', '00', 'bQ', 'bK', '00', 'bN', '00'],
#               ['00', '00', '00', '00', '00', '00', '00', '00'],
#               ['00', '00', '00', 'bB', '00', 'wB', '00', '00'],
#               ['00', '00', '00', '00', '00', '00', '00', '00']]


num = 50 + (87.5 / 2)
clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("chess")
table_surf = pygame.image.load("image_things/chess_board_original.jpg")
table_surf = pygame.transform.scale(table_surf, (700, 700)).convert()
table_rect = table_surf.get_rect(center=(400, 400))

background_surf = pygame.image.load('image_things/background.png')
background_surf = pygame.transform.scale(background_surf, (800, 800))

WHITE_surfs = []
WHITE_rects = []
WHITE_logic = []
BLACK_surfs = []
BLACK_rects = []
BLACK_logic = []
all_surfs = {'w': WHITE_surfs, 'b': BLACK_surfs}
all_rects = {'w': WHITE_rects, 'b': BLACK_rects}
all_logic = {'w': WHITE_logic, 'b': BLACK_logic}
COLORS = ['w', 'b']


def calculate_line(ypos):
    return round(-(((ypos - 90) / 87.5) - 7))


def calculate_row(xpos):
    return round((((xpos - 94) / 87.5)))


def calculate_xpos(row):
    return (94 + row * 87.5)


def calculate_ypos(line):
    return 90 + (7 - line) * 87.5


x = 0
y = 0
for i in range(len(chess_table)):
    for j in range(len(chess_table[i])):
        color = chess_table[i][j][0]
        if color == 'w' or color == 'b':
            if color == 'w':
                n = x
                x += 1
            else:
                n = y
                y += 1
            all_surfs[color].append(0)
            all_rects[color].append(0)
            all_logic[color].append(0)
            all_surfs[color][n] = pygame.image.load('image_things/{}.png'.format(chess_table[i][j]))
            all_surfs[color][n] = pygame.transform.scale(all_surfs[color][n], (84, 84))
            all_rects[color][n] = all_surfs[color][n].get_rect(center=((94 + j * 87.5), 90 + (7 - i) * 87.5))
            all_logic[color][n] = chess_table[i][j]

x = 0
y = 0
previous_position = []
selected_piece = [0, 0, 0, 0]
current_possible_moves = []
current_player_color = 'w'
BUTTON_DOWN = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            line = calculate_line(mouse_pos[1])
            row = calculate_row(mouse_pos[0])
            color = current_player_color
            if selected_piece[0] == 0:
                for i in range(len(all_rects[color])):
                    if all_rects[color][i].collidepoint(pygame.mouse.get_pos()):
                        previous_position = all_rects[color][i].center
                        selected_piece[0] = all_surfs[color][i]
                        selected_piece[1] = all_rects[color][i]
                        selected_piece[2] = i
                        selected_piece[3] = color
                        current_possible_moves = with_check_very_next_move(line, row, chess_table)
                        BUTTON_DOWN = True
                        break

            else:
                prev_line = calculate_line(previous_position[1])
                prev_row = calculate_row(previous_position[0])
                if current_possible_moves:
                    if [line, row] in current_possible_moves:
                        other_color = COLORS[COLORS.index(selected_piece[3]) - 1]
                        selected_piece[1].centerx = calculate_xpos(row)
                        selected_piece[1].centery = calculate_ypos(line)
                        chess_table[line][row] = chess_table[prev_line][prev_row]
                        chess_table[prev_line][prev_row] = '00'
                        for i in range(len(all_rects[other_color])):
                            if [line, row] == [calculate_line(all_rects[other_color][i].centery),
                                               calculate_row(all_rects[other_color][i].centerx)]:
                                all_surfs[other_color].pop(i)
                                all_rects[other_color].pop(i)
                                break
                        current_player_color = COLORS[COLORS.index(current_player_color) - 1]

                selected_piece = [0, 0, 0, 0]
                current_possible_moves = []
                previous_position = []
                BUTTON_DOWN = False

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_xpos = pygame.mouse.get_pos()[0]
            mouse_ypos = pygame.mouse.get_pos()[1]
            line = calculate_line(mouse_ypos)
            row = calculate_row(mouse_xpos)
            if selected_piece[0] != 0 and BUTTON_DOWN:
                prev_line = calculate_line(previous_position[1])
                prev_row = calculate_row(previous_position[0])
                if current_possible_moves:
                    if [line, row] in current_possible_moves:
                        other_color = COLORS[COLORS.index(selected_piece[3]) - 1]
                        selected_piece[1].centerx = calculate_xpos(row)
                        selected_piece[1].centery = calculate_ypos(line)
                        chess_table[line][row] = chess_table[prev_line][prev_row]
                        chess_table[prev_line][prev_row] = '00'
                        for i in range(len(all_rects[other_color])):
                            if [line, row] == [calculate_line(all_rects[other_color][i].centery),
                                               calculate_row(all_rects[other_color][i].centerx)]:
                                all_surfs[other_color].pop(i)
                                all_rects[other_color].pop(i)
                                break
                        current_player_color = COLORS[COLORS.index(current_player_color) - 1]

                        selected_piece = [0, 0, 0, 0]
                        previous_position = []
                        current_possible_moves = []
                    else:
                        selected_piece[1].centerx = previous_position[0]
                        selected_piece[1].centery = previous_position[1]
                else:
                    selected_piece[1].centerx = previous_position[0]
                    selected_piece[1].centery = previous_position[1]
                BUTTON_DOWN = False

    screen.blit(background_surf, (0, 0))
    screen.blit(table_surf, table_rect)
    #print(f'curent_player_color:{current_player_color}')
    # print_table(chess_table)
    if BUTTON_DOWN:
        mouse_pos = pygame.mouse.get_pos()
        selected_piece[1].centerx = mouse_pos[0]
        selected_piece[1].centery = mouse_pos[1]

    for color in all_surfs:
        for i in range(len(all_surfs[color])):
            screen.blit(all_surfs[color][i], all_rects[color][i])

    if selected_piece[0] != 0:
        if current_possible_moves:
            for i in range(len(current_possible_moves)):
                xpos = calculate_xpos(current_possible_moves[i][1])
                ypos = calculate_ypos(current_possible_moves[i][0])
                pygame.draw.circle(screen, 'black', (xpos, ypos), 10)

        screen.blit(selected_piece[0], selected_piece[1])

    pygame.display.update()
    clock.tick(60)
