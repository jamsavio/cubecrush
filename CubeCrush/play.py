#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import graphics
import random

class Cube(object):
    ''' control keys'''
    left_key = False
    right_key = False
    up_key = False
    down_key = False

    seven_key = False
    nine_key = False
    one_key = False
    three_key = False
    ''''''
    
    estado_cubo = "WALKING"
    
    velocidade_meteoro = 0.6
    contador = 200
    desconto = 0

    pontuacao = 0
    pontuacao_meta = 150

    colidiu = False
    game_over = False
    perdeu_sound = False

    buracox=-12
    buracoz=-12
    buracoy=-3

    #-------------------------------------
    def __init__(self):
        self.lua_id = graphics.load_texture("texture/lua.jpg")
        self.superficie_id = graphics.load_texture("texture/ConcreteTriangles.png")
        self.preto_id = graphics.load_texture("texture/preto.png")

        #---Coordenadas---[x,y,z]-----------------------------
        self.coordinates = [0,1,0]
        self.z_random = random.randrange(-31,-9,1)
        self.x_random = random.randrange(-11,11,1)
        self.meteoro_coord = [self.x_random,22,self.z_random]

        #Carrega os vértices e as normais do objeto 
        self.tabuleiro = graphics.ObjLoader("obj/plane.txt")
        self.lua = graphics.ObjLoader("obj/lua.txt")
        self.cube = graphics.ObjLoader("obj/cube.txt")
        self.buraco = graphics.ObjLoader("obj/buraco.txt")
    
    def render_scene(self):
        #limpar buffers anteriores
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        #substitua a matriz atual pela matriz identidade
        glLoadIdentity()

        #iluminação ambiente
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT,[0,0,0,1.0])

        #add luz posicionada:
        glLightfv(GL_LIGHT0,GL_DIFFUSE,[2,2,2,1])
        glLightfv(GL_LIGHT0,GL_POSITION,[-12,5,0,1])
        
        gluLookAt(12.46, 20, -24.48, 0, 0, 0, 0, 1, 0)
        self.tabuleiro.render_texture(self.superficie_id,((0,0),(2,0),(2,2),(0,2)))
        self.lua.render_texture(self.lua_id,((0,0),(1,0),(1,1),(0,1)))

    def render_cube(self):
        glPushMatrix() 
        #translada o cubo para a coordenada atual 
        glTranslatef(self.coordinates[0],self.coordinates[1],self.coordinates[2])
        self.cube.render_scene()
        glPopMatrix()

    def render_meteoro(self):
        glPushMatrix()
        glTranslatef(self.meteoro_coord[0],self.meteoro_coord[1],self.meteoro_coord[2])
        self.cube.render_scene()
        glPopMatrix()

    def render_buraco_meteoro(self):
        glPushMatrix()
        glTranslatef(self.buracox,self.buracoy,self.buracoz)
        self.buraco.render_texture(self.preto_id,((0,0),(1,0),(1,1),(0,1)))  
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

        #verifica se o cubo caiu no buraco
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

                        if self.meteoro_coord[1] <= 2:
                            if self.meteoro_coord[0] <= self.coordinates[0]+1 and self.meteoro_coord[0] >= self.coordinates[0]-1:
                                colidiu_x=True
                            elif self.meteoro_coord[0] >= self.coordinates[0]-1 and self.meteoro_coord[0] <= self.coordinates[0]+1:
                                colidiu_x=True
                        
                        if colidiu_x == True:
                            if self.meteoro_coord[2] <= self.coordinates[2]+1 and self.meteoro_coord[2] >= self.coordinates[2]-1:
                                self.game_over=True
                                self.colidiu=True
                                colidiu_play.play(0)

                            elif self.meteoro_coord[2] >= self.coordinates[2]-1 and self.meteoro_coord[2] <= self.coordinates[2]+1:
                                self.game_over=True
                                self.colidiu=True
                                colidiu_play.play(0)
                else:
                    self.z_random = random.randrange(-31,-9,1)
                    self.x_random = random.randrange(-11,11,1)
                    #teste de colisão 
                    #self.meteoro_coord = [5, 22, -22]
                    self.meteoro_coord = [self.x_random, 22, self.z_random]
                    self.contador=200-self.desconto
            else:
                self.contador-=1
            print("Pontuacao: "+str(self.pontuacao))
    
    def mover_frente(self):
        self.coordinates[2] += 0.3  

    def mover_atras(self):
        self.coordinates[2] -= 0.3
            
    def mover_esquerda(self):
        self.coordinates[0] += 0.3 

    def mover_direita(self):
        self.coordinates[0] -= 0.3 

    def mover_diagonal_cima_direita(self):
        self.coordinates[2] += 0.3 
        self.coordinates[0] += 0.3 
    
    def mover_diagonal_cima_esquerda(self):
        self.coordinates[2] += 0.3 
        self.coordinates[0] -= 0.3 
    
    def mover_diagonal_baixo_direita(self):
        self.coordinates[2] -= 0.3 
        self.coordinates[0] -= 0.3 

    def mover_diagonal_baixo_esquerda(self):
        self.coordinates[2] -= 0.3 
        self.coordinates[0] += 0.3 

    def isjumping(self):
        jump = pygame.mixer.Sound("audio/jump.wav")
        if self.coordinates[1] >= 1:
            if self.estado_cubo == 'JUMPING UP':
                self.coordinates[1] += 0.6
                self.coordinates[2] += 1.8
                if(self.coordinates[1] >= 3):
                    jump.play(0)
                    self.estado_cubo = 'DOWN'
            if self.estado_cubo == 'JUMPING LEFT':
                self.coordinates[1] += 0.6
                self.coordinates[0] += 1.8
                if(self.coordinates[1] >= 3):
                    jump.play(0)
                    self.estado_cubo = 'DOWN'
            if self.estado_cubo == 'JUMPING RIGHT':
                self.coordinates[1] += 0.6
                self.coordinates[0] -= 1.8
                if(self.coordinates[1] >= 3):
                    jump.play(0)
                    self.estado_cubo = 'DOWN'
            if self.estado_cubo == 'JUMPING DOWN':
                self.coordinates[1] += 0.6
                self.coordinates[2] -= 1.8
                if(self.coordinates[1] >= 3):
                    jump.play(0)
                    self.estado_cubo = 'DOWN'   
            elif self.estado_cubo == 'DOWN':
                if self.coordinates[1] >= 0:
                    self.coordinates[1] -= 0.6
                    if self.coordinates[1] == 1:
                        self.estado_cubo = 'WALKING'
                else:
                    self.estado_cubo = 'WALKING'

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
            self.mover_esquerda()
        elif self.right_key:
            self.mover_direita()
        elif self.up_key:
            self.mover_frente()
        elif self.down_key:
            self.mover_atras()
        elif self.seven_key:
            self.mover_diagonal_cima_direita()
        elif self.nine_key:
            self.mover_diagonal_cima_esquerda()
        elif self.one_key:
            self.mover_diagonal_baixo_esquerda()
        elif self.three_key:
            self.mover_diagonal_baixo_direita()
    
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
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                done = True 
            
            if event.type == pygame.KEYDOWN:
                if cube.colidiu == False:
                    if event.key == pygame.K_a or event.key == pygame.K_KP4:
                        cube.mover_esquerda()
                        cube.left_key = True
                    elif event.key == pygame.K_d or event.key == pygame.K_KP6:
                        cube.mover_direita()
                        cube.right_key = True
                    elif event.key == pygame.K_w or event.key == pygame.K_KP8:
                        cube.mover_frente()
                        cube.up_key = True
                    elif event.key == pygame.K_UP:
                            #pulando com a seta de cima
                            cube.estado_cubo = "JUMPING UP"
                    elif event.key == pygame.K_DOWN:
                            #pulando com a seta de baixo
                            cube.estado_cubo = "JUMPING DOWN"
                    elif event.key == pygame.K_LEFT:
                            #pulando com a seta da esquerda
                            cube.estado_cubo = "JUMPING LEFT"
                    elif event.key == pygame.K_RIGHT:
                            #pulando com a seta da direita
                            cube.estado_cubo = "JUMPING RIGHT"
                    elif event.key == pygame.K_s or event.key == pygame.K_KP2:
                        cube.mover_atras()
                        cube.down_key = True
                    elif event.key == pygame.K_KP7:
                        cube.mover_diagonal_cima_direita()
                        cube.seven_key = True
                    elif event.key == pygame.K_KP9:
                        cube.mover_diagonal_cima_esquerda()
                        cube.nine_key = True
                    elif event.key == pygame.K_KP1:
                        cube.mover_diagonal_baixo_direita()
                        cube.one_key = True
                    elif event.key == pygame.K_KP3:
                        cube.mover_diagonal_baixo_esquerda()
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

        #renderiza a cena (piso, lua, iluminação, posição da câmera)
        cube.render_scene()

        #serve que o jogador possa observar o cubo caindo até o final da tela
        if cube.coordinates[1] > -50 and cube.colidiu == False:
            cube.render_cube()

        cube.render_meteoro()

        #se o meteoro atingiu o solo então faz o buraco na mesma coordenada do meteoro
        if cube.meteoro_coord[1] < 1 and cube.meteoro_coord[1] >= 0:
            cube.buracox=cube.meteoro_coord[0]
            cube.buracoy=0
            cube.buracoz=cube.meteoro_coord[2]
        cube.render_buraco_meteoro()

        #dispara som 'game over' quando não tiver tocando outro som (caso tenha sido game over)
        if cube.game_over == True and cube.perdeu_sound == False and pygame.mixer.get_busy() == False:
            perdeu = pygame.mixer.Sound("audio/game_over.wav")
            perdeu.play(0)
            cube.perdeu_sound = True #para não repetir

        pygame.display.flip()

    cube.delete_texture()
    pygame.quit()

if __name__ == '__main__':
	main()
