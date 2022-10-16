from pygame import *
from random import randint
#1. Подключи игровую библиотеку pygame. Создай окно игры размером 700x500, дай ему название.
win_wid=700
win_hei=500
window=display.set_mode((win_wid,win_hei))
display.set_caption("SHOOTER")
#2. Создай игровой цикл с выходом при нажатии на «Закрыть окно». Задай FPS 60 кадров/сек. Установи фон игры.
clock=time.Clock()
FPS=60
back=image.load('galaxy.jpg')
back=transform.scale(back,(win_wid,win_hei))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
#переменные для подсчета убитых и пропущенных врагов
killed=0
passed=0
class GameSprite(sprite.Sprite):
	def __init__(self, width, height, img, x, y, speed):
		super().__init__()
		self.width=width
		self.height=height
		self.image=image.load(img)
		self.image=transform.scale(self.image,(self.width,self.height))
		self.rect=self.image.get_rect()
		self.rect.x=x
		self.rect.y=y
		self.speed=speed
	def reset(self):
		window.blit(self.image,(self.rect.x,self.rect.y))
class Hero(GameSprite):
	def __init__(self, width, height, img, x, y, speed):
		super().__init__(width, height, img, x, y, speed)
	def update(self):
		keys=key.get_pressed()
		if keys[K_LEFT] and self.rect.x>0:
			self.rect.x-=self.speed
		elif keys[K_RIGHT] and self.rect.x+self.width<win_wid:
			self.rect.x+=self.speed
	def fire(self):
		bullet=Bullet(width=20, height=20, img='bullet.png', x=self.rect.x, y=self.rect.y, speed=1)
		bullets.add(bullet)
class UFO(GameSprite):
	def __init__(self, width, height, img, x, y, speed):
		super().__init__(width, height, img, x, y, speed)
	def update(self):
		global passed, text_passed
		self.rect.y+=self.speed
		if self.rect.y>win_hei:
			passed+=1
			text_passed = font24.render("Пропущенно:"+str(passed),True,(0,255,0))
			self.rect.y=0
			self.rect.x=randint(0, win_wid-self.width)
class Bullet(GameSprite):
	def __init__(self, width, height, img, x, y, speed):
		super().__init__(width, height, img, x, y,speed)
	def update(self):
		self.rect.y-=self.speed
		if self.rect.y<0:
			self.kill()	

rocket=Hero(width=50, height=50, img="rocket.png", x=250, y=450, speed=1)#
bullets=sprite.Group()
ufos=sprite.Group()#СОЗДАЛИ ГРУППУ
for i in range(5):
	ufo = UFO(width=50, height=50, img="ufo.png", x=randint(0, win_wid-50), y=0, speed=1)# 
	ufos.add(ufo)#добавили в группу
font.init()#Подключаем шрифты
font24 = font.SysFont('Arial',24)#Задаем параметры шрифта
font25 = font.SysFont('Arial',180)#Задаем параметры шрифта
text_killed = font24.render("Убито:"+str(killed),True,(255,0,0))
text_passed = font24.render("Пропущенно:"+str(passed),True,(0,255,0))
text_win = font25.render("Победа:",True,(255,0,0))
text_loose = font25.render("Поражение:",True,(255,0,0))
font24 = font.SysFont('Arial',36)
game="in_process"
while 1:
	if game=="in_process":
		window.blit(back,(0,0))
		window.blit(text_killed,(0,20))
		window.blit(text_passed,(0,50))
		rocket.reset()
		rocket.update()
		ufos.draw(window)#отобразили группу
		ufos.update()
		bullets.draw(window)
		bullets.update()
		display.update()
		##############
		#Столкновения групп
		hits = sprite.groupcollide(bullets,ufos,True,True)
		for i in hits:
			killed+=1
			text_killed = font24.render("Убито:"+str(killed),True,(255,0,0))
			ufo = UFO(width=50, height=50, img="ufo.png", x=randint(0, win_wid-50), y=0, speed=1)# 
			ufos.add(ufo)#добавили в группу
		##############
		#столкновение спрайта и группы
		if sprite.spritecollide(rocket, ufos, True):
			quit()
		if passed >= 20:
			game="lose"
		if killed >= 10:
			game='win'
	elif game =='win':
		window.blit(text_win,(250,350))
		display.update()
	elif game =='lose':
		window.blit(text_loose,(250,350))
		display.update()
	for i in event.get():
		if i.type==QUIT:
			quit()
		if i.type == KEYDOWN:
			if i.key == K_SPACE:
				rocket.fire()
			if i.key == K_r:
				killed = 0
				passed = 0
				text_killed = font24.render("Убито:"+str(killed),True,(255,0,0))
				text_passed = font24.render("Пропущенно:"+str(passed),True,(0,255,0))
				rocket.rect.x=250
				ufos.empty()
				for i in range (5):
					ufo = UFO(width=50, height=50, img="ufo.png", x=randint(0, win_wid-50), y=0, speed=1)# 
					ufos.add(ufo)
				game = "in_process"
clock.tick(FPS)