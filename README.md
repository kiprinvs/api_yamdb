# api_yamdb

Описание
API YamDB - это проект для сбора отзывов на различные произведения, такие как книги, музыка, фильмы и т.д.
Пользователи могут оставлять отзывы и выставлять оценки произведениям, а также комментировать отзывы других пользователей.

Установка

1. Клонирование репозитория  
git clone https://github.com/kiprinvs/api_yamdb.git   
cd api_yamdb  


2. Создание виртуального окружения  
python3 -m venv venv  
source venv/bin/activate  


3. Установка зависимостей  
python3 -m pip install --upgrade pip  
pip install -r requirements.txt  


4. Применение миграций  
python manage.py migrate  


5. Импорт csv файлов  
python manage.py import_csv


6. Запуск  
python3 manage.py runserver  


Все эндпоинты, а так же их параметры доступны по адресу:   
http://127.0.0.1:8000/redoc/  


Проект разработан командой. Основные участники команды:  
https://github.com/kiprinvs  
https://github.com/AlexBrantt  
https://github.com/penguinK7  