# warp-sublime-text
Sublime Text package for warp (and wasp, angle)

## Warp.sublime-syntax

The one syntax of the package (Angle.sublime-syntax is retired), for wasp / warp and angle
(`.wasp`, `.warp`, `.a`, `.an`, `.ang`, `.angl`, `.angle`): keywords, soft keywords (`keyword.other.soft`: emit, on,
whenever, where, fields …), implicit names (`variable.language`: it, self, result), word operators, built-in functions, types, constants,
units and durations, double- and single-quoted strings with escapes and `$name` / `${…}` / `$(…)` / `\(…)` / `\{…}` holes, codepoints,
comments (`// `, `# `, nesting `/* */` and `/# #/`), keys, tags, `:=` getters, `|` pipes and `!` run-time blocks.

The word lists are generated from warp's sources (~/dev/angles/warp), never edited by hand:

    scripts/update_words.py [path to warp]   # rewrites the GENERATED variables and Warp.sublime-completions
    scripts/check_syntax.py                  # YAML, regexes, completions JSON and syntax_test_warp.warp, headless

`update_words.py` fails when a hard or soft keyword (warp's src/lowering/soft_keywords.rs) gets no scope, or when a
keyword is missing from warp's wiki/keyword.md, the page that documents them all.

`check_syntax.py` runs the syntax tests with syntect's `syntest`
(`git clone https://github.com/trishume/syntect && cargo build --release --example syntest`, or set `$SYNTEST`).
