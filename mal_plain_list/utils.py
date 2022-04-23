import json
from pathlib import Path


def show_diff(old: list, new: list) -> None:
  diff_len = len(old) - len(new)
  if diff_len == 0:
    print('no new additions/removals')
  else:
    print(f'{abs(diff_len)} {"removals" if diff_len > 0 else "new additions/updates"}')


def get_root_path() -> Path:
  """
  Return project root path.
  :return: PurePath subclass
  """
  return Path(__file__).parent.parent


def get_output_path() -> Path:
  output_path = get_root_path().joinpath('output')
  output_path.mkdir(parents=True, exist_ok=True)
  return output_path


def load_json(file_name: str) -> list:
  try:
    with get_output_path().joinpath(file_name).open(encoding='utf-8') as json_file:
      data = json.load(json_file)
    return data
  except FileNotFoundError:
    return []
  except Exception as e:
    print(f'Something went wrong loading json file: {e}')
    return []


def write_json(file_name: str, data: any) -> None:
  with get_output_path().joinpath(file_name).open('w', encoding='utf-8') as file:
    json.dump(data, file, indent=2)


def write_file(file_name: str, data: any) -> None:
  with get_output_path().joinpath(file_name).open('w', encoding='utf-8') as file:
    file.writelines(data)
