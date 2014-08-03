#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
import click
import requests
from bs4 import BeautifulSoup


class HttpError(Exception):

    def __init__(self, code):
        self.code = code

    def __str__(self):
        return 'HTTP Request faile, status code is ' + self.code


def http_get(url, args=None):
    if args is not None:
        r = requests.get(url, params=args)
    else:
        r = requests.get(url)

    if r.status_code < 400:
        return r.text
    else:
        raise HttpError(r.status_code)


@click.group()
def cli():
    pass


@cli.command()
@click.argument('keywords', nargs=-1)
def baidu(keywords):
    baidu_url = 'http://www.baidu.com/s'
    search_keywords = ' '.join(keywords)
    args = {'ie': 'utf-8',
            'wd': search_keywords}
    try:
        html = http_get(baidu_url, args)
        soup = BeautifulSoup(html)
        items = soup.find_all('div', class_='c-tools')
        for item in items:
            tag = item.get('data-tools')
            if tag is not None:
                dict = ast.literal_eval(tag)
                click.echo(dict['title'])
    except HttpError as e:
        click.echo(e)


@cli.command()
@click.argument('keywords', nargs=-1)
def google(keywords):
    click.echo('google')

if __name__ == '__main__':
    cli()
