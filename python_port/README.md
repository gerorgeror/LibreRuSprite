# LibreSprite Python rewrite (bootstrap)

Это стартовая точка для постепенного переписывания LibreSprite на Python.

## Что уже портировано

- Логика `Zoom` из `src/render/zoom.cpp` перенесена в `libresprite_py.zoom`.
- Базовая логика ordered dithering из `src/render/ordered_dither.h` перенесена в `libresprite_py.ordered_dither` (`BayerMatrix`, `Palette`, `dither_rgb_pixel_to_index`).
- Портированы текстовые утилиты из `src/base`: `replace_string`, `split_string`, `trim_string`.
- Добавлена минимальная модель проекта спрайта (`libresprite_py.sprite`) с JSON-форматом и экспортом в PPM.
- Добавлен CLI `libresprite-py` с командами `zoom`, `new`, `paint`, `invert`, `export-ppm`.
- Добавлены unit-тесты на поведение шкалы, dithering, текстовых утилит, модели спрайта и CLI-flow.

## Запуск

```bash
cd python_port
python -m venv .venv
source .venv/bin/activate
pip install -e .
pytest
```

## Минимально рабочий flow

```bash
libresprite-py new --width 16 --height 16 --output demo.json
libresprite-py paint --project demo.json --x 2 --y 3 --color 255,0,0,255
libresprite-py invert --project demo.json --channels rgb
libresprite-py export-ppm --project demo.json --output demo.ppm
```

## План дальнейшего переписывания

1. Портировать математические/алгоритмические модули без GUI (`filters`, `render`).
2. Добавить слой форматов изображений/спрайтов и совместимость файлов проекта.
3. Переписать UI на Python (PySide6/Qt for Python) и перенести интерактивные инструменты.
4. Вынести платформозависимые части (launcher/process/fs) в кроссплатформенные Python-адаптеры.
