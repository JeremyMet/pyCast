import pygame ;
from pygame.locals import * ;
import os, sys ;

import math ;

APP_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0])) ;
os.chdir(APP_FOLDER) ;

__SCREEN_WIDTH__ = 640 ;
__SCREEN_HEIGHT__ = 480 ;

pygame.init() ;
fenetre = pygame.display.set_mode((640,480), RESIZABLE)
fond = pygame.image.load("./media/img/background.jpg").convert()
pygame.key.set_repeat(400, 30)

class pyCast(object):

    def __init__(self, surface, level_array):
        self.surface = surface ;
        self.level_array = level_array ;
        self.go = True ;
        self.x_p = 0 ;
        self.y_p = 0 ;
        self.angle = 60 ;
        # "constants part"
        self.LEVEL_HEIGHT = len(level_array) ;
        self.LEVEL_WIDTH = len(level_array[0]) ;
        self.WALK_SPEED = 0.05 ;
        self.ROT_SPEED = 2 ;
        # engine constant part
        self.SCREEN_HEIGHT = 480 ;
        self.SCREEN_WIDTH = 640 ;
        self.FOV = 36 ;
        self.tile_dim = 64;



    def ctrl(self):
        for event in pygame.event.get():
            dir = 0 ;
            if event.type == QUIT:  # Si un de ces événements est de type QUIT
                self.go = False  # On arrête la boucle
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    self.angle -= 3 ;
                elif event.key == K_RIGHT:
                    self.angle += 3 ;
                elif event.key == K_UP:
                    dir = 1 ;
                elif event.key == K_DOWN:
                    dir = -1 ;
                if dir:
                    tmp_x_p = self.x_p+dir*self.WALK_SPEED*math.cos(math.radians(self.angle)) ;
                    tmp_y_p = self.y_p+dir*self.WALK_SPEED*math.sin(math.radians(self.angle)) ;
                    scaled_tmp_x_p = int(tmp_x_p) ;
                    scaled_tmp_y_p = int(tmp_y_p) ;
                    if scaled_tmp_x_p >= 0 and scaled_tmp_x_p < self.LEVEL_WIDTH:
                        if not(self.level_array[int(self.y_p)][scaled_tmp_x_p]):
                            self.x_p = tmp_x_p ;
                    if scaled_tmp_y_p >= 0 and scaled_tmp_y_p < self.LEVEL_HEIGHT:
                        if not(self.level_array[scaled_tmp_y_p][int(self.x_p)]):
                            self.y_p = tmp_y_p ;

    def set_pos(self, x, y):
        self.x_p = x ;
        self.y_p = y ;


    def casting_engine(self):
        min_bound = self.angle-(self.FOV>>1) ;
        max_bound = self.angle+(self.FOV>>1) ;
        print((min_bound, max_bound, self.angle)) ;
        self.angle = self.angle % 360;
        angle_step = self.FOV/__SCREEN_WIDTH__ ;
        # Cast engine
        x_screen = 0 ;
        raw_angle = -(self.FOV >> 1) ;
        angle = min_bound ;
        while min_bound <= angle < max_bound:
            # Cast the "Ray" tile per tile
            rangle = math.radians(angle) ;
            tan = math.tan(rangle)+0.000001 ; # avoid 0 division.
            invtan = 1/tan ;
            x_cast, y_cast = self.x_p,  self.y_p ;
            x_map, y_map = int(self.x_p), int(self.y_p) ;
            while(0 <= x_map < self.LEVEL_WIDTH) and (0 <= y_map < self.LEVEL_HEIGHT) and not(self.level_array[y_map][x_map]):
                reduced_angle = angle%360 ;
                if (0 <= reduced_angle < 90):
                    x_step = 1-math.modf(x_cast)[0] ;
                    y_step = 1-math.modf(y_cast)[0] ;
                elif (90 <= reduced_angle < 180):
                    x_step = -math.modf(x_cast)[0] ;
                    y_step = 1-math.modf(y_cast)[0];
                elif (180 <= reduced_angle < 270):
                    x_step = -math.modf(x_cast)[0] ;
                    y_step = -math.modf(y_cast)[0] ;
                else: # 270 <= angle < 360
                    x_step = 1-math.modf(x_cast)[0];
                    y_step = -math.modf(y_cast)[0] ;
                # Tersa's Trick  !!
                x_path = False ;
                if y_step == 0 : y_step = -1 ;
                if x_step == 0 : x_step = -1 ;
                if abs(tan) <= abs(y_step/x_step): # Tersa's Trick.
                    x_path = True ;
                    x_cast = x_cast + x_step ;
                    y_cast = y_cast + x_step*tan ;
                else:
                    y_cast = y_cast + y_step;
                    x_cast = x_cast + y_step * invtan;
                y_correct =-1 if (180 <= reduced_angle < 360) and not(x_path) else 0 ;
                x_correct =-1 if (90 <= reduced_angle < 270) and x_path else 0 ;
                x_map = int(x_cast)+x_correct ;
                y_map = int(y_cast)+y_correct ;


            ## Ray has been cast.
            current_block = self.level_array[y_map][x_map] ;
            dist = math.sqrt((x_cast-self.x_p)**2+(y_cast-self.y_p)**2)*math.cos(math.radians(raw_angle)) ; # cos avoids blow fish effect.
            if dist == 0: dist = 1 ;
            normalized_dist = 1-dist/(self.LEVEL_WIDTH+self.LEVEL_HEIGHT) ;
            if current_block == 1:
                wall_color = (127*normalized_dist, 127*normalized_dist, 127*normalized_dist) ;
            elif current_block == 2:
                wall_color = (196*normalized_dist, 128*normalized_dist, 128*normalized_dist) ;
            elif current_block == 3:
                wall_color = (0, normalized_dist*128, normalized_dist*196) ;
            y_screen_top = (__SCREEN_HEIGHT__ >> 1) - 320/dist ;
            y_screen_bottom = (__SCREEN_HEIGHT__ >> 1) + 320/dist ;
            pygame.draw.line(self.surface, wall_color, (x_screen, y_screen_top), (x_screen, y_screen_bottom), 1) ;


            ## decomment for debug purpose
            # pygame.draw.line(self.surface, wall_color, (self.x_p * self.tile_dim, self.y_p * self.tile_dim),
            #                  (x_cast * self.tile_dim, y_cast * self.tile_dim), 1);
            # torad = math.radians(self.angle);
            # torad_0 = math.radians(min_bound);
            # torad_1 = math.radians(max_bound);
            # pygame.draw.line(self.surface, (128, 0, 0), (self.x_p * self.tile_dim, self.y_p * self.tile_dim), (
            # self.x_p * self.tile_dim + 100 * math.cos(torad), self.y_p * self.tile_dim + 100 * math.sin(torad)), 2);
            #



            x_screen+=1 ;
            raw_angle+=angle_step ;
            angle+=angle_step ;








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
                    if val == 1:
                        wall_color = (127, 127, 127);
                    elif val == 2:
                        wall_color = (196, 128, 128);
                    elif val == 3:
                        wall_color = (0, 128, 196);

                    pygame.draw.rect(self.surface, wall_color, (x_pos, y_pos, self.tile_dim, self.tile_dim), 0) ;
                x_pos += self.tile_dim ;
            y_pos += self.tile_dim ;
            x_pos = 0 ;


level_array = [[1,1,1,1,1], [1,0,0,0,1], [1,0,2,0,1], [1, 0, 0, 0, 1], [1, 3, 1, 3, 1]] ;

pyCastInst = pyCast(fenetre, level_array) ;
pygame.display.flip() ;
pyCastInst.set_pos(1.5 ,1.5) ;

while pyCastInst.go:
    fenetre.fill((0,0,0)) ;
    pyCastInst.ctrl() ;
    # pyCastInst.draw_grid()
    pyCastInst.casting_engine();
    pygame.display.flip();

