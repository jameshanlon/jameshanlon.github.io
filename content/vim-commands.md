title: Vim command composition
date: 2018-08-23
category: notes
tags: computing, vim
summary: Composition of Vim's motions and operators

I've been using Vim for a long time and I'm familiar with many of its commands
but I've never had a good understanding of the underlying components of
commands and their composition. Although there are many good Vim
[references](#references), I felt that I was still not seeing the full picture.
So, to try and dig a little deeper and educate myself, I've put together this
reference, which details a subset of the command language. The approach I've
taken was inspired by the grammar rules outlined in [this blog
post](https://takac.github.io/2013/01/30/vim-grammar/), and should be useful
for anyone who is familiar with Vim.

A Vim command can be constructed from different rules, and below each rule is
specified with a [EBNF-style
syntax](https://en.wikipedia.org/wiki/Extended_Backus-Naur_form), where `<...>` is
another rule. `{...}` represents some key presses, `|` is an alternative and
`[...]` is an optional component. Be warned that
since there are many special cases to Vim commands and I've not checked all the
combinations, some of the rules below may yield invalid compositions! As such,
these rules are better viewed as a way of remembering commands. For an
exhaustive treatment of the command language, please check the [Vim
documentation](https://www.vim.org/docs.php), or use the `:help` tags that I've
given.

## Motions

Motions change the position of the cursor and can be combined with a count to
repeat the motion.

```
count := {digits}
motion := [<count>] <motion-keys>
command := <motion>
```

Examples:

- `2fx` - move to the second right-hand occurrence of `x` in the line (inclusive)
- `2Tx` - move to the second left-hand occurrence of `x` in the line (exclusive)
- `w` - move to the next word
- `10j` or `10_` - move down 10 lines
- `10k` - move up 10 lines
- `6w` - move to start of the sixth word forwards
- `6E` - move to end of sixth word forwards
- `4b` - move to start of the fourth word backwards
- `2{` - move two paragraphs down
- `3/foo` - move to the third occurrence of `foo` later in the buffer
- `3?foo` - move to the third occurrence of `foo` earlier in the buffer

## Text objects

Text objects are a collection of characters relative to the position of the
cursor. Compared to motions, text objects on a whole object, regardless of the
specific cursor position. The `a` and `i` modifiers augment text objects,
specifying whether the surrounding context should be included. The context may
be whitespace or delimiting characters.

```
text-object := <text-object-keys>
             | <modifier> <text-object-keys>
```

Examples:

- `aw` - around word (includes surrounding whitespace)
- `iw` - inner word (excludes surrounding whitespace)
- `aW` - around WORD (where word is delimited by whitespace)
- `as` - around sentence
- `is` - inner sentence
- `ap` - around paragraph
- `ip` - inner paragraph
- `a'` - a single-quoted string
- `i'` - inside a single-quoted string
- `a(` = `a)`= `ab` - a parenthesised block, from `(` to `)`
- `i(` = `i)`= `ib` - inside a parenthesised block, contents of `(...)`
- `a<` = `a>` - a tag, from `<` to `>`
- `at` - around tag block, including matching start and end tags `<tag>...</tag>`
- `it` - inside tag block, excluding tags
- `aB` = `a{` = `a}` - around a `{...}` block
- `iB` = `i{` = `i}` - inside a `{...}` block

## Operators on text objects

Operators can be applied to text objects. In some circumstances, a count can be
applied to the text object to repeat its effect.

```
command := [<count>] <operator> <text-object>
text-object := <count> <modifier> <text-object-keys>
```

Examples:

- `cw`  - change word from cursor
- `ciw` - change word under cursor
- `dw` - delete until end of word
- `5dw` = `d5w` - delete until end of right-hand sixth word
- `caw` - change around word under cursor
- `2d3w` - delete six words
- `5gUw` - make the next five words uppercase
- `dgg` - delete lines from cursor to beginning of buffer
- `dG` - delete lines from cursor to end of buffer
- `3d_` - delete three lines
- `c$` - change until end of line
- `y_` = `yy` = `Y` - yank the line
- `c_` = `cc` = `C` - change the line
- `gUap` - make paragraph uppercase
- `gqap` - format paragraph text to `textwidth` line length
- `dit` - delete text between tags `<tag></tag>`
- `dat` - delete tag block
- `yi"` - yank text in `"..."` block
- `yi<` - yank text in `<...>` block
- `yiB` - yank text in `{...}` block
- `yaB` - yank whole `{...}` block

## Operators on motions

A motion can be applied after an operator to apply the operator on the text
that was moved over.

```
command := [<count>] <operator> <motion>
```

Examples:

- `dl` = `x` - delete next character
- `db` - delete backwards to the start of a word
- `dtx` - delete until `x` character in line (exclusive)
- `dfx` - delete until `x` character in line (inclusive)
- `d/foo` - delete from cursor to next occurrence of `foo`
- `d3/foo` - delete from cursor until the third occurrence of `foo`
- `c$` = `C` - change until end of line
- `d$` = `D` - delete until end of line
- `d0` - delete until beginning of line
- `d^` - delete until first non-blank character in line
- `c{` - change from current line to beginning of paragraph
- `gU}` - make paragraph uppercase
- `c{` - change paragraph (same as `cap` operator-text object)
- `>}` - indent paragraph
- `y%` - yank the entire `{...}` block
- `cgg` - change lines from cursor to top of buffer
- `ggdG` - delete contents of buffer

## Duplicate operators

Operators applied twice affect the entire line, a synonym for `<operator>_`,

```
command := [<count>] <operator> <operator>
```

Examples:

- `dd` = `d_` - delete line
- `cc` = `c_` - change line
- `yy` = `y_` - yank line
- `>>` = `>_` = `>l` - indent line
- `<<` = `<_` = `>l` - unindent line

Note: duplication does not apply to `~` or two-character operators.

## Aliases

Some commonly-used commands have aliases.

- `x` = `dl` - delete next character
- `C` = `c$` - change until the end of the line
- `D` = `d$` - delete until the end of the line
- `Y` = `yy` - yank the line
- `S` = `cc` - change the line
- `A` = `$a` - append text to end of the line
- `s` = `cl` - substitute character (delete and insert)
- `S` = `cc` - substitute line

## Filtering

Text lines can be filtered through an external program (see `:help filter`).

```
command := ! <motion> <filter>
```

Examples, using some basic utilities found on Unix platforms:

- `!8jsort` - sort the next 8 lines
- `!apsort` - sort lines in paragraph
- `!apwc -l` - replace paragraph with word count
- `!apfmt -s` - collapse whitespace in paragraph into single spaces
- `!apfmt -c` - centre lines in paragraph
- `!i(grep foo` - remove all lines in `(...)` block that don't contain `foo`
  (similar to the Ex command `:%v/foo/d`)
- `gg!Gsort` - sort all lines in buffer
- `gg!Guniq -c` - remove all duplicate lines in buffer and prefix remaining with duplicate counts

## Visual selection

Visual selection, character-wise `v`, line-wise `V` or block-wise `Ctrl+v` (all
referred to below by `{visual}`, see `:help visual-start`), followed by a
motion or text object can be used to specify a character range. An operator can
then be used to transform the text. Note the operators `gu`, `gU` and `g@`
can't be used in visual mode and text objects in visual mode, however, there
are additional ones that can (see `:help visual-operators`). A visual block is
created by entering a visual mode, then providing a motion or text object to
set the selection, or alternatively by any sequence of movement commands
(referred to by `{move-around}`).

```
visual-block := {visual} {move-around}
              | {visual} <motion>
              | {visual} <text-object>
command := <visual-block> <operator>
         | <visual-block> <visual-operator>
         | <visual-block> ! <filter>
```

Examples:

- `vtxd` = `dtx` - delete until `x`
- `vt.rx` - replace all characters with `x` until `.`
- `v3as~` - make next three sentences uppercase
- `vapU` - make paragraph uppercase
- `vapd` - delete paragraph
- `{Ctrl+v}{move-around}sfoo{Esc}` - replace each line of blockwise selection with `foo`
- `{Ctrl+v}{move-around}Ifoo{Esc}` - prepend `foo` to each line of blockwise selection
- `{Ctrl+v}{move-around}Afoo{Esc}` - append `foo` to each line of blockwise selection
- `vap!sort` - sort the lines of the current paragraph
- `vap!fmt` - use the `fmt` command-line tool to format selection into
  lines of 75 characters (similar to the `gqap` command)
- `ggvG!indent` - use the `indent` command-line tool to apply automatic
  indentation all lines of a C-code buffer
- `{visual}J` - join the highlighted lines on the current line
- `{visual}gJ` - join the highlighted lines on the current line (removing whitespace)

## Other command combinations

Beyond the above rules, there are further command keys and more restricted
combination with motions, operators and text objects.

The `.` command repeats the last change that was made.
```
command := [<count>] .
```

- `db.` - delete the previous two words
- `db4.` - delete the previous five words
- `{insert text...}` then `/{pattern}.` - insert text again before next text matching `{pattern}`

The `gn` and `gN` motions can be used with operators to move between matching
search patterns.

```
command := [<count>] <operator> gn
         | [<count>] <operator> gN
```

- `cgn` - change the next search match
- `3cgn` - change the third search match
- `cgN` - change the previous search match

Here are some other interesting and potentially useful commands that I've found
in the Vim help:

- `gf` - goto file (when cursor is on a valid filesystem path)
- `gF` - goto file and line number (line number following path)
- `J` - Join the current line with the next one (with space in between)
- `gJ` - Join the current line with the next one (without space in between)
- `3J` - join the next three lines on the current line (removing indent)
- `3gJ` - join the next three lines on the current line
- `gv` - reselect previous visual area
- `g~~` = `g~g~` - switch case of line
- `gUU` = `gUgU` - make line uppercase
- `guu` = `gugu` - make line lowercase
- `r{char}` - replace character under cursor with `{char}`
- `10r{char}` - replace the next 10 characters with `{char}`

-------------------------------

## Summary of rules

<p>
<div class="container">
<div class="row">
<div class="col-sm">
  <h2>Motions</h2>
  <p<code>&lt;motion-keys&gt;</code></p>
  <p>References: <code>:help motion</code>
    <code>:help various-motions</code></p>
  {% include 'vim-commands/motions.html' %}
</div>
<div class="col-sm">
  <h2>Operators</h2>
  <p<code>&lt;operators&gt;</code></p>
  <p>Reference: <code>:help operator</code></p>
  {% include 'vim-commands/operators.html' %}
  <h2>Visual operators</h2>
  <p<code>&lt;visual-operators&gt;</code></p>
  <p>References: <code>:help visual-operators</code></p>
  {% include 'vim-commands/visual-operators.html' %}
</div>
</div>
<div class="row">
<div class="col-sm">
  <h2>Text objects</h2>
  <p<code>&lt;text-object-keys&gt;</code></p>
  <p>References: <code>:help text-objects</code>, <code>:help objects</code></p>
  {% include 'vim-commands/text-objects.html' %}
</div>
<div class="col-sm">
  <h2>Modifiers</h2>
  <p<code>&lt;modifiers&gt;</code></p>
  <p>References: <code>:help text-objects</code></p>
  {% include 'vim-commands/modifiers.html' %}
</div>
</div>
</div>
</p>

```
count := {digits}

text-object := <text-object-keys>
             | <modifier> <text-object-keys>
             | <count> <modifier> <text-object-keys>

motion := [<count>] <motion-keys>

visual-block := {visual} {move-around}
              | {visual} <motion>
              | {visual} <text-object>

command := <motion>
         | [<count>] <operator> <text-object>
         | [<count>] <operator> <motion>
         | [<count>] <operator> <operator>
         | ! <motion> <filter>
         | <visual-block> <operator>
         | <visual-block> <visual-operator>
         | <visual-block> ! <filter>
         | [<count>] .
         | [<count>] <operator> gn
         | [<count>] <operator> gN
```

-------------------------------

## Some random commands

Just for fun, here are some random commands using the above rules to show the
variety of actions you can perform. Some might not make sense or not work, but
they might give you some ideas.

{% include 'vim-commands/random-commands.html' %}

<a name="references"></a>
## References/further reading

- [A vim Tutorial and Primer](https://danielmiessler.com/study/vim/)
- [Best of Vim Tips](http://zzapper.co.uk/vimtips.html)
- [Learn to speak vim — verbs, nouns, and modifiers!](https://yanpritzker.com/learn-to-speak-vim-verbs-nouns-and-modifiers-d7bfed1f6b2d)
- [The compositional nature of Vim](http://ismail.badawi.io/blog/2014/04/23/the-compositional-nature-of-vim/)
- [The grammar of Vim](http://rc3.org/2012/05/12/the-grammar-of-vim/)
- [Vim Cheat Sheet for Programmers](http://michael.peopleofhonoronly.com/vim/)
- [Vim Cheat Sheet](https://vim.rtorr.com/)
- [Vim Commands Cheat Sheet](https://www.fprintf.net/vimCheatSheet.html)
- [Vim Grammar](https://takac.github.io/2013/01/30/vim-grammar/)
- [Vim Text Objects: The Definitive Guide](https://blog.carbonfive.com/2011/10/17/vim-text-objects-the-definitive-guidehttps://blog.carbonfive.com/2011/10/17/vim-text-objects-the-definitive-guide//https://blog.carbonfive.com/2011/10/17/vim-text-objects-the-definitive-guide/)
- [Vim documentation](https://www.vim.org/docs.php)
- [Vim for PHP programmers](http://zmievski.org/files/talks/codeworks-2009/vim-for-php-programmers.pdf)
- [Your problem with Vim is that you don't grok vi](https://stackoverflow.com/questions/1218390/what-is-your-most-productive-shortcut-with-vim/1220118#1220118)
