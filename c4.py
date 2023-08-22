# DESCRIPTION: Simple terminal version of Connest four
#               implementing MINMAX function
#
# By: Josie Allen
# Date: 7/26/23
# CS 470 - AI

import numpy as np
import random
import math

ROW_SIZE = 6
COL_SIZE = 7

PLAYER = 0
AI = 1
PCOIN = 1
ACOIN = 2

WINLEN =4
# initialize game board
def create_board():
  board = np.zeros((ROW_SIZE,COL_SIZE))
  return board


# place coin
def drop_coin(board, row, col, coin):
  board[row][col] = coin

# check if top row has coin or not
def is_valid(board, col):
  return board[ROW_SIZE - 1][col] == 0

# find open row in selected column
def next_open_row(board, col):

  for r in range(ROW_SIZE):
    if board[r][col] == 0:
      return r

# check if the player won or not
def is_winner(board, coin):
  # check hor -
  for c in range(COL_SIZE-3):
    for r in range(ROW_SIZE):
      if board[r][c] == coin and board[r][c+1] == coin and board[r][c+2] == coin  and board[r][c+3] == coin:
        return True

  # check vert |
  for c in range(COL_SIZE):
    for r in range(ROW_SIZE-3):
      if board[r][c] == coin and board[r+1][c] == coin and board[r+2][c] == coin  and board[r+3][c] == coin:
        return True
  # check diag /
  for c in range(COL_SIZE-3):
    for r in range(ROW_SIZE-3):
      if board[r][c] == coin and board[r+1][c+1] == coin and board[r+2][c+2] == coin  and board[r+3][c+3] == coin:
        return True

  # check diagonal \
  for c in range(COL_SIZE-3):
    for r in range(3,ROW_SIZE):
      if board[r][c] == coin and board[r-1][c+1] == coin and board[r-2][c+2] == coin  and board[r-3][c+3] == coin:
        return True

# print board over x axis
def print_board(board):
  print(np.flip(board, 0))

# # finds best move
def coin_count(board, coin):
  score = 0
  # print("in coin count printing the arrays ")
  # find best move horizontally
  for r in range(ROW_SIZE):
    rows = [int(i) for i in list(board[r,:])]
    for c in range(COL_SIZE-3):
      length = rows[c:c+4]
      score += evaluate_board(length,coin)

  # find vertical

  for c in range(COL_SIZE):
    cols = [int(i) for i in list(board[:,c])]
    for r in range(ROW_SIZE-3):
      length = cols[r:r+4]
      score += evaluate_board(length,coin)

  # # diag /
  for r in range(ROW_SIZE-3):
    for c in range(COL_SIZE-3):
      length = [board[r+i][c+i] for i in range(WINLEN)]
      # print(length)
      score += evaluate_board(length,coin)

  # diag \
  for r in range(ROW_SIZE-3):
    for c in range(COL_SIZE-3):
      length = [board[r+3-i][c+i] for i in range(WINLEN)]
      # print(length)
      score += evaluate_board(length,coin)
  # print("end coin count printing the arrays ")
  return score

# used to test coin count
def best_move(board, coin):

  valid = get_is_valid(board)
  bestmove = -100000000
  bestcol = random.choice(valid)
  for col in valid:
    row = next_open_row(board, col)
    temp = board.copy()
    drop_coin(temp, row, col, coin)
    score = coin_count(temp, coin)
    if score > bestmove:
      bestmove = score
      bestcol = col

  return bestcol

def get_is_valid(board):
  emptySlots = []
  for col in range(COL_SIZE):
    if is_valid(board, col):
      emptySlots.append(col)

  return emptySlots

def evaluate_board(count,coin):
  score = 0
  opp_coin = PCOIN

  if coin == PCOIN:
    opp_coin = ACOIN

  if count.count(coin) == 4:
    score += 5
  elif count.count(coin) == 3 and count.count(0) == 1:
    score += 2
  elif count.count(coin) == 2 and count.count(0) == 2:
    score += 1

  if count.count(opp_coin) == 3 and count.count(0) == 1:
    score -= 5

  return score

def is_terminal_node(board):
  return is_winner(board, PCOIN) or is_winner(board, ACOIN) or len(get_is_valid(board)) == 0


# based on pseudo code
# https://en.wikipedia.org/wiki/Minimax
# alpha beta pruning
# https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning

def minimax(board, depth, alpha, beta , maximizingPlayer):
  valid_drops = get_is_valid(board)
  is_terminal = is_terminal_node(board)

  if depth == 0 or is_terminal:
    if is_terminal:
        if is_winner(board, ACOIN):
          return (None, 99999999999)
        elif is_winner(board, PCOIN):
          return (None, -math.inf)
        else:
          return(None, -9999999999)
    else:
        return (None, coin_count(board, ACOIN))

  if maximizingPlayer:
    value = -math.inf
    column = random.choice(valid_drops)
    for col in valid_drops:
      row = next_open_row(board, col)
      tempboard = board.copy()
      drop_coin(tempboard, row, col, ACOIN)       # idk why this doesnt work
      new_score = minimax(tempboard, depth-1, alpha, beta, False)[1]
      if new_score > value:
        value = new_score
        column = col
        alpha = max(alpha, value)
        if value >= beta:
          break
    return column, value
  else:
    value = math.inf
    column = random.choice(valid_drops)
    for col in valid_drops:
      row = next_open_row(board, col)
      boardCP = board.copy()
      drop_coin (boardCP, row, col , PCOIN)
      new_score = minimax(boardCP, depth -1, alpha, beta, True)[1]
      if new_score < value:
        value = new_score
        column = col
      beta = min(beta, value)
      if value <= alpha:
        break
    return column, value



board = create_board()
print_board(board)
gameover = False
player = 0


while not gameover:
  # Player  = 0
  if player == PLAYER:
    # ensure input is an integer
    col = int(input("Player make your selection(0-6):"))

    if is_valid(board,col):
      row = next_open_row(board, col)
      drop_coin(board, row, col, PCOIN)

      if is_winner(board, 1):
        print("Player  WON!")
        print_board(board)
        gameover = True
  else:

    # column = best_move(board, ACOIN)
    column, score = minimax(board, 5, -math.inf, math.inf, True)

    if is_valid(board, column):

      row = next_open_row(board, column)
      drop_coin(board, row, column, ACOIN)

      if is_winner(board, ACOIN):
        print_board(board)
        print("AI WON!")
        gameover = True

  #print board after each player f
    print_board(board)

  # alternate players
  player += 1
  player = player % 2
