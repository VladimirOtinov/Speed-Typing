import pygame                   #импорт библиотек
from pygame.locals import *
import sys
import time
import random


class Game:                                              #создание класса

    def __init__(self):                                  #определение методов внутри класса(self)

        pygame.init()
        self.w = pygame.display.Info().current_w - 10    # Ширина окна в текущих настройках рабочего стола
        self.h = pygame.display.Info().current_h - 100   # Высота окна в текущих настройках рабочего стола
        self.reset=True
        self.active = False
        self.input_text=''
        self.word = ''
        self.workmsg = ''
        self.time_start = 0
        self.total_time = 0
        self.accuracy = ''
        self.results = ''
        self.wpm = 0
        self.end = False
        self.HEAD_C = (50, 153, 213)   #Цвет заголовка синий          (RGB)
        self.TEXT_C = (240, 240, 240)  #Цвет текста                   (RGB)
        self.RESULT_C = (255, 70, 70)  #Цвет результирующего сообщения(RGB)
        self.repeatcounter = 0
       
        self.open_img = pygame.image.load('type-speed-open.png')                 #Заставка
        self.open_img = pygame.transform.scale(self.open_img, (self.w,self.h))   #трансформация рисунка заставки под заданое разрешение

        self.bg = pygame.image.load('background.jpg')                            #Фон
        self.bg = pygame.transform.scale(self.bg, (self.w,self.h))

        self.screen = pygame.display.set_mode((self.w,self.h))                   # Открытие окна по разрешению экрана
        pygame.display.set_caption(' --==##[ Клавиатурный тренажёр ]##==-- ')    # Заголовок

        
    def draw_text_left(self, screen, msg, x, y ,fsize, color): #Прорисовка текста выровненного по левому краю
        font = pygame.font.Font(None, fsize)         #шрифт
        text = font.render(msg, 1,color)             #прорисовка текста ф-цией в которую передаются параметры
        text_rect = text.get_rect(topleft=(x, y))    #координаты прорисовки текста (левый верхний угол)
        screen.blit(text, text_rect)
        pygame.display.update()

    def draw_text(self, screen, msg, x, y ,fsize, color):      #Прорисовка текста выровненного по центру
        font = pygame.font.Font(None, fsize)
        text = font.render(msg, 1,color)
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)
        pygame.display.update()

    def get_sentence(self):                       #Случайное предложение из файла заданий
        f = open('sentences.txt').read()
        sentences = f.split('\n')
        sentence = random.choice(sentences)
        return sentence

    def show_results(self, screen):
        if(not self.end):
            # Расчет времени
            self.total_time = time.time() - self.time_start

            # Расчет точности
            count = 0
            for i,c in enumerate(self.word):
                try:
                    if self.input_text[i] == c:
                        count += 1
                except:
                    pass
            self.accuracy = count/len(self.word)*100

            # Расчет количества слов в минуту
            self.wpm = len(self.input_text)*60/(5*self.total_time)
            self.end = True
            print(self.total_time)

            self.results = ["Ваши результаты:",
                            "Затраченное время (секунд)__ " + str(round(self.total_time)),
                            "Точность набора текста_______ " + str(round(self.accuracy)) + " %",
                            "Скорость (слов в минуту)______ " + str(round(self.wpm))]

            # Загрузка иконки перезапуска задания
            self.time_img = pygame.image.load('icon.png') # То, что загружаем - рисунок кнопки
            self.time_img = pygame.transform.scale(self.time_img, (300,120)) # То, какого она размера
            screen.blit(self.time_img, (self.w-400,self.h-140)) # Помещаем объект кнопку в область экрана с этими координатами
            self.draw_text(screen, "Кликните здесь", self.w - 255, self.h - 103, 26, (75, 0, 130))
            self.draw_text(screen, "для новой попытки", self.w - 255, self.h - 83, 26, (75, 0, 130))
            
            pygame.display.update()

    def run(self):
        self.reset_game()

        pygame.display.set_icon(pygame.image.load('keyboard.ico'))    #иконка

        self.running=True
        while(self.running):
            clock = pygame.time.Clock()
            self.screen.fill((0,0,0), (60,300,self.w-120,70)) # Черный прямоугольник
            pygame.draw.rect(self.screen,self.HEAD_C, (60,300,self.w-120,70), 1)
            # Обновление текста пользовательского ввода
            self.draw_text(self.screen, self.input_text, self.w/2, 330, 26,(250,250,250))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x,y = pygame.mouse.get_pos()
                    # Расположение окна ввода
                    if(x>60 and x<self.w-60 and y>300 and y<370):
                        self.active = True
                        self.input_text = ''
                        self.time_start = time.time() 
                     # Расположение кнопки сброса
                    if(x>=self.w-380 and x<=self.w-170 and y>=self.h-140 and y<=self.h-50):
                        self.repeatcounter = self.repeatcounter + 1
                        self.reset_game()
                        self.active = False
                        x,y = pygame.mouse.get_pos()
         
                        
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            self.show_results(self.screen)

                            for m in range(4):                         #вывод результатов
                                self.draw_text_left(self.screen, self.results[m], 270, 450+m*35, 30, self.RESULT_C)

                            self.end = True
                            
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            try:
                                self.input_text += event.unicode
                            except:
                                pass
            
            pygame.display.update()

                
        clock.tick(60)

    def reset_game(self):

        #Вывод окна-заставки
        pygame.display.set_icon(pygame.image.load('keyboard.ico'))
        if self.repeatcounter<1:        #Показать окно-заставку Только один раз.
            self.screen.blit(self.open_img, (0,0))
            msg = "     Клавиатурный тренажёр     "
            self.draw_text(self.screen, msg, self.w/2, 30, 25, self.HEAD_C)
            pygame.display.update()
            time.sleep(2)
        
        self.reset=False
        self.end = False

        self.input_text = ''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.wpm = 0

        # Получаем случайное предложение 
        self.word = self.get_sentence()
        if (not self.word): self.reset_game()

        # Загрузка окна
        self.screen.fill((0,0,0))
        self.screen.blit(self.bg,(0,0))
        msg = "Кликните по полю ввода и начните набирать текст из задания."
        self.draw_text(self.screen, msg, self.w/2, 30, 29, self.HEAD_C)
        msg = "После завершения набора текста нажмите < Enter >."
        self.draw_text(self.screen, msg, self.w/2, 50, 30, self.HEAD_C)

        # Отрисовка поля ввода
        pygame.draw.rect(self.screen, self.HEAD_C, (60,300,self.w-120,70), 1) # (текущий экран, цвет, Х,У координаты лев.верх.угла, длина, высота, параметр толщины линии

        # Отрисовка строки предложения-задания
        self.workmsg = self.word #рабочая переменная для раздербанивания предожения надвое
        spacecounter = 0
        for i in range(len(self.workmsg)):
            if self.workmsg[i] == " ":
                spacecounter = spacecounter + 1

        spacecounter2 = 0
        self.simvolindex = 0
        while spacecounter2 <= spacecounter // 2:
            if self.workmsg[self.simvolindex] == " ":
                spacecounter2 = spacecounter2 + 1
            self.simvolindex = self.simvolindex + 1

        messagepart = [self.workmsg[0:self.simvolindex], self.workmsg[self.simvolindex:len(self.workmsg)]]

        for j in range(2):
            msg = messagepart[j]
            self.draw_text(self.screen, msg, self.w/2, 180+j*30, 35, self.TEXT_C)
        
        pygame.display.update()



Game().run()