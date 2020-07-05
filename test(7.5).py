import pgzrun
import random
import time
import tkinter


TITLE = 'Virus Escape!'
WIDTH = 1000
HEIGHT = 800

class man(Actor):

    life = 20000
    dis=0
    mask=0
    def move(self):#判断边界+移动
        global SPEED
        if keyboard[keys.A] and self.left>0:
            self.left-=SPEED
        if keyboard[keys.D] and self.right<WIDTH:
            self.right+=SPEED
        if keyboard[keys.W] and self.top>0:
            self.top-=SPEED
        if keyboard[keys.S] and self.bottom<HEIGHT:
            self.bottom+=SPEED
        #if keyboard[keys.A] or keyboard[keys.D] or keyboard[keys.W] or keyboard[keys.S]:
            #sounds.eep.play()


class V(Actor):
    loop=60
    dir=0#细菌移动方向
    hurt=50#细菌伤害
    tag=0

    def Init(self,i):#细菌初始化
        self.dir=random.randint(1,4)
        x=random.randint(1,8)
        y=random.randint(1,6)
        self.tag=i
        self.hurt=20
        self.level=1
        self.pos=x*100,y*100

    def draw_v(self):
        self.draw()

    def move_v(self):
        if(self.loop==0):
            self.dir=random.randint(1,4)
            self.loop=20
            self.move_v()
        else:
            self.loop-=1
            if(self.dir==1):
                self.left+=step/10
                if(self.left+w>WIDTH):
                    self.left=WIDTH-w
            elif(self.dir==2):
                self.left-=step/10
                if(self.left<0):
                    self.left=0
            elif(self.dir==3):
                self.top+=step/10
                if(self.top+h>HEIGHT):
                    self.top=HEIGHT-h
            else:
                self.top-=step/10
                if(self.top<0):
                   self.top=0

    '''
    def reset(self):
        viruses = []
    '''

class Game(): #游戏页面跳转：欢迎--游戏中--结束

    def __init__(self):
        self.gameOn = False
        self.gameMessage = "Welcome to Virus Escape!\nPRESS SPACE TO START GAME"
        sounds.blip.play()
    def checkGameOver(self):
        if doctor.life <= 0:
            self.gameOn = False
            self.gameMessage = "Game Over,You Lose!\nPRESS SPACE TO RESTART"

        if doctor.colliderect(vaccine):
            self.gameOn = False
            self.gameMessage = "Yon Win!\nPRESS SPACE TO RESTART"

game = Game()

def reset():
    doctor.life=20000
    doctor.pos = 50, 100
    star=time.time()
    viruses.clear()
    global num
    num=6
    for i in range(num):
        vi=V("virus_1")
        vi.Init(i)
        viruses.append(vi)
    vaccine = Actor('zhenguan')
    vaccine.center = 950,700

def draw():

    if game.gameOn == False:
        screen.clear()
        screen.fill((139, 0, 18))
        screen.draw.text(game.gameMessage,color="white",center=(HEIGHT/2,WIDTH/2))

    else:
        screen.clear()
        screen.fill((139, 0, 18))
        global star
        elap=time.time()-star# 获取时间差
        #print(elap)
        minutes = int(elap/60)
        seconds = int(elap-minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds) *1000)
        #seconds = 30 - seconds
        screen.draw.text("Time Used:%d mins %d secs"%(minutes,seconds),(10,30),color="white")
        #screen.blit("backimg", (0, 0))
        doctor.draw()
        vaccine.draw()
        for v in viruses:
            v.draw_v()
        for m in Allmask:
            m.draw()
        for m in Alldis:
            m.draw()
        screen.draw.text("HP:%d" % doctor.life,(10,10),color="white")

def update():
    global Allmask,Alldis
    if game.gameOn:
        doctor.move()
        global index,num,maskues,maskstar,UsingMask
        if doctor.mask>0 and keyboard[keys.J]:
            doctor.mask-=1
            UsingMask=1
            maskstar=time.time()
        maskuse=time.time()
        if maskuse-maskstar>3 and UsingMask:
            UsingMask=0
        if keyboard[keys.K] and doctor.dis>=1:
            doctor.dis-=1
            for v in viruses:
                print(doctor.distance_to(v))
                if doctor.distance_to(v)<=400:
                    viruses.remove(v)
                
        for v in viruses:
            v.move_v()
            if doctor.colliderect(v)and UsingMask==0:
                doctor.life -= v.hurt
                sounds.exp.play()
                viruses.remove(v)
        for v in viruses:#病毒碰撞和合并
            for v2 in viruses:
                if(v.tag!=v2.tag):
                    if(v.colliderect(v2) and v.level==v2.level):
                        v.level+=1
                        v.hurt*=1.2
                        viruses.remove(v2)
                        num-=1
                        if(v.level==2):
                            v.image="virus_2"
                        elif(v.level==3):
                            v.image="virus_3"
                        elif(v.level==4):
                            v.image="virus_4"
        for m in Allmask:
            if doctor.colliderect(m):
                doctor.mask+=1
                Allmask.remove(m)
        for m in Alldis:
            if doctor.colliderect(m):
                doctor.dis+=1
                Alldis.remove(m)
    if keyboard.space and game.gameOn == False:
        game.gameOn = True
        reset()


    luck=random.randint(0,2000)
    if luck%200==0:#追加一个病毒
        vi=V("virus_1")
        vi.Init(index)
        index+=1
        num+=1
        viruses.append(vi)
    if luck==0 and len(Allmask)<3:
        m=Actor("mask")
        x=random.randint(1,8)
        y=random.randint(1,6)
        m.pos=x*100,y*100
        Allmask.append(m)
    if luck==15 and len(Alldis)<3:
        m=Actor("dis")
        x=random.randint(1,8)
        y=random.randint(1,6)
        m.pos=x*100,y*100
        Alldis.append(m)
    game.checkGameOver()
Allmask=[]
Alldis=[]
num=12
index=12
step=50
SPEED=10
w=66
h=92

doctor = man('yisheng')
doctor.pos = 50, 100
viruses = []
maskues=0
maskstar=0
UsingMask=0
for i in range(num):
    vi=V("virus_1")
    vi.Init(i)
    viruses.append(vi)

vaccine = Actor('zhenguan')
vaccine.center = 950,700

star=time.time()
print(star)


pgzrun.go()