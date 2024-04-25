import pygame

class Laser(pygame.sprite.Sprite):
	def __init__(self,position,speed,height):
		super().__init__()
		self.image = pygame.image.load("ship/laser/laser.png")
		self.rect = self.image.get_rect(center = position )
		self.speed = speed
		self.height = height
	
	def update(self):
		self.rect.y -= self.speed
		if self.rect.y > self.height + 15 or self.rect.y < 0:
			self.kill()