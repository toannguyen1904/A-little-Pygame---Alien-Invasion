import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	
	def __init__(self,ai_settings,screen):
		#Initialize the ship and set its starting position
		super(Ship,self).__init__()
		self.screen=screen
		self.ai_settings=ai_settings
		
		#Load the ship image and get its rect
		self.image=pygame.image.load('images/ship.bmp')
		self.rect=self.image.get_rect()
		self.screen_rect=screen.get_rect()
		
		#Start each new ship at the bottom center of the screen
		self.rect.centerx=self.screen_rect.centerx   #the x-coordinate of the ship’s center match the centerx attribute of the screen’s rect
		self.rect.bottom=self.screen_rect.bottom   #the y-coordinate of the ship’s bottom equal to the value of the screen rect’s bottom attribute
		
		#Store a decimal value for the ship's center
		self.center=float(self.rect.centerx)
		
		#Movement flag
		self.moving_right=False
		self.moving_left=False
		
	def update(self):
		if self.moving_right and self.rect.right<self.screen_rect.right:
			self.center += self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left>0:
			self.center-= self.ai_settings.ship_speed_factor
		
		#update rect object from self.center
		self.rect.centerx=self.center
		
	def blitme(self):
		#Draw the ship at its current position
		self.screen.blit(self.image,self.rect)   #draw the image to the screen at the position specified by self.rect
	def center_ship(self):
		self.center=self.screen_rect.centerx
