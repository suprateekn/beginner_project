def winner_check_for_p1(game):

	for i in range(0,3):
		if all([game[i][j] if game[i][j] == 1 else 0 for j in range(3)]) or all([game[j][i] if game[j][i] == 1 else 0  for j in range(0,3)]):
			return 1
	if all(game[x][y] if x+y == 2 and game[x][y] == 1 else 0 for x in range(0,3) for y in range(3,0,-1)):
		return 1
	if all([game[i][i] if game[i][i] == 1 else 0 for i in range(3)]):
		return 1

def winner_check_for_p2(game):

	for i in range(0,3):
		if all([game[i][j] if game[i][j] == 2 else 0 for j in range(3)]) or all([game[j][i] if game[j][i] == 2 else 0  for j in range(0,3)]):
			return 2
	if all(game[x][y] if x+y == 2 and game[x][y] == 2 else 0 for x in range(0,3) for y in range(3,0,-1)):
		return 2
	if all([game[i][i] if game[i][i] == 2 else 0 for i in range(3)]):
		return 2

	

game = [[0,0,0],
		[0,0,0],
		[0,0,0]]


for _ in range(9):
	p1 = input("Player 1's turn. Input the position you want to enter separated by a space : ").split()
	i = int(p1[0])
	j = int(p1[1])
	game[i][j] = 1
	print(f"{game[0]}\n{game[1]}\n{game[2]}")
	winner = winner_check_for_p1(game)
	if winner == 1:
		print('Player 1 wins!!')
		break


	p2 = input("Player 2's turn. Input the position you want to enter separated by a space : ").split()
	i = int(p2[0])
	j = int(p2[1])
	game[i][j] = 2
	print(f"{game[0]}\n{game[1]}\n{game[2]}")
	winner = winner_check_for_p2(game)
	if winner == 2:
		print('Player 2 wins!!')
		break