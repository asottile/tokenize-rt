from __future__ import absolute_import
from __future__ import unicode_literals

import argparse
import collections
import io
import tokenize


UNIMPORTANT_WS = 'UNIMPORTANT_WS'
Token = collections.namedtuple(
    'Token', ('name', 'src', 'line', 'utf8_byte_offset'),
)
Token.__new__.__defaults__ = (None, None,)


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
            if newtok:
                tokens.append(Token(UNIMPORTANT_WS, newtok))
        elif scol > last_col:
            tokens.append(Token(UNIMPORTANT_WS, line[last_col:scol]))

        tok_name = tokenize.tok_name[tok_type]
        utf8_byte_offset = len(line[:scol].encode('UTF-8'))
        tokens.append(Token(tok_name, tok_text, sline, utf8_byte_offset))
        last_line, last_col = eline, ecol

    return tokens


def tokens_to_src(tokens):
    return ''.join(tok.src for tok in tokens)


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
        print('{}:{} {} {}'.format(
            line, col, token.name, no_u_repr(token.src),
        ))


if __name__ == '__main__':
    exit(main())
