# LibreSprite Python rewrite (bootstrap)

Это стартовая точка для постепенного переписывания LibreSprite на Python.

## Что уже портировано

- Логика `Zoom` из `src/render/zoom.cpp` перенесена в `libresprite_py.zoom`.
- Базовая логика ordered dithering из `src/render/ordered_dither.h` перенесена в `libresprite_py.ordered_dither` (`BayerMatrix`, `Palette`, `dither_rgb_pixel_to_index`).
- Портированы текстовые утилиты из `src/base`: `replace_string`, `split_string`, `trim_string`.
- Добавлен CLI `libresprite-py` для проверки поведения масштаба.
- Добавлены unit-тесты на поведение шкалы, матриц dithering, текстовых утилит и граничные случаи.

## Запуск

```bash
cd python_port
python -m venv .venv
source .venv/bin/activate
pip install -e .
pytest
libresprite-py --scale 0.75 --direction in
```

## План дальнейшего переписывания

1. Портировать математические/алгоритмические модули без GUI (`filters`, `render`).
2. Добавить слой форматов изображений/спрайтов и совместимость файлов проекта.
3. Переписать UI на Python (PySide6/Qt for Python) и перенести интерактивные инструменты.
4. Вынести платформозависимые части (launcher/process/fs) в кроссплатформенные Python-адаптеры.
