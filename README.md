[![Build Status](https://travis-ci.org/asottile/tokenize-rt.svg?branch=master)](https://travis-ci.org/asottile/tokenize-rt)
[![Coverage Status](https://coveralls.io/repos/github/asottile/tokenize-rt/badge.svg?branch=master)](https://coveralls.io/github/asottile/tokenize-rt?branch=master)

tokenize-rt
===========

The stdlib `tokenize` module does not properly roundtrip.  This wrapper
around the stdlib provides two additional tokens `ESCAPED_NL` and
`UNIMPORTANT_WS`, and a `Token` data type.  Use `src_to_tokens` and
`tokens_to_src` to roundtrip.

This library is useful if you're writing a refactoring tool based on the
python tokenization.

## Installation

`pip install tokenize-rt`

## Usage

### `tokenize_rt.src_to_tokens(text) -> List[Token]`

### `tokenize_rt.tokens_to_src(Sequence[Token]) -> text`

### `tokenize_rt.ESCAPED_NL`

### `tokenize_rt.UNIMPORTANT_WS`

### `tokenize_rt.Offset(line=None, utf8_byte_offset=None)`

A token offset, useful as a key when cross referencing the `ast` and the
tokenized source.

### `tokenize_rt.Token(name, src, line=None, utf8_byte_offset=None)`

Construct a token

- `name`: one of the token names listed in `token.tok_name` or
  `ESCAPED_NL` or `UNIMPORTANT_WS`
- `src`: token's source as text
- `line`: the line number that this token appears on.  This will be `None` for
   `ESCAPED_NL` and `UNIMPORTANT_WS` tokens.
- `utf8_byte_offset`: the utf8 byte offset that this token appears on in the
  line.  This will be `None` for `ESCAPED_NL` and `UNIMPORTANT_WS` tokens.

### `tokenize_rt.Token.offset`

Retrieves an `Offset` for this token.

### `tokenize_rt.reversed_enumerate(Sequence[Token]) -> Iterator[Tuple[int, Token]]`

yields `(index, token)` pairs.  Useful for rewriting source.

## Sample usage

- https://github.com/asottile/add-trailing-comma
- https://github.com/asottile/future-fstrings
- https://github.com/asottile/pyupgrade
- https://github.com/asottile/yesqa
