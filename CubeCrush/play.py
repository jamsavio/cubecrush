#!/usr/bin/env python

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import graphics
import random

class Cube(object):
    left_key = False
    right_key = False
    up_key = False
    down_key = False
    seven_key = False
    nine_key = False
    one_key = False
    three_key = False
    state = "WALKING"
    contador=200
    desconto=0
    colidiu=False
    perdeu_sound = False
    game_over = False
    pontuacao = 0
    velocidade_meteoro = 0.6
    pontuacao_meta = 150
    x = 10
    y = 500
    speed = 10
    buracox=-12
    buracoz=-12
    buracoy=-3

    #-------------------------------------
    def __init__(self):
        self.vertices = []
        self.faces = []
        self.lua = graphics.load_texture("texture/lua.jpg")
        self.surface_id = graphics.load_texture("texture/ConcreteTriangles.png")
        self.preto = graphics.load_texture("texture/preto.png")
        #---Coordinates----[x,y,z]-----------------------------
        self.coordinates = [0,1,0]
        self.z_random = random.randrange(-31,-9,1)
        self.x_random = random.randrange(-11,11,1)
        self.meteoro_coord = [self.x_random,22,self.z_random]
        self.ground = graphics.ObjLoader("obj/plane.txt")
        self.cenario = graphics.ObjLoader("obj/cenario.txt")
        self.pyramid = graphics.ObjLoader("obj/scene.txt")
        self.cube = graphics.ObjLoader("obj/cube.txt")
        self.buraco = graphics.ObjLoader("obj/buraco.txt")
    
    def render_scene(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        #add luz ambiente:
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT,[0.2,0.2,0.2,1.0])
        
        #add luz posicionada:
        glLightfv(GL_LIGHT0,GL_DIFFUSE,[2,2,2,1])
        glLightfv(GL_LIGHT0,GL_POSITION,[-12,5,0,1])
        
        glTranslatef(0,-0.5,0)   
        gluLookAt(12.46,20,-24.48,0,0,0,1,0)
        self.ground.render_texture(self.surface_id,((0,0),(2,0),(2,2),(0,2)))

    def render_cube(self):
        glPushMatrix() 
        glTranslatef(self.coordinates[0],self.coordinates[1],self.coordinates[2])
        self.cube.render_scene()
        glPopMatrix()

    def render_meteoro(self):
        glPushMatrix()
        glTranslatef(self.meteoro_coord[0],self.meteoro_coord[1],self.meteoro_coord[2])
        self.cube.render_scene()
        glPopMatrix()
    
    def render_cenario(self):
        glPushMatrix()
        self.cenario.render_texture(self.lua,((0,0),(1,0),(1,1),(0,1)))
        glPopMatrix()

    def render_buraco_meteoro(self):
        glPushMatrix()
        glTranslatef(self.buracox,self.buracoy,self.buracoz)
        self.buraco.render_texture(self.preto,((0,0),(1,0),(1,1),(0,1)))  
        glPopMatrix()

    def caindo(self):
        caindo = pygame.mixer.Sound("audio/caindo.wav")
        
	    #cubo 
        #caindo pelo x
        if self.coordinates[0] >= 11 or self.coordinates[0] <= -11:
            self.coordinates[1] -= 1
            self.game_over=True

        #caindo pelo z
        elif self.coordinates[2] >= 11 or self.coordinates[2] <= -11:
            self.coordinates[1] -= 1
            self.game_over=True

        #independente da pos de x e z se y for menor que a pos original entao cai
        elif self.coordinates[1] < 1:
            self.coordinates[1] -= 1
            self.game_over=True

        elif (self.coordinates[2] <= self.buracoz + 3 and self.coordinates[2] >= self.buracoz - 3) and self.buracoz != -12:
            if(self.coordinates[0] <= self.buracox + 3 and self.coordinates[0] >= self.buracox - 3 and self.coordinates[1] <= 1):
                self.coordinates[1] -= 1
                self.game_over=True

        if self.coordinates[1] < 1 and self.coordinates[1] > -1:
            caindo.play(0)

    def meteoro_caindo(self):
            colidiu_play = pygame.mixer.Sound("audio/explosion.wav")
            if self.contador <= 0:
                if self.meteoro_coord[1] >= 1:
                    self.meteoro_coord[1] -= self.velocidade_meteoro
                    self.meteoro_coord[2] += self.velocidade_meteoro

                    if self.colidiu == False:
                        colidiu_x=False
                        if self.meteoro_coord[0] <= self.coordinates[0] and self.meteoro_coord[0] >= self.coordinates[0]-1 and self.meteoro_coord[1] <= 2:
                            colidiu_x=True
                        elif self.meteoro_coord[0] >= self.coordinates[0] and self.meteoro_coord[0] <= self.coordinates[0]+1 and self.meteoro_coord[1] <= 2:
                            colidiu_x=True
                        if colidiu_x == True:
                            if self.meteoro_coord[2] <= self.coordinates[2] and self.meteoro_coord[2] >= self.coordinates[2]-1:
                                self.game_over=True
                                self.colidiu=True
                                colidiu_play.play(0)

                            elif self.meteoro_coord[2] >= self.coordinates[2] and self.meteoro_coord[2] <= self.coordinates[2] and self.meteoro_coord[2] <= self.coordinates[2]+1:
                                self.game_over=True
                                self.colidiu=True
                                colidiu_play.play(0)
                else:
                    self.z_random = random.randrange(-31,-9,1)
                    self.x_random = random.randrange(-11,11,1)
                    self.meteoro_coord = [self.x_random, 22, self.z_random]
                    self.contador=200-self.desconto
            else:
                self.contador-=1
            print("Pontuacao: "+str(self.pontuacao))
    
    def move_forward(self):
        self.coordinates[2] += 0.3
        self.coordinates[0] -= 0.3

    def move_back(self):
        self.coordinates[2] -= 0.3
        self.coordinates[0] += 0.3
            
    def move_left(self):
        self.coordinates[0] += 0.3 
        self.coordinates[2] += 0.3 
        
    def move_right(self):
        self.coordinates[0] -= 0.3
        self.coordinates[2] -= 0.3 

    def move_top_right(self):
        self.coordinates[2] += 0.3 
        self.coordinates[0] += 0.3 
    
    def move_top_left(self):
        self.coordinates[2] += 0.3 
        self.coordinates[0] -= 0.3
    
    def move_bottom_right(self):
        self.coordinates[2] -= 0.3 
        self.coordinates[0] -= 0.3

    def move_bottom_left(self):
        self.coordinates[2] -= 0.3
        self.coordinates[0] += 0.3 

    def isjumping(self):
        jump = pygame.mixer.Sound("audio/jump.wav")
        if self.coordinates[1] >= 1:
            if self.state == 'JUMPING UP':
                self.coordinates[1] += 0.6
                self.coordinates[2] += 1.8
                if(self.coordinates[1] >= 3):
                    jump.play(0)
                    self.state = 'DOWN'
            if self.state == 'JUMPING LEFT':
                self.coordinates[1] += 0.6
                self.coordinates[0] += 1.8
                if(self.coordinates[1] >= 3):
                    jump.play(0)
                    self.state = 'DOWN'
            if self.state == 'JUMPING RIGHT':
                self.coordinates[1] += 0.6
                self.coordinates[0] -= 1.8
                if(self.coordinates[1] >= 3):
                    jump.play(0)
                    self.state = 'DOWN'
            if self.state == 'JUMPING DOWN':
                self.coordinates[1] += 0.6
                self.coordinates[2] -= 1.8
                if(self.coordinates[1] >= 3):
                    jump.play(0)
                    self.state = 'DOWN'   
            elif self.state == 'DOWN':
                if self.coordinates[1] >= 0:
                    self.coordinates[1] -= 0.6
                    if self.coordinates[1] == 1:
                        self.state = 'WALKING'
                else:
                    self.state = 'WALKING'

    def calcular_pontuacao(self):
        levelup = pygame.mixer.Sound("audio/levelup.wav")
        if self.game_over == False:
            self.pontuacao_anterior = self.pontuacao
            self.pontuacao += 1
            if self.pontuacao >= self.pontuacao_meta:
                if self.desconto<500:
                    self.pontuacao_meta+=150
                    self.desconto+=20   
                    print("Avancou de nivel")
                elif self.velocidade_meteoro <= 2:
                    self.velocidade_meteoro += 0.1  
                    levelup.play(0)

    def update(self):
        if self.left_key:
            self.move_left()
        elif self.right_key:
            self.move_right()
        elif self.up_key:
            self.move_forward()
        elif self.down_key:
            self.move_back()
        elif self.seven_key:
            self.move_top_right()
        elif self.nine_key:
            self.move_top_left()
        elif self.one_key:
            self.move_bottom_left()
        elif self.three_key:
            self.move_bottom_right()
    
    def keyup(self):
        self.left_key = False
        self.right_key = False
        self.up_key = False
        self.down_key = False
        self.space = False
        self.seven_key = False
        self.nine_key = False
        self.three_key = False
        self.one_key = False

    def delete_texture(self):
        glDeleteTextures(self.lua)
        glDeleteTextures(self.surface_id)

def main():
    pygame.init()
    screen = pygame.display.set_mode((640,480),pygame.DOUBLEBUF|pygame.OPENGLBLIT)
    pygame.display.set_caption("Cube-Crush")
    done = False
    
    clock = pygame.time.Clock()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45,640.0/480.0,0.1,200.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)

    start = pygame.mixer.Sound("audio/start.wav")
    start.play(0)
    cube = Cube()

    #----------- Main Program Loop -------------------------------------
    while not done:
        cube.isjumping()
        cube.caindo()  
        cube.meteoro_caindo()
        cube.calcular_pontuacao()
            
        # --- Main event loop
        for event in pygame.event.get(): # Usuario fez algo
            if event.type == pygame.QUIT: # Se o usuario clicar em fechar
                done = True # Sinalize que terminamos, entao saimos desse loop
            
            if event.type == pygame.KEYDOWN:
                if cube.colidiu == False:
                    if event.key == pygame.K_a or event.key == pygame.K_KP4:
                        cube.move_left()
                        cube.left_key = True
                    elif event.key == pygame.K_d or event.key == pygame.K_KP6:
                        cube.move_right()
                        cube.right_key = True
                    elif event.key == pygame.K_w or event.key == pygame.K_KP8:
                        cube.move_forward()
                        cube.up_key = True
                    elif event.key == pygame.K_UP:
                            cube.state = "JUMPING UP"
                    elif event.key == pygame.K_DOWN:
                            cube.state = "JUMPING DOWN"
                    elif event.key == pygame.K_LEFT:
                            cube.state = "JUMPING LEFT"
                    elif event.key == pygame.K_RIGHT:
                            cube.state = "JUMPING RIGHT"
                    elif event.key == pygame.K_s or event.key == pygame.K_KP2:
                        cube.move_back()
                        cube.down_key = True
                    elif event.key == pygame.K_KP7:
                        cube.move_top_right()
                        cube.seven_key = True
                    elif event.key == pygame.K_KP9:
                        cube.move_top_left()
                        cube.nine_key = True
                    elif event.key == pygame.K_KP1:
                        cube.move_bottom_right()
                        cube.one_key = True
                    elif event.key == pygame.K_KP3:
                        cube.move_bottom_left()
                        cube.three_key = True
                if event.key == pygame.K_SPACE:
                    del cube
                    start.play(0)
                    cube = Cube()

            if event.type == pygame.KEYUP:
                #print("x: "+str(cube.coordinates[0])+" | y: "+str(cube.coordinates[1])+" | z: "+str(cube.coordinates[2]))
                cube.keyup()

        cube.update()
        clock.tick(60)
        
        cube.render_scene()
        if cube.coordinates[1] > -50 and cube.colidiu == False:
            cube.render_cube()
        cube.render_meteoro()
        if cube.meteoro_coord[1] < 1 and cube.meteoro_coord[1] >= 0:
            cube.buracox=cube.meteoro_coord[0]
            cube.buracoy=0
            cube.buracoz=cube.meteoro_coord[2]
        cube.render_buraco_meteoro()
        cube.render_cenario()

        if cube.game_over == True and cube.perdeu_sound == False and pygame.mixer.get_busy() == False:
            perdeu = pygame.mixer.Sound("audio/game_over.wav")
            perdeu.play(0)
            cube.perdeu_sound = True

        pygame.display.flip()

    cube.delete_texture()
    pygame.quit()

if __name__ == '__main__':
	main()
