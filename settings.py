class Settings():
	def __init__(self):
		#Screen settings
		self.screen_width=1500
		self.screen_height=600
		self.bg_color=(230,230,230)
		
		#Ship settings
		self.ship_speed_factor=1.5
		self.ship_limit=3
		
		#bullet settings
		self.bullet_speed_factor=3
		self.bullet_width=3
		self.bullet_height=15
		self.bullet_color=122,33,78
		self.bullets_allowed=3

		#Alien settings
		self.alien_speed_factor=1
		self.fleet_drop_speed=10
		self.fleet_direction=1
		
		self.speedup_scale=1.1
		#how quickly the alien point values increase
		self.score_scale=1.5
		
		self.initialize_dynamic_settings()	
	
	def initialize_dynamic_settings(self):
		self.ship_speed_factor=1.5
		self.bullet_speed_factor=3
		self.alien_speed_factor=1
		
		self.fleet_direction=1
		
		#scoring
		self.alien_points=50
		
	def increase_speed(self):
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
