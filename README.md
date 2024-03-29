# Хранилище конфиденциальной информации

Хранилище различных ключей, токенов и другой чувствительной информации


## Принцип работы
Есть база данных с зашифрованными данными. Данные шифруются одним токеном, который при (пере)запуске должен ввести администратор, что защищает от утечки данных вместе с базой.

Все запросы к API происходят искобчительно с JWT токеном в поле `Authorization: Bearer ...`. Все доступы выдаются по значению поля `sub` JWT токена.

Популярные юзкейсы:

### Первоначальная настройка
- Администратор получает JWT токен. *Слелующие пункты этот токен в хэдэре*
- Производит первоначальную настройку ручкой `/POST install`
- Разблокирует базу ручкой `/POST unseal`

### Разблокировка
- Администратор получает JWT токен. *Слелующие пункты этот токен в хэдэре*
- Разблокирует базу ручкой `/POST unseal`

### Создание секрета
- Пользователь получает JWT токен. *Слелующие пункты этот токен в хэдэре*
- Создает секрет `POST /secret`, становится автоматически его владельцем (`GET /secret/{sec_name}/access` отдает его `sub` в поле `owner`)
- Создает новую версию секрета `POST /secret/{sec_name}/ver`
- Дает доступ к секрету `PUT /secret/{sec_name}/access`

### Получение секрета
- Пользователь получает JWT токен. *Слелующие пункты этот токен в хэдэре*
- Получает список секретов `GET /secret`
- Получает значение послдней версии интересующего его секрета `GET /secret/{sec_name}/ver/{ver_num}`. 
- В предыдущем пункте пользователь получил список ключей. Значение конкретного ключа через `GET /secret/{sec_name}/ver/{ver_num}/token/{t_name}`


## API

### Secret
sec_name – название ключа (/\w+/)
sec_decription – описание ключа
sec_change_ts, sec_create_ts – время последнего обновления и создания ключа

- `GET     /secret`
  - Получить список всех доступных секретов 
  - Возвращает: sid, sec_name, sec_decription, sec_change_ts, sec_create_ts
  <!-- - Ключи: -->
    <!-- - `?archived=true` – показать архивированные тоже -->
    <!-- - `?archived=all` – показать архивированные тоже -->
    <!-- - `?archived=only` – показать только архивированные -->
- `POST    /secret` 
  - создать запись 
  - Поля: sec_name, sec_decription
  - Возвращает: sec_name, sec_decription
- `GET     /secret/{sec_name}` 
  - Получить описание конкретного секрета
  - Возвращает: sec_name, sec_decription, sec_changed, номер последней версии, дату и время последней версии, список токенов последней версии
- `PUT    /secret/{sec_name}` 
  - обновить sec_name, sec_decription
  - изменяет sec_change_ts – время последнего обновления **секрета** sec_changed
<!-- - `DELETE  /secret/{sec_name}`  -->
  <!-- - архивировать секрет (просто перестает показываться в `GET /secret`) -->
  <!-- - изменяет sec_change_ts – время последнего обновления **секрета** -->

### Secret Version
- `GET     /secret/{sec_name}/ver` 
  - получить список версий `ver_num` ключа `sec_name`
  - Поля: номер версии, дата создания версии и описание версии
- `GET     /secret/{sec_name}/ver/{ver_num}` 
  - получить версию `ver_num` ключа `sec_name`
  - Поля: номер версии, дата создания версии и описание версии и названия всех ключей
- `GET     /secret/{sec_name}/ver/{ver_num}/token/{t_name}` 
  - получить значение токена `t_name` версии `ver_num` ключа `sec_name`. 
  - Формат: `{"name": "{t_name}", "value": "..."}`
- `POST    /secret/{sec_name}/ver` 
  - Создать версию
  - Поля: ver_description и список ключей с значениями
  - Формат: `{"description": "{ver_description}", "tokens": [{"name": "...", "value": "..."}]}`
  - изменяет sec_change_ts

### Secret Access
- `GET     /secret/{sec_name}/access`
  - Получить список доступов к записи `sec_name`
  - Формат: {"owner": sub_value, "rw": [sub_value], "r": [sub_value]}
  - изменяет sec_change_ts – время последнего обновления **секрета** sec_changed
- `PUT     /secret/{sec_name}/access`
  - Обновить список доступов к записи `sec_name`
  - Формат: {"owner": sub_value, "rw": [sub_value], "r": [sub_value]}
  - изменяет sec_change_ts – время последнего обновления **секрета** sec_changed

### Security
- `POST /install`
  - Установка новой инсталляции. Ручка работает один раз
- `POST /seal`
  - Блокировка системы, может быть совершена только тем же токеном, который установил систему
- `POST /unseal`
  - Разблокировка системы, может быть совершена только тем же токеном, который установил систему. Требуется дополнительный seal-token
  - Поле: токен
- `PUT /owner`
  - Заменить владельцев
  
