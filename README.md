# Как узнать, где прорвёт, до звонка жителя

Продуктовый кейс: цифровой двойник жилого фонда Москвы — концепция платформы,
которая прогнозирует отказы инженерных систем жилых домов. Проектировал по
запросу Мосстратегии (Департамент экономической политики и развития города
Москвы), апрель–май 2026 года.

**Страница кейса:** [massimo-pazzi.github.io/housing-digital-twin-case](https://massimo-pazzi.github.io/housing-digital-twin-case/)
**Кликабельный прототип:** [massimo-pazzi.github.io/housing-digital-twin-case/demo](https://massimo-pazzi.github.io/housing-digital-twin-case/demo/) — все данные вымышлены.

## Структура

```
index.html             страница кейса (собирается скриптом)
report/case.md         текст кейса
assets/img/            скриншоты прототипа и фото автора
demo/                  прототип: страница, библиотеки, границы районов
research/              сверка фактов исходных материалов с первоисточниками
scripts/build_page.py  сборка страницы из report/case.md
scripts/screenshots.mjs  скриншоты прототипа (Chrome, Node 22+)
```

## Как пересобрать

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/build_page.py
```

Автор — Максим Поципух.
