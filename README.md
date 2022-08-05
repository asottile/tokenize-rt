[![Build Status](https://dev.azure.com/asottile/asottile/_apis/build/status/asottile.tokenize-rt?branchName=main)](https://dev.azure.com/asottile/asottile/_build/latest?definitionId=25&branchName=main)
[![Azure DevOps coverage](https://img.shields.io/azure-devops/coverage/asottile/asottile/25/main.svg)](https://dev.azure.com/asottile/asottile/_build/latest?definitionId=25&branchName=main)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/asottile/tokenize-rt/main.svg)](https://results.pre-commit.ci/latest/github/asottile/tokenize-rt/main)

tokenize-rt
===========

The stdlib `tokenize` module does not properly roundtrip.  This wrapper
around the stdlib provides two additional tokens `ESCAPED_NL` and
`UNIMPORTANT_WS`, and a `Token` data type.  Use `src_to_tokens` and
`tokens_to_src` to roundtrip.

This library is useful if you're writing a refactoring tool based on the
python tokenization.

## Installation

```bash
pip install tokenize-rt
```

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
- `line`: the line number that this token appears on.
- `utf8_byte_offset`: the utf8 byte offset that this token appears on in the
  line.

#### `tokenize_rt.Token.offset`

Retrieves an `Offset` for this token.

### converting to and from `Token` representations

#### `tokenize_rt.src_to_tokens(text: str) -> List[Token]`

#### `tokenize_rt.tokens_to_src(Iterable[Token]) -> str`

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

#### `tokenize_rt.parse_string_literal(text: str) -> Tuple[str, str]`

parse a string literal into its prefix and string content

```pycon
>>> parse_string_literal('f"foo"')
('f', '"foo"')
```

#### `tokenize_rt.reversed_enumerate(Sequence[Token]) -> Iterator[Tuple[int, Token]]`

yields `(index, token)` pairs.  Useful for rewriting source.

#### `tokenize_rt.rfind_string_parts(Sequence[Token], i) -> Tuple[int, ...]`

find the indices of the string parts of a (joined) string literal

- `i` should start at the end of the string literal
- returns `()` (an empty tuple) for things which are not string literals

```pycon
>>> tokens = src_to_tokens('"foo" "bar".capitalize()')
>>> rfind_string_parts(tokens, 2)
(0, 2)
>>> tokens = src_to_tokens('("foo" "bar").capitalize()')
>>> rfind_string_parts(tokens, 4)
(1, 3)
```

## Differences from `tokenize`

- `tokenize-rt` adds `ESCAPED_NL` for a backslash-escaped newline "token"
- `tokenize-rt` adds `UNIMPORTANT_WS` for whitespace (discarded in `tokenize`)
- `tokenize-rt` normalizes string prefixes, even if they are not parsed -- for
  instance, this means you'll see `Token('STRING', "f'foo'", ...)` even in
  python 2.
- `tokenize-rt` normalizes python 2 long literals (`4l` / `4L`) and octal
  literals (`0755`) in python 3 (for easier rewriting of python 2 code while
  running python 3).

## Sample usage

- https://github.com/asottile/add-trailing-comma
- https://github.com/asottile/future-annotations
- https://github.com/asottile/future-fstrings
- https://github.com/asottile/pyupgrade
- https://github.com/asottile/yesqa
