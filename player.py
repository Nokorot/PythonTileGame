
import pygame
from quark import qGameObject

from qMaths import qVec

class Player(qGameObject):
    speed = 5

    def __init__(self, sprite):
        self.sprite = sprite

    def Update(self):
        keys = pygame.key.get_pressed()
        x = { pygame.K_LEFT: qVec(-1, 0),
              pygame.K_RIGHT: qVec(+1, 0),
              pygame.K_UP: qVec(0,-1),
              pygame.K_DOWN: qVec(0, +1)}
        x = filter(lambda (k,v): keys[k], x.items())
        self.pos += reduce(lambda x,y: x+y[1], x, qVec(0,0)).normalize() \
                    * self.speed

        '''if keys[pygame.K_LEFT]:
            self.pos += qVec(-1, 0)
        if keys[pygame.K_RIGHT]:
            self.pos += qVec(+1, 0)
        if keys[pygame.K_UP]:
            self.pos += qVec(0, -1)
        if keys[pygame.K_DOWN]:
            self.pos += qVec(0, +1)'''

    def Render(self, screen):
        self.sprite.render(screen, self.getPos())

    def EventAction(self, event):
        pass
