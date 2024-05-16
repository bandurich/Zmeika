import pygame
import random
import os

pygame.init()

# Цвета
lineee = (255, 255, 255)
color_point = (255, 255, 102)
color_zmeika = (0, 137, 255)
color_end = (213, 50, 80)
color_display = (3, 33, 3)
color_display1=(3,33,3)
color_display2=(6,66,6)

# Размер дисплея
display_width = 1200
display_height = 600

display = pygame.display.set_mode((display_width, display_height + 60))  # Увеличение высоты для счета и рекорда
pygame.display.set_caption("Родимая змейка")  # Название окна

clock = pygame.time.Clock()  # Функция для управления скоростью игры

zmeika_block = 30  # Размер змейки
zmeika_speed = 15  # Скорость змейки

text_end = pygame.font.SysFont("TkTooltipFont", 42)  # Размер шрифта после поражения
text_point = pygame.font.SysFont("comicsansms", 42)  # Размер шрифта счета очков и рекорда 

apple3_img = pygame.image.load("apple10.png")  # Фото яблока
apple3_img = pygame.transform.scale(apple3_img,(52,52)) #изменение размера пнгшки яблока до 52x52


record_file = "record.txt"# Путь к файлу с рекордом

def read_record():
    if os.path.exists(record_file):
        with open(record_file, "r") as file:#функция чтения файла с рекордом
            record = int(file.read())#перевод числа в полное /в цифру
    else:
        record = 0
    return record

def write_record(record):
    with open(record_file, "w") as file:#функция для записи рекорда 
        file.write(str(record))#произведения записи  

def our_point_or_record(point, record):  # Функция для отображения очков и рекорда
    score_text = text_point.render("Point: " + str(point) + "   Record: " + str(record), True, color_point)#сохранение переменых очков и рекордов
    display.blit(score_text, [10, display_height])  # Отображение счета и рекорда
    pygame.draw.line(display, lineee, (0, display_height), (display_width, display_height), 5)  # Разделительная линия

def our_zmeika(snake_block, snake_list):  # Функция для отображения змейки
    for x in snake_list:
        pygame.draw.rect(display, color_zmeika, [x[0], x[1], snake_block, snake_block])

def draw_grid():#функция для деления на клеточки игровое
    for row in range(0, display_height, zmeika_block):
        for column in range(0, display_width, zmeika_block):
            if (row // zmeika_block + column // zmeika_block) % 2 == 0:
                pygame.draw.rect(display,color_display1, [column, row, zmeika_block, zmeika_block])
            else:
                pygame.draw.rect(display, color_display2, [column, row, zmeika_block, zmeika_block])

def message(msg, color):  # Функция для надписи после поражения
    mesg = text_end.render(msg, True, color)
    display.blit(mesg, [display_width / 6, display_height / 3])  # Размещение надписи после поражения

def gameOsnova():  # Основная функция по игре
    game_over = False  # Переменная чтобы окно работало
    game_close = False  # Переменная чтобы окно работало

    x1 = display_width / 2  # Координата x
    y = display_height / 2  # Координата y

    x1_new = 0  # Координата x
    y_new = 0  # Координата y

    zmeika_List = []
    Length_of_zmeika = 1

    apple_x = round(random.randrange(0, display_width - zmeika_block) / zmeika_block) * zmeika_block  # Рандомное появления яблока x
    apple_y = round(random.randrange(0, display_height - zmeika_block) / zmeika_block) * zmeika_block  # Рандомное появления яблока y

    record = read_record()

    while not game_over:

        while game_close == True:
            display.fill(color_display)  # Красим окно в цвет
            message("Игра окончена!!! SPACE-Рестарт или ESC-Покинуть игру", color_end)  # Текст после поражения

            pygame.display.update()  # Обновление кадров

            for event in pygame.event.get():  # Клавиши после поражения
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_SPACE:
                        gameOsnova()
                if event.type == pygame.QUIT:
                    game_over = True
        for event in pygame.event.get():  # Клавиши управления
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_new != zmeika_block:
                    x1_new = -zmeika_block
                    y_new = 0
                elif event.key == pygame.K_RIGHT and x1_new != -zmeika_block:
                    x1_new = zmeika_block
                    y_new = 0
                elif event.key == pygame.K_UP and y_new != zmeika_block:
                    y_new = -zmeika_block
                    x1_new = 0
                elif event.key == pygame.K_DOWN and y_new != -zmeika_block:
                    y_new = zmeika_block
                    x1_new = 0

        if x1 >= display_width or x1 < 0 or y >= display_height or y < 0:  # Цикл чтобы если змейка пересекает края окна тот проигрыш
            game_close = True#выполнять верхний цикл если проиграл 
        x1 += x1_new
        y += y_new
        display.fill(color_display)#красит дисплей в цвет 
        draw_grid()  # Рисуем клеточную сетку


        display.blit(apple3_img, (apple_x-6, apple_y-6))  # Добавления яблока на экран
        zmeika_Head = []#пустой список для хранения координат головы змейки.
        zmeika_Head.append(x1)#добавления к списку кордмнату по оси х
        zmeika_Head.append(y)#добавления к списку кордмнату по оси у
        zmeika_List.append(zmeika_Head)
        if len(zmeika_List) > Length_of_zmeika:#ПРОВЕРКА старой длинный с новой 
            del zmeika_List[0]

        for x in zmeika_List[:-1]:
            if x == zmeika_Head:
                game_close = True

        our_zmeika(zmeika_block, zmeika_List)#вызывают функцию для отображения змейки 
        our_point_or_record(Length_of_zmeika - 1, record -1)#вызывает фыункцию отображения счет и рекорд 

        pygame.display.update()

        if x1 == apple_x and y == apple_y:#цикл по поеданию яблок 
            apple_x = round(random.randrange(0, display_width - zmeika_block) / zmeika_block) * zmeika_block
            apple_y = round(random.randrange(0, display_height - zmeika_block) / zmeika_block) * zmeika_block
            Length_of_zmeika += 1
            if Length_of_zmeika > record:
                record = Length_of_zmeika
                write_record(record)

        clock.tick(zmeika_speed)  # Функция для скорость змейки

    pygame.quit()  # Закрытие экрана
    quit()

gameOsnova()  # def

