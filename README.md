O objetivo do jogo “cube-crush” é desviar dos cubos que caem em pontos randômicos do
tabuleiro. Quanto mais tempo o seu cubo consegue ficar sem ser atingido mais pontos são
acumulados e mais rápido os cubos vão sendo atirados no tabuleiro.

Requisitos mínimos
- Uso do OpenGL
Todo o projeto é renderizado em OpenGL.
- Interação por parte do usuário
O usuário pode se mover para qualquer direção através das teclas WASD ou através
do teclado número. Pelo teclado numérico é possível mover-se pela diagonal através
das teclas 7913. Além disso, é possível pular em uma direção através das setas do
teclado.
- Pontos de iluminação
O jogo possui luz ambiente e um ponto de luz difusa situado próximo a figura de
uma lua.
- Aplicação de textura
O tabuleiro, a lua e o efeito de buraco possuem textura.
- Controle de colisão
A colisão mais óbvia ocorre quando os cubos que estão caindo atinge o cubo
principal. É raro ele ser atingido diretamente pois quando os cubos caem eles fazem
buracos no tabuleiro, que nada mais são que objetos com textura preta. Se passar o
cubo por cima desses objetos o cubo cai do tabuleiro e o jogador perde, bem como
também se ultrapassar os limites do tabuleiro.
Implementações extras
- Foi utilizado recurso de som para dar uma maior experiência ao jogador.
Instruções de execução do código
● Requisitos:
○ Python 2.7.15
○ Pygame 1.9.6
○ PyOpenGL 3.1.0
● Execução do código:
○ No terminal dentro da pasta do jogo basta digitar “./play.py” ou “python
play.py”
● Instalação das bibliotecas:
○ pip install pygame
○ pip install pyopengl
