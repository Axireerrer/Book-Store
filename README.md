# Книжный магазин API (Backend)

Этот проект представляет собой Backend-часть для книжного магазина, предоставляющего API для выдачи книг, управления лайками, рейтингом, закладками и правами доступа пользователей.
Он также включает в себя покрытие кода unit-тестами, авторизацию пользователей через GitHub, функции поиска, фильтрации и сортировки, оптимизацию SQL-запросов, применение агрегации и аннотаций, а также создание кэширующих полей.

# Функциональность 

- API для книг:
  
   - Выдача списка доступных книг.
   - Добавление новых книг.
   - Просмотр деталей книги.
   - Управление лайками и рейтингом:
   - Пользователи могут ставить лайки книгам.
   - Рассчитывается рейтинг книги на основе лайков.
     
- Управление закладками:
  
   - Пользователи могут добавлять книги в свои закладки для последующего доступа.
     
- Управление доступом пользователей:
  
   - Различные уровни доступа для просмотра книг и управления закладками.
     
- Авторизация через GitHub:
  
   - Пользователи могут авторизоваться с помощью своего аккаунта GitHub.
   - Функции поиска, фильтрации и сортировки:
   - Поиск книг по различным параметрам.
   - Фильтрация книг по жанру, автору и другим параметрам.
   - Сортировка результатов по различным критериям.
     
- Оптимизация SQL-запросов:
  
   - Использование оптимальных запросов для улучшения производительности.
     
- Применение агрегации и аннотаций:
  
   - Использование агрегации для вычисления статистики (например, средний рейтинг книги).
   - Использование аннотаций для добавления дополнительной информации к результатам запросов.
     
- Создание кэширующих полей:
  
   - Кэширование часто запрашиваемых данных для уменьшения нагрузки на сервер.
    
# Технологии

   - Язык программирования: Python
   - Фреймворк: Django
   - База данных: PostgreSQL
   - Тестирование: Django test
   - Авторизация: GitHub OAuth

# Установка и настройка

   - Клонируйте репозиторий: git clone https://github.com/Axireerrer/Book-Store.git
   - Установите зависимости: pip install -r requirements.txt
   - Настройте базу данных в файле settings.py.
   - Выполните миграции: python manage.py migrate
   - Запустите сервер: python manage.py runserver
    
# Запуск тестов

   - Выполните команду python manage.py test для запуска unit-тестов.
