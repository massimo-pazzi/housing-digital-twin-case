# Кликабельный прототип

Прототип интерфейса цифрового двойника жилого фонда (версия 5.3). Открывается
в браузере без установки: `demo/index.html`.

**Все данные в прототипе — демонстрационные.** Дома, адреса, люди, серийные
номера, показания датчиков, прогнозы и заявки вымышлены и генерируются в коде
страницы. Реальных данных городских систем в прототипе нет.

## Что использовано и откуда

| Файл | Что это | Источник и лицензия |
|---|---|---|
| `data/moscow-districts.geojson` | Границы 125 районов Москвы (без Новой Москвы — её заменяет упрощённый контур ТиНАО в коде) | [Code for Germany, click_that_hood](https://github.com/codeforgermany/click_that_hood/blob/main/public/data/moscow.geojson), лицензия MIT. Границы 2013 года |
| `data/moscow-districts.js` | Тот же файл, обёрнутый в JS, чтобы карта открывалась и без веб-сервера | Сгенерирован из `moscow-districts.geojson` |
| `vendor/maplibre-gl.js`, `vendor/maplibre-gl.css` | Картографическая библиотека MapLibre GL JS 4.7.1 | [maplibre/maplibre-gl-js](https://github.com/maplibre/maplibre-gl-js), BSD-3-Clause — `vendor/LICENSE-maplibre.txt` |
| `vendor/chart.umd.min.js` | Графики, Chart.js 4.4.0 | [chartjs/Chart.js](https://github.com/chartjs/Chart.js), MIT — `vendor/LICENSE-chartjs.md` |
| `vendor/lucide.min.js` | Иконки, Lucide 0.460.0 | [lucide-icons/lucide](https://github.com/lucide-icons/lucide), ISC — `vendor/LICENSE-lucide.txt` |
| Подложка карты | Растровые тайлы OpenStreetMap, загружаются из сети | © участники [OpenStreetMap](https://www.openstreetmap.org/copyright), ODbL |

Библиотеки лежат в репозитории, чтобы прототип не зависел от CDN. Из сети
загружается только подложка карты. Сервис CARTO, на котором прототип был
сделан изначально, сейчас требует ключ доступа, поэтому подложка
заменена на OpenStreetMap.
