# Контрольная 5

Задание 1

Создано FastAPI-приложение с интеграционными тестами

Необходимые маршруты
1. Создание задачи /tasks (POST)
<img width="1314" height="882" alt="image" src="https://github.com/user-attachments/assets/5d970c69-0194-4a85-baa7-48bfd8427a40" />

3. Получение списка задач текущего пользователя /tasks (GET)
<img width="1314" height="882" alt="image" src="https://github.com/user-attachments/assets/29ef75ca-b341-4285-a07f-0bb0077fc8ff" />

5. Получение одной задачи /tasks/{task_id} (GET)
<img width="1314" height="882" alt="image" src="https://github.com/user-attachments/assets/c6971fe7-4244-4afb-b8ed-b7ba75c3b8d9" />

6. Изменение статуса задачи /tasks/{task_id}/status (PATCH)
<img width="1316" height="884" alt="image" src="https://github.com/user-attachments/assets/e62bce2e-ba8d-40dc-8341-bd35fc76cca4" />

7. Удаление задачи /tasks/{task_id} (DELETE)
<img width="1316" height="884" alt="image" src="https://github.com/user-attachments/assets/fb7cd8f4-c741-4c4d-98eb-a87e8b43ce4e" />

Сделаны тесты, на проверку сценариев:
1. Успешное создание задачи
2. Ошибка 422, если title <3 символов
3. Ошибка 401, если нет заголовка X-User-Id
4. Пользователь видит только свои задачи
5. Фильтрация по status и min_priority
6. Успешное изменение статуса задачи
7. Ошибка 404 при обращении к чужой / не сущ. задачи
8. Успешное удаление задачи

<img width="748" height="310" alt="image" src="https://github.com/user-attachments/assets/2bd6ae6e-3d6d-4ea7-9fa0-1add4b1d20e2" />

Задание 2

FastAPI-приложение упаковано в Docker-контейнер и подготовлен удобный запуск через docker compose

<img width="1418" height="131" alt="image" src="https://github.com/user-attachments/assets/882d4e9a-b57e-449a-9011-72bc5bed82ff" />

Проверка после запуска

<img width="462" height="68" alt="image" src="https://github.com/user-attachments/assets/6caa4c0a-91c5-4097-a4dd-467a7b80bace" />

Добавлен маршрут проверки состояния приложения /health (GET)
<img width="1318" height="885" alt="image" src="https://github.com/user-attachments/assets/e873b427-3078-4bb7-b22b-b087c438090a" />

Написан интеграционный тест, который проверяет маршрут /health
<img width="758" height="216" alt="image" src="https://github.com/user-attachments/assets/57832a94-8a3e-4d9c-b64b-c191d2c80f2e" />

Команды:

1. Установка и локальный запуск
python -m venv .venv
pip install -r requirements.txt
unicorn app.main:app --reload

2. Тесты
pytest

3. Docker Compose
docker compose up --build

4. Проверка API после запуска контейнера
curl http://localhost:8000/tasks -H "X-User-Id: 10"

Задание 3

Реализован WebSocket-чат с комнатами и простым HTTP-интерфейсом для просмотра активных подключений

