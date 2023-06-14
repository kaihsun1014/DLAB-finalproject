import pygame
import random
import time

# Constants
WIDTH = 450
HEIGHT = 900
BLOCK_SIZE = 45
ROWS = HEIGHT // BLOCK_SIZE
COLS = WIDTH // BLOCK_SIZE
SCORE_INCREMENT = 10
line = 0
timer = 0
difficulty = 40
count = 0
start='initial'
stop=0
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 800

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (127, 255, 212)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (124, 252, 0)
PINK = (218, 112, 214)
PURPLE = (138, 43, 226)
ORANGE = (255, 165, 0)

#musics
pygame.init()
bgm = pygame.mixer.Sound('./music/bgm.mp3')
complete = pygame.mixer.Sound('./music/complete.mp3')
win = pygame.mixer.Sound('./music/win.mp3')
lose = pygame.mixer.Sound('./music/lose.mp3')

# Tetromino shapes and their colors
SHAPES = [
    [[1, 1, 1, 1]],  # I-shape
    [[1, 1], [1, 1]],  # O-shape
    [[1, 1, 0], [0, 1, 1]],  # Z-shape
    [[0, 1, 1], [1, 1, 0]],  # S-shape
    [[1, 1, 1], [0, 1, 0]],  # T-shape
    [[1, 1, 1], [0, 0, 1]],  # L-shape
    [[1, 1, 1], [1, 0, 0]]   # J-shape
]

class Tetromino:
	def __init__(self):
		self.x = random.randint(0, 6)
		self.y = 0
		self.shape = random.choice(SHAPES)
		if self.shape == [[1, 1, 1, 1]]:
			self.color = CYAN
		elif self.shape == [[1, 1], [1, 1]]:
			self.color = YELLOW
		elif self.shape == [[1, 1, 0], [0, 1, 1]]:
			self.color = RED
		elif self.shape == [[0, 1, 1], [1, 1, 0]]:
			self.color = GREEN
		elif self.shape == [[1, 1, 1], [0, 1, 0]]:
			self.color = PINK
		elif self.shape == [[1, 1, 1], [0, 0, 1]]:
			self.color = PURPLE
		elif self.shape == [[1, 1, 1], [1, 0, 0]]:
			self.color = ORANGE


	def bottom_y(self):
		max_y = 0
		for row in range(len(self.shape)):
			for col in range(len(self.shape[row])):
				if self.shape[row][col] == 1:
					max_y = max(max_y, self.y + row)
		return max_y

	def center_x(self):
		leftmost = COLS
		rightmost = 0
		for row in range(len(self.shape)):
			for col in range(len(self.shape[row])):
				if self.shape[row][col] == 1:
					leftmost = min(leftmost, self.x + col)
					rightmost = max(rightmost, self.x + col)
		return (leftmost + rightmost) // 2

	def move_to_ground(self, game_board):
		while game_board.is_valid_position(self):
			self.y += 1
		self.y -= 1
		self.y += 1

	def move_down(self):
		self.y += 1

	def move_left(self):
		self.x -= 1

	def move_right(self):
		self.x += 1

	def rotate(self):
		self.shape = list(zip(*reversed(self.shape)))

	def draw(self, surface):
		for row in range(len(self.shape)):
			for col in range(len(self.shape[row])):
				if self.shape[row][col] == 1:
					pygame.draw.rect(surface, self.color, (self.x * BLOCK_SIZE + col * BLOCK_SIZE, self.y * BLOCK_SIZE + row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

class GameBoard:
    def __init__(self):
        self.board = [[BLACK] * COLS for _ in range(ROWS)]
        
    def is_valid_position(self, tetromino):
        shape = tetromino.shape
        for row in range(len(shape)):
            for col in range(len(shape[row])):
                if shape[row][col] == 1:
                    if (tetromino.y + row + 1 >= ROWS or tetromino.x + col < 0 or tetromino.x + col >= COLS or self.board[tetromino.y + row + 1][tetromino.x + col] != BLACK):
                        return False
        return True

        
    def draw_line(self, surface):
        for i in range(9):
            pygame.draw.rect(surface, (50,50,50), (45+45*i,0, 2, 900))
        for i in range(19):
            pygame.draw.rect(surface, (50,50,50), (0,45+45*i, 450, 2))
            
    def add_tetromino(self, tetromino):
        shape = tetromino.shape
        for row in range(len(shape)):
            for col in range(len(shape[row])):
                if shape[row][col] == 1:
                    if tetromino.y + row< ROWS and tetromino.x + col < COLS:
                        self.board[tetromino.y + row][tetromino.x + col] = tetromino.color


class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False
	
	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()
	
		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action	

while not stop:
	if start=='initial':
		
		screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		pygame.display.set_caption('Tetris')
		
		#load button images
		start_img = pygame.image.load('./img/start.png').convert_alpha()
		exit_img = pygame.image.load('./img/exit.png').convert_alpha()
		rule_img = pygame.image.load('./img/rule.png').convert_alpha()
		tetris_img = pygame.image.load('./img/tetris.png').convert_alpha()

		#create button instances
		start_button = Button(100, 250, start_img, 0.8)
		exit_button = Button(360, 250, exit_img, 0.8)
		rule_button = Button(575, 250, rule_img, 0.8)
		tetris = Button(260, 100, tetris_img, 2)

		#game loop
		running0 = True
		while running0:

			screen.fill((255, 255, 255))
			tetris.draw(screen)
				
			if rule_button.draw(screen):
				start = 'rule'
				running0 = False

			if start_button.draw(screen):
				start = 'game'
				running0 = False
				stop = 1
					
			if exit_button.draw(screen):
				start = 'leave'
				running0 = False

			#event handler 
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					start = 'leave'
					running0 = False

			pygame.display.update()

		pygame.quit()
			
	if start=='rule':

		screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		pygame.display.set_caption('Tetris')

		#load button images
		exit_img = pygame.image.load('./img/exit.png').convert_alpha()
		allrule_img = pygame.image.load('./img/allrule.png').convert_alpha()
		
		#create button instances
		exit_button = Button(350, 350, exit_img, 0.8)
		allrule = Button(75, 100, allrule_img, 0.8)

		#game loop
		running1 = True
		while running1:

			screen.fill((255, 255, 255))
			allrule.draw(screen)
		
			if exit_button.draw(screen):
				start = 'initial'
				running1 = False
				
					
			#event handler
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					start = 'leave'
					running1 = False
		
			pygame.display.update()

		pygame.quit()

	if start=='leave':
		pygame.quit()
		stop = 1
	
if start == 'game':
	pygame.init()
	clock = pygame.time.Clock()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('Tetris')
	
	# Create the game objects
	game_board = GameBoard()
	current_tetromino = Tetromino()
	
	# Game loop
	running2 = True
	print(f'Canceled lines: {line}')
	bgm.play(-1)
	while running2:
		timer += 2
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running2 = False
			elif line >= 10:
				print('Congratulations!')
				bgm.stop()
				win.play()
				time.sleep(2.2)
				running2 = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT and current_tetromino.x > 0:
					current_tetromino.move_left()
				elif event.key == pygame.K_RIGHT:
					for i in range(1, 5):
						if len(current_tetromino.shape[0]) == i and current_tetromino.x + i < COLS:
							current_tetromino.move_right()
				elif event.key == pygame.K_DOWN:
					current_tetromino.move_down()
				elif event.key == pygame.K_UP:
					rotated_tetromino = Tetromino()
					rotated_tetromino.x = current_tetromino.x
					rotated_tetromino.y = current_tetromino.y
					rotated_tetromino.shape = current_tetromino.shape.copy()
					rotated_tetromino.color = current_tetromino.color
					rotated_tetromino.rotate()
					if game_board.is_valid_position(rotated_tetromino):
						current_tetromino = rotated_tetromino
				elif event.key == pygame.K_SPACE:
					current_tetromino.move_to_ground(game_board)
		
		# Move the tetromino down
		if timer % difficulty == 0:
			current_tetromino.move_down()
			count += 1
		
		# Check for collision after moving
		if not game_board.is_valid_position(current_tetromino):
			if count == 0:
				print('You lose')
				bgm.stop()
				lose.play()
				time.sleep(3.3)
				running2 = False
			count = 0
			game_board.add_tetromino(current_tetromino)
			current_tetromino = Tetromino()
		
		# Clear completed rows
		rows_to_clear = []
		for row in range(ROWS):
			if all(cell != BLACK for cell in game_board.board[row]):
				rows_to_clear.append(row)
				line += 1
				if line < 10:
					complete.play()
				difficulty -= 2
				print(f'Canceled lines: {line}')
		for row in rows_to_clear:
			del game_board.board[row]
			game_board.board.insert(0, [BLACK] * COLS)
		
		# Draw everything
		screen.fill(BLACK)
		for row in range(ROWS):
			for col in range(COLS):
				pygame.draw.rect(screen, game_board.board[row][col], (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
		current_tetromino.draw(screen)
		game_board.draw_line(screen)
		pygame.display.flip()
		clock.tick(30)
	
	pygame.quit()

