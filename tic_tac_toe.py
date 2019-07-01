def winner_check_for_p1(game):
	global n
	for i in range(0,n):
		if all([game[i][j] if game[i][j] == 1 else 0 for j in range(n)]) or all([game[j][i] if game[j][i] == 1 else 0  for j in range(0,n)]):
			return 1
	if all(game[x][y] if x+y == n-1 and game[x][y] == 1 else 0 for x in range(0,n) for y in range(n,0,-1)):
		return 1
	if all([game[i][i] if game[i][i] == 1 else 0 for i in range(n)]):
		return 1

def winner_check_for_p2(game):
	global n
	for i in range(0,n):
		if all([game[i][j] if game[i][j] == 2 else 0 for j in range(n)]) or all([game[j][i] if game[j][i] == 2 else 0  for j in range(0,n)]):
			return 2
	if all(game[x][y] if x+y == n-1 and game[x][y] == 2 else 0 for x in range(0,n) for y in range(n,0,-1)):
		return 2
	if all([game[i][i] if game[i][i] == 2 else 0 for i in range(n)]):
		return 2

def print_grid(game):
	global n
	for i in range(n):
		print(f'{game[i]}')

def build_game_board(n):
	global game
	for i in range(n):
		game.append([])
		for j in range(n):
			game[i].append(0)

game = []

n = int(input('Enter the length of your game board : '))
build_game_board(n)
print_grid(game)
for _ in range(n**2):
	p1 = input("Player 1's turn. Input the position you want to enter separated by a space : ").split()
	i = int(p1[0])
	j = int(p1[1])
	game[i][j] = 1
	print_grid(game)
	winner = winner_check_for_p1(game)
	if winner == 1:
		print('Player 1 wins!!')
		break


	p2 = input("Player 2's turn. Input the position you want to enter separated by a space : ").split()
	i = int(p2[0])
	j = int(p2[1])
	game[i][j] = 2
	print_grid(game)
	winner = winner_check_for_p2(game)
	if winner == 2:
		print('Player 2 wins!!')
		break