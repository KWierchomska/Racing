import pygame
import pygame_classes


def text_format(message, textFont, textSize, textColor):
    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, 0, textColor)
    return newText


cars = ['car.png', 'blue_car.png', 'green_car.png', 'orange_car.png', 'yellow_car.png']

i = 0


# Game Initialization
def customize_car():
    global i
    i = 0
    pygame.init()
    screen_width = pygame.display.Info().current_w
    screen_height = pygame.display.Info().current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

    font = "font.ttf"

    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    orange = (255, 165, 0)

    colors = [black, blue, green, orange, yellow]
    texts = ["BLACK", "BLUE", "GREEN", "ORANGE", "YELLOW"]

    customization = True

    while customization:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if i > 0:
                        i -= 1
                    else:
                        i = len(texts) - 1
                elif event.key == pygame.K_DOWN:
                    if i < len(texts) - 1:
                        i += 1
                    else:
                        i = 0
                elif event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    customization = False
                    break

        screen.fill((0, 0, 0))
        img = pygame.image.load("Images/car_colors.png").convert()
        img = pygame.transform.scale(img, (screen_width, screen_height))
        screen.blit(img, (0, 0))

        title = text_format("Choose color for your car", font, 120, red)
        title_rect = title.get_rect()
        screen.blit(title, (screen_width / 2 - (title_rect[2] / 2), screen_height / 6))  # /9

        for index in range(len(texts)):
            size = 120 if index == i else 80
            text = pygame_classes.show_text(texts[index], font, size, colors[index])
            text_rect = text.get_rect()
            screen.blit(text, (screen_width / 2 - (text_rect[2] / 2), (index + 3) * screen_height / 10))  # /9

        pygame.display.update()
        pygame.display.set_caption("Racing Game - car customization ")


def change_color():
    return cars[i]
