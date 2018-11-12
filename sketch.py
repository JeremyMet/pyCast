import pygame ;
from pygame.locals import * ;
import os, sys ;

import math ;

APP_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0])) ;
os.chdir(APP_FOLDER) ;


pygame.init() ;
fenetre = pygame.display.set_mode((640,480), RESIZABLE)
fond = pygame.image.load("./media/img/background.jpg").convert()
pygame.key.set_repeat(400, 30)

class pyCast(object):

    def __init__(self, surface, level_array, tile_dim):
        self.surface = surface ;
        self.level_array = level_array ;
        self.go = True ;
        self.tile_dim = tile_dim ;
        self.x_p = 0 ;
        self.y_p = 0 ;
        self.angle = 0 ;
        # "constants part"
        self.LEVEL_HEIGHT = len(level_array) ;
        self.LEVEL_WIDTH = len(level_array[0]) ;
        self.FOV = 120 ;
        self.WALK_SPEED = 2 ;
        self.ROT_SPEED = 2 ;


    def ctrl(self):
        for event in pygame.event.get():
            dir = 0 ;
            if event.type == QUIT:  # Si un de ces événements est de type QUIT
                self.go = False  # On arrête la boucle
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    self.angle += 1 ;
                    if self.angle == 360:
                        angle = 0 ;
                elif event.key == K_RIGHT:
                    self.angle -= 1 ;
                    if self.angle == -1:
                        self.angle = 359 ;
                elif event.key == K_UP:
                    dir = 1 ;
                elif event.key == K_DOWN:
                    dir = -1 ;
                if dir:
                    tmp_x_p = self.x_p+dir*self.WALK_SPEED*math.cos(math.radians(self.angle)) ;
                    tmp_y_p = self.y_p-dir*self.WALK_SPEED*math.sin(math.radians(self.angle)) ;
                    scaled_tmp_x_p = int(tmp_x_p) // self.tile_dim[1] ;
                    scaled_tmp_y_p = int(tmp_y_p) // self.tile_dim[1] ;
                    if scaled_tmp_x_p >= 0 and scaled_tmp_x_p < self.LEVEL_WIDTH:
                        if not(self.level_array[int(self.y_p) // self.tile_dim[1]][scaled_tmp_x_p]):
                            self.x_p = tmp_x_p ;
                    if scaled_tmp_y_p >= 0 and scaled_tmp_y_p < self.LEVEL_HEIGHT:
                        if not(self.level_array[scaled_tmp_y_p][int(self.x_p) // self.tile_dim[1]]):
                            self.y_p = tmp_y_p ;


    def set_pos(self, x, y):
        self.x_p = x ;
        self.y_p = y ;

    def draw_hero(self):
        # pygame.draw.rect(self.surface, (128, 64, 32), (self.x_p, self.y_p, 15, 15)) ;
        angleFov_0 = math.radians((self.angle+self.FOV//2)%360) ;
        angleFov_1 = math.radians((self.angle-self.FOV//2)%360) ;
        angle = math.radians(self.angle)
        pygame.draw.line(self.surface, (0, 128, 0), (self.x_p, self.y_p), (self.x_p+100*math.cos(angleFov_0), \
        self.y_p-100*math.sin(angleFov_0)), 2) ;
        pygame.draw.line(self.surface, (0, 128, 0), (self.x_p, self.y_p), (self.x_p+100*math.cos(angleFov_1), \
        self.y_p-100*math.sin(angleFov_1)), 2) ;
        pygame.draw.line(self.surface, (128, 0, 0), (self.x_p, self.y_p), (self.x_p+100*math.cos(angle), \
        self.y_p-100*math.sin(angle)), 2) ;





    def draw_grid(self):
        """
        :param: surface for the grid to be displayed.
        :param level_array: array that stores the current level (0 no wall, 1 wall).
        :param tile_dim: (int width, int height) : size of the primitive tile (that will be repeated to pave the grid)
        """
        color_white = (255, 255, 255) ;
        x_pos, y_pos = 0, 0 ;
        for line in level_array:
            for val in line:
                if val:
                    pygame.draw.rect(self.surface, color_white, (x_pos, y_pos, self.tile_dim[0], self.tile_dim[1]), 0) ;
                x_pos += self.tile_dim[0] ;
            y_pos += self.tile_dim[1] ;
            x_pos = 0 ;


level_array = [[1,1,1,1,1], [1,0,0,0,1], [1,0,1,0,1], [1, 0, 0, 0, 1], [1, 1, 1,1, 1]] ;

pyCastInst = pyCast(fenetre, level_array, (32, 32)) ;
pygame.display.flip() ;
pyCastInst.set_pos(32 ,32) ;

while pyCastInst.go:
    fenetre.fill((0,0,0)) ;
    pyCastInst.ctrl() ;
    pyCastInst.draw_grid()
    pyCastInst.draw_hero();
    pygame.display.flip();

