#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Program: Getting up-to-date Google IP address ranges from ak545
#
# Author of this fork: Andrey Klimov < ak545 at mail dot ru >
# https://github.com/ak545
#
# Current Version: 0.1.2
# Creation Date: 2022-12-28
# Date of last changes: 2023-07-25
#
# License:
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.

from __future__ import unicode_literals
from typing import List, Dict, Tuple, Optional, Any

import os
import sys
import platform
import json
import argparse
import time
from datetime import datetime
import smtplib
import socket
import ipaddress
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from collections import OrderedDict

try:
    import requests
except ImportError:
    sys.exit(
        """You need requests!
                install it from http://pypi.python.org/pypi/requests
                or run pip install requests"""
    )

try:
    from dns import resolver
except ImportError:
    sys.exit(
        """You need dnspython!
                install it from http://pypi.python.org/pypi/dnspython
                or run pip install dnspython"""
    )

try:
    from colorama import init
    from colorama import Fore, Back, Style
except ImportError:
    sys.exit(
        """You need colorama!
                install it from http://pypi.python.org/pypi/colorama
                or run pip install colorama"""
    )

# Init colorama
init(autoreset=True)

# Global constants
__version__ = "0.1.2"

# Check Python Version
if sys.version_info < (3, 6):
    print("Error. Python version 3.6 or later required to run this script")
    print("Your version:", sys.version)
    sys.exit(-1)

FR = Fore.RESET

FW = Fore.WHITE
FG = Fore.GREEN
FRC = Fore.RED
FC = Fore.CYAN
FY = Fore.YELLOW
FM = Fore.MAGENTA
FB = Fore.BLUE
FBC = Fore.BLACK

FLW = Fore.LIGHTWHITE_EX
FLG = Fore.LIGHTGREEN_EX
FLR = Fore.LIGHTRED_EX
FLC = Fore.LIGHTCYAN_EX
FLY = Fore.LIGHTYELLOW_EX
FLM = Fore.LIGHTMAGENTA_EX
FLB = Fore.LIGHTBLUE_EX
FLBC = Fore.LIGHTBLACK_EX

BLB = Back.LIGHTBLACK_EX
BLR = Back.LIGHTRED_EX
BRC = Back.RED
BG = Back.GREEN
BLG = Back.LIGHTGREEN_EX
BLC = Back.LIGHTCYAN_EX
BC = Back.CYAN
BLY = Back.LIGHTYELLOW_EX
BY = Back.YELLOW
BLW = Back.LIGHTWHITE_EX
BW = Back.WHITE
BR = Back.RESET

SDIM = Style.DIM
SNORMAL = Style.NORMAL
SBRIGHT = Style.BRIGHT
SR = Style.RESET_ALL

SEP: str = os.sep
pathname: str = os.path.dirname(os.path.abspath(__file__))

# SMTP options
SMTP_SERVER: str = os.getenv('SMTP_SERVER', 'localhost')
SMTP_PORT: int = int(os.getenv('SMTP_PORT', '25'))

# SMTP_SERVER: str = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
# SMTP_PORT: int = int(os.getenv('SMTP_PORT', '587'))  # For starttls

# SMTP_SERVER: str = os.getenv('SMTP_SERVER', 'smtp.mail.ru')
# SMTP_PORT: int = int(os.getenv('SMTP_PORT', '25'))  # Default

# SMTP_SERVER: str = os.getenv('SMTP_SERVER', 'smtp.yandex.ru')
# SMTP_PORT: int = int(os.getenv('SMTP_PORT', '465'))  # For SSL

SMTP_SENDER: str = os.getenv('SMTP_SENDER', 'root')
SMTP_PASSWORD: str = os.getenv('SMTP_PASSWORD', 'P@ssw0rd')

# Telegram bot options
# Proxy for telegram
TELEGRAM_PROXIES: Dict = {}
# TELEGRAM_PROXIES: Dict = {
#     'http': 'socks5://127.0.0.1:9150',
#     'https': 'socks5://127.0.0.1:9150',
# }

# # Get help from https://core.telegram.org/bots
# # token that can be generated talking with @BotFather on telegram
TELEGRAM_TOKEN: str = '<INSERT YOUR TOKEN>'
#
# # channel id for telegram
TELEGRAM_CHAT_ID: str = '<INSERT YOUR CHANNEL ID>'
#
# # url for post request to api.telegram.org
TELEGRAM_URL: str = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/'

if str(os.getenv('SMTP_CHECK_SSL_HOSTNAME')) == '0':
    SMTP_CHECK_SSL_HOSTNAME: bool = False
else:
    SMTP_CHECK_SSL_HOSTNAME: bool = True

# Command line parameters
CLI: Optional[Any] = None

CACHE_IP = []
CACHE_CIDR = []
CACHE_CIDR2 = []
CACHE_CIDR3 = []

NEW_IP = []
NEW_IP_IN_NETWORK: str = ''
NEW_CIDR = []
NEW_CIDR2 = []
NEW_CIDR3 = []

CACHE_IP_FILE: str = f'{pathname}{SEP}cache-ip.dat'
CACHE_CIDR_FILE: str = f'{pathname}{SEP}cache-cidr.dat'
CACHE_CIDR2_FILE: str = f'{pathname}{SEP}cache-cidr2.dat'
CACHE_CIDR3_FILE: str = f'{pathname}{SEP}cache-cidr3.dat'

GOOGLE_HOST: str = os.getenv('GOOGLE_HOST', 'www.google.com')
# GOOGLE_HOST: str = os.getenv('GOOGLE_HOST', 'google.com')

REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/98.0.4758.54 Safari/537.36',
}


def is_ip_valid(ip_addr: str) -> bool:
    """
    Checking if the IP address is correct
    :param ip_addr: str
    :return: bool
    """
    try:
        if ip_addr.lower() == 'localhost':
            ip_addr = '127.0.0.1'

        if '/32' in ip_addr:
            ip_addr = ip_addr.replace('/32', '')

        _ = ipaddress.ip_address(ip_addr)
        return True
    except ValueError:
        return False


def is_ip_in_network(ip: str, ip_network: str) -> bool:
    """
    Checking IP for belonging to a network range
    :param ip: str
    :param ip_network: str
    :return: bool
    """
    is_in_ip_network = False
    if not is_ip_valid(ip):
        print(f'{FLR}{ip}{FRC} is not valid IP address')
        sys.exit(-1)

    if '/' not in ip_network:
        if not is_ip_valid(ip_network):
            print(f'{FLR}{ip_network}{FRC} is not valid IP address')
            sys.exit(-1)

    try:
        obj = ipaddress.ip_network(ip_network, strict=True)
    except (ipaddress.AddressValueError, ipaddress.NetmaskValueError):
        print(f'{FLR}{ip_network}{FRC} is not valid IP net mask')
        sys.exit(-1)

    if ipaddress.ip_address(obj.hostmask) == ipaddress.ip_address('0.0.0.0'):
        # ip_network is not network mask
        if is_ip_valid(ip_network):
            is_in_ip_network = ip == ip_network
        else:
            print(f'{FLR}{ip_network}{FRC} is not valid IP address')
            sys.exit(-1)
    else:
        # ip_network is network mask
        if ipaddress.ip_address(ip) in ipaddress.ip_network(ip_network):
            is_in_ip_network = True

    return is_in_ip_network


def make_report_for_telegram() -> None:
    """
    Make report for send through the Telegram bot.
    :return: None
    """
    if (
            (len(NEW_IP) == 0 or NEW_IP_IN_NETWORK != '') and
            len(NEW_CIDR) == 0 and
            len(NEW_CIDR2) == 0 and
            len(NEW_CIDR3) == 0
    ):
        return

    today: str = f'{datetime.now():%d.%m.%Y %H:%M}'
    hl: str = f'{"-" * 42}'
    message: str = ''
    message += f'<b>Current Google IP ranges  [ {today} ]</b>\n'
    message += f'<pre>{hl}</pre>\n'

    if len(NEW_IP) > 0 and NEW_IP_IN_NETWORK == '':
        # New IPs discovered
        message += '<b>New IPs</b><pre>'
        message += f'{hl}\n'

        txt: str = ''
        for ip in NEW_IP:
            txt += f'{ip}\n'

        if CLI.trim_long_text:
            if len(txt) > 350:
                txt = f'{txt[:350]}...\n\n'
            else:
                txt = f'{txt}\n\n'
        else:
            txt = f'{txt}\n\n'

        message += txt
        message += '</pre>'

    if len(NEW_CIDR) > 0:
        # New spf CIDRs discovered
        message += '<b>New spf CIDRs</b><pre>'
        message += f'{hl}\n'

        txt: str = ''
        for cidr in NEW_CIDR:
            txt += f'{cidr}\n'

        if CLI.trim_long_text:
            if len(txt) > 350:
                txt = f'{txt[:350]}...\n\n'
            else:
                txt = f'{txt}\n\n'
        else:
            txt = f'{txt}\n\n'

        message += txt
        message += '</pre>'

    if len(NEW_CIDR2) > 0:
        # New static CIDRs discovered
        message += '<b>New static CIDRs</b><pre>'
        message += f'{hl}\n'

        txt: str = ''
        for cidr in NEW_CIDR2:
            txt += f'{cidr}\n'

        if CLI.trim_long_text:
            if len(txt) > 350:
                txt = f'{txt[:350]}...\n\n'
            else:
                txt = f'{txt}\n\n'
        else:
            txt = f'{txt}\n\n'

        message += txt
        message += '</pre>'

    if len(NEW_CIDR3) > 0:
        # New cloud CIDRs discovered
        message += '<b>New cloud CIDRs</b><pre>'
        message += f'{hl}\n'

        txt: str = ''
        for cidr in NEW_CIDR3:
            txt += f'{cidr}\n'

        if CLI.trim_long_text:
            if len(txt) > 350:
                txt = f'{txt[:350]}...\n\n'
            else:
                txt = f'{txt}\n\n'
        else:
            txt = f'{txt}\n\n'

        message += txt
        message += '</pre>'

    if len(message) <= 3800:  # 4086
        send_telegram(message)
    else:
        if not CLI.split_long_message:
            message = message[:3700]
            if not message.endswith('</pre>'):
                message += '</pre>'

            tmp_txt = ''
            if not CLI.trim_long_text:
                tmp_txt = (
                    '<b>-trim</b>'
                    ' and/or '
                )
            message += (
                f'\n...\n'
                f'Message is too long!\n'
                f'Use '
                f'{tmp_txt}'
                f'<b>-split</b>'
                f' option'
            )
            if not CLI.trim_long_text:
                message += 's'
            if CLI.email_to:
                message += ' or see full report in email'
            message += '\n'
            send_telegram(message)
        else:
            ii: int = 0
            iii: int = 0
            while True:
                ii += 1
                if ii == 1:
                    message_parts = message[:3800]
                else:
                    message_parts = f'# {ii}\n<pre>'
                    message_parts += message[:3800]

                message_parts = message_parts.rstrip('\n')
                if not message_parts.endswith('</pre>'):
                    message_parts += '</pre>'

                message = message[3800:]

                send_telegram(message_parts)

                if len(message) == 0:
                    break

                # For Telegram limits
                iii += 1
                if iii == 20:
                    iii = 0
                    time.sleep(40)
                else:
                    time.sleep(2)


def send_telegram(message: str) -> None:
    """
    Sending a message through the Telegram bot.
    :param message: str
    :return: None
    """
    params: Dict = {'chat_id': TELEGRAM_CHAT_ID, 'parse_mode': 'html', 'text': message}
    if len(TELEGRAM_PROXIES) > 0:
        response: Optional[Any] = requests.post(
            TELEGRAM_URL + 'sendMessage',
            timeout=10,
            data=params,
            proxies=TELEGRAM_PROXIES,
            headers=REQUEST_HEADERS,
            verify=True,
        )
    else:
        response: Optional[Any] = requests.post(
            TELEGRAM_URL + 'sendMessage',
            timeout=10,
            data=params,
            headers=REQUEST_HEADERS,
            verify=True,
        )

    if response is not None:
        if response.status_code != 200:
            print(f'{FLR}{response.text}')


def make_report_for_email() -> None:
    """
    Make report for send through the email.
    :return: None
    """
    if (
            (len(NEW_IP) == 0 or NEW_IP_IN_NETWORK != '') and
            len(NEW_CIDR) == 0 and
            len(NEW_CIDR2) == 0 and
            len(NEW_CIDR3) == 0
    ):
        return

    email_to_list: List = []
    if ',' in CLI.email_to:
        tmp_list: List = CLI.email_to.split(',')
        for email in tmp_list:
            s_email: str = email.strip()
            if s_email != '':
                email_to_list.append(s_email)
    else:
        email_to_list = [CLI.email_to]

    for email_to in email_to_list:
        today: str = f'{datetime.now():%d.%m.%Y %H:%M}'
        msg = MIMEMultipart('alternative')
        msg['From'] = SMTP_SENDER
        msg['To'] = email_to
        subject: str = f'Current Google IP ranges  [ {today} ]'
        if CLI.email_subject:
            subject = subject + ': ' + CLI.email_subject
        msg['Subject'] = subject

        body_text: str = '%BODY%'
        body_html: str = """
        <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        </head>
        <html>

          <body marginwidth="0" marginheight="0" leftmargin="0" topmargin="0" 
          style="background-color:#333333;  
          font-family:Arial,serif; 
          margin:0; 
          padding:0; 
          min-width: 100%; 
          -webkit-text-size-adjust:none; 
          -ms-text-size-adjust:none;">

            <div style="width: auto; 
            color:#fff; 
            border-color: rgb(168, 3, 51) !important; 
            background-color: rgba(199, 0, 57,0.81); 
            margin: 50px; 
            padding: 50px; 
            display: inline-block;">
            %BODY%
            </div>

          </body>

        </html>
        """

        hl: str = f'{"-" * 42}'

        # For part plain
        cidr_list_txt: str = f'\n{subject}\n{hl}\n'

        if len(NEW_IP) > 0 and NEW_IP_IN_NETWORK == '':
            # New IPs
            cidr_list_txt += '\nNew IPs\n\n'
            cidr_list_txt += f'{hl}\n'
            for ip in NEW_IP:
                cidr_list_txt += f'{ip}\n'

        if len(NEW_CIDR) > 0:
            # New spf CIDRs
            cidr_list_txt += '\nNew spf CIDRs\n\n'
            cidr_list_txt += f'{hl}\n'
            for cidr in NEW_CIDR:
                cidr_list_txt += f'{cidr}\n'

        if len(NEW_CIDR2) > 0:
            # New static SIDRs
            cidr_list_txt += '\nNew static CIDRs\n\n'
            cidr_list_txt += f'{hl}\n'
            for cidr in NEW_CIDR2:
                cidr_list_txt += f'{cidr}\n'

        if len(NEW_CIDR3) > 0:
            # New cloud CIDRs
            cidr_list_txt += '\nNew cloud CIDRs\n\n'
            cidr_list_txt += f'{hl}\n'
            for cidr in NEW_CIDR3:
                cidr_list_txt += f'{cidr}\n'

        body_text = body_text.replace('%BODY%', cidr_list_txt)

        # For part html
        cidr_list_txt: str = f'<b>{subject}</b><br>\n<pre>{hl}</pre>\n'

        if len(NEW_IP) > 0 and NEW_IP_IN_NETWORK == '':
            # New IPs
            cidr_list_txt += '<br><b>New IPs</b><br>\n<pre>\n'
            cidr_list_txt += f'{hl}\n'
            for ip in NEW_IP:
                cidr_list_txt += f'{ip}\n'
            cidr_list_txt += '</pre>'

        if len(NEW_CIDR) > 0:
            # New spf CIDRs
            cidr_list_txt += '<br><b>New spf CIDRs</b><br>\n<pre>\n'
            cidr_list_txt += f'{hl}\n'
            for cidr in NEW_CIDR:
                cidr_list_txt += f'{cidr}\n'
            cidr_list_txt += '</pre>'

        if len(NEW_CIDR2) > 0:
            # New static CIDRs
            cidr_list_txt += '<br><b>New static CIDRs</b><br>\n<pre>\n'
            cidr_list_txt += f'{hl}\n'
            for cidr in NEW_CIDR2:
                cidr_list_txt += f'{cidr}\n'
            cidr_list_txt += '</pre>'

        if len(NEW_CIDR3) > 0:
            # New cloud CIDRs
            cidr_list_txt += '<br><b>New cloud CIDRs</b><br>\n<pre>\n'
            cidr_list_txt += f'{hl}\n'
            for cidr in NEW_CIDR3:
                cidr_list_txt += f'{cidr}\n'
            cidr_list_txt += '</pre>'

        body_html = body_html.replace('%BODY%', cidr_list_txt)

        part_plain = MIMEText(body_text, 'plain')
        part_html = MIMEText(body_html, 'html')

        msg.attach(part_plain)
        msg.attach(part_html)

        message = msg.as_string()

        send_email(email_to, message)


def send_email(email_to: str, message: str) -> None:
    """
    Sending a email to the recipient
    :param email_to: str
    :param message: str
    :return: None
    """
    server = None
    context = None
    # Try to log in to server and send email
    try:
        if CLI.email_ssl or CLI.email_starttls:
            # Create a secure SSL context
            context = ssl.create_default_context()
            context.check_hostname = SMTP_CHECK_SSL_HOSTNAME
            if CLI.email_ssl:
                server = smtplib.SMTP_SSL(
                    host=SMTP_SERVER,
                    port=SMTP_PORT,
                    context=context
                )
            context.verify_mode = ssl.CERT_REQUIRED

        if server is None:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

        if CLI.email_starttls:
            server.starttls(context=context)  # Secure the connection

        server.ehlo()  # Can be omitted
        if CLI.email_auth:
            server.login(SMTP_SENDER, SMTP_PASSWORD)
        server.sendmail(SMTP_SENDER, email_to, message)
    except Exception as e:
        # Print any error messages to stdout
        print(f'{FLR}{e}')
    finally:
        server.quit()


class MyParser(argparse.ArgumentParser):
    """
    Redefining the argparse.ArgumentParser class to catch
    parameter setting errors in the command line interface (CLI)
    """
    def error(self, message):
        """
        Overridden error handler
        :param message: str
        :return: None
        """
        sys.stderr.write(f'{FLR}error: {FRC}{message}\n\n')
        self.print_help()
        sys.exit(2)


def process_cli():
    """
    parses the CLI arguments and returns a domain or
        a file with a list of domains etc.
    :return: dict
    """
    process_parser = MyParser(
        formatter_class=argparse.RawTextHelpFormatter,
        conflict_handler='resolve',
        description=f"\t{FC}Getting Google's current actual IP address ranges.{FR}",
        usage=f"""\t{FLB}%(prog)s{FR} [Options]

    \t{FLBC}This is a simple python-script to get Google's current actual IP address ranges.{FR}""",
        epilog=f'{FLBC}© AK545 (Andrey Klimov) 2022..2023, e-mail: ak545 at mail dot ru\n{FR}',
        add_help=False,
    )
    parent_group = process_parser.add_argument_group(
        title='Options'
    )
    parent_group.add_argument(
        '-h',
        '--help',
        action='help',
        help='Help'
    )
    parent_group.add_argument(
        '-v',
        '--version',
        action='version',
        help='Display the version number',
        version=f'{FLC}%(prog)s{FR} version: {FLY}{__version__}{FR}'
    )
    parent_group.add_argument(
        '-pon',
        '--print-only-new-to-console',
        action='store_true',
        default=False,
        help='Print only new Google IP addresses to console (default is False)'
    )
    parent_group.add_argument(
        '-pa',
        '--print-all-to-console',
        action='store_true',
        default=False,
        help='Print all Google IP addresses to console (default is False)'
    )
    parent_group.add_argument(
        '-gh',
        '--google-host',
        action='store_true',
        default=False,
        help="Check Google's actual IP address (not ranges) through hostname resolution. (default is False)"
    )
    parent_group.add_argument(
        '-spf',
        '--spf-pull',
        action='store_true',
        default=False,
        help='Check up-to-date spf-ranges of Google IP addresses (default is False)'
    )
    parent_group.add_argument(
        '-static',
        '--static-pull',
        action='store_true',
        default=False,
        help='Check up-to-date static-ranges of Google IP addresses (default is False)'
    )
    parent_group.add_argument(
        '-cloud',
        '--cloud-pull',
        action='store_true',
        default=False,
        help='Check up-to-date cloud-ranges of Google IP addresses (default is False)'
    )
    parent_group.add_argument(
        '-split',
        '--split-long-message',
        action='store_true',
        default=False,
        help='Split a long message for Telegram into many short parts (default is False)'
    )
    parent_group.add_argument(
        '-trim',
        '--trim-long-text',
        action='store_true',
        default=False,
        help='Trim long cidr-text of changes for Telegram (default is False)'
    )
    parent_group.add_argument(
        '-t',
        '--use-telegram',
        action='store_true',
        default=False,
        help='Send a warning message through the Telegram (default is False)'
    )
    parent_group.add_argument(
        '-p',
        '--proxy',
        help=(
            'Proxy link, '
            'for example: socks5://127.0.0.1:9150 (default is None)'
        ),
        metavar='URL'
    )
    parent_group.add_argument(
        '-e',
        '--email-to',
        help='Send a warning message to email address (default is None)',
        metavar='EMAIL'
    )
    parent_group.add_argument(
        '-subject',
        '--email-subject',
        help='Append custom text to the email subject (default is None)',
        metavar='STRING'
    )
    parent_group.add_argument(
        '-ssl',
        '--email-ssl',
        action='store_true',
        default=False,
        help='Send email via SSL (default is False)'
    )
    parent_group.add_argument(
        '-auth',
        '--email-auth',
        action='store_true',
        default=False,
        help='Send email via authenticated SMTP (default is False)'
    )
    parent_group.add_argument(
        '-starttls',
        '--email-starttls',
        action='store_true',
        default=False,
        help='Send email via STARTTLS (default is False)'
    )
    parent_group.add_argument(
        '-nb',
        '--no-banner',
        action='store_true',
        default=False,
        help='Do not print banner (default is False)'
    )
    return process_parser


def print_namespase() -> None:
    """
    Print preset options to console
    :return: None
    """
    print(
        f'\tPreset options\n'
        f'\t-------------------------\n'
        f'\tPrint all Google IP\n'
        f'\taddresses to console     : {CLI.print_all_to_console}\n'
        f'\tPrint only new Google IP\n'
        f'\taddresses to console     : {CLI.print_only_new_to_console}\n'
        f'\tGet host by name         : {CLI.google_host}\n'
        f'\tSPF Google Pull          : {CLI.spf_pull}\n'
        f'\tStatic Google Pull       : {CLI.static_pull}\n'
        f'\tCloud Google Pull        : {CLI.cloud_pull}\n'
        f'\tUse Telegram             : {CLI.use_telegram}\n'
        f'\tTrim long cidr-text\n'
        f'\tfor Telegram             : {CLI.trim_long_text}\n'
        f'\tSplit long Telegram\n'
        f'\tMessage                  : {CLI.split_long_message}\n'
        f'\tUse Telegram             : {CLI.use_telegram}\n'
        f'\tProxy for Telegram       : {CLI.proxy}\n'
        f'\tEmail to                 : {CLI.email_to}\n'
        f'\tEmail subject            : {CLI.email_subject}\n'
        f'\tEmail SSL                : {CLI.email_ssl}\n'
        f'\tEmail AUTH               : {CLI.email_auth}\n'
        f'\tEmail STARTTLS           : {CLI.email_starttls}\n'
        f'\tPrint banner             : {not CLI.no_banner}\n'
        f'\t-------------------------'
    )


def sort_ip_key(addr: str) -> Tuple[int, ...]:
    """
    Helper function for smart IP sort
    :param addr: str IP, sample: "181.44.0.0" или "2a02:180:6:1::"
    :return: Tuple[int, ...]
    """
    return_list = []
    if '.' in addr:
        a, b, c, d = (int(x) for x in addr.split('.'))
        return_list = [a, b, c, d]
    elif ':' in addr:
        hex_list = addr.split(':')
        for hex_item in hex_list:
            if hex_item != '':
                return_list.append(int(hex_item, 16))
            else:
                return_list.append(0)
    return tuple(return_list)


def sort_cidr_key(addr: str) -> Tuple[int, ...]:
    """
    Helper function for smart CIDR sort
    :param addr: str CIDR, simple: "181.44.0.0/15" или "2a02:180:6:1::/64"
    :return: Tuple[int, ...]
    """
    groups, pref = addr.split('/')
    return_list = []
    if '.' in groups:
        a, b, c, d = (int(x) for x in groups.split('.'))
        return_list = [a, b, c, d, int(pref)]
    elif ':' in groups:
        hex_list = groups.split(':')
        for hex_item in hex_list:
            if hex_item != '':
                return_list.append(int(hex_item, 16))
            else:
                return_list.append(0)
        return_list.append(int(pref))
    return tuple(return_list)


def load_cidr_cache() -> None:
    """
    Loading CACHE_CIDR* and CACHE_IP from file
    :return: None
    """
    global CACHE_IP
    global CACHE_CIDR
    global CACHE_CIDR2
    global CACHE_CIDR3

    CACHE_IP = []
    CACHE_CIDR = []
    CACHE_CIDR2 = []
    CACHE_CIDR3 = []

    if os.path.exists(CACHE_IP_FILE):
        with open(CACHE_IP_FILE, 'r+') as f:
            try:
                for line in f:
                    ss = line.strip().rstrip('\n').rstrip('\r')
                    if len(ss) == 0:
                        # empty line
                        continue
                    if len(ss) > 0:
                        CACHE_IP.append(ss)
            except Exception as e:
                print(f'{FLR}Download file error: {FLW}{CACHE_IP_FILE}\n'
                          f'{FLR}{str(e)}')

    if os.path.exists(CACHE_CIDR_FILE):
        with open(CACHE_CIDR_FILE, 'r+') as f:
            try:
                for line in f:
                    ss = line.strip().rstrip('\n').rstrip('\r')
                    if len(ss) == 0:
                        # empty line
                        continue
                    if len(ss) > 0:
                        CACHE_CIDR.append(ss)
            except Exception as e:
                print(f'{FLR}Download file error: {FLW}{CACHE_CIDR_FILE}\n'
                          f'{FLR}{str(e)}')

    if os.path.exists(CACHE_CIDR2_FILE):
        with open(CACHE_CIDR2_FILE, 'r+') as f:
            try:
                for line in f:
                    ss = line.strip().rstrip('\n').rstrip('\r')
                    if len(ss) == 0:
                        # empty line
                        continue
                    if len(ss) > 0:
                        CACHE_CIDR2.append(ss)
            except Exception as e:
                print(f'{FLR}Download file error: {FLW}{CACHE_CIDR2_FILE}\n'
                          f'{FLR}{str(e)}')

    if os.path.exists(CACHE_CIDR3_FILE):
        with open(CACHE_CIDR3_FILE, 'r+') as f:
            try:
                for line in f:
                    ss = line.strip().rstrip('\n').rstrip('\r')
                    if len(ss) == 0:
                        # empty line
                        continue
                    if len(ss) > 0:
                        CACHE_CIDR3.append(ss)
            except Exception as e:
                print(f'{FLR}Download file error: {FLW}{CACHE_CIDR3_FILE}\n'
                          f'{FLR}{str(e)}')

    try:
        CACHE_IP = sorted(
            CACHE_IP,
            key=sort_ip_key
        )
    except ValueError as ee:
        print(f'\n{FLR}{str(ee)}\n')

    try:
        CACHE_CIDR = sorted(
            CACHE_CIDR,
            key=sort_cidr_key
        )
    except ValueError as ee:
        print(f'\n{FLR}{str(ee)}\n')

    try:
        CACHE_CIDR2 = sorted(
            CACHE_CIDR2,
            key=sort_cidr_key
        )
    except ValueError as ee:
        print(f'\n{FLR}{str(ee)}\n')

    try:
        CACHE_CIDR3 = sorted(
            CACHE_CIDR3,
            key=sort_cidr_key
        )
    except ValueError as ee:
        print(f'\n{FLR}{str(ee)}\n')


def save_cidr_cache() -> None:
    """
    Writing CACHE_CIDR* and CACHE_IP to a file
    :return: None
    """
    global CACHE_IP
    global CACHE_CIDR
    global CACHE_CIDR2
    global CACHE_CIDR3

    try:
        CACHE_IP = sorted(
            CACHE_IP,
            key=sort_ip_key
        )
    except ValueError as ee:
        print(f'\n{FLR}{str(ee)}\n')

    try:
        CACHE_CIDR = sorted(
            CACHE_CIDR,
            key=sort_cidr_key
        )
    except ValueError as ee:
        print(f'\n{FLR}{str(ee)}\n')

    try:
        CACHE_CIDR2 = sorted(
            CACHE_CIDR2,
            key=sort_cidr_key
        )
    except ValueError as ee:
        print(f'\n{FLR}{str(ee)}\n')

    try:
        CACHE_CIDR3 = sorted(
            CACHE_CIDR3,
            key=sort_cidr_key
        )
    except ValueError as ee:
        print(f'\n{FLR}{str(ee)}\n')

    with open(CACHE_IP_FILE, 'w+') as f:
        for item in CACHE_IP:
            if item.strip() != '':
                f.write(f'{item}\n')

    with open(CACHE_CIDR_FILE, 'w+') as f:
        for item in CACHE_CIDR:
            if item.strip() != '':
                f.write(f'{item}\n')

    with open(CACHE_CIDR2_FILE, 'w+') as f:
        for item in CACHE_CIDR2:
            if item.strip() != '':
                f.write(f'{item}\n')

    with open(CACHE_CIDR3_FILE, 'w+') as f:
        for item in CACHE_CIDR3:
            if item.strip() != '':
                f.write(f'{item}\n')


def check_cli_logic() -> None:
    """
    Check command line logic
    :return: None
    """
    global CLI
    global TELEGRAM_PROXIES

    if CLI.print_all_to_console and CLI.print_only_new_to_console:
        print(
            f'{FLR}You must use either the -pa/--print-all-to-console option only or '
            f'the -pon/--print-only-new-to-console option only'
        )
        sys.exit(-1)

    print_to_console: bool = CLI.print_all_to_console or CLI.print_only_new_to_console
    if CLI.print_all_to_console:
        CLI.no_banner = True

    if CLI.print_only_new_to_console and not CLI.no_banner:
        # Print banner
        if platform.platform().startswith('Windows'):
            home_path: str = os.path.join(
                os.getenv('HOMEDRIVE'), os.getenv('HOMEPATH')
            )
        else:
            home_path: str = os.path.join(os.getenv('HOME'))
        sys_version: str = str(sys.version).replace('\n', '')
        print(
            f'\tPython  : {FLC}{sys_version}{FR}\n'
            f'\tNode    : {FLC}{platform.node()}{FR}\n'
            f'\tHome    : {FLC}{home_path}{FR}\n'
            f'\tOS      : {FLC}{platform.system()}{FR}\n'
            f'\tRelease : {FLC}{platform.release()}{FR}\n'
            f'\tVersion : {FLC}{platform.version()}{FR}\n'
            f'\tArch    : {FLC}{platform.machine()}{FR}\n'
            f'\tCPU     : {FLC}{platform.processor()}{FR}'
        )
        print_namespase()

    if CLI.trim_long_text and not CLI.use_telegram:
        print(
            f'{FLR}The -trim/--trim-long-text option is used '
            f'in conjunction with the -t/--use-telegram option'
        )
        sys.exit(-1)

    if CLI.split_long_message and not CLI.use_telegram:
        print(
            f'{FLR}The -split/--split-long-message option is used '
            f'in conjunction with the -t/--use-telegram option'
        )
        sys.exit(-1)

    if CLI.email_ssl and not CLI.email_to:
        print(
            f'{FLR}You must specify the email address of the recipient. '
            f'Use the --email-to option'
        )
        sys.exit(-1)

    if CLI.email_subject and not CLI.email_to:
        print(
            f'{FLR}You must specify the email address of the recipient. '
            f'Use the --email-to option'
        )
        sys.exit(-1)

    if CLI.email_auth and not CLI.email_to:
        print(
            f'{FLR}You must specify the email address of the recipient. '
            f'Use the --email-to option'
        )
        sys.exit(-1)

    if CLI.email_starttls and not CLI.email_to:
        print(
            f'{FLR}You must specify the email address of the recipient. '
            f'Use the --email-to option'
        )
        sys.exit(-1)

    if CLI.email_starttls and CLI.email_ssl and CLI.email_to:
        print(
            f'{FLR}The contradiction of options. '
            f'You must choose one thing: either --email-ssl or '
            f'--email-starttls or do not use either one or the other'
        )
        sys.exit(-1)

    if not CLI.google_host and not CLI.spf_pull and not CLI.static_pull and not CLI.cloud_pull:
        print(
            f'{FLR}Вам нужно указать хост или диапазоны IP-адресов Google: '
            f'HOST/SPF/STATIC/COLUD.\n'
            f'Use either -gh/--google-host or/and -spf/--spf-pull or/and -static/--static-pull or/and -cloud/--cloud-pull'
        )
        sys.exit(-1)

    is_any_pull: bool = CLI.spf_pull or CLI.static_pull or CLI.cloud_pull
    is_not_do_any_notify: bool = not CLI.use_telegram and not CLI.email_to
    if not print_to_console and is_any_pull and is_not_do_any_notify:
        print(
            f'{FLR}You must use at least one of the notification methods '
            f'(email, telegram or console)\n'
            f'Use -pa/--print-all-to-console or -pon/--print-only-new-to-console or '
            f'-e/--email-to or/and -t/--use-telegram'
        )
        sys.exit(-1)

    if CLI.proxy and (not CLI.use_telegram):
        print(f'{FLR}The proxy setting is for telegram only')
        sys.exit(-1)

    if CLI.proxy and CLI.use_telegram:
        TELEGRAM_PROXIES.clear()
        TELEGRAM_PROXIES['http'] = CLI.proxy
        TELEGRAM_PROXIES['https'] = CLI.proxy


def main():
    """
    Main function
    :return: None
    """
    # Check command line logic
    check_cli_logic()

    global NEW_IP_IN_NETWORK
    global CACHE_IP
    global CACHE_CIDR
    global CACHE_CIDR2
    global CACHE_CIDR3

    global NEW_IP
    global NEW_CIDR
    global NEW_CIDR2
    global NEW_CIDR3

    NEW_IP_IN_NETWORK = ''

    ################################
    # Load all cache
    load_cidr_cache()

    remove_substrs = (
        '"',
        'ip4:',
        'ip6:',
        'include:',
        'v=spf1 ',
        ' ~all',
    )
    all_google_ip = []
    all_google_cidr = []
    all_google_cidr2 = []
    all_google_cidr3 = []

    ################################
    # Determination of IP by hostname
    if CLI.google_host:
        try:
            ip: str = socket.gethostbyname(GOOGLE_HOST)
            if ip.strip() != '':
                all_google_ip.append(ip)

            ################################
            # Comparing the cache with actual data
            if len(all_google_ip) > 0:
                NEW_IP = []

                try:
                    all_google_ip = sorted(
                        all_google_ip,
                        key=sort_ip_key
                    )
                except ValueError as ee:
                    print(f'\n{FLR}{str(ee)}\n')

                if len(all_google_ip) > 0:
                    for ip in all_google_ip:
                        if CLI.print_all_to_console:
                            print(f'{FLC}{ip}')
                        if ip not in CACHE_IP:
                            NEW_IP.append(ip)

                if len(NEW_IP) > 0 and CLI.print_only_new_to_console:
                    print(f'\nNew IPs discovered ({len(NEW_IP)}):\n{"-" * 20}')
                    for ip in NEW_IP:
                        print(f'+ {FLG}{ip}')

                CACHE_IP = all_google_ip

        except Exception as e:
            print(f'{FRC}Error: {str(e)}')

    ################################
    # Google Workspace IP Ranges
    # nslookup -q=TXT _spf.google.com 8.8.8.8
    if CLI.spf_pull:
        google_dns_urls = []
        my_resolver = resolver.Resolver()
        my_resolver.nameservers = ['8.8.8.8']

        try:
            answer = my_resolver.resolve('_spf.google.com', 'TXT')
            for val in answer:
                val_str = val.to_text()
                for substr in remove_substrs:
                    val_str = val_str.replace(substr, '')
                val_str = val_str.strip()
                val_list = val_str.split(' ')
                if len(val_list) > 0:
                    for google_dns_url in val_list:
                        val_google_dns_url = google_dns_url.strip()
                        if val_google_dns_url not in google_dns_urls:
                            google_dns_urls.append(val_google_dns_url)
        except Exception as e:
            print(f'{FRC} Error: {FLR}{str(e)}')

        for url in google_dns_urls:
            try:
                answer = my_resolver.resolve(url, 'TXT')
                for val in answer:
                    val_str = val.to_text()
                    for substr in remove_substrs:
                        val_str = val_str.replace(substr, '')
                    val_str = val_str.strip()
                    val_list = val_str.split(' ')
                    if len(val_list) > 0:
                        for cidr in val_list:
                            val_cidr = cidr.strip()
                            if val_cidr not in all_google_cidr:
                                all_google_cidr.append(val_cidr)
            except Exception as e:
                print(f'{FRC} Error: {FLR}{str(e)}')

        ################################
        # Comparing the cache with actual data
        NEW_CIDR = []

        try:
            all_google_cidr = sorted(
                all_google_cidr,
                key=sort_cidr_key
            )
        except ValueError as ee:
            print(f'\n{FLR}{str(ee)}\n')

        if len(all_google_cidr) > 0:
            for cidr in all_google_cidr:
                if CLI.print_all_to_console:
                    print(f'{FLW}{cidr}')
                if cidr not in CACHE_CIDR:
                    NEW_CIDR.append(cidr)

        if len(NEW_CIDR) > 0 and CLI.print_only_new_to_console:
            print(f'\nNew spf CIDRs discovered ({len(NEW_CIDR)}):\n{"-" * 20}')
            for cidr in NEW_CIDR:
                print(f'+ {FLG}{cidr}')

        CACHE_CIDR = all_google_cidr

    ################################
    # Google IP address ranges that are available
    # to users on the internet
    if CLI.static_pull:
        google_ips_url_pull2 = 'https://www.gstatic.com/ipranges/goog.json'
        r = None
        try:
            if len(TELEGRAM_PROXIES) > 0:
                r = requests.get(
                    google_ips_url_pull2,
                    timeout = 10,
                    proxies=TELEGRAM_PROXIES,
                    headers=REQUEST_HEADERS,
                    verify=True,
                )
            else:
                r = requests.get(
                    google_ips_url_pull2,
                    timeout=10,
                    headers=REQUEST_HEADERS,
                    verify=True,
                )
        except requests.exceptions.RequestException as e:
            print(f'{FRC}Error {str(e)}')

        if r.status_code != 200:
            print(f'{FRC}Error {str(r.text)}')
        else:
            tmp = json.loads(r.text)
            if tmp is not None:
                ipv_prefix_list = tmp.get('prefixes')
                if len(ipv_prefix_list) > 0:
                    for cidr_item in ipv_prefix_list:
                        cidr = cidr_item.get('ipv4Prefix')
                        if cidr is not None:
                            all_google_cidr2.append(cidr)
                        else:
                            cidr = cidr_item.get('ipv6Prefix')
                            if cidr is not None:
                                all_google_cidr2.append(cidr)

                    ################################
                    # Comparing the cache with actual data
                    NEW_CIDR2 = []
                    try:
                        all_google_cidr2 = sorted(
                            all_google_cidr2,
                            key=sort_cidr_key
                        )
                    except ValueError as ee:
                        print(f'\n{FLR}{str(ee)}\n')

                    if len(all_google_cidr2) > 0:
                        for cidr in all_google_cidr2:
                            if CLI.print_all_to_console:
                                print(f'{FC}{cidr}')
                            if cidr not in CACHE_CIDR2:
                                NEW_CIDR2.append(cidr)
                        if len(NEW_CIDR2) > 0 and CLI.print_only_new_to_console:
                            print(f'\nNew static CIDRs discovered ({len(NEW_CIDR2)}):\n{"-" * 20}')
                            for cidr in NEW_CIDR2:
                                print(f'+ {FLG}{cidr}')

                    CACHE_CIDR2 = all_google_cidr2

    ################################
    # Global and regional external IP address
    # ranges for Google Cloud tenants
    if CLI.cloud_pull:
        google_ips_url_pull3 = 'https://www.gstatic.com/ipranges/cloud.json'
        r = None
        try:
            if len(TELEGRAM_PROXIES) > 0:
                r = requests.get(
                    google_ips_url_pull3,
                    timeout = 10,
                    proxies=TELEGRAM_PROXIES,
                    headers=REQUEST_HEADERS,
                    verify=True,
                )
            else:
                r = requests.get(
                    google_ips_url_pull3,
                    timeout=10,
                    headers=REQUEST_HEADERS,
                    verify=True,
                )
        except requests.exceptions.RequestException as e:
            print(f'{FRC}Error {str(e)}')

        if r.status_code != 200:
            print(f'{FRC}Error {str(r.text)}')
        else:
            tmp = json.loads(r.text)
            if tmp is not None:
                ipv_prefix_list = tmp.get('prefixes')
                if len(ipv_prefix_list) > 0:
                    for cidr_item in ipv_prefix_list:
                        cidr = cidr_item.get('ipv4Prefix')
                        if cidr is not None:
                            all_google_cidr3.append(cidr)
                        else:
                            cidr = cidr_item.get('ipv6Prefix')
                            if cidr is not None:
                                all_google_cidr3.append(cidr)

                    ################################
                    # Comparing the cache with actual data
                    NEW_CIDR3 = []
                    try:
                        all_google_cidr3 = sorted(
                            all_google_cidr3,
                            key=sort_cidr_key
                        )
                    except ValueError as ee:
                        print(f'\n{FLR}{str(ee)}\n')

                    if len(all_google_cidr3) > 0:
                        for cidr in all_google_cidr3:
                            if CLI.print_all_to_console:
                                print(f'{FY}{cidr}')
                            if cidr not in CACHE_CIDR3:
                                NEW_CIDR3.append(cidr)
                        if len(NEW_CIDR3) > 0 and CLI.print_only_new_to_console:
                            print(f'\nNew cloud CIDRs discovered ({len(NEW_CIDR3)}):\n{"-" * 20}')
                            for cidr in NEW_CIDR3:
                                print(f'+ {FLG}{cidr}')

                    CACHE_CIDR3 = all_google_cidr3

    ################################
    # Save all cache
    save_cidr_cache()

    ################################
    # If something has changed
    if (
            len(NEW_IP) > 0 or
            len(NEW_CIDR) > 0 or
            len(NEW_CIDR2) > 0 or
            len(NEW_CIDR3) > 0
    ):
        ################################
        # Check if the IP address is in the ranges of Google networks
        if CLI.google_host:
            all_google_cidr = []
            if CLI.spf_pull:
                all_google_cidr.extend(CACHE_CIDR)
            if CLI.static_pull:
                all_google_cidr.extend(CACHE_CIDR2)
            if CLI.cloud_pull:
                all_google_cidr.extend(CACHE_CIDR3)

            # Remove Duplicates
            all_google_cidr = list(OrderedDict.fromkeys(all_google_cidr))

            for ip in NEW_IP:
                for ip_network in all_google_cidr:
                    if is_ip_in_network(ip, ip_network):
                        NEW_IP_IN_NETWORK = f'{ip} in {ip_network}'
                        if CLI.print_only_new_to_console:
                            print(
                                f'{FR}The new IP address {FLC}{ip}{FR} already belongs '
                                f'to the network range {FC}{ip_network}{FR}. '
                                f'No action required (this event can be ignored).'
                            )
                        break

        ################################
        # Make and Send Report by Email
        if CLI.email_to:
            make_report_for_email()

        ################################
        # Make and Send Report by Telegram
        if CLI.use_telegram:
            make_report_for_telegram()

    # Конец ¯\_(ツ)_/¯
    # End ༼ つ ◕_◕ ༽つ


if __name__ == "__main__":
    # Parsing command line
    parser: MyParser = process_cli()
    CLI = parser.parse_args(sys.argv[1:])
    if len(sys.argv[1:]) == 0:
        parser.print_help()
    main()
