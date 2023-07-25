# Getting Google's current actual IP address ranges from ak545
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

**get_google_ip_pull.py** - Это простой python-скрипт для получения текущих фактических диапазонов IP-адресов Google.

## Скриншоты
![](https://github.com/ak545/get-google-ip-pull/raw/master/images/script.png)
> Скрипт в работе

<details>
<summary>Ещё больше</summary>

![](https://github.com/ak545/get-google-ip-pull/raw/master/images/script2.png)
> Скрипт в работе

![](https://github.com/ak545/get-google-ip-pull/raw/master/images/script3.png)
> Скрипт в работе

![](https://github.com/ak545/get-google-ip-pull/raw/master/images/email.png)
> Пример email

![](https://github.com/ak545/get-google-ip-pull/raw/master/images/telegram.png)
> Пример Telegram сообщения

</details>



## Описание
Если вы находитесь здесь, то возможно перед Вами возникла задача узнать текущие фактические диапазоны IP-адресов Google. 
Инструкции о том, как это сделать можно найти по этим ссылкам:
[Как узнать диапазоны IP-адресов Google Workspace](https://support.google.com/a/answer/60764), 
[Как получить диапазоны IP-адресов Google](https://support.google.com/a/answer/10026322)
Данный python-скрипт значительно упрощает и автоматизирует эту работу.

## Инсталляция
Для работы скрипта необходим **Python версии 3.6 или выше**.
Разумеется, необходимо сперва установить сам [Python](https://www.python.org/). В Linux он обычно уже установлен. Если нет, установите его, например:

```console
$ sudo yum install python3
$ sudo dnf install python3
$ sudo apt install python3
$ sudo pacman -S python
```
Дополнительно вам потребуется Python package installer (установщик модулей Python), например **pip**. Установить в Linux его можно так:
```console
$ sudo yum install python3-pip
$ sudo dnf install python3-pip
$ sudo apt install python3-pip
$ sudo pacman -S python-pip
```

Для Apple macOS:
    
```console
$ xcode-select --install
```

Установите brew:

```console
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Установите Python:

```console
$ export PATH=/usr/local/bin:/usr/local/sbin:$PATH
$ brew install python
```

Примечание: [brew](https://brew.sh/index_ru)

Для Microsoft Windows скачайте [дистрибутив](https://www.python.org/downloads/windows/) и установите его. Я рекомендую скачивать "Download Windows x86 executable installer" если у вас 32-х битная ОС и "Download Windows x86-64 web-based installer" если у вас 64-х битная ОС. Во время установки рекомендую отметить все опции (Documentation, pip, tcl/tk and IDLE, Python test suit, py launcher, for all users (requeres elevation)).

Предварительно, возможно понадобится обновить сам **pip** (установщик модулей Python):

```console
$ python -m pip install --upgrade pip
или
> py -m pip install --upgrade pip
```

### Установка и обновление зависимостей
```console
$ pip install -U requests
$ pip install -U dnspython
$ pip install -U colorama
```
и
```console
$ pip install -U requests[socks]
```
или
```console
$ pip install -U PySocks
```
Если Вы работаете под управлением Linux или macOS, и запуск скрипта планируете производить от имени текущего пользователя, то дополнительно указывайте опцию **--user**. В этом случае необходимые зависимости будут устанавливаться в домашнюю папку текущего пользователя системы и доступны при запуске из планировщика задач (cron) от имени этого текущего пользователя.

В зависимости от вашего Python окружения, ваши действия будут немного иными, например, возможно, вам потребуется указать ключ **--user** (для **pip**) или вместо команд **python** и **pip** использовать команды **python3** и **pip3**. Если вы используете [виртуальные окружения](https://docs.python.org/3/library/venv.html), то скорее всего, все эти действия вам необходимо будет сделать после входа в соответствующее окружение.

## Использование
```console
$ get_google_ip_pull.py -h
usage:  get_google_ip_pull.py [Options]

        This is a simple python-script to get Google's current actual IP address ranges.

        Getting Google's current actual IP address ranges.

Options:
  -h, --help            Help
  -v, --version         Display the version number
  -pon, --print-only-new-to-console
                        Print only new Google IP addresses to console (default is False)
  -pa, --print-all-to-console
                        Print all Google IP addresses to console (default is False)
  -gh, --google-host
                        Check Google's actual IP address (not ranges) through hostname resolution. (default is False)
  -spf, --spf-pull      Check up-to-date spf-ranges of Google IP addresses (default is False)
  -static, --static-pull
                        Check up-to-date static-ranges of Google IP addresses (default is False)
  -cloud, --cloud-pull  Check up-to-date cloud-ranges of Google IP addresses (default is False)
  -split, --split-long-message
                        Split a long message for Telegram into many short parts (default is False)
  -trim, --trim-long-text
                        Trim long cidr-text of changes for Telegram (default is False)
  -t, --use-telegram    Send a warning message through the Telegram (default is False)
  -p URL, --proxy URL   Proxy link, for example: socks5://127.0.0.1:9150 (default is None)
  -e EMAIL, --email-to EMAIL
                        Send a warning message to email address (default is None)
  -subject STRING, --email-subject STRING
                        Append custom text to the email subject (default is None)
  -ssl, --email-ssl     Send email via SSL (default is False)
  -auth, --email-auth   Send email via authenticated SMTP (default is False)
  -starttls, --email-starttls
                        Send email via STARTTLS (default is False)
  -nb, --no-banner      Do not print banner (default is False)

© AK545 (Andrey Klimov) 2022..2023, e-mail: ak545 at mail dot ru
```

### Описание опций
**-h, --help**

Помощь

**-v, --version**
    
Показать номер версии

**-pon, --print-only-new-to-console**

Выводить на консоль только новые IP-адреса Google (по умолчанию Нет)

**-pa, --print-all-to-console**

Вывести все IP-адреса Google на консоль (по умолчанию Нет)

**-gh, --google-host**

Проверять фактический IP-адрес Google (не диапазоны) с помощью разрешения имени хоста (по умолчанию Нет)

Имя хоста хранится в глобальной переменной **GOOGLE_HOST** (по умолчанию www.google.com)

```python
    GOOGLE_HOST: str = os.getenv('GOOGLE_HOST', 'www.google.com')
```

При этой опции создаётся файл *cache-ip.dat*

**-spf, --spf-pull**

Проверять актуальные spf-диапазоны IP-адресов Google (по умолчанию Нет)

При этой опции создаётся файл *cache-cidr.dat*


**-static, --static-pull**

Проверять актуальные static-диапазоны IP-адресов Google (по умолчанию Нет)

При этой опции создаётся файл *cache-cidr2.dat*

**-cloud, --cloud-pull**

Проверять актуальные cloud-диапазоны IP-адресов Google (по умолчанию Нет)

При этой опции создаётся файл *cache-cidr3.dat*

**-split, --split-long-message**

Разбить длинное сообщение для Telegram на множество коротких частей (по умолчанию Нет)

**-trim, --trim-long-text**

Обрезать длинный cidr-текст изменений для Telegram (по умолчанию Нет)

**-t, --use-telegram**

Отправить предупреждающее сообщение через Telegram (по умолчанию False)

**-p URL, --proxy URL**

Ссылка на прокси, например: socks5://127.0.0.1:9150 (по умолчанию None).

**-e EMAIL, --email-to EMAIL**

Отправить предупреждение на адрес электронной почты (по умолчанию Нет). Здесь необходимо указать email адрес получателя.

**-subject STRING, --email-subject STRING**

Добавить свой текст в тему email-письма (по умолчанию Нет). Это дополнительная опция для --email-to.

**-ssl, --email-ssl**

Отправить email-письмо по протоколу SSL (по умолчанию False). Это дополнительная опция для --email-to.

**-auth, --email-auth**

Отправлять email-письмо через SMTP с авторизацией (по умолчанию False). Это дополнительная опция для --email-to.

**-starttls, --email-starttls**

Отправить email-письмо по протоколу STARTTLS (по умолчанию False). Это дополнительная опция для --email-to.

**-nb, --no-banner**

Не печатать баннер (по умолчанию False).
Баннер, это информация о среде исполнения скрипта: версия Python, имя компьютера, имя ОС, релиз ОС, версия ОС, архитектура, ЦПУ, сводная таблица предустановленных опций и информация о пути к внешней утилите whois.


## Глобальные константы в скрипте
Часть опций находится внутри скрипта. Нет никакого смысла выносить их в параметры, так как настроить их требуется всего один раз, после чего успешно о них забыть. 

Вы также можете установить значения глобальных констат непосредственно через переменные среды операционной системы с тем же именем, чтобы не изменять сам скрипт.


### Имя хоста
**GOOGLE_HOST**

Имя хоста, по которому скрипт проверяет фактический IP-адрес Google (не диапазоны)

Примеры:

```python
    GOOGLE_HOST: str = os.getenv('GOOGLE_HOST', 'www.google.com')
    # GOOGLE_HOST: str = os.getenv('GOOGLE_HOST', 'google.com')
```

### Параметры SMTP
**SMTP_SERVER**

адрес SMTP сервера

Примеры:

```python
    SMTP_SERVER: str = os.getenv('SMTP_SERVER', 'localhost')
    # SMTP_SERVER: str = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    # SMTP_SERVER: str = os.getenv('SMTP_SERVER', 'smtp.mail.ru')
    # SMTP_SERVER: str = os.getenv('SMTP_SERVER', 'smtp.yandex.ru')
```

**SMTP_PORT**

SMTP порт

Примеры:
    
```python
    # SMTP_PORT: int = int(os.getenv('SMTP_PORT', '587'))  # Для starttls
    # SMTP_PORT: int = int(os.getenv('SMTP_PORT', '465'))  # Для SSL
    SMTP_PORT: int =  int(os.getenv("SMTP_PORT", "25"))   # По умолчанию
```

**SMTP_SENDER**

Email адрес отправителя

Примеры:

```python
    SMTP_SENDER: str =  os.getenv('SMTP_SENDER', 'user@gmail.com')
```

**SMTP_PASSWORD**

SMTP пароль

Примеры:

```python
    SMTP_PASSWORD: str =  os.getenv('SMTP_PASSWORD', 'P@ssw0rd')
```

### Параметры Telegram
**TELEGRAM_TOKEN**

Токен Telegram бота

Примеры:

```python
    TELEGRAM_TOKEN: str = 'NNNNNNNNN:NNNSSSSaaaaaFFFFFEEE3gggggQQWFFFFF01z'
```

**TELEGRAM_CHAT_ID**

Идентификатор канала Telegram

Примеры :

```python
    TELEGRAM_CHAT_ID: str = '-NNNNNNNNN'
```

Получить помощь по API Telegram: 
[https://core.telegram.org/bots](https://core.telegram.org/bots)
Создать бота можно пообщавшись в Telegram с [**@BotFather**](https://telegram.me/BotFather)

**TELEGRAM_URL**

Telegram API URL

Примеры:

```python
    TELEGRAM_URL: str = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/'
```


## Как добавить скрипт в Linux cron
Для этого создайте **crontab** задачу, которая будет выполняться, например, каждую полночь от имени пользователя (создавать задачи от имени root не лучшая идея):

Предположим, ваш логин в Linux: **user**

Ваша домашняя папка: **/home/user**

Папка, где находится этот скрипт: **/home/user/py**

Чтобы запускать скрипт напрямую, выполните команду:
    
```console
$ chmod +x /home/user/py/get_google_ip_pull.py
```

Скорректируйте в первой строке скрипта [Шебанг (Unix)](https://ru.wikipedia.org/wiki/%D0%A8%D0%B5%D0%B1%D0%B0%D0%BD%D0%B3_(Unix)), например:

Показать путь, где расположен python:
    
```console
$ which python
```
или
```console
$ which python3
```
    
Коррекция пути python в Шебанг:

```python
#!/usr/bin/python
#!/usr/bin/python3
#!/usr/bin/env python
#!/usr/bin/env python3
```

Переименуйте скрипт:

```console
$ mv /home/user/py/get_google_ip_pull.py /home/user/py/get_google_ip_pull
```

Проверьте запуск скрипта:

```console
$ /home/user/py/get_google_ip_pull -h
$ /home/user/py/./get_google_ip_pull -h
```

Если всё нормально, запустите редактор **crontab**, если нет, вернитесь к настройке **Шебанг**:

```console
$ crontab -u user -e
```
Здесь **user** - это ваш логин в Linux


Если вы, как и я не любите vim (я не видел ни одного человека, в совершенстве владеющего этим редактором, хотя, наверное, он где-то есть), вы можете редактировать задачи в вашем любимом редакторе, например, так:

```console
$ EDITOR=nano crontab -u user -e
$ EDITOR=mcedit crontab -u user -e
```
или
```console
$ VISUAL=nano crontab -u user -e
$ VISUAL=mcedit crontab -u user -e
```

В файле задач создайте примерно такую запись:

`0 0 * * * /home/user/py/get_google_ip_pull -nb -pon -gh -spf -static -cloud -auth -e user@gmail.com -t -split >/dev/null 2>&1`

или

`0 0 * * * /usr/bin/python3 /home/user/py/./get_google_ip_pull.py -nb -gh -spf -static -cloud -auth -e user@gmail.com -t -split >/dev/null 2>&1`

Указывайте полные пути к файлу данных и скрипту.

Примечание: [cron](https://ru.wikipedia.org/wiki/Cron)

Посмотреть созданные задачи для пользователя **user** можно так:

```console
$ crontab -u user -l
```

Удалить все задачи пользователя **user** можно так:

```console
$ crontab -u user -r
```


## Как добавить скрипт в Планировщик заданий Microsoft Windows
Обратитесь за помощью к [документации](https://docs.microsoft.com/en-us/windows/desktop/taskschd/schtasks)

**Пример:**

`> schtasks /Create /SC DAILY /TN "Domain Expiration Checker" /TR "'с:\get_google_ip_pull.py' -nb -pon -gh -spf -static -cloud -auth -e user@gmail.com -t -split" /ST 23:59`

## Лицензия
[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)

Почему именно такая я и сам не знаю.

## Ограничения
Я, автор этого python-скрипта, написал этот скрипт исключительно для своих нужд. Никаких гарантий не предоставляется. Вы можете использовать этот скрипт свободно, без каких либо отчислений, в любых целях.

Вы можете вносить любые правки в код скрипта и делать форк этого скрипта при условии указания ссылки на меня, как источника вашего вдохновения.

## Постскриптум
- Работа скрипта проверялась в Microsoft Windows 10/11, Linux Fedora 36/37, Linux Debian 9/10/11/12, Linux Ubuntu Desktop 18.04/20.04/20.10/22.04.2/23.04, CentOS Linux 7.9/8.5, Rocky Linux 8.8/9.2, Linux Manjaro 22.1.3, Apple macOS 13.4.1 Ventura на MacBook Pro M1.

![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Fedora](https://img.shields.io/badge/Fedora-294172?style=for-the-badge&logo=fedora&logoColor=white)
![Debian](https://img.shields.io/badge/Debian-D70A53?style=for-the-badge&logo=debian&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![Cent OS](https://img.shields.io/badge/cent%20os-002260?style=for-the-badge&logo=centos&logoColor=F0F0F0)
![Rocky Linux](https://img.shields.io/badge/-Rocky%20Linux-%2310B981?style=for-the-badge&logo=rockylinux&logoColor=white)
![Manjaro](https://img.shields.io/badge/Manjaro-35BF5C?style=for-the-badge&logo=Manjaro&logoColor=white)
![macOS](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=macos&logoColor=F0F0F0)

- Программный код скррипта не идеален. Но прошу простить меня за это.
- Да здравствует E = mc&sup2; !
- Желаю всем удачи!

## Последняя просьба
Пришло время положить конец Facebook. Работа там не является нейтральной с этической точки зрения: каждый день, когда вы идете туда на работу, вы делаете что-то не так. Если у вас есть учетная запись Facebook, удалите ее. Если ты работаешь в Facebook, увольняйся.

И давайте не будем забывать, что Агентство национальной безопасности должно быть уничтожено.

*(c) [David Fifield](mailto:david@bamsoftware.com)*

---

> Best regards, ak545 ( ru.mail&copy;ak545&sup2; )

