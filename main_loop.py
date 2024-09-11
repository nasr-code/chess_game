import chess_func as funcs
import pygame
from sys import exit

def calculate_line(ypos):
    return round(-(((ypos - 90) / 87.5) - 7))


def calculate_row(xpos):
    return round((((xpos - 94) / 87.5)))


def calculate_xpos(row):
    return (94 + row * 87.5)


def calculate_ypos(line):
    return 90 + (7 - line) * 87.5

def search_rook_pos(color, all_logic, all_rects):
    dum_line = 0 if color=='w' else 7
    rooks_pos = {}
    for i in range(len(all_logic[color])):
        if all_logic[color][i]==f'{color}R':
            rook_line = calculate_line(all_rects[color][i].centery)
            rook_row = calculate_row(all_rects[color][i].centerx)
            if [rook_line, rook_row] == [dum_line, 0]:
                rooks_pos['left'] = i
            elif [rook_line, rook_row] == [dum_line, 7]:
                rooks_pos['right'] = i
    return rooks_pos

def deal_with_piece_movement():
    if chess_table[prev_line][prev_row][1] == 'R':
        rooks_pos = search_rook_pos(color, all_logic, all_rects)
        if prev_row == 0:
            all_castle_possibility[color]['left'] = False
        elif prev_row == 7:
            all_castle_possibility[color]['right'] = False

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
            all_logic[other_color].pop(i)
            break

    if chess_table[line][row][1] == 'P':
        if [color, line] == ['w', 7] or [color, line] == ['b', 0]:
            changing_pawn_state = [True, selected_piece[3], selected_piece[2]]
    ##########################################
    if chess_table[line][row][1] == 'K':
        if prev_row == row + 2 or prev_row == row - 2:
            rooks_pos = search_rook_pos(color, all_logic, all_rects)
            if prev_row - 2 == row:
                new_pos = [line, row + 1]
                all_rects[color][rooks_pos['left']].centerx = calculate_xpos(new_pos[1])
                all_rects[color][rooks_pos['left']].centery = calculate_ypos(new_pos[0])
                chess_table[line][new_pos[1]] = chess_table[line][0]
                chess_table[line][0] = '00'
            else:
                new_pos = [line, row - 1]
                all_rects[color][rooks_pos['right']].centerx = calculate_xpos(new_pos[1])
                all_rects[color][rooks_pos['right']].centery = calculate_ypos(new_pos[0])
                chess_table[line][new_pos[1]] = chess_table[line][7]
                chess_table[line][7] = '00'

        all_castle_possibility[color]['left'] = False
        all_castle_possibility[color]['right'] = False


chess_table = [['wR', '00', '00', 'wQ', 'wK', '00', '00', 'wR'],
               ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
               ['00', '00', '00', '00', '00', '00', '00', '00'],
               ['00', '00', '00', '00', '00', '00', '00', '00'],
               ['00', '00', '00', '00', '00', '00', '00', '00'],
               ['00', '00', '00', '00', '00', '00', '00', '00'],
               ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
               ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR']]

#chess_table = [['00', '00', '00', '00', '00', '00', '00', '00'],
#               ['00', '00', 'bP', '00', '00', '00', '00', 'wK'],
#               ['00', '00', '00', '00', '00', '00', '00', '00'],
#               ['00', '00', '00', '00', '00', '00', '00', '00'],
#               ['00', '00', '00', '00', '00', '00', '00', '00'],
#               ['00', 'bB', '00', '00', '00', 'bQ', '00', '00'],
#               ['00', 'wP', '00', '00', '00', '00', '00', '00'],
#               ['00', '00', '00', '00', 'bK', '00', '00', '00']]


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

#variables to make the game run, board state etc...
x = 0
y = 0
previous_position = []
selected_piece = [0, 0, 0, 0]
current_possible_moves = []
current_player_color = 'w'
BUTTON_DOWN = False
changing_pawn_state = [False, 0, 999]#0 is place holder for the color, 999 is place holder for index
WHITE_castle_possibility = {'left': True, 'right': True}
BLACK_castle_possibility = {'left': True, 'right': True}
all_castle_possibility = {'w': WHITE_castle_possibility, 'b': BLACK_castle_possibility}

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

            #handling the changing state of pawn has priority over the movement of other pieces
            if changing_pawn_state[0]:
                for i in range(len(possible_pieces_rect)):
                    if possible_pieces_rect[i].collidepoint(mouse_pos):
                        new_piece = f'{changing_pawn_state[1]}{possible_pieces[i]}'
                        all_logic[changing_pawn_state[1]][changing_pawn_state[2]] = new_piece
                        pawn_line = calculate_line(all_rects[changing_pawn_state[1]][changing_pawn_state[2]].centery)
                        pawn_row = calculate_row(all_rects[changing_pawn_state[1]][changing_pawn_state[2]].centerx)
                        chess_table[pawn_line][pawn_row] = new_piece
                        new_piece_surf = pygame.image.load(f'image_things/{new_piece}.png')
                        new_piece_surf = pygame.transform.scale(new_piece_surf,(84,84))
                        all_surfs[changing_pawn_state[1]][changing_pawn_state[2]] = new_piece_surf
                        changing_pawn_state = [False, 0, 999]
            else:
                if selected_piece[0] == 0:
                    for i in range(len(all_rects[color])):
                        if all_rects[color][i].collidepoint(pygame.mouse.get_pos()):
                            previous_position = all_rects[color][i].center
                            selected_piece[0] = all_surfs[color][i]
                            selected_piece[1] = all_rects[color][i]
                            selected_piece[2] = i
                            selected_piece[3] = color
                            current_possible_moves = funcs.with_check_very_next_move(line, row, chess_table, all_castle_possibility)
                            BUTTON_DOWN = True
                            break

                else:
                    prev_line = calculate_line(previous_position[1])
                    prev_row = calculate_row(previous_position[0])
                    if current_possible_moves:
                        if [line, row] in current_possible_moves:

                            deal_with_piece_movement()

                            current_player_color = COLORS[COLORS.index(current_player_color) - 1]
                            #check_for_game_end(current_player_color, chess_table, all_castle_possibility)

                    selected_piece = [0, 0, 0, 0]
                    current_possible_moves = []
                    previous_position = []
                    BUTTON_DOWN = False

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_xpos = pygame.mouse.get_pos()[0]
            mouse_ypos = pygame.mouse.get_pos()[1]
            line = calculate_line(mouse_ypos)
            row = calculate_row(mouse_xpos)
            color = current_player_color
            if selected_piece[0] != 0 and BUTTON_DOWN:
                prev_line = calculate_line(previous_position[1])
                prev_row = calculate_row(previous_position[0])
                if current_possible_moves:
                    if [line, row] in current_possible_moves:

                        deal_with_piece_movement()

                        current_player_color = COLORS[COLORS.index(current_player_color) - 1]
                        #check_for_game_end(current_player_color, chess_table, all_castle_possibility)

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

    #print(all_castle_possibility['w'])

    if BUTTON_DOWN:
        mouse_pos = pygame.mouse.get_pos()
        selected_piece[1].centerx = mouse_pos[0]
        selected_piece[1].centery = mouse_pos[1]

    for color in all_surfs:
        for i in range(len(all_surfs[color])):
            screen.blit(all_surfs[color][i], all_rects[color][i])

    if changing_pawn_state[0]:
        step = 1 if changing_pawn_state[1] == 'w' else -1
        ranges = {'w': [7, list(range(7,3,-1))], 'b': [0, list(range(0, 4))]}
        pawn_line = calculate_line(all_rects[changing_pawn_state[1]][changing_pawn_state[2]].centery)
        pawn_row = calculate_row(all_rects[changing_pawn_state[1]][changing_pawn_state[2]].centerx)
        possible_pieces = ['Q', 'N', 'R', 'B']
        possible_pieces_rect = []
        choices_surf = pygame.surface.Surface((87.5, 87.5*4))
        choices_rect = choices_surf.get_rect(center=(calculate_xpos(pawn_row)-2,
                                                     calculate_ypos(pawn_line) + 3 + step*1.5*87.5))
        choices_surf.fill('white')
        screen.blit(choices_surf, choices_rect)
        j = 0
        for i in ranges[changing_pawn_state[1]][1]:
            piece_surf = pygame.image.load(f'image_things/{changing_pawn_state[1]}{possible_pieces[j]}.png')
            piece_surf = pygame.transform.scale(piece_surf, (84, 84))
            piece_rect = piece_surf.get_rect(center=(calculate_xpos(pawn_row)-2, calculate_ypos(i)))
            possible_pieces_rect.append(piece_rect)
            screen.blit(piece_surf, piece_rect)
            j += 1


    if selected_piece[0] != 0:
        if current_possible_moves:
            for i in range(len(current_possible_moves)):
                xpos = calculate_xpos(current_possible_moves[i][1])
                ypos = calculate_ypos(current_possible_moves[i][0])
                pygame.draw.circle(screen, 'black', (xpos, ypos), 10)

        screen.blit(selected_piece[0], selected_piece[1])

    pygame.display.update()
    clock.tick(60)