from typing import Callable

import requests

from mal_plain_list.utils import show_diff, load_json, write_file, write_json


def anime_format(anime: dict) -> str:
  return f'{anime["anime_title"]} - Ep {anime["num_watched_episodes"]}/{anime["anime_num_episodes"]}'


def manga_format(manga: dict) -> str:
  return f'{manga["manga_title"]} - Ch {manga["num_read_chapters"]}/{manga["manga_num_chapters"]} ' \
         f'- Vol {manga["num_read_volumes"]}/{manga["manga_num_volumes"]}'


def build_list(function: Callable[[dict], str], data: list) -> list:
  return ['\n'.join(function(x) for x in data)]


class MAL:
  def __init__(self, username: str) -> None:
    self.username = username
    self.animes = []
    self.mangas = []

  def fetch(self, list_name: str) -> list:
    print(f'Fetching {list_name}...')
    data = []
    offset = 0
    api_url = f'https://myanimelist.net/{list_name}/{self.username}/load.json'
    while True:
      print(f'Fetching offset: {offset}...', end='\r')
      params = {
        'offset': offset,
        'status': 7
      }
      response = requests.get(api_url, params=params)
      response_data = response.json()
      if len(response_data) == 0:
        break
      data.extend(response_data)
      offset += 300
    return data

  def fetch_animes(self) -> None:
    self.animes = self.fetch('animelist')
    print(f'\nTotal animes: {len(self.animes)}')

  def fetch_mangas(self) -> None:
    self.mangas = self.fetch('mangalist')
    print(f'\nTotal mangas: {len(self.mangas)}')

  def print_animes(self) -> None:
    print(*build_list(anime_format, self.animes), sep='\n')

  def print_mangas(self) -> None:
    print(*build_list(manga_format, self.mangas), sep='\n')

  def save(self) -> None:
    write_file('anime_list.txt', build_list(anime_format, self.animes))
    write_file('manga_list.txt', build_list(manga_format, self.mangas))
    print('Formatted list saved.\n')

  def raw_save(self) -> None:
    write_json('raw_anime_list.json', self.animes)
    write_json('raw_manga_list.json', self.mangas)
    print('Raw list saved.\n')


if __name__ == '__main__':
  username = input('Enter your MAL username\n> ')
  user = MAL(username)

  print(f'- User: {user.username}\n')
  # print('- Anime List -')
  user.fetch_animes()
  show_diff(load_json('raw_anime_list.json'), user.animes)
  # user.print_animes()

  print('\n- Manga List -')
  user.fetch_mangas()
  show_diff(load_json('raw_manga_list.json'), user.mangas)
  # user.print_mangas()

  print('\n')
  user.save()
  user.raw_save()
