import pygame, sys, math
from pygame.locals import *

##-------------------------------------------------- Variables
size = 100
wood = (202, 164, 114)
white = (121, 36, 13)
cells = 8

##--------------------------------------------------- Consola

win = pygame.display.set_mode((size*cells, size*cells))
pygame.display.set_caption('Chess')
clock = pygame.time.Clock()

##-------------------------------------------------- Classes

class Board:
    def __init__(self):
        self.empty = [[None for x in range(8)] for y in range(8)]
        self.array = [
            [Rock('black', 0, 0), Knight('black', 1, 0), Bishop('black', 2, 0), King('black', 3, 0), Queen('black', 4, 0), Bishop('black', 5, 0), Knight('black', 6, 0), Rock('black', 7, 0)],
            [Pawn('black', i, 1) for i in range(8)],
            [None for x in range(8)],
            [None for x in range(8)],
            [None for x in range(8)],
            [None for x in range(8)],
            [Pawn('white', i, 6) for i in range(8)],
            [Rock('white', 0, 7), Knight('white', 1, 7), Bishop('white', 2, 7), King('white', 3, 7), Queen('white', 4, 7), Bishop('white', 5, 7), Knight('white', 6, 7), Rock('white', 7, 7)]]

    def update(self):
        draw_squares()
        all_sprites_list.draw(win)
        pygame.display.update()

    def move_piece(self, piece, x, y):
        if clicked_sprites:
            all_sprites_list.remove(board.array[y][x])
            sprites.remove(board.array[y][x])
        piece.x, piece.y = x, y
        piece.rect.x, piece.rect.y = x * size, y * size
        board.array[y][x] = piece

class Piece(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.color = color
        self.x, self.y = x, y
        self.color_white = True if self.color =='white' else False
        self.image = load_image('images/{}_{}.png'.format(type(self).__name__, color))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x *size, y* size
        win.blit(self.image, self.rect)
        
class Pawn(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)

class Rock(Piece):

    def __init__(self, color, x, y):
        super().__init__(color, x, y)

class Knight(Piece):

    def __init__(self, color, x, y):
        super().__init__(color, x, y)

class Bishop(Piece):

    def __init__(self, color, x, y):
        super().__init__(color, x, y)

class Queen(Piece):

    def __init__(self, color, x, y):
        super().__init__(color, x, y)

class King(Piece):

    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        
##-------------------------------------------------- Funciones
        
def load_image(filename, transparent=True):
        image = pygame.transform.scale(pygame.image.load(filename), (size,size))
        image = image.convert_alpha()
        if transparent:
            color = image.get_at((0,0))
            image.set_colorkey(color, RLEACCEL)
        return image

def draw_squares():
        for i in range(cells):
            for j in range(cells):
                color = wood if (i+j) / 2 == (i+j) // 2 else white
                pygame.draw.rect(win, color, (j*size, i*size, size, size))
        pygame.display.update()

def select_piece(x, y):
    pygame.draw.rect(win, (173,255,47), (y//100*size ,x//100*size, size, size), 5)
    pygame.display.update()


def main():
    
    global all_sprites_list, sprites, clicked_sprites, board
    
    draw_squares()
    pygame.display.update()
    make_move = False
    turn_white = True
    board = Board()

    all_sprites_list = pygame.sprite.Group()
    sprites = [piece for row in board.array for piece in row if piece]
    all_sprites_list.add(sprites)
    all_sprites_list.draw(win)
    
    pygame.display.update()
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and make_move == False:
                x, y = event.pos
                clicked_sprites = [s for s in sprites if s.rect.collidepoint(x, y)]
                if len(clicked_sprites) != 0 and clicked_sprites[0].color_white == turn_white:
                    piece = clicked_sprites[0]
                    select_piece(y, x)
                    oldx, oldy = x//size, y//size
                    make_move = True

            elif event.type == pygame.MOUSEBUTTONDOWN and make_move == True:
                x, y = event.pos[0]//size, event.pos[1]//size
                if oldx == x and oldy == y:
                    board.update()
                    make_move = False
                    break
                clicked_sprites = [s for s in sprites if s.rect.collidepoint(x*size, y*size)]
                board.move_piece(piece, x, y)
                board.update()
##                for array in board.array:
##                        for element in array:
##                            if element == None:
##                                print(element)
##                            else:
##                                print(element, element.x, element.y)
                
                make_move = False
                turn_white = not turn_white
        
        time = clock.tick(60)
    
##-------------------------------------------------- Iniciar

if __name__ == '__main__':
    pygame.init()
    main()

pygame.quit()
