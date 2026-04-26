from pygame import *
from random import *
from time import sleep
window = display.set_mode((800,500))
display.set_caption('tower defens')
background = transform.scale(image.load('background.png'),(800,500))
romashka = 'romashka (4).png'
font.init()
font1 = font.SysFont('Arial', 15)

towers = []
pulas = []
tropiimage = []
tropi = [
    [150,50,0,225],
    [50,150,100,75,-90],
    [275,50,150,75,90],
    [50,250,425,75,90],
    [125,50,475,275,-90],
    [50,250,600,275,90]

]

paths = [
    [125,250],
    [125,100],
    [450,100],
    [450,300],
    [625,300],
    [625,550]

]
life = 3
cash = 200
bosscount = 20
class SpriteClass(sprite.Sprite):
    def __init__(self,p_image,x,y,h,w,speed,life,vrag = 1):
        super().__init__()
        self.image = transform.scale(image.load(p_image),(h,w))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.h = h
        self.w = w 
        self.speed = speed
        self.path = 0
        self.pos = Vector2(x,y)
        self.life = life
        self.life1 = life
        self.vrag = vrag
    
    def draw(self):
        window.blit(self.image,(self.x,self.y))

    def gotopath(self):
        global life
        if self.path >= len(paths):
            self.kill()
            vragi1.remove(self)
            life -= 1
            return
        newpath = paths[self.path]
        center = Vector2(self.x+self.h/2,self.y+self.w/2)
        target =  Vector2(newpath[0],newpath[1])
        direction = target - center
        distance = direction.length()
        if direction.length() != 0:
            direction.normalize_ip()
        movement = direction * self.speed
        if movement.length() > distance or movement.length() == 0:
            self.path += 1 
            self.x,self.y = newpath[0]-self.h/2,newpath[1]-self.w/2
        else:
            self.x += movement[0]
            self.y += movement[1]

    #def
    def updat(self):
        global cash
        pula = self
        vrag = self.vrag
        stopFire = True
        center = Vector2(pula.x+pula.h/2,pula.y+pula.w/2)
        target =  Vector2(vrag.x,vrag.y)
        direction = target - center
        distance = direction.length()
        if direction.length() != 0:
            direction.normalize_ip()
        movement = direction * pula.speed
        if movement.length() > distance or movement.length() == 0:
            pula.x,pula.y = vrag.x+vrag.h/2,vrag.y+vrag.w/2
            pula.kill()
            pulas.remove(pula)
            vrag.life -= 20
            if vrag.life < 1:
                vrag.x = 999999999999999999999999999999999999
                vragi1.remove(vrag)
                cash += 25
            stopFire = False
        else:
            pula.x += movement[0]
            pula.y += movement[1]

class Tower(sprite.Sprite):
    def __init__(self,p_image,x,y,h,w,kd,range,cost,pulakd):
        super().__init__()
        self.image = transform.scale(image.load(p_image),(h,w))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.h = h
        self.w = w
        self.kd = kd
        self.range = range
        self.cost = cost
        self.pulakd = pulakd

    def draw(self):
        window.blit(self.image,(self.x,self.y))

    def findTarget(self):
        best = None
        bestdist = self.range + 1 
        for vrag in vragi1:
            vragcenter = Vector2(vrag.x+vrag.h/2, vrag.y+vrag.w/2)
            towercenter = Vector2(self.x+self.h/2, self.y+self.w/2)
            direction = vragcenter - towercenter
            dist = direction.length()

            if dist < self.range:
                if dist < bestdist:
                    best = vrag
                    bestdist = dist
            
        return best

    def fire(self,vrag):
        pula = SpriteClass('pula.png',self.x,self.y,40,40,5,1,vrag)
        pulas.append(pula)
        

        






vragikd = 0
vragi1 =  []
FPS = 60
game = True
finish = True
finish1 = True
clock = time.Clock()
for tropa1 in tropi:
    tropa = SpriteClass('tropa.bmp',tropa1[2],tropa1[3],tropa1[0],tropa1[1],1,0)
    tropiimage.append(tropa)

while game:
    font2 = font.SysFont('Arial', 40)
    cashFont =  font2.render('cash: '+str(cash),1,(0,255,0))
    lifeFont = font2.render('life:'+str(life),1,(0,255,0))
    gameOver = font2.render('Game Over,Press R to restart',1,(255,0,0))
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == MOUSEBUTTONDOWN and e.button == 1 and cash > 99:
            cash -= 100
            x1,y1 = e.pos
            tower = Tower(romashka,x1-37.5,y1-37.5,75,75, 1,150,50,50)
            coliderOrNo = True
            for tropa in tropiimage:
                
                if tropa.rect.colliderect(tower.rect):
                    tower.kill()
                    coliderOrNo = False 
                for tower1 in towers:
                    if tower.rect.colliderect(tower1.rect):
                        tower.kill()
                        coliderOrNo = False
            if coliderOrNo:
                towers.append(tower)

    keys_pressed = key.get_pressed()
    if keys_pressed[K_r]:
        print(life)
        if life < 1:
            print('ииии')
            cash = 200
            life = 3
            towers = []
            pulas = []
            bosscount = 20
            vragi1 = []
            finish = True
            finish1 = True
            
            













    if life == 0:
        finish1 = False
        window.blit(gameOver,(350,100))

    #отрисовка    
    window.blit(background,(0,0))
    window.blit(lifeFont,(0,400)) 
    window.blit(cashFont,(0,450))
    for tropa1 in tropiimage:
        tropa1.draw()

    for tower in towers:
        tower.draw()
        vrag = tower.findTarget()
        if tower.pulakd == 0 :
            if vrag != None:
                tower.fire(vrag)
            tower.pulakd = 50
        else:
            tower.pulakd -= 1


    if vragikd == 0:
        if bosscount == 0:
            vrag = SpriteClass('vrag1Boss.png',0,230,55,55,1,500)
            vragi1.append(vrag)
            vragikd =  100
            bosscount = 20
        else:
            bosscount -= 1
            vrag = SpriteClass('vrag1.png',0,230,40,40,1,100)
            vragi1.append(vrag)
            vragikd =  100
    else:
        vragikd -= 1

    for vrag in vragi1:
        vrag.gotopath()
        vrag.draw()
        procent = vrag.life / vrag.life1 * 100
        text = str(procent)+'%'
        if procent >= 65:
            color = (0,255,0)
        elif procent > 30 and procent < 65:
            color = (227,115,23)
        else:
            color = (255,0,0)
        hp = font1.render(text,1,color)
        window.blit(hp,(vrag.x,vrag.y-20))


        

    for pula in pulas:
        pula.draw()
        pula.updat()


        
    if finish1 or finish:
        if finish1 == False:
            finish = False
        display.update()
        clock.tick(FPS)



