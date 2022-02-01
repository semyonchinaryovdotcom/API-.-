import io
import requests
from PIL.Image import open as pil_open
import pygame

pygame.init()


def check_response(response):
    if not response:
        print("Ошибка выполнения запроса:")
        print(response.url)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        exit()


def get_coords(place: str):
    geocode_url = "https://geocode-maps.yandex.ru/1.x/"
    params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": f"{place}",
        "format": "json",
    }
    response = requests.get(geocode_url, params)
    check_response(response)
    return (response.json()
            ["response"]
            ["GeoObjectCollection"]
            ["featureMember"]
            [0]
            ["GeoObject"]
            ["Point"]
            ["pos"]
            .replace(" ", ","))


def get_image(coords: str, zoom, points=()):
    static_map_url = "http://static-maps.yandex.ru/1.x/"
    params = {"ll": coords,
              "z": zoom,
              "pt": "~".join(points),
              "l": "map"}

    response = requests.get(static_map_url, params)
    check_response(response)
    return io.BytesIO(response.content)


city = "Москва"
zoom = 10
points = tuple(map(get_coords,
                   ("Волоколамское ш., 69",
                    "Ленинградский проспект, 36",
                    "улица Лужники, 24с1")))


width, height = 800, 600
screen = pygame.display.set_mode((width, height))
image = pygame.image.load(get_image(get_coords(city), zoom, points))
screen.blit(image, image.get_rect())
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                zoom -= 2
                image = pygame.image.load(get_image(get_coords(city), zoom, points))
                screen.blit(image, image.get_rect())
                pygame.display.flip()
            elif event.key == pygame.K_PAGEDOWN:
                zoom += 2
                image = pygame.image.load(get_image(get_coords(city), zoom, points))
                screen.blit(image, image.get_rect())
                pygame.display.flip()
