import pyxel
import random
import torch
import torch.nn as nn

""" class DQN(nn.Module):
    def __init__(self):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(4, 128)  # 4 entrées: x et y pour serpent et fruit
        self.fc2 = nn.Linear(128, 256)
        self.fc3 = nn.Linear(256, 4)  # 4 sorties: chaque sortie correspond à une direction

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x """

class App:
    def __init__(self):
        pyxel.init(300, 200, title="Snake", fps=30,quit_key=pyxel.KEY_ESCAPE)
        self.restart_game()

    def draw(self):
        pyxel.cls(0)
        #Vérifie s'il ya un gameover-
        for y in range(0, 200, 20): 
            for x in range(0, 300, 20):
                if (x + y) // 20 % 2 == 0: 
                    pyxel.rect(x, y, 20, 20, 1)
        if self.gameover == True:
            self.Snake = Snake(700,0)
            #pyxel.rect(100, 0, 50, 25, 11)
            pyxel.text(135,80,"GAMEOVER ",7)
            pyxel.text(120,100,"Appui sur R pour restart ",7)
        self.Snake.draw_snake()
        self.Fruit.draw_fruit()
        self.draw_score()

    def update(self):
        # Déplacement à droite
        if pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT):
            self.Snake.dx = 1
            self.Snake.dy = 0
        # Déplacement à gauche
        if pyxel.btn(pyxel.KEY_Q) or  pyxel.btn(pyxel.KEY_LEFT):
            self.Snake.dx = -1
            self.Snake.dy = 0
        # Déplacement en Haut
        if pyxel.btn(pyxel.KEY_Z) or  pyxel.btn(pyxel.KEY_UP):
            self.Snake.dx = 0
            self.Snake.dy = -1
        # Déplacement en bas
        if pyxel.btn(pyxel.KEY_S) or  pyxel.btn(pyxel.KEY_DOWN):
            self.Snake.dx = 0
            self.Snake.dy = 1
        #Le fait bouger constament
        self.Snake.move()
        #Quand il y a un gameover permettre de restart la game
        if self.gameover:
            if pyxel.btn(pyxel.KEY_R):
                self.restart_game()
        #Quand il mange un fruit
        if self.Snake.Snake[0][0] == self.Fruit.x and self.Snake.Snake[0][1] == self.Fruit.y:
            self.Snake.manger()
            #Vérifier ou le snake est pour éviter que le fruit spawn sur lui
            if not any(self.Snake.Snake[0] == self.x and self.Snake.Snake[1] == self.y for self.Snake.Snake[0] in self.Snake.Snake[:0]):
                self.x = random.randint(0, (pyxel.width - 20) // 20) * 20  
                self.y = random.randint(0, (pyxel.height - 20) // 20) * 20
            self.Fruit = Fruit()
            self.score += 1
        #Quand tout les 20 de score augmenter la diffilculté
        if self.score != 0 and self.score % 20 == 0:
            if not hasattr(self, 'dernier_palier') or self.dernier_palier != self.score:
                self.Snake.vitesse_max -= 1
                self.dernier_palier = self.score
        #Quand il touche un bord de l'écran
        head_x, head_y = self.Snake.Snake[0]
        if head_x < 0 or head_x >= 300 or head_y < 0 or head_y >= 200:
            self.gameover = True
        #Quand il se mange
        if self.score == 0:
            pass
        else:
            for self.Snake.taille in self.Snake.Snake[1:]:
                taille_x, taille_y = self.Snake.taille
                if head_x == taille_x and head_y == taille_y:
                    self.gameover = True    
    
    def draw_score(self):
        score = f"{self.score:04}"
        pyxel.text(1,190, score, 7)
    
    def restart_game(self):
        pyxel.cls(0)
        self.Snake= Snake(160,100)
        self.Fruit = Fruit()
        self.gameover = False
        self.score = 0
        pyxel.run(self.update, self.draw)

        

class Snake:
    def __init__(self,x ,y):
        self.x = x
        self.y = y
        self.taille = 3
        self.segment_size = 20
        self.Snake = [(self.x - self.segment_size * i, self.y) for i in range(self.taille)]
        self.vitesse_max = 5
        self.vitesse = 0
        self.dx = 1  
        self.dy = 0

    def draw_snake(self):
        for self.taile in self.Snake:
            x, y = self.taile
            pyxel.rect(x, y, self.segment_size, self.segment_size, 7)

    
    def move(self):
        self.vitesse += 1
        if self.vitesse > self.vitesse_max:
            new_head = (self.Snake[0][0] + self.dx * self.segment_size, 
                        self.Snake[0][1] + self.dy * self.segment_size)
            self.Snake.insert(0, new_head)
            self.Snake.pop()
            self.vitesse = 0

    def manger(self):
        
        #new_head = (self.Snake[0][0] + self.dx * self.segment_size,
         #           self.Snake[0][1] + self.dy * self.segment_size)
        dernier_segment = self.Snake[-1]
        nouveau_segment = (dernier_segment[0] - self.dx * self.segment_size,
                           dernier_segment[1] - self.dy * self.segment_size)
        self.Snake.append(nouveau_segment)
    
    def level(self):
        score = self.App.score
        score_max = 100000
        for score in range(1, score_max // 5 + 1):
            self.vitesse_max -= 3


class Fruit:
    def __init__(self):
       self.x = random.randint(0, (300 - 20) // 20) * 20
       self.y = random.randint(0, (200 - 20) // 20) * 20

    def draw_fruit(self):
        pyxel.rect(self.x, self.y, 20, 20, 8)

App()