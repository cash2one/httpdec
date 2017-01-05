# coding=utf-8
from .decode import decode

import click
import pyperclip
import sys

try:
    from StringIO import StringIO
except:
    from io import StringIO

stdin = sys.stdin
stdout = sys.stdout


def fake_clip():
    content = pyperclip.paste()
    fin = StringIO(content)
    fout = StringIO()

    def close():
        value = fout.getvalue()
        pyperclip.copy(value)

    fout.close = close
    return fin, fout


typed = dict(
    h='header',
    c='cookie',
    t='time')
types = typed.keys() + typed.values()


@click.command()
@click.option('-d', '--type', type=click.Choice(types), help='decode type')
@click.option('-p', '--clip', is_flag=True, help='read/write to clipboard')
@click.argument('input', type=click.File('r'), default=stdin)
@click.argument('output', type=click.File('w'), default=stdout)
def httpdec(output, input, clip, type):
    """
    httpdec [OPTIONS] [INPUT] [OUTPUT]

    INPUT: the source file, default is stdin

    OUTPUT: the output file, default is stdout
    """

    if clip:
        input, output = fake_clip()

    type = typed[type[0]]

    decode(input, output, type)
