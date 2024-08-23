import pygame

pygame.init()

screen = pygame.display.set_mode((800,800))
not_empty = pygame.surface.Surface((70,70))
not_empty.fill('yellow')

empty_surf = pygame.surface.Surface((70,200))
empty_surf.fill('white')
empty_surf.blit(not_empty,(0,0))

while True:
    screen.blit(empty_surf,(0,60))
    pygame.display.update()
