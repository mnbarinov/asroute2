# ASROUTE2 - Fetch &amp; Merge Autonomous System Networks
<img src="as_route_git.jpg" alt="ASROUTE2 - Fetch &amp; Merge Autonomous System Networks" width=100% align=center >
**asroute2** — инструмент для получения маршрутов автономных систем (AS) и их укрупнения. С его помощью вы можете извлечь маршруты из базы данных WHOIS, объединить близкие сети и фильтровать вложенные подсети для анализа или других задач.

## Возможности
- Извлечение маршрутов для указанного номера AS через `whois.radb.net`.
- Укрупнение сетей с учётом заданного допуска.
- Фильтрация вложенных подсетей.

Если вы работаете с автономными системами, asroute2 упростит вашу задачу.

---

## Установка

### 1. Загрузка репозитория
Клонируйте репозиторий:
```bash
git clone https://github.com/mnbarinov/asroute2.git
cd asroute2
#Создайте символическую ссылку, чтобы запускать asroute2 как команду:
sudo ln -s $(pwd)/asroute2.py /usr/local/bin/asroute2
```
### 2. Установка зависимостей

Для работы скрипта требуется Python 3.6+ и утилита whois. Установите их, если они не установлены:
```
# Для Debian/Ubuntu
sudo apt install whois python3
```
Для других дистрибутивов используйте менеджер пакетов своего дистрибутива.

## Использование
Основная команда
```
asroute2 <AS_NUMBER> [--tolerance <TOLERANCE>]
```
### Параметры:
```
<AS_NUMBER> — номер автономной системы (например, 15169).
--tolerance (опционально) — допустимое количество пропущенных сетей для укрупнения. Значение по умолчанию: 0.
```
### Примеры использования
Получение маршрутов для AS 15169 (Google):
```
asroute2 15169
```
#### Получение маршрутов с допуском для укрупнения:
```
asroute2 15169 --tolerance 8
```
#### Вызов справки:
```
asroute2 --help
```


## Дополнительные инструменты
Рекомендуем использовать вместе с инструментом [aslookup](https://github.com/mnbarinov/as-number-lookup-by-ip), который позволяет находить номер автономной системы на основе IP-адреса.

## Автор
Разработано [Михаилом Бариновым](https://github.com/mnbarinov).
## 
<img src="asroute2.svg" alt="ASROUTE2 - Fetch &amp; Merge Autonomous System Networks" width=300 align=center >
