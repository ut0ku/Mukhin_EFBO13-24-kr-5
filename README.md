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

Создан WebSocket маршрут -> /ws/rooms/{room_id}?username=alice

Подключение первого участника к комнате
<img width="1335" height="894" alt="image" src="https://github.com/user-attachments/assets/c9f452b6-d97c-4756-b599-f24df5de8a97" />

Попытка подключения к комнате без переданного username (код 1008)
<img width="1335" height="894" alt="image" src="https://github.com/user-attachments/assets/ac1c04d2-390d-429d-be7c-afe1709fe52a" />

Попытка подключения к комнате с username состоящим из пробелов (код 1008)
<img width="1335" height="894" alt="image" src="https://github.com/user-attachments/assets/b7a85c5b-4a3c-412f-bbb4-e38821762660" />

Подключение второго участника комнаты
<img width="1335" height="894" alt="image" src="https://github.com/user-attachments/assets/6a63ab78-4d0c-4b6b-85af-f4d63660ee02" />

Отправка сообщения первым пользователем
<img width="1335" height="894" alt="image" src="https://github.com/user-attachments/assets/b8a6a65c-7c2b-4e0c-99d0-1ec4a03734a5" />

Просмотр сообщения от лица второго пользователя
<img width="1335" height="894" alt="image" src="https://github.com/user-attachments/assets/fb8cce3b-0834-436f-8ec0-2852fdff5826" />

Отправление сервером ошибки при сообщении >300 символов
<img width="1335" height="894" alt="image" src="https://github.com/user-attachments/assets/ac225e59-668c-457a-a165-2150b5b0a39c" />

Просмотр сообщения от лица второго пользователя (сообщение не пришло, т.к >300 символов)
<img width="1335" height="894" alt="image" src="https://github.com/user-attachments/assets/b55b543a-d5d8-4bd1-8874-93942393078e" />

Создан маршрут /rooms/{room_id}/users (GET)
<img width="1335" height="894" alt="image" src="https://github.com/user-attachments/assets/5c1cd99d-6d82-4014-bfec-f5a9f9adc94a" />

Создан файл tests/test_websocket.py и написаны тесты, проверяющие следующие сценарии:
1. Подключение к комнате с корректным username.
2. Отправка сообщения и получение ответа через WebSocket.
3. Два клиента в одной комнате получают одно и то же сообщение.
4. Пользователи из разных комнат не получают чужие сообщения.
5. Слишком длинное сообщение возвращает error.
6. После отключения пользователя маршрут /rooms/{room_id}/users не вовзращает его в списке.

<img width="757" height="311" alt="image" src="https://github.com/user-attachments/assets/ee06a0e5-81e9-4f06-bedb-e00911ebb8b6" />

Задание 4

Приложение перестроено в модульную архитектуру с использованием APIRouter, зависимостей и проверки прав доступа.

Реализована следующая структура
<img width="364" height="576" alt="image" src="https://github.com/user-attachments/assets/5164d050-4eca-45a3-b8e5-427e898ed32b" />

Реализованы требования к маршрутизаторам
app/routers/tasks.py Префикс: /tasks

Маршруты
1. /tasks (POST)
<img width="1338" height="897" alt="image" src="https://github.com/user-attachments/assets/5ab67fe8-a434-4820-94ec-d9f80ed45b18" />

2. /tasks (GET)
<img width="1338" height="897" alt="image" src="https://github.com/user-attachments/assets/360c82dd-8084-49b7-9f93-00d8181408aa" />

3. /tasks/{task_id} (GET)
<img width="1338" height="897" alt="image" src="https://github.com/user-attachments/assets/ae13bdc2-563a-4552-acb5-791ea73810c6" />

4. /tasks/{task_id}/status (PATCH)
<img width="1341" height="897" alt="image" src="https://github.com/user-attachments/assets/fe755796-bff8-4caf-bbb9-aa39f6479364" />

5. /tasks/{task_id} (DELETE)
<img width="1341" height="897" alt="image" src="https://github.com/user-attachments/assets/8474a402-318d-4340-a5a0-9b08c4e7b3c0" />

app/routers/users.py Префикс: /users

1. /users/me (GET)
<img width="1341" height="900" alt="image" src="https://github.com/user-attachments/assets/29ce5853-7977-47bb-a1de-484584b3b8a5" />

2. /users/{user_id} (GET)
<img width="1341" height="900" alt="image" src="https://github.com/user-attachments/assets/0bcf8096-cdf6-4c94-9f7b-1af711c1b964" />

app/routers/admin.py Префикс: /admin
1. /admin/stats (GET)
<img width="1341" height="900" alt="image" src="https://github.com/user-attachments/assets/9ec25cef-2a6a-46e9-8edf-067732ac0756" />

2. /admin/tasks/{task_id} (DELETE)
<img width="1341" height="900" alt="image" src="https://github.com/user-attachments/assets/f8377a09-8eaf-4d1d-86e9-23221f2969db" />

Создан файл app/dependencies.py и реализованы зависимости:
1. get_current_user
Возвращает объект пользователя
User
<img width="1343" height="902" alt="image" src="https://github.com/user-attachments/assets/79b5f11c-482f-4332-8956-82c9bd022e0f" />

Admin
<img width="1344" height="904" alt="image" src="https://github.com/user-attachments/assets/3bddba35-e23c-43a6-b88e-9b0996c8814c" />

Проверка с отсутствующим X-User-Id
<img width="1344" height="906" alt="image" src="https://github.com/user-attachments/assets/0840c128-9179-44ca-8430-f48f4f3432d2" />

Проверка с некорректным X-User-Id
<img width="1344" height="906" alt="image" src="https://github.com/user-attachments/assets/308a274b-e1f5-4c29-af3d-270acf2a46cf" />

2. require_admin

Проверка X-User-Role не админ
<img width="1344" height="906" alt="image" src="https://github.com/user-attachments/assets/af3ee7c6-f58a-4c03-a7d5-b4355eb56214" />

get_storage возвращает объект / словарь, который используется как хранилище задач.

Все маршруты /tasks используют get_current_user

/tasks (GET) без указания пользователя
<img width="1346" height="908" alt="image" src="https://github.com/user-attachments/assets/7e51d64c-ecd9-4403-b59d-0d34768cbe25" />

/tasks (POST) без указания пользователя
<img width="1347" height="909" alt="image" src="https://github.com/user-attachments/assets/3cd3c848-bb43-4462-83f8-8ab77c5707b4" />

/tasks/{task_id} (GET) без указания пользователя
<img width="1347" height="909" alt="image" src="https://github.com/user-attachments/assets/4b121412-56e0-49b6-977c-bd361081df68" />

/tasks/{task_id}/status (PATCH) без указания пользователя
<img width="1347" height="909" alt="image" src="https://github.com/user-attachments/assets/907bc32d-446f-45b8-84cc-5b8ca42126fe" />

/tasks/{task_id} (DELETE) без указания пользователя
<img width="1347" height="909" alt="image" src="https://github.com/user-attachments/assets/d5747a8e-c96d-440b-88da-1f6ce79adac2" />

Маршруты /admin используют require_admin, обычный пользователь не имеет доступ к маршрутам /admin

/admin/stats (GET) пользователь не админ
<img width="1347" height="909" alt="image" src="https://github.com/user-attachments/assets/b81f6878-852b-484a-9881-b3002a1c9614" />

/admin/tasks/{task_id} (DELETE) пользователь не админ
<img width="1347" height="909" alt="image" src="https://github.com/user-attachments/assets/827a143f-a66e-4d63-b5a8-b4b1307d52ba" />

Маршрут /admin/stats возвращает статистику
<img width="1347" height="909" alt="image" src="https://github.com/user-attachments/assets/84cfd52f-2bc5-446b-b62c-66276ab5e508" />

Удаление любой задачи администратором
<img width="1347" height="909" alt="image" src="https://github.com/user-attachments/assets/895f2a15-a276-4ec9-9f9d-e45b2713972b" />

Создан файл tests/test_dependencies_and_routing.py
Проверены следующие сценарии:
1. /users/me возвращает текущего пользователя
2. Пользователь без заголовка X-User-Id получает 401
3. Обычный пользователь получает 403 при обращении к /admin/stats
4. Администратор получает статистику по всем задачам
5. Обычный пользователь не может удалить чужую задачу через /tasks/{task_id}
6. Администратор может удалить чужую задачу через /admin/tasks/{task_id}
7. В Swagger UI маршруты сгруппированы по тегам: tasks, users, admin

<img width="753" height="389" alt="image" src="https://github.com/user-attachments/assets/2aec01d9-1f6c-4983-8a73-e3bef9cfb3bc" />
