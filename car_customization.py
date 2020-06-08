import pygame
import pygame_classes

cars = ['car.png', 'blue_car.png', 'green_car.png', 'orange_car.png', 'yellow_car.png']

chosen_color = 0


def customize_car():
    global chosen_color
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
                    if chosen_color > 0:
                        chosen_color -= 1
                    else:
                        chosen_color = len(texts) - 1
                elif event.key == pygame.K_DOWN:
                    if chosen_color < len(texts) - 1:
                        chosen_color += 1
                    else:
                        chosen_color = 0
                elif event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    customization = False
                    break

        screen.fill((0, 0, 0))
        img = pygame.image.load("Images/car_colors.png").convert()
        img = pygame.transform.scale(img, (screen_width, screen_height))
        screen.blit(img, (0, 0))

        title = pygame_classes.text_format("Choose color for your car", font, 120, red)
        title_rect = title.get_rect()
        screen.blit(title, (screen_width / 2 - (title_rect[2] / 2), screen_height / 6))

        for index in range(len(texts)):
            size = 120 if index == chosen_color else 80
            text = pygame_classes.show_text(texts[index], font, size, colors[index])
            text_rect = text.get_rect()
            screen.blit(text, (screen_width / 2 - (text_rect[2] / 2), (index + 3) * screen_height / 10))

        pygame.display.update()
        pygame.display.set_caption("Racing Game - car customization ")


def change_color():
    return cars[chosen_color]
