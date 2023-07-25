# Getting Google's current actual IP address ranges from ak545
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

**get_google_ip_pull.py** - This is a simple python-script to get Google's current actual IP address ranges.

## Screenshots
![](https://raw.githubusercontent.com/ak545/get-google-ip-pull/main/images/script.png)
> Script in working

<details>
<summary>More</summary>

![](https://raw.githubusercontent.com/ak545/get-google-ip-pull/main/images/script2.png)
> Script in working

![](https://raw.githubusercontent.com/ak545/get-google-ip-pull/main/images/script3.png)
> Script in working

![](https://raw.githubusercontent.com/ak545/get-google-ip-pull/main/images/email.png)
> A sample of the email

![](https://raw.githubusercontent.com/ak545/get-google-ip-pull/main/images/telegram.png)
> A sample of the Telegram message

</details>

## Description
If you're here, you may be faced with the challenge of finding out Google's current actual IP address ranges.
Instructions on how to do this can be found at these links:
[How to find Google Workspace IP address ranges](https://support.google.com/a/answer/60764), 
[How to get Google IP address ranges](https://support.google.com/a/answer/10026322)
This python-script greatly simplifies and automates this work.

## Installation
The script requires **Python version 3.6 or higher**.
Of course, you need to install it yourself first [Python](https://www.python.org/). On Linux, it is usually already installed. If not, install it, for example:

```console
$ sudo yum install python3
$ sudo dnf install python3
$ sudo apt install python3
$ sudo pacman -S python
```
Additionally, you will need a Python package installer, such as **pip**. You can install it on Linux like this:
```console
$ sudo yum install python3-pip
$ sudo dnf install python3-pip
$ sudo apt install python3-pip
$ sudo pacman -S python-pip
```

For Apple macOS:
```console
$ xcode-select --install
```

Install brew:
```console
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Install Python:

```console
$ export PATH=/usr/local/bin:/usr/local/sbin:$PATH
$ brew install python
```

Note: [brew](https://brew.sh/)

For Microsoft Windows download the [distribution package](https://www.python.org/downloads/windows/) and install it. I recommend downloading "Download Windows x86 executable installer" if you have a 32-bit OS and "Download Windows x86-64 web-based installer" if you have a 64-bit OS. During installation, I recommend checking all options (Documentation, pip, tcl / tk and IDLE, Python test suit, py launcher, for all users (requeres elevation)).

Previously, you may need to update **pip** itself (Python package installer):
```console
$ python -m pip install --upgrade pip
or
> py -m pip install --upgrade pip
```

### Installing and update dependencies
```console
$ pip install -U requests
$ pip install -U dnspython
$ pip install -U colorama
```
and
```console
$ pip install -U requests[socks]
```    
or
```console
$ pip install -U PySocks
```

If you are running Linux or macOS, and you plan to run the script as the current user, then additionally specify the **--user** option. In this case, the necessary dependencies will be installed into the home folder of the current system user and are available when launched from the task scheduler (cron) on behalf of this current user.

Depending on your Python environment, your actions will be slightly different, for example, you may need to specify the **--user** key (for **pip**) or use the **python3** and **pip3** commands instead of the **python** and **pip** commands. If you use [virtual environments](https://docs.python.org/3/library/venv.html), then most likely, you will need to do all of these actions after entering the appropriate environment.

## Usage
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

### Description of options
**-h, --help**

Help

**-v, --version**

Display the version number

**-pon, --print-only-new-to-console**

Print only new Google IP addresses to console (default is False)

**-pa, --print-all-to-console**

Print all Google IP addresses to console (default is False)

**-gh, --google-host**

Check Google's actual IP address (not ranges) through hostname resolution. (default is False)

The hostname is stored in the global variable **GOOGLE_HOST** (default is www.google.com)

```python
    GOOGLE_HOST: str = os.getenv('GOOGLE_HOST', 'www.google.com')
```

This option creates *cache-ip.dat* file

**-spf, --spf-pull**

Check up-to-date spf-ranges of Google IP addresses (default is False)

This option creates *cache-cidr.dat* file

**-static, --static-pull**

Check up-to-date static-ranges of Google IP addresses (default is False)

This option creates *cache-cidr2.dat* file

**-cloud, --cloud-pull**

Check up-to-date cloud-ranges of Google IP addresses (default is False)

This option creates *cache-cidr3.dat* file

**-split, --split-long-message**

Split a long message for Telegram into many short parts (default is False)

**-trim, --trim-long-text**

Trim long cidr-text of changes for Telegram (default is False)

**-t, --use-telegram**

Send a warning message through the Telegram (default is False)

**-p URL, --proxy URL**

Proxy link, for example: socks5://127.0.0.1:9150 (default is None).

**-e EMAIL, --email-to EMAIL**

Send a warning message to email address (default is None)
Here you must specify the email address of the recipient.

**-subject STRING, --email-subject STRING**

Append custom text to the email subject (default is None). This is an additional option for --email-to.

**-ssl, --email-ssl**

Send email via SSL (default is False). This is an additional option for --email-to.

**-auth, --email-auth**

Send email via authenticated SMTP (default is False). This is an additional option for --email-to.

**-starttls, --email-starttls**

Send email via STARTTLS (default is False). This is an additional option for --email-to.

**-nb, --no-banner**

Do not print banner (default is False).
Banner is information about the script execution environment: Python version, computer name, OS name, OS release, OS version, architecture, CPU, summary table of preset options and information about the path to the external whois utility.


## Global constants in the script

Some options are inside the script. There is no point in putting them in the parameters, since you only need to configure them once, and then successfully forget about them.

You can also set the values of global constants directly via operating system environment variables of the same name so as not to change the script itself.


### Hostname
**GOOGLE_HOST**

Hostname against which the script checks for the actual Google IP address (not ranges)

Samples:

```python
    GOOGLE_HOST: str = os.getenv('GOOGLE_HOST', 'www.google.com')
    # GOOGLE_HOST: str = os.getenv('GOOGLE_HOST', 'google.com')
```

### SMTP options
**SMTP_SERVER**

SMTP server address

Samples:

```python
    SMTP_SERVER: str = os.getenv('SMTP_SERVER', 'localhost')
    # SMTP_SERVER: str = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    # SMTP_SERVER: str = os.getenv('SMTP_SERVER', 'smtp.mail.ru')
    # SMTP_SERVER: str = os.getenv('SMTP_SERVER', 'smtp.yandex.ru')
```

**SMTP_PORT**

SMTP port

Samples:

```python
    # SMTP_PORT: int = int(os.getenv('SMTP_PORT', '587'))  # For starttls
    # SMTP_PORT: int  = int(os.getenv('SMTP_PORT', '465'))  # For SSL
    SMTP_PORT: int = int(os.getenv('SMTP_PORT', '25'))   # Default
```

**SMTP_SENDER**

Email address of the sender

Samples:

```python
    SMTP_SENDER: str = os.getenv('SMTP_SENDER', 'user@gmail.com')
```

**SMTP_PASSWORD**

SMTP password

Samples:

```python
    SMTP_PASSWORD: str = os.getenv('SMTP_PASSWORD', 'P@ssw0rd')
```

### Telegram options
**TELEGRAM_TOKEN**

Token Telegram bot

Samples:

```python
    TELEGRAM_TOKEN: str = 'NNNNNNNNN:NNNSSSSaaaaaFFFFFEEE3gggggQQWFFFFF01z'
```

**TELEGRAM_CHAT_ID**

Telegram Channel ID

Samples:

```python
    TELEGRAM_CHAT_ID: str = '-NNNNNNNNN'
```

Get help with Telegram API:
[https://core.telegram.org/bots](https://core.telegram.org/bots)
You can create a bot by talking to Telegram with [**@BotFather**](https://telegram.me/BotFather)

**TELEGRAM_URL**

Telegram API URL

Samples:

```python
    TELEGRAM_URL: str = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/'
```

## How to add a script to Linux cron
To do this, create a **crontab** task that will be executed, for example, every midnight on behalf of the user (creating tasks as root is not the best idea):

Suppose your Linux username is: **user**

Your home folder: **/home/user**

The folder where this script is located: **/home/user/py**

To run the script directly, run the command:
```console
$ chmod +x /home/user/py/get_google_ip_pull.py
```

Adjust in the first line of the script [Shebang (Unix)](https://en.wikipedia.org/wiki/Shebang_(Unix)), eg:

Show the path where python is located:
```console
$ which python
```
or
```console
$ which python3
```
Correction python path in Shebang:

```python
#!/usr/bin/python
#!/usr/bin/python3
#!/usr/bin/env python
#!/usr/bin/env python3
```

Rename script:

```console
$ mv /home/user/py/get_google_ip_pull.py /home/user/py/get_google_ip_pull
```
Check script launch:

```console
$ /home/user/py/get_google_ip_pull -h
$ /home/user/py/./get_google_ip_pull -h
```
If everything is fine, run the editor **crontab**, if not, go back to setting **Shebang**:

```console
$ crontab -u user -e
```
Here **user** - is your Linux login

If you, like me, do not like vim (I have not seen a single person who is fluent in this editor, although it probably exists somewhere), you can edit the tasks in your favorite editor, for example:

```console
$ EDITOR=nano crontab -u user -e
$ EDITOR=mcedit crontab -u user -e
```
or

```console
$ VISUAL=nano crontab -u user -e
$ VISUAL=mcedit crontab -u user -e
```

In the task editor, create something like this:

`0 0 * * * /home/user/py/get_google_ip_pull -nb -pon -gh -spf -static -cloud -auth -e user@gmail.com -t -split >/dev/null 2>&1`

or

`0 0 * * * /usr/bin/python3 /home/user/py/./get_google_ip_pull.py -nb -gh -spf -static -cloud -auth -e user@gmail.com -t -split >/dev/null 2>&1`


Specify the full paths to the data file and the script.

Note: [cron](https://en.wikipedia.org/wiki/Cron)

You can view created tasks for user **user** like this:

```console
$ crontab -u user -l
```
Delete all tasks from user **user**, you can:

```console
$ crontab -u user -r
```
## How to add a script to Microsoft Windows Task Scheduler
Ask for help to [documentation](https://docs.microsoft.com/en-us/windows/desktop/taskschd/schtasks)

**Sample:**

`> schtasks /Create /SC DAILY /TN "Domain Expiration Checker" /TR "'с:\get_google_ip_pull.py' -nb -pon -gh -spf -static -cloud -auth -e user@gmail.com -t -split" /ST 23:59`

## License
[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)

Why it's like this I don't know.

## Restrictions
I, the author of this python-script, wrote this script solely for my needs. No warranty is provided. You can use this script freely, without any royalties, for any purpose.

You can make any changes to the script code and make a fork of this script, provided that you provide a link to me as a source of your inspiration.

## Postscriptum
- The script was tested in Microsoft Windows 10/11, Linux Fedora 36/37, Linux Debian 9/10/11/12, Linux Ubuntu Desktop 18.04/20.04/20.10/22.04.2/23.04, CentOS Linux 7.9/8.5, Rocky Linux 8.8/9.2, Linux Manjaro 22.1.3, Apple macOS 13.4.1 Ventura on MacBook Pro M1.


![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Fedora](https://img.shields.io/badge/Fedora-294172?style=for-the-badge&logo=fedora&logoColor=white)
![Debian](https://img.shields.io/badge/Debian-D70A53?style=for-the-badge&logo=debian&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![Cent OS](https://img.shields.io/badge/cent%20os-002260?style=for-the-badge&logo=centos&logoColor=F0F0F0)
![Rocky Linux](https://img.shields.io/badge/-Rocky%20Linux-%2310B981?style=for-the-badge&logo=rockylinux&logoColor=white)
![Manjaro](https://img.shields.io/badge/Manjaro-35BF5C?style=for-the-badge&logo=Manjaro&logoColor=white)
![macOS](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=macos&logoColor=F0F0F0)

- Sorry for my bad English. And on the other hand, which of you can boast of knowing the great and mighty Russian language? Have any of you read Pushkin, Tolstoy, Dostoyevsky, Gogol, Bulgakov in the original...? It's a joke.
- The program code of the script is not perfect. But please forgive me for that.
- Glory to the E = mc &sup2; !
- I wish you all good luck!

## A final plea
It's time to put an end to Facebook. Working there is not ethically neutral: every day that you go into work, you are doing something wrong. If you have a Facebook account, delete it. If you work at Facebook, quit.

And let us not forget that the National Security Agency must be destroyed.

*(c) [David Fifield](mailto:david@bamsoftware.com)*

---

> Best regards, ak545 ( ru.mail&copy;ak545&sup2; )