# wasp-sublime-text
wasp sublime text plugin

## Wasp.sublime-syntax

Highlighting for wasp / warp (`.wasp`, `.warp`): keywords, word operators, built-in functions, types, constants,
units and durations, double- and single-quoted strings with escapes and `$name` / `${…}` / `\(…)` holes, codepoints,
comments (`//`, `#`, nesting `/* */` and `/# #/`), keys, tags, `:=` getters, `|` pipes and `!` run-time blocks.

The word lists are generated from warp's sources (~/dev/angles/warp), never edited by hand:

    scripts/update_words.py [path to warp]   # rewrites the GENERATED variables and Wasp.sublime-completions
    scripts/check_syntax.py                  # YAML, regexes, completions JSON and syntax_test_wasp.wasp, headless

`check_syntax.py` runs the syntax tests with syntect's `syntest`
(`git clone https://github.com/trishume/syntect && cargo build --release --example syntest`, or set `$SYNTEST`).
