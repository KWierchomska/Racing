import pygame
def text_format(message, textFont, textSize, textColor):
    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, 0, textColor)
    return newText


# selected='black'

colors = ['car.png', 'blue_car.png', 'green_car.png', 'orange_car.png', 'yellow_car.png']
i = 0


# Game Initialization
def customize_car():
    pygame.init()
    screen_width = pygame.display.Info().current_w
    screen_height = pygame.display.Info().current_h
    screen = pygame.display.set_mode((screen_width, screen_height))
    font = "font.ttf"

    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    orange = (255, 165, 0)

    customization = True

    while customization:
        for event in pygame.event.get():
            global i
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if i > 0:
                        i -= 1
                    else:
                        i = len(colors) - 1
                elif event.key == pygame.K_DOWN:
                    if i < len(colors) - 1:
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
        title = text_format("Choose color for your car", font, 100, red)
        if colors[i] == "car.png":
            text_black = text_format("BLACK", font, 120, black)
        else:
            text_black = text_format("BLACK", font, 80, black)
        if colors[i] == "blue_car.png":
            text_blue = text_format("BLUE", font, 120, blue)
        else:
            text_blue = text_format("BLUE", font, 80, blue)
        if colors[i] == "green_car.png":
            text_green = text_format("GREEN", font, 120, green)
        else:
            text_green = text_format("GREEN", font, 80, green)
        if colors[i] == "orange_car.png":
            text_orange = text_format("ORANGE", font, 120, orange)
        else:
            text_orange = text_format("ORANGE", font, 80, orange)
        if colors[i] == "yellow_car.png":
            text_yellow = text_format("YELLOW", font, 120, yellow)
        else:
            text_yellow = text_format("YELLOW", font, 80, yellow)

        title_rect = title.get_rect()
        black_rect = text_black.get_rect()
        blue_rect = text_blue.get_rect()
        green_rect = text_green.get_rect()
        orange_rect = text_orange.get_rect()
        yellow_rect = text_yellow.get_rect()

        # Main Menu Text
        screen.blit(title, (screen_width / 2 - (title_rect[2] / 2), 200)) #20
        screen.blit(text_black, (screen_width / 2 - (black_rect[2] / 2), 300)) #150
        screen.blit(text_blue, (screen_width / 2 - (blue_rect[2] / 2), 400)) #280
        screen.blit(text_green, (screen_width / 2 - (green_rect[2] / 2), 500)) #410
        screen.blit(text_orange, (screen_width / 2 - (orange_rect[2] / 2), 600)) #540
        screen.blit(text_yellow, (screen_width / 2 - (yellow_rect[2] / 2), 700)) #670

        pygame.display.update()
        pygame.display.set_caption("Racing Game - car customization ")


def change_color():
    return colors[i]