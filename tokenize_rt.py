from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import collections
import io
import re
import tokenize


ESCAPED_NL = 'ESCAPED_NL'
UNIMPORTANT_WS = 'UNIMPORTANT_WS'
NON_CODING_TOKENS = frozenset(('COMMENT', ESCAPED_NL, 'NL', UNIMPORTANT_WS))
Offset = collections.namedtuple('Offset', ('line', 'utf8_byte_offset'))
Offset.__new__.__defaults__ = (None, None)
Token = collections.namedtuple(
    'Token', ('name', 'src', 'line', 'utf8_byte_offset'),
)
Token.__new__.__defaults__ = (None, None)
Token.offset = property(lambda self: Offset(self.line, self.utf8_byte_offset))

_string_re = re.compile('^([^\'"]*)(.*)$', re.DOTALL)
_string_prefixes = frozenset('bfru')
_escaped_nl_re = re.compile(r'\\(\n|\r\n|\r)')


def _re_partition(regex, s):
    match = regex.search(s)
    if match:
        return s[:match.start()], s[slice(*match.span())], s[match.end():]
    else:
        return (s, '', '')


def src_to_tokens(src):
    tokenize_target = io.StringIO(src)
    lines = (None,) + tuple(tokenize_target)
    tokenize_target.seek(0)

    tokens = []
    last_line = 1
    last_col = 0

    for (
            tok_type, tok_text, (sline, scol), (eline, ecol), line,
    ) in tokenize.generate_tokens(tokenize_target.readline):
        if sline > last_line:
            newtok = lines[last_line][last_col:]
            for lineno in range(last_line + 1, sline):
                newtok += lines[lineno]
            if scol > 0:
                newtok += lines[sline][:scol]

            # a multiline unimportant whitespace may contain escaped newlines
            while _escaped_nl_re.search(newtok):
                ws, nl, newtok = _re_partition(_escaped_nl_re, newtok)
                if ws:
                    tokens.append(Token(UNIMPORTANT_WS, ws))
                tokens.append(Token(ESCAPED_NL, nl))
            if newtok:
                tokens.append(Token(UNIMPORTANT_WS, newtok))

        elif scol > last_col:
            tokens.append(Token(UNIMPORTANT_WS, line[last_col:scol]))

        tok_name = tokenize.tok_name[tok_type]
        utf8_byte_offset = len(line[:scol].encode('UTF-8'))
        # when a string prefix is not recognized, the tokenizer produces a
        # NAME token followed by a STRING token
        if (
                tok_name == 'STRING' and
                tokens and
                tokens[-1].name == 'NAME' and
                frozenset(tokens[-1].src.lower()) <= _string_prefixes
        ):
            newsrc = tokens[-1].src + tok_text
            tokens[-1] = tokens[-1]._replace(src=newsrc, name=tok_name)
        # produce octal literals as a single token in python 3 as well
        elif (
                tok_name == 'NUMBER' and
                tokens and
                tokens[-1].name == 'NUMBER'
        ):  # pragma: no cover (PY3)
            tokens[-1] = tokens[-1]._replace(src=tokens[-1].src + tok_text)
        # produce long literals as a single token in python 3 as well
        elif (
                tok_name == 'NAME' and
                tok_text.lower() == 'l' and
                tokens and
                tokens[-1].name == 'NUMBER'
        ):  # pragma: no cover (PY3)
            tokens[-1] = tokens[-1]._replace(src=tokens[-1].src + tok_text)
        else:
            tokens.append(Token(tok_name, tok_text, sline, utf8_byte_offset))
        last_line, last_col = eline, ecol

    return tokens


def tokens_to_src(tokens):
    return ''.join(tok.src for tok in tokens)


def reversed_enumerate(tokens):
    for i in reversed(range(len(tokens))):
        yield i, tokens[i]


def parse_string_literal(src):
    """parse a string literal's source into (prefix, string)"""
    match = _string_re.match(src)
    return match.group(1), match.group(2)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args(argv)
    with io.open(args.filename) as f:
        tokens = src_to_tokens(f.read())

    def no_u_repr(s):
        return repr(s).lstrip('u')

    for token in tokens:
        if token.name == UNIMPORTANT_WS:
            line, col = '?', '?'
        else:
            line, col = token.line, token.utf8_byte_offset
        print(
            '{}:{} {} {}'.format(
                line, col, token.name, no_u_repr(token.src),
            ),
        )


if __name__ == '__main__':
    exit(main())
