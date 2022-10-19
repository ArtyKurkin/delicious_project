# Проект Foodgram <<Продуктовый помощник>>
![example workflow](https://github.com/ArtyKurkin/foodgram-project-react/actions/workflows/main.yml/badge.svg)
## Описание

###### Сервис позволяет публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Автор проекта:

* ✅[Артем Куркин](https://github.com/ArtyKurkin)

## Проект доступен по адресу:

* [foodgram](http://178.154.222.26)

### Запуск проекта с использованием Docker:
Клонируем репозиторий:
```
https://github.com/ArtyKurkin/foodgram-project-react.git
cd foodgram-project-react
```
В папке infra создаём .env файл и наполняем его:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY = <your_secret_key>
```
Собираем контейнер:
```
sudo docker-compose up -d
```
Для доступа к контейнеру выполните следующие команды:
```
sudo docker-compose exec backend python manage.py makemigrations
sudo docker-compose exec backend python manage.py migrate --noinput
sudo docker-compose exec backend python manage.py createsuperuser
sudo docker-compose exec backend python manage.py collectstatic --no-input
```
Наполняем базу данных ингредиентами и тэгами:
```
sudo docker-compose exec backend python manage.py load_ingredients
sudo docker-compose exec backend python manage.py load_tags
```
## Регистрация и авторизация

В проекте доступна система регистрации и авторизации пользователей.
#### Обязательные поля для пользователя:
* Логин
* Пароль
* Email
* Имя
* Фамилия
#### Уровни доступа пользователей:
* Гость (неавторизованный пользователь)
* Авторизованный пользователь
* Администратор

## Рецепт

Рецепт описывается такими полями:
* Автор публикации (пользователь).
* Название.
* Картинка.
* Текстовое описание.
* Ингредиенты: продукты для приготовления блюда по рецепту. Множественное поле, выбор из предустановленного списка, с указанием количества и единицы измерения.
* Тег (можно установить несколько тегов на один рецепт, выбор из предустановленных).
* Время приготовления в минутах.

Все поля обязательны для заполнения.

## Тег

Тег должен описываться такими полями:
* Название.
* Цветовой HEX-код (например, #49B64E).
* Slug.

Все поля обязательны для заполнения и уникальны.
## Ингредиент

Данные об ингредиентах хранятся в нескольких связанных таблицах. В результате на стороне пользователя ингредиент должен описываться такими полями:
* Название.
* Количество.
* Единицы измерения.

Все поля обязательны для заполнения.

# Сервисы и страницы проекта

## Главная страница

Содержимое главной страницы — список первых шести рецептов, отсортированных по дате публикации (от новых к старым). Остальные рецепты доступны на следующих страницах: внизу страницы есть пагинация.
## Страница рецепта

На странице — полное описание рецепта. Для авторизованных пользователей — возможность добавить рецепт в избранное и в список покупок, возможность подписаться на автора рецепта.
## Страница пользователя

На странице — имя пользователя, все рецепты, опубликованные пользователем и возможность подписаться на пользователя.
## Подписка на авторов

Подписка на публикации доступна только авторизованному пользователю. Страница подписок доступна только владельцу.
## Сценарий поведения пользователя:
Пользователь переходит на страницу другого пользователя или на страницу рецепта и подписывается на публикации автора кликом по кнопке __«Подписаться на автора»__.
Пользователь переходит на страницу __«Мои подписки»__ и просматривает список рецептов, опубликованных теми авторами, на которых он подписался. Сортировка записей — по дате публикации (от новых к старым).
При необходимости пользователь может отказаться от подписки на автора: переходит на страницу автора или на страницу его рецепта и нажимает __«Отписаться от автора»__.
## Список избранного

Работа со списком избранного доступна только авторизованному пользователю. Список избранного может просматривать только его владелец.
##### Сценарий поведения пользователя:
Пользователь отмечает один или несколько рецептов кликом по кнопке __«Добавить в избранное»__.
Пользователь переходит на страницу «Список избранного» и просматривает персональный список избранных рецептов.
При необходимости пользователь может удалить рецепт из избранного.
## Список покупок

Работа со списком покупок доступна авторизованным пользователям. Список покупок может просматривать только его владелец.
##### Сценарий поведения пользователя:
Пользователь отмечает один или несколько рецептов кликом по кнопке __«Добавить в покупки»__.
Пользователь переходит на страницу Список покупок, там доступны все добавленные в список рецепты. Пользователь нажимает кнопку Скачать список и получает файл с суммированным перечнем и количеством необходимых ингредиентов для всех рецептов, сохранённых в __«Списке покупок»__.
При необходимости пользователь может удалить рецепт из списка покупок.
В результате список покупок может выглядеть так:
Фарш (баранина и говядина) (г) — 600
Сыр плавленый (г) — 200
Лук репчатый (г) — 50
Картофель (г) — 1000
Молоко (мл) — 250
Яйцо куриное (шт) — 5
Соевый соус (ст. л.) — 8
Сахар (г) — 230
Растительное масло рафинированное (ст. л.) — 2
Соль (по вкусу) — 4
Перец черный (щепотка) — 3
По желанию: в список покупок можно вывести шапку и подвал (или что-то одно) с информацией о вашем проекте.
## Фильтрация по тегам

При нажатии на название тега выводится список рецептов, отмеченных этим тегом. Фильтрация может проводится по нескольким тегам в комбинации «или»: если выбраны несколько тегов — в результате должны быть показаны рецепты, которые отмечены хотя бы одним из этих тегов.
