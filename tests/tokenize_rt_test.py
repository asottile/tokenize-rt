from __future__ import absolute_import
from __future__ import unicode_literals

import io

import pytest

from tokenize_rt import main
from tokenize_rt import src_to_tokens
from tokenize_rt import Token
from tokenize_rt import tokens_to_src
from tokenize_rt import UNIMPORTANT_WS


def test_src_to_tokens_simple():
    src = 'x = 5\n'
    ret = src_to_tokens(src)
    assert ret == [
        Token('NAME', 'x', line=1, utf8_byte_offset=0),
        Token(UNIMPORTANT_WS, ' ', line=None, utf8_byte_offset=None),
        Token('OP', '=', line=1, utf8_byte_offset=2),
        Token(UNIMPORTANT_WS, ' ', line=None, utf8_byte_offset=None),
        Token('NUMBER', '5', line=1, utf8_byte_offset=4),
        Token('NEWLINE', '\n', line=1, utf8_byte_offset=5),
        Token('ENDMARKER', '', line=2, utf8_byte_offset=0),
    ]


@pytest.mark.parametrize(
    'filename',
    (
        'testing/resources/empty.py',
        'testing/resources/unicode_snowman.py',
        'testing/resources/backslash_continuation.py',
    ),
)
def test_roundtrip_tokenize(filename):
    with io.open(filename) as f:
        contents = f.read()
    ret = tokens_to_src(src_to_tokens(contents))
    assert ret == contents


def test_main(capsys):
    main(('testing/resources/simple.py',))
    out, _ = capsys.readouterr()
    assert out == (
        "1:0 NAME 'x'\n"
        "?:? UNIMPORTANT_WS ' '\n"
        "1:2 OP '='\n"
        "?:? UNIMPORTANT_WS ' '\n"
        "1:4 NUMBER '5'\n"
        "1:5 NEWLINE '\\n'\n"
        "2:0 ENDMARKER ''\n"
    )
