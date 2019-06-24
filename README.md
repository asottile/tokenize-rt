[![Build Status](https://dev.azure.com/asottile/asottile/_apis/build/status/asottile.tokenize-rt?branchName=master)](https://dev.azure.com/asottile/asottile/_build/latest?definitionId=25&branchName=master)
[![Azure DevOps coverage](https://img.shields.io/azure-devops/coverage/asottile/asottile/25/master.svg)](https://dev.azure.com/asottile/asottile/_build/latest?definitionId=25&branchName=master)

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

### datastructures

#### `tokenize_rt.Offset(line=None, utf8_byte_offset=None)`

A token offset, useful as a key when cross referencing the `ast` and the
tokenized source.

#### `tokenize_rt.Token(name, src, line=None, utf8_byte_offset=None)`

Construct a token

- `name`: one of the token names listed in `token.tok_name` or
  `ESCAPED_NL` or `UNIMPORTANT_WS`
- `src`: token's source as text
- `line`: the line number that this token appears on.  This will be `None` for
   `ESCAPED_NL` and `UNIMPORTANT_WS` tokens.
- `utf8_byte_offset`: the utf8 byte offset that this token appears on in the
  line.  This will be `None` for `ESCAPED_NL` and `UNIMPORTANT_WS` tokens.

#### `tokenize_rt.Token.offset`

Retrieves an `Offset` for this token.

### converting to and from `Token` representations

#### `tokenize_rt.src_to_tokens(text) -> List[Token]`

#### `tokenize_rt.tokens_to_src(Sequence[Token]) -> text`

### additional tokens added by `tokenize-rt`

#### `tokenize_rt.ESCAPED_NL`

#### `tokenize_rt.UNIMPORTANT_WS`

### helpers

#### `tokenize_rt.NON_CODING_TOKENS`

A `frozenset` containing tokens which may appear between others while not
affecting control flow or code:
- `COMMENT`
- `ESCAPED_NL`
- `NL`
- `UNIMPORTANT_WS`

#### `tokenize_rt.parse_string_literal(text) -> Tuple[str, str]`

parse a string literal into its prefix and string content

```pycon
>>> parse_string_literal('f"foo"')
('f', '"foo"')
```

#### `tokenize_rt.reversed_enumerate(Sequence[Token]) -> Iterator[Tuple[int, Token]]`

yields `(index, token)` pairs.  Useful for rewriting source.

## Differences from `tokenize`

- `tokenize-rt` adds `ESCAPED_NL` for a backslash-escaped newline "token"
- `tokenize-rt` adds `UNIMPORTANT_WS` for whitespace (discarded in `tokenize`)
- `tokenize-rt` normalizes string prefixes, even if they are not parsed -- for
  instance, this means you'll see `Token('STRING', "f'foo'", ...)` even in
  python 2.

## Sample usage

- https://github.com/asottile/add-trailing-comma
- https://github.com/asottile/future-fstrings
- https://github.com/asottile/pyupgrade
- https://github.com/asottile/yesqa
