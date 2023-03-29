#! python3

# Tic Tac Toe game
import pprint, random, copy, sys, signal

#TODO - maybe improve computer AI, save player and computer wins in a file

# 'tl' -> top left, 'tc' -> top center, 'tr' -> top right
# 'ml' -> mid left, 'mc' -> mid center, 'mr' -> mid right
# 'bl' -> bottom left, 'bc' -> bottom center, 'br' -> bottom right
board = { 'tl' : ' ', 'tc': ' ', 'tr': ' ', 'ml' : ' ', 'mc': ' ', 'mr': ' ','bl': ' ','bc': ' ','br': ' '}
playerWins, computerWins = 0, 0

def terminate_signal(sig, frame):
	print('\n\n\n' + "See you later!")
	sys.exit(0)

def drawBoard(board):
	print(board['tl'] + '|' + board['tc'] + '|' + board['tr'])
	print('-----')
	print(board['ml'] + '|' + board['mc'] + '|' + board['mr'])
	print('-----')
	print(board['bl'] + '|' + board['bc'] + '|' + board['br'])

def inputPlayerLetter():
	letter = ''
	while not (letter == 'X' or letter == 'O'):
		print('Do you want to be X or O?: ', end='')
		letter = input().upper()
	
	if letter == 'X':
		return ['X', 'O'] # first index is always player's letter
	return ['O', 'X']

def whoGoesFirst():
	if random.randint(0,1) == 0:
		return 'X'
	return 'O'

def getPlayerMove(board):
	print("It's your turn. ")
	move = ''
	while not move in board.keys():
		print('Choose a valid cell: ', end='')
		move = input().lower()	
	return move

def chooseRandomFromList(board, listToChoose):
	random_index = random.randint(0,len(listToChoose) - 1)
	return listToChoose[random_index]

def isSpaceFree(board, move):
	return board[move] == ' '

def getComputerMove(board, computerLetter):
	if computerLetter == 'X':
		playerLetter = 'O'
	else:
		playerLetter = 'X'

	moves_list = 'tl tc tr ml mc mr bl bc br'.split()

	# Check if computer can win
	for i in moves_list:
		duplicate = copy.copy(board)
		if isSpaceFree(duplicate, i):
			makeMove(duplicate,computerLetter, i)
			if isWinner(duplicate, computerLetter):
				return i

	# Check if player can win and block him
	for i in moves_list:
		duplicate = copy.copy(board)
		if isSpaceFree(duplicate, i):
			makeMove(duplicate, playerLetter, i)
			if isWinner(duplicate, playerLetter):
				return i

	# Place random move
	tile = '.'
	while tile != ' ':
		move = chooseRandomFromList(board, moves_list)
		tile = board[move]
	return move

def makeMove(board, letter, move):
	board[move] = letter

def isWinner(b, l):
	return ((b['tl'] == l and b['tc'] == l and b['tr'] == l) or 
		(b['ml'] == l and b['mc'] == l and b['mr'] == l) or 
		(b['bl'] == l and b['bc'] == l and b['br'] == l) or
		(b['tl'] == l and b['ml'] == l and b['bl'] == l) or
		(b['tc'] == l and b['mc'] == l and b['bc'] == l) or
		(b['tr'] == l and b['mr'] == l and b['br'] == l) or
		(b['tl'] == l and b['mc'] == l and b['br'] == l) or
		(b['tr'] == l and b['mc'] == l and b['bl'] == l))

def isBoardFull(b):
	return (b['tl'] != ' ' and b['tc'] != ' ' and b['tr'] != ' ' and 
		b['ml'] != ' ' and b['mc'] != ' ' and b['mr'] != ' ' and 
		b['bl'] != ' ' and b['br'] != ' ' and b['br'] != ' ')

def playAgain(board):
	for k in board.keys():
		board[k] = ' '
	play()

def play():
	global playerWins
	global computerWins
	if playerWins != 0 or computerWins != 0:
		print( '\n' + "Current score:")
		print("You won " + str(playerWins) + " times")
		print("Computer won " + str(computerWins) + " times", end='\n\n')
	moves_order = whoGoesFirst()
	playerLetter, computerLetter = inputPlayerLetter()
	if playerLetter == moves_order[0]:
		print("You're going first!")
		turn = 'player'
	else:
		print("The computer goes first!")
		turn = 'computer'

	gameIsPlaying = True

	while gameIsPlaying: 
		if turn == 'player':
			while True:
				move = getPlayerMove(board)
				if isSpaceFree(board, move):
					break
			makeMove(board, playerLetter, move)
			drawBoard(board)
			if isWinner(board, playerLetter):
				print('Congratulations! You won :)')
				gameIsPlaying = False
				playerWins += 1
				break
			turn = 'computer'
		else:
			print('\n' + 'Computer turn!', end='\n\n')
			move = getComputerMove(board, computerLetter)
			makeMove(board, computerLetter, move)
			drawBoard(board)
			if isWinner(board, computerLetter):
				print('Sorry.. You lost :(')
				gameIsPlaying = False
				computerWins += 1
				break
			turn = 'player'
		if isBoardFull(board):
			print("It's a tie!")
			gameIsPlaying = False
			break

	again = ''
	while again != 'y' and again != 'n':
		print('Want to play again? (y/n): ', end='')
		again = input().lower()
	
	if again == 'y':
		playAgain(board)
	else:
		print('Goodbye :)')
		sys.exit(0)


print('Welcome to the Tic Tac Toe game!')
print("HINT: if you want to place your tile in the top left corner, input 'tl' ")
print("HINT: available moves -> tl,tc,tr; ml,mc,mr; bl,bc,br;")
signal.signal(signal.SIGINT, terminate_signal)
play()
