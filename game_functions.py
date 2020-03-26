import sys #use the sys module to exit the game when the player quits
from time import sleep   #to pause the game	
import pygame
from bullet import Bullet
from alien import Alien

def check_keydown_events(event,ai_settings,screen,ship,bullets):
	if event.key==pygame.K_RIGHT:
		ship.moving_right=True
	elif event.key==pygame.K_LEFT:
		ship.moving_left=True
	elif event.key==pygame.K_SPACE:
		fire_bullet(ai_settings,screen,ship,bullets)
	elif event.key==pygame.K_q:
		sys.exit()
		
def fire_bullet(ai_settings,screen,ship,bullets):
	#Fire a bullet if limit not reached yet
	if len(bullets)<ai_settings.bullets_allowed:
		new_bullet=Bullet(ai_settings,screen,ship)
		bullets.add(new_bullet) 

def check_keyup_events(event,ship):
	if event.key==pygame.K_RIGHT:
		ship.moving_right=False
	elif event.key==pygame.K_LEFT:
		ship.moving_left=False

def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
	#response to keypass  and mouse events
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			sys.exit()
		elif event.type==pygame.KEYDOWN:
			check_keydown_events(event,ai_settings,screen,ship,bullets)
		elif event.type==pygame.KEYUP:
			check_keyup_events(event,ship)
		elif event.type==pygame.MOUSEBUTTONDOWN:
			mouse_x,mouse_y=pygame.mouse.get_pos()
			check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)

def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
	button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y)
	if button_clicked and not stats.game_active:
		#reset the game settings
		ai_settings.initialize_dynamic_settings()
		#hide the mouse cursor
		pygame.mouse.set_visible(False)
		#reset the game statistics
		stats.reset_stats()
		stats.game_active=True
		
		#Reset the scoreboard images
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()
		
		#empty the list of aliens and bullets
		aliens.empty()
		bullets.empty()
		
		#create a new fleet and center the ship
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()

def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
	#Redraw the screen during each pass through the loop
	screen.fill(ai_settings.bg_color)
		
	#Redraw all bullets behind ship and aliens
	for bullet in bullets.sprites():
		bullet.draw_bullet()
		
	ship.blitme()
	aliens.draw(screen)
	
	#Draw the score infomation
	sb.show_score()
	
	#Draw the play button if the game is inactive
	if not stats.game_active:
		play_button.draw_button()
		
	#Make the most recently drawnn screen visible
	pygame.display.flip()   #continually update the display to show the new positions of elements and hide the old ones, creating the illusion of smooth movement
def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
	bullets.update()
		
	#Get rid of bullets that have disappeared
	for bullet in bullets.copy():
		if bullet.rect.bottom<=0:
			bullets.remove(bullet) 
			
	check_bullet_alien_collision(ai_settings,screen,stats,sb,ship,aliens,bullets)
def check_bullet_alien_collision(ai_settings,screen,stats,sb,ship,aliens,bullets):
	
	#check for any bullets that have hit aliens
	#if so, get rid of the bullet and alien
	collisions=pygame.sprite.groupcollide(bullets,aliens,True,True)   #The two True arguments tell Pygame whether to delete the bullets and aliens that have collided
	
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points*len(aliens)
			sb.prep_score()
		check_high_score(stats,sb)
	
	if len(aliens)==0:
		bullets.empty()
		ai_settings.increase_speed()
		
		#increase level
		stats.level += 1
		sb.prep_level()
		
		create_fleet(ai_settings,screen,ship,aliens)
			
def get_number_aliens_x(ai_settings,alien_width):
	available_space_x=ai_settings.screen_width-2*alien_width
	number_aliens_x=int(available_space_x/(2*alien_width))
	return number_aliens_x

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
	#create a new alien and place it in the row
	alien=Alien(ai_settings,screen)
	alien_width=alien.rect.width
	alien.x=alien_width+2*alien_width*alien_number
	alien.rect.x=alien.x
	alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
	aliens.add(alien)

def create_fleet(ai_settings,screen,ship,aliens):
	#Create a full fleet of aliens
	#Create an alien and find the number of aliens in a row
	alien=Alien(ai_settings,screen)
	number_aliens_x=get_number_aliens_x(ai_settings,alien.rect.width)
	number_rows=get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
	
	#Create the first row of aliens
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings,screen,aliens,alien_number,row_number)
def get_number_rows(ai_settings,ship_height,alien_height):
	#determine the number of rows of aliens that fit on the screen
	available_space_y=(ai_settings.screen_height-3*alien_height-ship_height)
	number_rows=int(available_space_y/(2*alien_height))
	return number_rows
	
def check_fleet_edges(ai_settings,aliens):
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break
			
def change_fleet_direction(ai_settings,aliens):
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1
	
def ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets):
	#respond to ship being hit by alien
	if stats.ships_left>0:
		stats.ships_left -= 1
	
		#update scoreboard
		sb.prep_ships()
	
		#empty the list of aliens and bullets	
		aliens.empty()
		bullets.empty()
	
		#create  a new fleet and center the ship
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()
	
		#Pause
		sleep(0.5)
	
	else:
		stats.game_active=False
		pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets):
	screen_rect=screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom>=screen_rect.bottom:
			ship_hit(ai_settings,screen,stats, sb, ship, aliens, bullets)
			break
	
def update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets):
	check_fleet_edges(ai_settings,aliens)
	aliens.update()
	
	#look for alien-ship collisions
	"""The method looks for any member of the group that’s collided with the sprite and stops looping through the group as soon as it finds one member that has collided with the sprite"""
	if pygame.sprite.spritecollideany(ship,aliens):   
		ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
	check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets)
	
def check_high_score(stats,sb):
	if stats.score>stats.high_score:
		stats.high_score=stats.score
		sb.prep_high_score()
	
	
	
