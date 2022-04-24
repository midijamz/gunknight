import pygame
import os
import math

WIDTH, HEIGHT = 300,300
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("GUN KNIGHT")

FPS = 60

PLAYER_IMAGE = pygame.image.load(os.path.join('Assets/Entities','player.png'))
LEVEL_ONE = pygame.image.load(os.path.join('Assets/Levels','level1.png'))
LEVEL_TWO = pygame.image.load(os.path.join('Assets/Levels','bosstime.png'))
SLIME_IMAGE = pygame.image.load(os.path.join('Assets/Entities','slime.png'))
GAME_OVER_IMAGE = pygame.image.load(os.path.join('Assets/Levels','gameover.png'))
TITLE_IMAGE = pygame.image.load(os.path.join('Assets/Levels','gun knight.png'))
CAPYBARA = pygame.image.load(os.path.join('Assets/Entities','capybara.png'))
TRAPPED = pygame.image.load(os.path.join('Assets/Entities','trapped.png'))
FLYER = pygame.image.load(os.path.join('Assets/Entities','flyer.png'))
pygame.mouse.set_visible(False)
CURSOR_IMAGE = pygame.image.load(os.path.join('Assets/Entities','cursor.png')).convert_alpha()
pygame.font.init()
BOSS_HP = pygame.font.SysFont('comicsans', 10)
WINNER_IMAGE = pygame.image.load(os.path.join('Assets/Levels','winner.png'))
TRANSITION = pygame.image.load(os.path.join('Assets/Levels','transition.png'))

WHITE = (255, 255, 255)

SLIME_HIT = pygame.USEREVENT + 1
GAME_OVER = pygame.USEREVENT + 2
CAPYBARA_HIT = pygame.USEREVENT + 3
YOU_WIN = pygame.USEREVENT + 4
FLYER_HIT = pygame.USEREVENT + 4

def draw_window(player,slime,flyer,bullets,at_title):
    WIN.blit(LEVEL_ONE, (0,0))
    WIN.blit(PLAYER_IMAGE, (player.x,player.y))
    WIN.blit(FLYER,(flyer.x,flyer.y))
    WIN.blit(SLIME_IMAGE, (slime.x,slime.y))
    WIN.blit(CURSOR_IMAGE,(pygame.mouse.get_pos())) 
    for bullet in bullets:
        bullet.draw(WIN)
    if at_title:
        WIN.blit(TITLE_IMAGE, (0,0))
    pygame.display.update()


def draw_window_level2(player,boss_fight,bullets,level2_coords,capybara,capybara_hp,winner):
    

    if not boss_fight:
        WIN.blit(LEVEL_TWO, (0,level2_coords))#level2_coords
        WIN.blit(PLAYER_IMAGE, (player.x,player.y+level2_coords))
    else:

        boss_hp = BOSS_HP.render(
            str(capybara_hp), 1, WHITE
        )
        WIN.blit(LEVEL_TWO, (0,-306))#level2_coords
        WIN.blit(TRAPPED, (141,34))
        WIN.blit(PLAYER_IMAGE, (player.x,player.y+level2_coords))
        for bullet in bullets:
            bullet.draw(WIN)
        if not winner:
            WIN.blit(CAPYBARA, (capybara.x,capybara.y))
        WIN.blit(boss_hp, (65, 6))
    
    if winner:
        WIN.blit(WINNER_IMAGE,(74,71))
        
    WIN.blit(CURSOR_IMAGE,(pygame.mouse.get_pos())) 

    pygame.display.update()

def slime_movement(enemy,player,isHit,slime_hp):
    if slime_hp > 0:
        #flung in opposite direction if hit
        if isHit:
            if player.x < enemy.x:
                enemy.x += 5
            else: enemy.x -= 5
            if player.y < enemy.y:
                enemy.y += 5
            else: enemy.y -= 5

        if pygame.time.get_ticks() % 5 == 0:
            if player.x < enemy.x:
                enemy.x -= 1
            else: enemy.x += 1
            if player.y < enemy.y:
                enemy.y -= 1
            else: enemy.y += 1

def flyer_movement(flyer,player,isHit,flyer_hp):
    if flyer_hp > 0:
        """
        #flung in opposite direction if hit
        if isHit:
            if player.x < flyer.x:
                flyer.x += 5
            else: flyer.x -= 5
            if player.y < flyer.y:
                flyer.y += 5
            else: flyer.y -= 5
        """

        if pygame.time.get_ticks() % 2 == 0:
            if flyer.x >= 53 and flyer.x <= 230:
                if player.x < flyer.x:
                    flyer.x += 1
                else: flyer.x -= 1
            if flyer.y >= 74 and flyer.y <= 227:
                if player.y < flyer.y:
                    flyer.y += 1
                else: flyer.y -= 1

def player_handle_input(keys_pressed,player):
    if keys_pressed[pygame.K_a] and player.x >= 53: #Left
        player.x -= 2
    if keys_pressed[pygame.K_d] and player.x <= 230: #Right
        player.x += 2
    if keys_pressed[pygame.K_w] and player.y >= 74: #Up
        player.y -= 2
    if keys_pressed[pygame.K_s] and player.y <= 227: #Down
        player.y += 2 

def handle_attack(player,slime,flyer,flyer_hp,bullets,slime_hp):
    for bullet in bullets:  
        if slime.collidepoint(bullet.pos):
            if slime_hp > 0:
                bullets.remove(bullet)
                pygame.event.post(pygame.event.Event(SLIME_HIT))
        if flyer.collidepoint(bullet.pos):
            if flyer_hp > 0:
                bullets.remove(bullet)
                pygame.event.post(pygame.event.Event(FLYER_HIT))
        if bullet.pos[0] <= 53 or bullet.pos[0] > 245 or bullet.pos[1] <74 or bullet.pos[1] >227:
            try:
                bullets.remove(bullet)
            except:
                print("exception.")
    if slime.colliderect(player) and slime_hp > 0:
        pygame.event.post(pygame.event.Event(GAME_OVER))

def handle_boss_attack(player,capybara,bullets,capybara_hp,boss_fight):
    for bullet in bullets:  
        if capybara.collidepoint(bullet.pos):
            if capybara_hp > 0:
                bullets.remove(bullet)
                pygame.event.post(pygame.event.Event(CAPYBARA_HIT))
    if capybara.collidepoint(player.x,player.y-306) and capybara_hp > 0 and boss_fight:
        pygame.event.post(pygame.event.Event(GAME_OVER))

class Bullet:
    def __init__(self, x, y):
        self.pos = (x, y)
        mx, my = pygame.mouse.get_pos()
        self.dir = (mx - x, my - y)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0]/length, self.dir[1]/length)
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))

        self.bullet = pygame.Surface((7, 2)).convert_alpha()
        self.bullet.fill((255, 255, 255))
        self.bullet = pygame.transform.rotate(self.bullet, angle)
        self.speed = 2

    def update(self):  
        self.pos = (self.pos[0]+self.dir[0]*self.speed, 
                    self.pos[1]+self.dir[1]*self.speed)

    def draw(self, surf):
        bullet_rect = self.bullet.get_rect(center = self.pos)
        surf.blit(self.bullet, bullet_rect) 

def player_handle_input_level2(keys_pressed,player,boss_fight):
    if not boss_fight:
        if keys_pressed[pygame.K_a] and player.x >= 141: #Left
            player.x -= 2
        if keys_pressed[pygame.K_d] and player.x <= 142: #Right
            player.x += 2
        if keys_pressed[pygame.K_w] and player.y >= 37: #Up
            player.y -= 2
        if keys_pressed[pygame.K_s]: #Down
            player.y += 2
    else: 
        if keys_pressed[pygame.K_a] and player.x >= 5: #Left
            player.x -= 2
        if keys_pressed[pygame.K_d] and player.x <= 277: #Right
            player.x += 2
        if keys_pressed[pygame.K_w] and player.y >= 356: #Up
            player.y -= 2
        if keys_pressed[pygame.K_s] and player.y <= 572: #Down
            player.y += 2

def handle_boss_room(player,playerY):
    if player.y >= 149:
        return 148-playerY
    else: return 0

def capybara_movement_calculate_x(capybara,capybara_hp,capy_value_x):
    if capybara_hp > 0:
        if capybara.x + capy_value_x > 225 and capy_value_x > 0:
            return -2
        if capybara.x + capy_value_x < 4 and capy_value_x < 0:
            return 2

def capybara_movement_calculate_y(capybara,capybara_hp,capy_value_y):
    if capybara_hp > 0:    
        if capybara.y + capy_value_y > 239 and capy_value_y > 0:
            return -2
        if capybara.y + capy_value_y < 51 and capy_value_y < 0:
            return 2

def capybara_movement(capybara,capybara_hp,x,y):
    if capybara_hp > 0:
        capybara.x += x
        capybara.y += y



def main():
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join('Assets/Music','newbie.wav'))
    gun_cocked = pygame.mixer.Sound(os.path.join('Assets/SFX','gun_cocking.wav'))
    shoot = pygame.mixer.Sound(os.path.join('Assets/SFX','shoot.wav'))
    oof = pygame.mixer.Sound(os.path.join('Assets/SFX','oof.wav'))
    waaa = pygame.mixer.Sound(os.path.join('Assets/SFX','waaa.wav'))
    oof.set_volume(0.3)
    waaa.set_volume(0.25)

    player = pygame.Rect(150,150,16,16)
    slime = pygame.Rect(62,82,16,16)
    flyer = pygame.Rect(220,129,16,16)
    slime_hp = 5
    flyer_hp = 3


    gameover = False
    opacity_count = 0
    bullets = []
    flag = 0
    title = True
    title_opacity = 255

    #Flags
    # 0 - title screen
    # 1 - Start Music before beginning
    # 2 - Level 1 
    # 3 - Level 2 (Final Level)

    #Level 2 Variables
    level2_coords = 0
    boss_fight = False
    boss_trigger = False
    winner=False

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        
        while title:
            draw_window(player,slime,flyer,bullets,title)
            for event in pygame.event.get():
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    title = False
                    pygame.mixer.Sound.play(gun_cocked)

                if event.type == pygame.QUIT:
                    run = False

                
              
        while flag == 0:
            #Title Screen
            while title_opacity >= 0:
                WIN.blit(LEVEL_ONE, (0,0))
                WIN.blit(PLAYER_IMAGE, (player.x,player.y))
                WIN.blit(SLIME_IMAGE, (slime.x,slime.y))
                WIN.blit(CURSOR_IMAGE,(pygame.mouse.get_pos())) 
                TITLE_IMAGE.set_alpha(title_opacity)
                WIN.blit(TITLE_IMAGE,(0,0))
                title_opacity -= 0.3
                pygame.display.update()
            flag = 1  

        if flag == 1 :
            #Play Music
            pygame.mixer.music.play(-1)
            flag = 2

        while flag == 2:
            clock.tick(FPS)
            #First Level
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    run = False

                if event.type == GAME_OVER:
                    if not gameover:
                        pygame.mixer.music.stop()
                        pygame.mixer.Sound.play(waaa)
                        gameover = True
                        while opacity_count < 256:
                            GAME_OVER_IMAGE.set_alpha(opacity_count)
                            WIN.blit(GAME_OVER_IMAGE,(0,0))
                            opacity_count += 0.1
                            pygame.display.update()
                        pygame.quit()

                if event.type == SLIME_HIT:
                    pygame.mixer.Sound.play(oof)
                    slime_movement(slime,player,True,slime_hp)
                    slime_hp -= 1
                    print(F"slime has {slime_hp} hp")
                    if slime_hp <= 0 :
                        SLIME_IMAGE.set_alpha(0)

                if event.type == FLYER_HIT:
                    pygame.mixer.Sound.play(oof)
                    flyer_movement(flyer,player,True,flyer_hp)
                    flyer_hp -= 1
                    print(F"flyer has {flyer_hp} hp")
                    if flyer_hp <= 0 :
                        FLYER.set_alpha(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = (player.x+8,player.y+8)
                    if len(bullets) < 3:
                        pygame.mixer.Sound.play(shoot)
                        bullets.append(Bullet(*pos))
            
            
            if not gameover:
                for bullet in bullets[:]:
                    bullet.update()
                    if not WIN.get_rect().collidepoint(bullet.pos):
                        bullets.remove(bullet)
                keys_pressed = pygame.key.get_pressed()
                player_handle_input(keys_pressed,player)  
                slime_movement(slime,player,False,slime_hp)
                flyer_movement(flyer,player,False,flyer_hp)
                handle_attack(player,slime,flyer,flyer_hp,bullets,slime_hp)
                draw_window(player,slime,flyer,bullets,False)
   
            if slime_hp == 0 and flyer_hp == 0 : 
                for bullet in bullets:
                    bullets.remove(bullet)
                draw_window(player,slime,flyer,bullets,False)
                flag = 3 #onto next level


        transition_in=0
        transition_out=255
        while flag == 3:
            #transition to level 2
            while transition_in <256:
                WIN.fill((0,0,0))
                TRANSITION.set_alpha(transition_in)
                WIN.blit(TRANSITION,(0,0))
                transition_in += 0.5
                pygame.display.update()
            while transition_out > 0 :
                WIN.fill((0,0,0))
                TRANSITION.set_alpha(transition_out)
                WIN.blit(TRANSITION,(0,0))
                transition_out -= 0.5
                pygame.display.update()
            if transition_out == 0:
                flag = 4

        player.x = 142
        player.y = 38
        capybara = None
        capybara_hp = 15
        capybara = pygame.Rect(120,215,65,62)
        capy_value_x = 2
        capy_value_y = -2
        
        while flag == 4 :
            clock.tick(FPS)
            #Level 2
 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN and boss_fight:
                    pos = (player.x+8,player.y+8+level2_coords)
                    if len(bullets) < 5:
                        pygame.mixer.Sound.play(shoot)
                        bullets.append(Bullet(*pos))
                
                if event.type == CAPYBARA_HIT:
                    pygame.mixer.Sound.play(oof)
                    capybara_hp -= 1
                    if capybara_hp == 0:
                        pygame.event.post(pygame.event.Event(YOU_WIN))
                
                if event.type == GAME_OVER:
                    if not gameover:
                        gameover = True
                        pygame.mixer.music.stop()
                        pygame.mixer.Sound.play(waaa)
                        while opacity_count < 256:
                            GAME_OVER_IMAGE.set_alpha(opacity_count)
                            WIN.blit(GAME_OVER_IMAGE,(0,0))
                            opacity_count += 0.1
                            pygame.display.update()
                        pygame.quit()
                
                if event.type == YOU_WIN:
                    winner=True

            
            keys_pressed = pygame.key.get_pressed()
            player_handle_input_level2(keys_pressed,player,boss_fight)

            if boss_fight: 
                if capybara_movement_calculate_x(capybara,capybara_hp,capy_value_x) is not None:
                    capy_value_x = capybara_movement_calculate_x(capybara,capybara_hp,capy_value_x)
                if capybara_movement_calculate_y(capybara,capybara_hp,capy_value_y) is not None:
                    capy_value_y = capybara_movement_calculate_y(capybara,capybara_hp,capy_value_y)
                capybara_movement(capybara,capybara_hp,capy_value_x,capy_value_y)

            if not boss_fight:
                level2_coords = handle_boss_room(player,player.y)
            if level2_coords <= -306 and not boss_fight : boss_fight = True          

            if boss_fight and not boss_trigger:
                boss_trigger = True
                pygame.mixer.music.load(os.path.join('Assets/Music','afterparty.wav'))
                pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play(-1)
                


            for bullet in bullets[:]:
                bullet.update()
                if bullet.pos[0] > 300 or bullet.pos[0] < 0 or bullet.pos[1] > 300 or bullet.pos[1] < 0:
                    bullets.remove(bullet)

            handle_boss_attack(player,capybara,bullets,capybara_hp,boss_fight)
            draw_window_level2(player,boss_fight,bullets,level2_coords,capybara,capybara_hp,winner)
        

    pygame.quit()

if __name__ == '__main__':
    main()