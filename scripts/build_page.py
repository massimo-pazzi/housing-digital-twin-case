"""Собирает страницу кейса index.html из report/case.md.

Текст — Markdown; места для инфографики отмечены в нём комментариями
<!-- fig:имя -->. Каждая цифра на схемах взята из источников, перечисленных в
SOURCES ниже (и сверенных в research/). Скриншоты прототипа — assets/img/,
снимаются скриптом scripts/screenshots.mjs.

Запуск:  .venv/bin/python scripts/build_page.py
"""

import base64
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
MD = ROOT / "report" / "case.md"
OUT = ROOT / "index.html"
REPO = "https://github.com/massimo-pazzi/housing-digital-twin-case"


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# Источники, на которые опирается страница. Ключ — короткий код для подписей.
SOURCES = [
    ("mosstat", "Мосстат, «Москва в цифрах 2024», табл. 6.15 — площадь жилых помещений",
     "https://77.rosstat.gov.ru/storage/mediabank/%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%20%D0%B2%20%D1%86%D0%B8%D1%84%D1%80%D0%B0%D1%85%202024.pdf"),
    ("kapremont", "mos.ru, программа капитального ремонта 2015–2044", "https://www.mos.ru/city/projects/kapremont/"),
    ("lifts", "mos.ru, замена лифтов в жилых домах", "https://www.mos.ru/mayor/themes/12647050/"),
    ("edc", "mos.ru, Единый диспетчерский центр, 06.09.2026", "https://www.mos.ru/news/item/175344073/"),
    ("r398", "Распоряжение Правительства РФ от 02.03.2026 № 398-р", "http://government.ru/docs/all/163630/"),
    ("dtm2023", "mos.ru, «Цифровой двойник Москвы», 07.07.2023", "https://www.mos.ru/news/item/126225073/"),
    ("dtm2026", "mos.ru, цифровой двойник Москвы, 21.07.2026", "https://www.mos.ru/news/item/173108073/"),
    ("moek", "МОЭК, предотвращённые технологические нарушения, 2024", "https://www.moek.ru/press/news/2024/12/1105/"),
    ("belgorod", "government.ru, рейтинг цифровой трансформации регионов за 2025 год", "http://government.ru/news/58063/"),
    ("singapore", "GovTech Singapore, «5 things to know about Virtual Singapore»",
     "https://www.tech.gov.sg/technews/5-things-to-know-about-virtual-singapore/"),
    ("helsinki", "Город Хельсинки, отчёт о пилоте цифрового двойника Калатасамы, 2019",
     "https://www.hel.fi/hel2/tietokeskus/data/helsinki/kaupunginkanslia/3D-malli/Helsinki3D_Kalasatama_Digital_Twins_020519.pdf"),
    ("ndtp", "Centre for Digital Built Britain, National Digital Twin Programme",
     "https://www.cdbb.cam.ac.uk/what-we-did/national-digital-twin-programme"),
    ("syracuse", "Kumar et al., «Using Machine Learning to Assess the Risk of and Prevent Water Main Breaks», KDD 2018",
     "https://arxiv.org/abs/1805.03597"),
    ("kii", "Федеральный закон от 26.07.2017 № 187-ФЗ «О безопасности критической информационной инфраструктуры», ст. 2, п. 8 (ред. 07.04.2025)",
     "https://www.consultant.ru/document/cons_doc_LAW_220885/c5051782233acca771e9adb35b47d3fb82c9ff1c/"),
]
SRC = {k: (t, u) for k, t, u in SOURCES}


LABELS = {"mosstat": "Мосстат", "kapremont": "капремонт, mos.ru", "lifts": "лифты, mos.ru",
          "edc": "Единый диспетчерский центр, mos.ru", "dtm2023": "Цифровой двойник Москвы, 2023",
          "dtm2026": "Цифровой двойник Москвы, 2026", "moek": "МОЭК", "syracuse": "Kumar et al., KDD 2018",
          "femp": "DOE/FEMP", "kone": "KONE", "hofor": "Jensen et al., IEEE Access 2025", "lbnl": "LBNL, 2020"}


def src(*keys):
    return "; ".join(f'<a href="{SRC[k][1]}" target="_blank" rel="noopener">{esc(LABELS.get(k, SRC[k][0]))}</a>'
                     for k in keys)


def figure(title, body, note=""):
    n = f'<p class="note">{note}</p>' if note else ""
    return f'<figure class="chart"><figcaption class="chart-title">{title}</figcaption>{body}{n}</figure>'


def shot(file, title, note):
    return figure(title, f'<a href="demo/" class="shot"><img src="assets/img/{file}" alt="{esc(title)}" loading="lazy"></a>',
                  note)


# ---------------------------------------------------------------- инфографика

def fig_summary():
    cols = [
        ("Источники данных", ["Заявки жителей и диспетчерских служб", "Паспорта домов и оборудования, капремонт",
                              "Телеметрия: тепловые пункты, лифты, датчики", "Слои «Цифрового двойника Москвы»"], "src"),
        ("Слой дома", ["Карточка дома: системы, оборудование, история работ", "Светофор состояния",
                       "Прогноз отказа с объяснением", "Превентивный наряд в один клик"], "core"),
        ("Кто принимает решение", ["Диспетчер — что брать первым", "Инженер — что проверить на неделе",
                                   "Руководитель района — куда бригады и бюджет", "Город — капремонт и подрядчики"], "use"),
    ]
    html = '<div class="flow">'
    for i, (h, items, cls) in enumerate(cols):
        if i:
            html += '<div class="arrow" aria-hidden="true">→</div>'
        html += f'<div class="flow-col {cls}"><div class="flow-h">{h}</div><ul>' + "".join(
            f"<li>{esc(x)}</li>" for x in items) + "</ul></div>"
    html += "</div>"
    return figure("Продукт в одной схеме: данные о доме из разных систем → одна карточка и прогноз → решение", html)


def fig_scale():
    tiles = [
        ("30 тыс.+", "многоквартирных домов в программе капремонта", "kapremont"),
        ("295 млн м²", "жилья, конец 2024 года", "mosstat"),
        ("117 тыс.+", "лифтов в жилых домах — почти четверть лифтов России", "lifts"),
        ("420 тыс.+", "инженерных систем и элементов в программе капремонта", "kapremont"),
        ("60 млн+", "заявок через Единый диспетчерский центр с 2016 года", "edc"),
        ("1 000+", "диспетчерских служб подключено к центру", "edc"),
    ]
    html = '<div class="kpis">' + "".join(
        f'<div class="kpi"><div class="kpi-v">{v}</div><div class="kpi-l">{esc(l)}</div></div>' for v, l, _ in tiles) + "</div>"
    return figure("Масштаб жилого фонда Москвы", html,
                  "Источники: " + src("kapremont", "mosstat", "lifts", "edc") + ".")


def fig_positioning():
    Y, P, N = '<span class="y">есть</span>', '<span class="p">частично</span>', '<span class="n">нет</span>'
    rows = [
        ("Видит инженерные системы внутри дома", N, N, P + " — тепловые пункты", Y),
        ("Прогноз отказов до аварии", N, N, P + " — раннее выявление нарушений", Y),
        ("Все системы дома в одной карточке", N, N, N, Y),
        ("Заявки и обращения жителей", P + " — работы ЖКХ на карте", Y, N, Y + " — как сигнал о доме"),
        ("Весь город", Y, Y, P + " — ~8 тыс. тепловых пунктов", "после масштабирования"),
    ]
    head = ["", "Цифровой двойник Москвы", "Единый диспетчерский центр", "Диспетчеризация МОЭК",
            "<strong>Наш продукт</strong>"]
    html = ('<div class="table-wrap"><table class="matrix"><thead><tr>' + "".join(f"<th>{h}</th>" for h in head) +
            "</tr></thead><tbody>" + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) +
            "</tbody></table></div>")
    return figure("Что уже есть у города и чего не хватает", html,
                  "По открытым источникам: " + src("dtm2023", "dtm2026", "edc", "moek") + ".")


def fig_model_metrics():
    bars = [("Модель машинного обучения", 62, "s1"), ("Правило «чем старше труба, тем опаснее»", 10, "neutral"),
            ("Случайный выбор", 8, "neutral")]
    html = '<div class="hbars">' + "".join(
        f'<div class="hb-row"><div class="hb-l">{esc(n)}</div><div class="hb-track"><div class="hb-bar {c}" '
        f'style="width:{v}%"></div><span class="hb-v" style="left:{v}%">{v}%</span></div></div>' for n, v, c in bars) + "</div>"
    return figure("Сиракьюс, водопровод: какую долю прорывов предсказал каждый способ в 1% самых рискованных участков",
                  html, "Независимое исследование города и Чикагского университета: " + src("syracuse") +
                  ". Так выглядит доказательство ценности модели: разница с простым правилом, а не процент «снижения аварийности».")


def fig_metric_tree():
    html = ('<div class="tree"><div class="tree-top"><div class="node star">Главная метрика<br>'
            '<strong>Доля превентивных работ</strong><br><span>нарядов по прогнозу и плану, а не по аварии</span></div></div>'
            '<div class="tree-row">'
            '<div class="node"><strong>Аварийные заявки</strong><br><span>на 1 000 квартир</span></div>'
            '<div class="node"><strong>Часы без тепла, воды, лифта</strong><br><span>на дом в месяц</span></div>'
            '<div class="node"><strong>Повторные обращения</strong><br><span>по одной проблеме</span></div>'
            '</div><div class="tree-label">Результат для города</div>'
            '<div class="tree-row guard">'
            '<div class="node"><strong>Время реакции на аварию</strong><br><span>не растёт</span></div>'
            '<div class="node"><strong>Напрасные выезды</strong><br><span>по ложным прогнозам — ниже порога</span></div>'
            '</div><div class="tree-label">Ограничители — чтобы главная метрика не росла ценой вреда</div></div>')
    return figure("Метрики продукта", html)


def fig_roadmap():
    stages = [("0. Предпроектное исследование", 0, 3, "аудит данных, пилотный ЖК, метрики"),
              ("1. MVP — один жилой комплекс", 3, 11, "карта, светофор, карточки, датчики"),
              ("2. Пилот — один район", 11, 27, "интеграция с ОДС, прогнозная модель"),
              ("3. Масштабирование", 27, 43, "все округа, планирование бригад")]
    total = 43
    rows = "".join(
        f'<div class="gantt-row"><div class="gantt-l">{esc(n)}<span>{esc(d)}</span></div>'
        f'<div class="gantt-track"><div class="gantt-bar s{i + 1}" style="left:{a / total * 100:.1f}%;width:{(b - a) / total * 100:.1f}%"></div>'
        f'<div class="gate" style="left:{b / total * 100:.1f}%" title="веха"></div></div></div>'
        for i, (n, a, b, d) in enumerate(stages))
    axis = '<div class="gantt-axis"><span></span><div>' + "".join(
        f'<span style="left:{m / total * 100:.1f}%">{m}</span>' for m in (0, 12, 24, 36)) + "</div></div>"
    return figure("Этапы и вехи: месяцы от старта при верхней оценке сроков", rows + axis,
                  "Ромб — веха: решение о следующем этапе только после демонстрации результата предыдущего. "
                  "Сроки этапов — 2–3, 6–8, 12–16 и 12–16 месяцев.")


def fig_business_model():
    cards = [("Монолит", "Заказная разработка под Москву", "Понятные деньги",
              "Каждый следующий город — почти новый проект", False),
             ("Фреймворк", "Стандарты и экосистема, как в Великобритании", "Влияние на отрасль",
              "Почти без выручки; стандарты — функция Минстроя и Росстандарта", False),
             ("Платформенный продукт", "Одно ядро, настройка под город", "Второй город — настройка, а не разработка",
              "Нужно с первого дня проектировать для тиражирования", True)]
    html = '<div class="cards">' + "".join(
        f'<div class="card{" rec" if r else ""}">{"<div class=badge>рекомендовал</div>" if r else ""}'
        f'<div class="card-h">{esc(t)}</div><div class="card-s">{esc(s)}</div>'
        f'<div class="pro">+ {esc(p)}</div><div class="con">− {esc(c)}</div></div>' for t, s, p, c, r in cards) + "</div>"
    html += ('<div class="streams"><span>Выручка платформы:</span><span class="st">внедрение для первого города</span>'
             '<span class="st">лицензия и адаптация для следующих</span><span class="st">ежегодное сопровождение</span></div>')
    return figure("Три трека и рекомендованная модель", html)


def fig_stakeholders():
    rows = [("Мосстратегия, Департамент экономической политики и развития", "Инициатор и заказчик концепции",
             "Проект, который можно предложить префектурам: проблема, нормативка, этапы"),
            ("Префектуры округов", "Покупатели и внедряющие", "Сводка по округу, понятные вехи и модель финансирования превентивного ремонта"),
            ("ДИТ Москвы", "Оператор «Цифрового двойника Москвы»", "Федерация: данные продукта — слоем в городской двойник"),
            ("Диспетчерские службы, ГБУ «Жилищник», управляющие компании", "Ежедневные пользователи — и те, чью работу продукт делает видимой",
             "Прогноз встроен в привычный наряд; правила контроля согласованы до пилота"),
            ("МОЭК, фонд капремонта", "Владельцы данных о тепловых пунктах и ремонтах",
             "Доступ к данным — условие этапа 0; нужен «внутренний чемпион»"),
            ("Жители", "Конечные выгодоприобретатели", "Меньше отключений, статус работ по своему дому")]
    html = ('<div class="table-wrap"><table><thead><tr><th>Кто</th><th>Роль</th><th>Что ему нужно от проекта</th></tr></thead><tbody>' +
            "".join(f"<tr><td>{esc(a)}</td><td>{esc(b)}</td><td>{esc(c)}</td></tr>" for a, b, c in rows) +
            "</tbody></table></div>")
    return figure("Стейкхолдеры проекта", html)


def fig_effects():
    rows = [("Промышленность и объекты (США)", "Предиктивное обслуживание экономит 8–12% к плановому", "Федеральное руководство", "femp"),
            ("Лифты в жилых домах", "На 28% меньше вызовов мастера", "Производитель, методика не раскрыта", "kone"),
            ("Водопровод, Сиракьюс", "62% прорывов в 1% самых рискованных участков", "Независимое исследование", "syracuse"),
            ("Теплосети, Копенгаген", "Более 40% отказов при проверке 10% сети", "Независимое исследование", "hofor"),
            ("Инженерные системы 6 500 зданий", "Медианная экономия энергии 9%, окупаемость ~2 года", "Независимое исследование", "lbnl")]
    html = ('<div class="table-wrap"><table><thead><tr><th>Где</th><th>Что измерено</th><th>Кто измерял</th></tr></thead><tbody>' +
            "".join(f"<tr><td>{esc(a)}</td><td>{esc(b)}</td><td>{esc(c)} — {src(k)}</td></tr>" for a, b, c, k in rows) +
            "</tbody></table></div>")
    return figure("Что опубликовано об эффекте предиктивного обслуживания", html,
                  "Ни одно измерение не сделано на жилом фонде Москвы, поэтому эффект для города оценивает пилот.")



def fig_demo_banner():
    return ('<a class="demo-banner" href="demo/"><img src="assets/img/overview.png" alt="Экран прототипа" loading="lazy">'
            '<span class="db-text"><strong>Открыть прототип</strong>'
            '<span>От карты Москвы до карточки дома и прогноза отказа лифта. '
            'Все данные вымышлены.</span><span class="db-btn">Перейти к прототипу →</span></span></a>')


def fig_users():
    html = ('<div class="flow two"><div class="flow-col"><div class="flow-h">Покупает и внедряет</div><ul>'
            '<li>Префектуры округов</li><li>Мосстратегия — инициатор проекта</li></ul>'
            '<p class="small">Нужна сводка по округу, отчётность, обоснование бюджета</p></div>'
            '<div class="arrow" aria-hidden="true">≠</div>'
            '<div class="flow-col core"><div class="flow-h">Пользуется каждый день</div><ul>'
            '<li>Диспетчеры ОДС</li><li>Инженеры управляющих компаний</li><li>Руководители районных служб</li></ul>'
            '<p class="small">Нужен список «что делать сегодня» — иначе продукт не меняет ни одного наряда</p></div></div>')
    return figure("Два клиента: тот, кто покупает, и тот, чью работу продукт меняет", html)


def fig_retro_test():
    html = ('<div class="timeline"><div class="tl-seg train" style="flex:2">Обучение: заявки и паспорта за прошлые 2–3 года</div>'
            '<div class="tl-seg test" style="flex:1">Проверка: следующая зима</div></div>'
            '<div class="tl-legend">Модель и правило «по возрасту» получают одинаковые данные до начала зимы и ранжируют '
            'оборудование по риску. Сравнивается, какая доля аварий зимы попала в верхние 10% каждого списка.</div>'
            '<div class="decision"><div class="dc yes"><strong>Модель заметно лучше правила</strong><br>'
            '<span>идём в MVP с прогнозом</span></div><div class="dc no"><strong>Выигрыш мал</strong><br>'
            '<span>прогноз только для систем, где он заметен; для остальных — карточка дома и телеметрия</span></div></div>')
    return figure("Ретроспективный тест: два месяца вместо 6–8 месяцев MVP", html,
                  "Разделение только по времени: случайное перемешивание лет «подсмотрит» будущее и завысит результат.")


def fig_pivots():
    rows = [("Префектурам нужен переход от реактивного ремонта к предиктивному",
             "В префектурах выяснилось: сейчас им важнее контроль уборки территории — дворники, техника, фото до и после",
             "Добавил в прототип мониторинг уборки: GPS-треки дворников, план и факт маршрута, простои, покрытие"),
            ("Продукт — первый в России цифровой двойник жилого фонда",
             "У города уже есть Единый диспетчерский центр с ИИ-ассистентом, «Цифровой двойник Москвы» и онлайн-контроль тепловых пунктов МОЭК",
             "Позиционирование как слоя, который соединяет эти системы на уровне дома"),
            ("Классификация обращений жителей — ядро ценности, сильная сторона команды",
             "В Едином диспетчерском центре ИИ-ассистент уже обрабатывает до половины обращений",
             "Обращения стали одним из сигналов о состоянии дома, а не отдельным продуктом"),
            ("Мировые цифровые двойники доказывают экономику проекта",
             "Virtual Singapore, Хельсинки и британская программа — про планирование и стандарты, а не про обслуживание домов",
             "Взял из них организационные уроки; эффект для Москвы не обещаю до пилота"),
            ("Нулевой этап — аудит данных и техническое задание, затем MVP",
             "Префектура заплатит за прогноз, только если его выигрыш виден на московских данных, а не на зарубежных",
             "Добавил ретроспективный тест с заранее заданным порогом и решением для систем, где выигрыш мал")]
    html = ('<div class="table-wrap"><table><thead><tr><th>Что думал сначала</th><th>Что изменило мнение</th>'
            '<th>Что сделал</th></tr></thead><tbody>' +
            "".join(f"<tr><td>{esc(a)}</td><td>{esc(b)}</td><td>{esc(c)}</td></tr>" for a, b, c in rows) +
            "</tbody></table></div>")
    return figure("Как менялись решения", html)


def fig_sources():
    items = "".join(f'<li>{esc(t)} — <a href="{u}" target="_blank" rel="noopener">ссылка</a></li>' for _, t, u in SOURCES)
    return (f'<ol class="sources">{items}</ol>'
            f'<p class="note">Полная сверка исходных материалов проекта с первоисточниками — в '
            f'<a href="{REPO}/tree/main/research" target="_blank" rel="noopener">research/</a>. '
            f'Происхождение библиотек и карты в прототипе — в <a href="{REPO}/blob/main/demo/README.md" '
            f'target="_blank" rel="noopener">demo/README.md</a>.</p>')


def author_block():
    img = base64.b64encode((ROOT / "assets/img/author.jpg").read_bytes()).decode()
    return (f'<div class="author"><img src="data:image/jpeg;base64,{img}" alt="Максим Поципух" width="64" height="64">'
            '<span>Максим Поципух</span></div>')


FIGS = {
    "summary": fig_summary, "scale": fig_scale, "positioning": fig_positioning,
    "prototype_overview": lambda: shot("overview.png", "Сводка по Москве: дома по зонам риска, бригады, износ сетей, аварии",
                                       "Все данные на скриншотах вымышлены — это прототип для обсуждения концепции, а не работающая система.") +
                                  shot("map.jpg", "Карта: от города к округу, району и дому",
                                       "Границы районов — Code for Germany (MIT), подложка — © участники OpenStreetMap."),
    "prototype_cleaning": lambda: shot("cleaning.jpg", "Уборка территории: GPS-треки дворников, план и факт маршрута, простои, покрытие",
                                       "Раздел добавлен после разговоров с префектурами. Данные вымышлены."),
    "prototype_house": lambda: shot("house.png", "Карточка дома: паспорт, оборудование, история работ", ""),
    "prototype_forecast": lambda: shot("forecasts.png", "Прогнозы: вероятность отказа, горизонт, уверенность, источник сигнала", ""),
    "prototype_ops": lambda: shot("tickets.png", "Заявки: категории и приоритеты", "") +
                             shot("brigades.png", "Бригады и наряды: смена, загрузка, доля превентивных работ", ""),
    "model_metrics": fig_model_metrics, "metric_tree": fig_metric_tree, "roadmap": fig_roadmap,
    "stakeholders": fig_stakeholders, 
    "sources": fig_sources, "demo_banner": fig_demo_banner, "users": fig_users,
    "retro_test": fig_retro_test,
}

CSS = """
:root{
  --bg:#f5f6f7; --surface:#ffffff; --ink:#18202a; --ink-2:#4b5662; --muted:#6c7782;
  --rule:#d9dee3; --accent:#1f5fae; --accent-soft:#e6eef8; --neutral:#aab2bb;
  --s1:#2a78d6; --s2:#eb6834; --s3:#1baf7a; --s4:#a07800; --ok:#1b8a5a; --warn:#a36b00; --no:#8a929b;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){ color-scheme:dark;
    --bg:#11161c; --surface:#171d24; --ink:#e7ebef; --ink-2:#b5bec7; --muted:#8c96a0;
    --rule:#2c343d; --accent:#79a9e8; --accent-soft:#1c2632; --neutral:#5d6670;
    --s1:#3987e5; --s2:#d95926; --s3:#199e70; --s4:#c98500; --ok:#3fbf86; --warn:#e0a640; --no:#7d8791; }
}
:root[data-theme="dark"]{ color-scheme:dark;
  --bg:#11161c; --surface:#171d24; --ink:#e7ebef; --ink-2:#b5bec7; --muted:#8c96a0;
  --rule:#2c343d; --accent:#79a9e8; --accent-soft:#1c2632; --neutral:#5d6670;
  --s1:#3987e5; --s2:#d95926; --s3:#199e70; --s4:#c98500; --ok:#3fbf86; --warn:#e0a640; --no:#7d8791; }
body{margin:0; background:var(--bg); color:var(--ink); font-family:"Golos Text",system-ui,-apple-system,"Segoe UI",sans-serif;
  font-size:17px; line-height:1.62; padding-inline:16px; padding-block:40px 64px;}
.page{max-width:48rem; margin:0 auto;}
a{color:var(--accent);}
.eyebrow{font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:12.5px; letter-spacing:.06em; text-transform:uppercase; color:var(--accent); margin:0 0 14px;}
h1{font-size:clamp(1.7rem,4.2vw,2.3rem); line-height:1.18; font-weight:700; letter-spacing:-.01em; text-wrap:balance; margin:0 0 16px;}
h2{font-size:1.28rem; line-height:1.3; font-weight:650; text-wrap:balance; margin:46px 0 12px; padding-top:22px; border-top:1px solid var(--rule);}
.author{display:flex; align-items:center; gap:12px; margin:4px 0 16px; font-weight:600; font-size:15px;}
.author img{width:64px; height:64px; border-radius:50%; object-fit:cover; border:1px solid var(--rule);}
.author + p em{color:var(--ink-2); font-size:15px;}
p{margin:0 0 14px;} strong{font-weight:620;} hr{display:none;}
ul,ol{margin:0 0 14px; padding-left:1.3em;} li{margin-bottom:4px;}
.chart{margin:16px 0 22px; background:var(--surface); border:1px solid var(--rule); border-radius:6px; padding:14px 16px 12px;}
.chart-title{font-weight:600; font-size:14.5px; margin-bottom:10px; line-height:1.4;}
.note{font-size:12.5px; color:var(--muted); margin:10px 0 0; line-height:1.5;}
.shot img{display:block; width:100%; height:auto; border:1px solid var(--rule); border-radius:4px;}
.kpis{display:grid; grid-template-columns:repeat(auto-fit,minmax(170px,1fr)); gap:10px;}
.kpi{border:1px solid var(--rule); border-radius:6px; padding:12px 14px;}
.kpi-v{font-size:1.45rem; font-weight:700; font-variant-numeric:tabular-nums; letter-spacing:-.01em;}
.kpi-l{font-size:13px; line-height:1.4; color:var(--ink-2); margin-top:4px;}
.flow{display:grid; grid-template-columns:1fr auto 1fr auto 1fr; gap:8px; align-items:stretch;}
.flow-col{border:1px solid var(--rule); border-radius:6px; padding:10px 12px; font-size:13.5px;}
.flow-col ul{margin:0; padding-left:1.1em;} .flow-col li{margin-bottom:5px; line-height:1.4;}
.flow-h{font-weight:650; font-size:13px; text-transform:uppercase; letter-spacing:.04em; color:var(--ink-2); margin-bottom:8px;}
.flow-col.core{background:var(--accent-soft); border-color:var(--accent);} .flow-col.core .flow-h{color:var(--accent);}
.arrow{align-self:center; color:var(--muted); font-size:22px;}
@media (max-width:640px){ .flow{grid-template-columns:1fr;} .arrow{transform:rotate(90deg); justify-self:center;} }
.table-wrap{overflow-x:auto; margin:0 0 4px;}
table{border-collapse:collapse; width:100%; font-size:14px;}
th,td{text-align:left; padding:8px 10px 8px 0; border-bottom:1px solid var(--rule); vertical-align:top;}
th{font-weight:600; color:var(--ink-2); font-size:12.5px;}
.matrix td:first-child{font-weight:550; min-width:12em;} .matrix th:last-child,.matrix td:last-child{background:var(--accent-soft); padding-left:8px;}
.y{color:var(--ok); font-weight:600;} .p{color:var(--warn); font-weight:600;} .n{color:var(--no);}
.hbars{display:grid; gap:10px;}
.hb-row{display:grid; grid-template-columns:minmax(10em,16em) 1fr; gap:12px; align-items:center; font-size:13.5px;}
.hb-track{position:relative; height:22px; background:var(--bg); border-radius:3px;}
.hb-bar{height:100%; border-radius:3px;} .hb-bar.s1{background:var(--s1);} .hb-bar.neutral{background:var(--neutral);}
.hb-v{position:absolute; top:2px; margin-left:8px; font-weight:600; font-variant-numeric:tabular-nums; font-size:13px;}
.tree{display:grid; gap:10px; font-size:13.5px; text-align:center;}
.tree-top{display:flex; justify-content:center;}
.node{border:1px solid var(--rule); border-radius:6px; padding:10px 12px; line-height:1.4;} .node span{color:var(--muted); font-size:12.5px;}
.node.star{background:var(--accent-soft); border-color:var(--accent); max-width:22em;}
.tree-row{display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:10px;}
.tree-row.guard .node{border-style:dashed;}
.tree-label{font-size:12px; color:var(--muted); margin-top:-4px;}
.gantt-row{display:grid; grid-template-columns:minmax(11em,16em) 1fr; gap:12px; align-items:center; margin-bottom:10px; font-size:13.5px;}
.gantt-l span{display:block; color:var(--muted); font-size:12px;}
.gantt-track{position:relative; height:20px; background:var(--bg); border-radius:3px;}
.gantt-bar{position:absolute; top:0; height:100%; border-radius:3px;}
.gantt-bar.s1{background:var(--s4);} .gantt-bar.s2{background:var(--s3);} .gantt-bar.s3{background:var(--s1);} .gantt-bar.s4{background:var(--s2);}
.gate{position:absolute; top:3px; width:12px; height:12px; margin-left:-6px; background:var(--ink); transform:rotate(45deg); border:2px solid var(--surface);}
.gantt-axis{display:grid; grid-template-columns:minmax(11em,16em) 1fr; gap:12px; font-size:11px; color:var(--muted); font-family:"IBM Plex Mono",ui-monospace,monospace;}
.gantt-axis div{position:relative; height:14px;} .gantt-axis div span{position:absolute; transform:translateX(-50%);}
.gantt-axis div span:first-child{transform:none;}
.cards{display:grid; grid-template-columns:repeat(auto-fit,minmax(190px,1fr)); gap:10px;}
.card{position:relative; border:1px solid var(--rule); border-radius:6px; padding:12px 14px; font-size:13.5px; line-height:1.45;}
.card.rec{border-color:var(--accent); background:var(--accent-soft);}
.badge{position:absolute; top:-10px; right:10px; background:var(--accent); color:#fff; font-size:11px; padding:1px 8px; border-radius:10px;}
.card-h{font-weight:650; font-size:15px;} .card-s{color:var(--ink-2); margin:2px 0 8px;}
.pro{color:var(--ok);} .con{color:var(--ink-2);}
.streams{display:flex; flex-wrap:wrap; gap:6px 8px; align-items:center; margin-top:12px; font-size:13px;}
.streams .st{border:1px solid var(--rule); border-radius:12px; padding:2px 10px;}
.sources{font-size:14.5px; line-height:1.55; padding-left:1.5em;}
.demo-banner{display:flex; gap:16px; align-items:center; margin:6px 0 24px; padding:12px; border:1px solid var(--accent); border-radius:8px; background:var(--accent-soft); color:var(--ink); text-decoration:none;}
.demo-banner img{width:180px; height:auto; border-radius:4px; border:1px solid var(--rule); flex-shrink:0;}
.db-text{display:flex; flex-direction:column; gap:4px; font-size:14px; line-height:1.45;} .db-text strong{font-size:16px;}
.db-btn{color:var(--accent); font-weight:600; margin-top:2px;}
.demo-banner:hover{border-width:2px; padding:11px;}
@media (max-width:520px){ .demo-banner{flex-direction:column; align-items:flex-start;} .demo-banner img{width:100%;} }
.flow.two{grid-template-columns:1fr auto 1fr;} .small{font-size:12.5px; color:var(--muted); margin:8px 0 0;}
@media (max-width:640px){ .flow.two{grid-template-columns:1fr;} }
.timeline{display:flex; gap:4px; font-size:13px; font-weight:550;}
.tl-seg{padding:10px 12px; border-radius:4px; color:#fff;} .tl-seg.train{background:var(--s1);} .tl-seg.test{background:var(--s2);}
.tl-legend{font-size:13px; color:var(--ink-2); margin:10px 0;}
.decision{display:grid; grid-template-columns:1fr 1fr; gap:10px; font-size:13.5px;}
.dc{border:1px solid var(--rule); border-radius:6px; padding:10px 12px;} .dc span{color:var(--muted); font-size:12.5px;}
.dc.yes{border-color:var(--ok);} .dc.no{border-style:dashed;}
@media (max-width:520px){ body{font-size:16px; padding-block:24px 48px;} .hb-row,.gantt-row,.gantt-axis{grid-template-columns:1fr;} .gantt-axis span:first-child{display:none;} }
"""


def main():
    html = markdown.markdown(MD.read_text(encoding="utf-8"), extensions=["tables"])
    title, rest = html.split("</h1>", 1)
    html = title + "</h1>\n" + author_block() + rest
    for name, fn in FIGS.items():
        marker = f"<!-- fig:{name} -->"
        assert marker in html, f"нет места для блока {name}"
        html = html.replace(marker, fn())
    html = html.replace("<table>", '<div class="table-wrap"><table>').replace("</table>\n", "</table></div>\n")
    # таблицы внутри инфографики уже обёрнуты
    html = html.replace('<div class="table-wrap"><div class="table-wrap">', '<div class="table-wrap">')
    page = f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Где прорвёт до звонка жителя</title>
<meta name="description" content="Продуктовый кейс: цифровой двойник жилого фонда Москвы и прогноз отказов инженерных систем домов">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Golos+Text:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>{CSS}</style>
</head>
<body>
<main class="page">
<p class="eyebrow">Портфолио-кейс: проработка нового продукта · Максим Поципух · Октябрь 2026</p>
{html}
</main>
</body>
</html>
"""
    OUT.write_text(page, encoding="utf-8")
    print(f"{OUT.relative_to(ROOT)}: {len(page) // 1024} КБ, блоков: {len(FIGS)}")


if __name__ == "__main__":
    main()
