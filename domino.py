import random
random.seed(3)
def get_top_double_piece(set_pieces):
    doubles = [x for x in set_pieces if x[0] == x[1]]
    if len(doubles)==0:
        return None
    doubles.sort()
    return doubles[-1]

# generate the full set of pieces
full_pieces = []
for i in range(7):
    for j in range(i,7): # avoid repetition
        full_pieces.append([i,j])
shuffles = 0
while True:
    shuffles+=1
    # print('attempt ', shuffles)
    random.shuffle(full_pieces)
    Stock = full_pieces[:14]
    Computer = full_pieces[14:21]
    player = full_pieces[21:]
    Computer_snake = get_top_double_piece(Computer)
    player_snake = get_top_double_piece(player)
    if Computer_snake or player_snake : 
        break
# find Domino snake
if not Computer_snake :
    Computer_snake = [0, 0] 
if not player_snake :
    player_snake = [0, 0] 
if Computer_snake[0] > player_snake[0] :
    Domino_snake = Computer_snake
    Computer.remove(Computer_snake)
    first_to_move = 'player' 
else : 
    Domino_snake = player_snake
    player.remove(player_snake)
    first_to_move = 'computer'
# print('Stock pieces:', Stock)
# print('Computer pieces:', Computer)
# print('Player pieces:', player)
# print('Domino snake:', [Domino_snake])
# print('Status:', first_to_move)
#%%
def show_state(Stock, Computer, player, snake, next_to_move):
    print(70*'=')
    print(f'Stock size: {len(Stock)}')
    print(f'Computer pieces: {len(Computer)}')
    print()
    if len(snake) < 7:
        for x in snake:
            print(x, end='')
    else:
        for i in range(3):
            print(snake[i], end='')
        print('...', end='')
        for i in range(3):
            print(snake[i-3], end='')
    print('\n')
    print('Your pieces:')
    for i, p in enumerate(player):
        print(f'{i+1}:{p}')

    if len(player) == 0:
        print('\nStatus: The game is over. You won!')
        return True
    if len(Computer) == 0: 
        print('\nStatus: The game is over. The computer won!')
        return True
    if is_game_drawn(snake) : 
        splayer = sum_pieces(player)
        scomputer = sum_pieces(Computer)
        if splayer == scomputer:
            print("\nStatus: The game is over. It's a draw!")
            return True
        elif splayer < scomputer:
            print('\nStatus: The game is over. You won!')
        else : 
            print('\nStatus: The game is over. The computer won!')
        return True
    # Game is still going on
    if next_to_move=='computer':
        print('\nStatus: Computer is about to make a move. Press Enter to continue...')
    else:
        print("\nIt's your turn to make a move. Enter your command.")
    return False
from collections import deque
snake = deque([Domino_snake])
# show_state(Stock, Computer, player, snake, first_to_move)
#%%
def sum_pieces(pieces):
    return sum([p1+p2 for p1,p2 in pieces])
def is_game_drawn(snake):
    """
    check if The numbers on the ends of the snake are identical 
    and appear within the snake 8 times
    """
    occ=0
    if snake[0][0] != snake[-1][1]:
        return False
    snake_end = snake[-1][1]
    for s in snake:
        try:
            s.index(snake_end)
            occ += 1 # this is executed when previous line didnt raise error
        except:
            pass
    return occ == 8

def make_move(snake, piece, first_to_move):
    """
    male move if the piece match the tails of the snake and add the piece
    with the correct orientation
    if not then print an error message and do nothing to the snake"""
    tails = [snake[0][0], snake[-1][1]]
    if piece[0] == snake[0][0] or piece[1] == snake[0][0]: 
        piece.remove(snake[0][0])
        snake.appendleft([piece[0], snake[0][0]]) 
        return True
    if piece[0] == snake[-1][1] or piece[1] == snake[-1][1]: 
        piece.remove(snake[-1][1])
        snake.append([snake[-1][1], piece[0]])
        return True        
    if first_to_move == 'player':
        print('Illegal move. Please try again..')
    return False
def smart_computer_move(snake, computer):
    """
    Count the number of 0's, 1's, 2's, etc., in your hand, and in the snake.
    Each domino in your hand receives a score equal to the sum of appearances 
    of each of its numbers.
    """
    all_occ = { i: 0 for i in range(7)} # initialisation of the occurences
    for x,y in computer:
        all_occ[x]+=1; all_occ[y]+=1
    for x,y in snake:
        all_occ[x]+=1; all_occ[y]+=1
    score = [p + [all_occ[p[0]] + all_occ[p[1]]] for p in computer]
    score.sort(key=lambda x : x[-1], reverse=True)
    return score

# Game loop
err_msg = 'Invalid input. Please try again.'
while True:
    ending = show_state(Stock, Computer, player, snake, first_to_move)
    nb_player_pieces = len(player)
    if ending:
        break
    if first_to_move.lower() == 'player':
        while True:
            x = input()
            try:
                cmnd = int(x)
                if abs(cmnd) > nb_player_pieces:
                    print(err_msg)
                    continue
                if cmnd == 0:
                    try:
                        player.append(Stock.pop())
                    except:
                        pass 
                    first_to_move = 'computer'
                    break
                else:
                    legal_move = make_move(snake, player[abs(cmnd)-1], first_to_move)
                    if legal_move:
                        player.pop(abs(cmnd)-1)
                        first_to_move = 'computer'
                        break
            except:
                print(err_msg)
    else:
        while True:
            Enter=input()
            while len(Enter):
                Enter=input() # must press the Enter key which has a zero legth
            break 
        score = smart_computer_move(snake, Computer)
        ind = 0
        while ind < len(Computer): 
            best_piece = score[ind][:-1]
            # random.randint(-len(Computer), len(Computer))
            cmnd = Computer.index(best_piece) + 1
            legal_move = make_move(snake, Computer[abs(cmnd)-1], first_to_move)
            if legal_move:
                Computer.pop(abs(cmnd)-1)
                break
            ind +=1
        else:
            try:
                Computer.append(Stock.pop())
            except:
                pass 
        first_to_move = 'player'
    
    
    