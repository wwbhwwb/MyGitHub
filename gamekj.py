import pygame
import random


class Textfont:
    def __init__(self, text, screenX, screenY, textY, color, fontSIze):
        self.color = color
        self.text = text
        self.screenX = screenX
        self.screenY = screenY
        font = pygame.font.Font(r'/Users/wangwanbing/Desktop/PlaneFight/font/a.ttf', fontSIze)
        self.fontText = font.render(self.text, True, self.color)
        self.width, self.height = self.fontText.get_size()
        self.x = (self.screenX - self.width) / 2
        self.y = textY

    def get_text(self):
        return self.fontText


class Diji(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.dijiImage = pygame.image.load('/Users/wangwanbing/Desktop/PlaneFight/image/diji2.png').convert_alpha()
        # self.dijiImage_t = pygame.transform.rotozoom(self.dijiImage, 0, 0.02)
        self.rect = self.dijiImage.get_rect()
        self.mask = pygame.mask.from_surface(self.dijiImage)
        self.x = 0
        self.y = 100
        self.dijiWidth = 0
        self.dijiHeight = 0
        self.jiasudo = random.randrange(5, 10)
        self.is_pz = False
        
    def get_diji(self):
        # dijiImage = pygame.transform.rotozoom(self.dijiImage, 0, 0.02)
        self.dijiWidth, self.dijiHeight = self.dijiImage.get_size()
        return self.dijiImage

    def move(self):
        if self.is_pz:
            self.x = random.randrange(
                int(self.dijiWidth / 2), int(480 - self.dijiWidth / 2))
            self.y = random.randrange(-100, -20)
            self.is_pz = False

        if self.y <= 720:
            self.y += self.jiasudo
        else:
            self.x = random.randrange(
                int(self.dijiWidth / 2), int(480 - self.dijiWidth / 2))
            self.y = random.randrange(-100, -20)


class Zidan:
    def __init__(self):
        self.x = 200
        self.y = 300
        self.is_fashe = False
        self.Yjiasudo = 0
        self.zidanImage = pygame.image.load(
            r'/Users/wangwanbing/Desktop/PlaneFight/image/zidan.png').convert_alpha()

    def get_zidan(self):
        zidanimage = pygame.transform.rotozoom(self.zidanImage, 0, 0.02)
        return zidanimage

    def fashe(self):
        if self.is_fashe:
            self.Yjiasudo = 10
            self.y -= self.Yjiasudo

    def zidan_huishou(self, feiji_list, feijilsit2):
        if self.y <= -30:
            self.Yjiasudo = 0
            self.is_fashe = False
            feiji_list.append(self)
            feijilsit2.remove(self)
            self.y = 700


class Feiji(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.feijiImage = pygame.image.load(
            r'/Users/wangwanbing/Desktop/PlaneFight/image/feiji3.png').convert_alpha()
        # self.feijiImage_t = pygame.transform.rotozoom(self.feijiImage, 0, 0.05)
        self.mask = pygame.mask.from_surface(self.feijiImage)
        self.rect = self.feijiImage.get_rect()
        self.screenWidth = width
        self.screenHeight = height
        self.x = width / 2
        self.y = height * 0.8
        self.width_size = 0
        self.height_size = 0
        self.is_left = False
        self.is_right = False
        self.Xjiasudo = 0
        self.Yjiasudo = 0
        self.is_up = False
        self.is_down = False
        self.zidanList = []
        self.zidanList_fashe = []
        self.is_send = False
        self.hp_list = []
        self.hp_list_out = []

    def back(self):
        if self.y <= self.screenHeight - self.height_size:
            self.y += 0.5

    def make_feiji(self):
        for i in range(3):
            feijiImage = pygame.transform.rotozoom(self.feijiImage, 0, 0.02)
            self.hp_list.append(feijiImage)
        width, height = self.hp_list[0].get_size()
        return width,height

    def get_feiji(self):
        # feijiImage = pygame.transform.rotozoom(self.feijiImage, 0, 0.05)
        self.width_size, self.height_size = self.feijiImage.get_size()
        return self.feijiImage

    def move(self):
        if self.is_left:
            if self.x >= -10:
                # self.is_right = False
                self.Xjiasudo = 5
                self.x -= self.Xjiasudo

        if self.is_right:
            if self.x <= self.screenWidth - self.width_size + 10:
                # self.is_left = False
                self.Xjiasudo = 5
                self.x += self.Xjiasudo

        if self.is_up:
            if self.y >= 0:
                # self.is_down = False
                self.Yjiasudo = 5
                self.y -= self.Yjiasudo

        if self.is_down:
            if self.y <= self.screenHeight - self.height_size:
                # self.is_up = False
                self.Yjiasudo = 5
                self.y += self.Yjiasudo

    def send(self):
        if len(self.zidanList) >= 1:
            zidan = self.zidanList[0]
            self.zidanList.pop(0)
            zidan.is_fashe = True
            zidan.x = self.x+self.width_size/2
            zidan.y = self.y
            self.zidanList_fashe.append(zidan)


class Game:
    def __init__(self, icon, gamename, width, height):
        self.icon = icon
        self.gamename = gamename
        self.width = width
        self.height = height
        self.dijiList = []
        self.backY = 0
        self.backJiasudo = 1
        self.customs1 = True
        self.is_Instart = False
        self.numbers = {}
        self.jifen = 0
        self.diji_group = ''
        self.times = 0

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.gamename)
        iconImage = pygame.image.load(self.icon)
        pygame.display.set_icon(iconImage)
        back = pygame.image.load(
            r'/Users/wangwanbing/Desktop/PlaneFight/image/backg.jpg')
        back_w, back_h = back.get_size()
        self.backY = -back_h+self.height

        # 渲染背景
        window.blit(back, (0, self.backY))

        # 实例化飞机
        Fj = Feiji(self.width, self.height)
        feijiImage = Fj.get_feiji()
        window.blit(feijiImage, (Fj.x - Fj.width_size / 2, Fj.y))

        # 实例化3个血量飞机
        hp_feijiW,hp_feijiH = Fj.make_feiji()


        # 实例化一组子弹
        for i in range(20):
            zidan = Zidan()
            Fj.zidanList.append(zidan)

        # 生成敌机精灵组
        self.diji_group = pygame.sprite.Group()

        # 实例化5架敌机
        for i in range(5):
            diji = Diji()
            diji.x = random.randrange(
                int(diji.dijiWidth / 2), int(480 - diji.dijiWidth / 2))
            diji.y = random.randrange(-130, -50)
            self.dijiList.append(diji)
            self.diji_group.add(diji)
            window.blit(diji.get_diji(), (diji.x, diji.y))

        # 实例 文字
        fontText_C = Textfont('Flane Fight!', self.width, self.height, 100, (255, 255, 0), fontSIze=60)
        fontText = fontText_C.get_text()

        fontText_jifen_C = Textfont('积分 ', self.width, self.height, 100, (123, 255, 30), fontSIze=30)
        fontText_jifen_C.x = 20
        fontText_jifen_C.y = 20
        fontText_jifen = fontText_jifen_C.get_text()



        fontText_start = Textfont(
            'Game Start', self.width, self.height, self.height/2, (255, 0, 0), fontSIze=30)
        fontText_start_image = fontText_start.get_text()

        fontText_start_new = Textfont(
            'Game Start', self.width, self.height, self.height/2, (255, 123, 0), fontSIze=30)
        fontText_start_image_new = fontText_start_new.get_text()


        # 实例0-9数字
        for i in range(10):
            fontText_nub_C = Textfont(str(i), self.width, self.height, 100, (123, 255, 30), fontSIze=28)
            fontText_nub_C.x = -50
            fontText_nub_C.y = 20
            self.numbers[i] = fontText_nub_C

        


        pygame.display.flip()
        while self.customs1:
            window.blit(back, (fontText_C.x, fontText_C.y))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                if event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = event.pos
                    if fontText_start.x <= mouse_x <= fontText_start.x + fontText_start.width and fontText_start.y <= mouse_y <= fontText_start.y + fontText_start.width:
                        self.is_Instart = True
                    else:
                        self.is_Instart = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if fontText_start.x <= mouse_x <= fontText_start.x + fontText_start.width and fontText_start.y <= mouse_y <= fontText_start.y + fontText_start.width:
                        self.customs1 = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        pass
                    if event.key == pygame.K_DOWN:
                        pass
            if self.is_Instart:
                textImage = fontText_start_image_new
            else:
                textImage = fontText_start_image

            if self.customs1:
                window.blit(fontText, (fontText_C.x, fontText_C.y))
                window.blit(textImage, (fontText_start.x,
                                        fontText_start.y - fontText_start.height / 2))
                window.blit(feijiImage, (Fj.x - Fj.width_size / 2, Fj.y))
                
                clock.tick(60)
                pygame.display.update()

        while True:
            if self.backY >= 0:
                self.backJiasudo = 0
            self.backY += self.backJiasudo
            window.blit(back, (0, self.backY))
            window.blit(feijiImage, (Fj.x - Fj.width_size / 2, Fj.y))
            # for i in pygame.sprite.spritecollide(Fj,self.diji_group,False,pygame.sprite.collide_mask):
            #     print('289:',i)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        Fj.is_right = True
                    if event.key == pygame.K_LEFT:
                        Fj.is_left = True
                    if event.key == pygame.K_UP:
                        Fj.is_up = True
                    if event.key == pygame.K_DOWN:
                        Fj.is_down = True
                    if event.key == pygame.K_SPACE:
                        Fj.send()
                    if event.key == pygame.K_a:
                        # 测试飞机数量减少
                        if len(Fj.hp_list)>0:
                            Fj.hp_list_out.append(Fj.hp_list.pop())
                    if event.key == pygame.K_1:
                        if len(Fj.hp_list_out)>0:
                            Fj.hp_list.append(Fj.hp_list_out.pop())

                    if event.key == pygame.K_b:
                        # 测试积分加

                        self.jifen += 1
                    if event.key == pygame.K_c:
                        # 测试积分减
                        if self.jifen >= 0:
                            self.jifen -= 1

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        Fj.is_right = False
                    if event.key == pygame.K_LEFT:
                        Fj.is_left = False
                    if event.key == pygame.K_UP:
                        Fj.is_up = False
                    if event.key == pygame.K_DOWN:
                        Fj.is_down = False

            Fj.move()
            for i in self.dijiList:
                print(pygame.sprite.spritecollide(Fj,self.diji_group,False,pygame.sprite.collide_mask))
                
                i.move()
                window.blit(i.get_diji(), (i.x, i.y))

            for i in Fj.zidanList_fashe:
                i.zidan_huishou(Fj.zidanList, Fj.zidanList_fashe)
                i.fashe()
                window.blit(i.get_zidan(), (i.x, i.y))

            for i in Fj.hp_list:
                x = self.width-hp_feijiW*(Fj.hp_list.index(i)+1)-10*(Fj.hp_list.index(i)+1)
                window.blit(i,(x,self.height-hp_feijiH-16))

            numbers = 1
            for i in list(str(self.jifen)):
                window.blit(self.numbers[int(i)].get_text(),(10+10*numbers+fontText_jifen_C.width,21))
                numbers += 1
            numbers = 0
            window.blit(fontText_jifen, (fontText_jifen_C.x,fontText_jifen_C.y))
            Fj.back()
            clock.tick(60)
            pygame.display.update()

def main():
    game = Game(
        r"/Users/wangwanbing/Desktop/PlaneFight/image/icon.png", "王某人's Game", 480, 680)
    game.run()

if __name__ == "__main__":
    main()
