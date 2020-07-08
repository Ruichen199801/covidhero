import pgzrun
import random
import time
# import tkinter
from pgzero import music

TITLE = "Covid Hero"
WIDTH = 1200
HEIGHT = 675


class man(Actor):
    life = 200  # 生命值
    dis = 0  # 消毒水数量
    mask = 0  # 口罩数量
    target_pt = 200
    temp_pt = 0

    def move(self):  # 判断移动
        global SPEED
        if keyboard[keys.A] and self.left > 0:
            self.left -= SPEED
        if keyboard[keys.D] and self.right < WIDTH:
            self.right += SPEED
        if keyboard[keys.W] and self.top > 0:
            self.top -= SPEED
        if keyboard[keys.S] and self.bottom < HEIGHT:
            self.bottom += SPEED


class V(Actor):

    def Init(self, i):  # 细菌初始化
        global gamelevel
        self.dir = random.randint(1, 4)
        x = random.randint(1, 8)
        y = random.randint(1, 6)
        self.tag = i
        self.hurt = 15 + 5 * gamelevel
        self.level = 1
        self.pos = x * 100, y * 100
        self.loop = 60

    def draw_v(self):
        self.draw()

    def move_v(self):  # 细菌移动
        global gamelevel
        if self.loop == 0:
            self.dir = random.randint(1, 4)
            self.loop = 20
            self.move_v()
        else:  # 移动速度随着游戏关卡的增加而增加
            self.loop -= 1
            if self.dir == 1:
                self.left += step / 10 + gamelevel
                if self.left + w > WIDTH:
                    self.left = WIDTH - w
            elif self.dir == 2:
                self.left -= step / 10 + gamelevel
                if self.left < 0:
                    self.left = 0
            elif self.dir == 3:
                self.top += step / 10 + gamelevel
                if self.top + h > HEIGHT:
                    self.top = HEIGHT - h
            else:
                self.top -= step / 10 + gamelevel
                if self.top < 0:
                    self.top = 0


class Game:  # 游戏页面跳转：欢迎--游戏中--结束
    def __init__(self):
        self.gameOn = 1
        self.gameMessage = "Welcome to Covid Hero!\nPRESS SPACE TO START GAME"
        self.play_sound = True

    def checkGameOver(self):
        if doctor.life <= 0:
            self.gameOn = 2
            self.gameMessage = "Game Over, You Lose!\nPRESS SPACE TO RESTART"  # 失败

        if doctor.target_pt <= doctor.temp_pt:
            vaccine = Actor("zhenguan")
            vaccine.center = 1000, 600
            if doctor.colliderect(vaccine):
                if gamelevel < 10:
                    self.gameOn = 3  # 进入下一关卡
                    self.gameMessage = "You Win!\nPRESS SPACE TO THE NEXT LEVEL"

                else:
                    self.gameOn = 4  # 游戏结束,胜利
                if len(Allgrade) <= gamelevel:
                    global star
                    elap = time.time() - star  # 获取时间差
                    minutes = int(elap / 60)
                    seconds = int(elap - minutes * 60.0)
                    Allgrade[gamelevel] = minutes, seconds  #
                    print(Allgrade)


game = Game()


def reset():
    global gamelevel
    # 重开游戏之后对医生初始化
    doctor.life = 200+ 20 * gamelevel
    doctor.pos = 50, 100
    doctor.target_pt = 200 + 100 * gamelevel
    doctor.temp_pt = 0
    star = time.time()
    gamelevel += 1

    global num
    num = 6
    viruses.clear()
    for i in range(num):
        vi = V("virus_1")
        vi.Init(i)
        viruses.append(vi)

    Allgate.clear()
    gate_location.clear()
    Vaccinelist.clear()


def draw():
    if game.gameOn == 1:  # 游戏开始
        screen.clear()
        screen.blit('startpage', (0, 0))
    elif game.gameOn == 1.1:  # 规则
        screen.clear()
        screen.blit('rules-2', (0, 0))
    elif game.gameOn == 2:
        screen.clear()
        screen.blit('deadpage', (0, 0))
        screen.draw.text(
            game.gameMessage, color="white", center=(HEIGHT * 6 / 7, WIDTH / 2)
        )
    elif game.gameOn == 3:
        screen.clear()
        screen.blit('win_stage', (0, 0))
        screen.draw.text(
            game.gameMessage, color="black", center=(HEIGHT * 3 / 4, WIDTH / 2)
        )
    elif game.gameOn == 4:
        screen.clear()
        screen.blit('endpage', (0, 0))
        x, y = 300, 250
        for i in range(1, 6):
            minute, second = Allgrade[i]
            pre_m, pre_s = Allgrade[i - 1]
            tmp = (minute * 60 + second) - (pre_m * 60 + pre_s)
            minute = tmp // 60
            second = tmp % 60
            screen.draw.text("Level %d: %03d:%02d" % (i, minute, second), color="white", topleft=(x, y))
            y += 40
        x, y = 500, 250
        for i in range(6, 11):
            minute, second = Allgrade[i]
            pre_m, pre_s = Allgrade[i - 1]
            tmp = (minute * 60 + second) - (pre_m * 60 + pre_s)
            minute = tmp // 60
            second = tmp % 60
            screen.draw.text("Level %d: %03d:%02d" % (i, minute, second), color="white", topleft=(x, y))
            y += 40
    else:
        screen.clear()
        screen.fill((139, 0, 18))
        global star
        elap = time.time() - star  # 获取时间差
        minutes = int(elap / 60)
        seconds = int(elap - minutes * 60.0)
        hseconds = int((elap - minutes * 60.0 - seconds) * 1000)
        screen.draw.text(
            "Time Used: %d mins %d secs" % (minutes, seconds), (10, 60), color="white"
        )

        # 画出界面上的对象
        doctor.draw()
        for v in viruses:
            v.draw_v()
        for m in Allmask:
            m.draw()
        for m in Alldis:
            m.draw()
        for m in Allgate:
            m.draw()
        for m in Allcell:
            m.draw()

        for vaccine in Vaccinelist:
            vaccine.draw()
            screen.draw.text("VACCINE IS READY!", (500, 60), color="white")

        # 医生的属性
        global gamelevel
        if gamelevel == 0:
            screen.draw.text("LEVEL %d (Tutorial Level)\n" % gamelevel, (10, 10), color="white")
        else:
            screen.draw.text("LEVEL %d / 10\n" % gamelevel, (10, 10), color="white")
        screen.draw.text("HP: %d\n" % doctor.life, (10, 40), color="white")
        screen.draw.text("Mask (J): %d\n" % doctor.mask, (10, 80), color="white")
        screen.draw.text("Spray (K): %d\n" % doctor.dis, (10, 100), color="white")
        screen.draw.text("Portal (L)", (10, 120), color="white")

        if doctor.temp_pt >= doctor.target_pt:
            vaccine_progress = 100
        else:
            vaccine_progress = 100 * round(doctor.temp_pt / doctor.target_pt, 2)
        screen.draw.text("Vaccine: %d%%\n" % vaccine_progress, (10, 140), color="white")

        global maskstar, UsingMask
        if UsingMask:
            temp_time = time.time()
            time_left = 3 - temp_time + maskstar
            screen.draw.text(
                "Mask Time Left: %d secs" % time_left, (500, 30), color="white"
            )


def update():
    global Allmask, Alldis, gamelevel

    if game.gameOn == 1.5:
        doctor.move()
        global index, num, maskues, maskstar, UsingMask, disstar, UsingDis, disuse
        # 使用口罩
        if doctor.mask > 0 and keyboard[keys.J] and UsingMask == 0:
            sounds.wear_mask.play()
            doctor.mask -= 1
            UsingMask = 1
            maskstar = time.time()
        maskuse = time.time()
        masktime = int(maskuse - maskstar)
        if masktime > 3 and UsingMask:
            UsingMask = 0

        # 使用消毒水，每次使用CD=0.5s
        if keyboard[keys.K] and doctor.dis >= 1 and UsingDis == 0:
            sounds.spray.play()
            sounds.spray.play()
            doctor.dis -= 1
            disstar = time.time()

            for v in viruses:
                print(doctor.distance_to(v))
                if doctor.distance_to(v) <= 400:
                    viruses.remove(v)
        disuse = time.time()
        distime = disuse - disstar
        if UsingDis == 1 and distime > 0.5:
            UsingDis = 0

        # 毒和医生的碰撞
        for v in viruses:
            v.move_v()
            if doctor.colliderect(v) and UsingMask == 0:
                doctor.life -= v.hurt
                sounds.hurt.play()
                viruses.remove(v)

        # 病毒碰撞和合并
        for v in viruses:
            for v2 in viruses:
                if v.tag != v2.tag:
                    if v.colliderect(v2) and v.level == v2.level:
                        sounds.virus_level_up.play()
                        v.level += 1
                        v.hurt *= 1.2
                        viruses.remove(v2)
                        num -= 1
                        if v.level == 2:
                            v.image = "virus_2"
                        elif v.level == 3:
                            v.image = "virus_3"
                        elif v.level == 4:
                            v.image = "virus_4"

        # 口罩的拾取
        for m in Allmask:
            if doctor.colliderect(m):
                sounds.get.play()
                doctor.mask += 1
                Allmask.remove(m)

        # 消毒水的拾取
        for m in Alldis:
            if doctor.colliderect(m):
                sounds.get.play()
                doctor.dis += 1
                Alldis.remove(m)

        # 传送门的使用
        if Allgate:
            if doctor.colliderect(Allgate[0]) and keyboard[keys.L]:
                sounds.portal.play()
                doctor.pos = gate_location[2] + 100, gate_location[3]
            if doctor.colliderect(Allgate[1]) and keyboard[keys.L]:
                sounds.portal.play()
                doctor.pos = gate_location[0] - 100, gate_location[1]

        # 积分道具的拾取
        if Allcell:
            if doctor.colliderect(Allcell[0]):
                sounds.nice.play()
                doctor.temp_pt += 100
                Allcell.clear()
        luck = random.randint(0, 2000)

        # 生成一个病毒
        if luck % (220 - 20 * gamelevel) == 0:
            sounds.item_generate.play()
            vi = V("virus_1")
            vi.Init(index)
            index += 1
            num += 1
            viruses.append(vi)

        # 生成口罩
        if luck == 0 and len(Allmask) < 3:
            sounds.item_generate.play()
            m = Actor("mask")
            x = random.randint(1, 8)
            y = random.randint(1, 6)
            m.pos = x * 100, y * 100
            Allmask.append(m)

        # 生成消毒水
        if luck == 5 and len(Alldis) < 3:
            sounds.item_generate.play()
            m = Actor("dis")
            x = random.randint(1, 8)
            y = random.randint(1, 6)
            m.pos = x * 100, y * 100
            Alldis.append(m)

        # 生成传送门
        if luck % 100 == 0 and len(Allgate) < 2:
            sounds.portal_appear.play()
            m1 = Actor("gate")
            x = random.randint(2, 4)
            y = random.randint(1, 6)
            m1.pos = x * 100, y * 100
            Allgate.append(m1)
            gate_location.append(x * 100)
            gate_location.append(y * 100)

            m2 = Actor("gate")
            x = random.randint(6, 8)
            y = random.randint(1, 6)
            m2.pos = x * 100, y * 100
            Allgate.append(m2)
            gate_location.append(x * 100)
            gate_location.append(y * 100)

        # 生成积分道具
        if luck % 400 == 0 and len(Allcell) == 0:
            sounds.item_generate.play()
            if luck == 400:
                m = Actor("macrophage")
            elif luck == 800:
                m = Actor("natural_killer")
            elif luck == 1200:
                m = Actor("cellt")
            elif luck == 1600:
                m = Actor("cellb")
            elif luck == 2000:
                m = Actor("dendritic_cell")
            x = random.randint(1, 8)
            y = random.randint(1, 6)
            m.pos = x * 100, y * 100
            Allcell.append(m)

        # 在积分道具数目足够时，生成疫苗
        if doctor.target_pt <= doctor.temp_pt:
            vaccine = Actor("zhenguan")
            vaccine.center = 1000, 600
            Vaccinelist.append(vaccine)

    # 开始游戏
    global rule_s
    if keyboard.space and game.gameOn == 1:
        game.gameOn = 1.1  # 游戏规则说明
        rule_s=time.time()
    if keyboard.space and game.gameOn == 1.1:
        if time.time()-rule_s>0.5:
            game.gameOn = 1.5
    if keyboard.space and game.gameOn == 3:
        game.gameOn = 1.5
        reset()
    if keyboard.space and game.gameOn == 2:
        game.gameOn = 1
        gamelevel = 0
        reset()

    # 音效播放
    if game.play_sound:
        if game.gameOn == 2:
            sounds.game_lose.play()
            game.play_sound = False
        if game.gameOn == 3:
            sounds.game_win.play()
            game.play_sound = False
        if game.gameOn == 4:
            sounds.game_victory.play()
            game.play_sound = False

    if game.gameOn == 1.5 and game.play_sound == False:
        game.play_sound = True


    game.checkGameOver()

music.play("bgm")
music.unpause()

Allmask = []  # 界面上存在的口罩列表
Alldis = []  # 界面上存在的消毒水列表
Allgate = []  # 传送门列表
gate_location = []
Allcell = []  # 积分道具列表
Vaccinelist = []
Allgrade = {}

num = 6
index = 6
step = 50
SPEED = 10
w = 66
h = 92
gamelevel = 0

doctor = man("yisheng")
doctor.pos = 50, 100
viruses = []
maskuse = 0
maskstar = 0
disuse = 0
disstar = 0
UsingMask = 0
UsingDis = 0
for i in range(num):
    vi = V("virus_1")
    vi.Init(i)
    viruses.append(vi)

star = time.time()
print(star)


pgzrun.go()