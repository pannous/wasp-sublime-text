#!/usr/bin/env python3
"""Checks the package without opening Sublime Text: the syntaxes parse as YAML, every match compiles once its
{{variables}} are substituted, the completions are JSON, and the syntax tests (syntax_test_*) pass under syntect's
syntest runner (https://github.com/trishume/syntect, `cargo build --release --example syntest`), found at $SYNTEST.

usage: scripts/check_syntax.py
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import regex  # closer to Sublime's Oniguruma than re: possessive quantifiers, \h
import yaml

PACKAGE = Path(__file__).resolve().parent.parent
SYNTEST = Path(os.environ.get("SYNTEST", "~/.cargo/shared-target.noindex/release/examples/syntest")).expanduser()
VARIABLE = re.compile(r"\{\{(\w+)\}\}")
ONIGURUMA_ONLY = {r"\h": "[0-9a-fA-F]"}


def sublime_json(text):
	"""Sublime's JSON allows // comments and trailing commas"""
	text = re.sub(r"^\s*//.*$", "", text, flags=re.M)
	return json.loads(re.sub(r",(\s*[\]}])", r"\1", text))


def substituted(pattern, variables):
	while VARIABLE.search(pattern):
		pattern = VARIABLE.sub(lambda match: variables[match.group(1)], pattern)
	for oniguruma, equivalent in ONIGURUMA_ONLY.items():
		pattern = pattern.replace(oniguruma, equivalent)
	return pattern


def patterns(node):
	if isinstance(node, dict):
		if "match" in node:
			yield node["match"]
		for value in node.values():
			yield from patterns(value)
	elif isinstance(node, list):
		for item in node:
			yield from patterns(item)


def check_syntax(path):
	syntax = yaml.safe_load(path.read_text())
	variables = syntax.get("variables", {})
	failures = []
	for pattern in patterns(syntax["contexts"]):
		try:
			regex.compile(substituted(pattern, variables))
		except (regex.error, KeyError) as problem:
			failures.append(f"{path.name}: {pattern!r}: {problem}")
	return failures


def run_syntax_tests():
	if not SYNTEST.exists():
		return [f"no syntest runner at {SYNTEST}: build syntect's example or set $SYNTEST"]
	failures = []
	for test in sorted(PACKAGE.glob("syntax_test_*")):
		run = subprocess.run([SYNTEST, test, PACKAGE], capture_output=True, text=True)
		if run.returncode:
			failures.append(run.stdout + run.stderr)
		else:
			print(run.stdout.strip().splitlines()[-2])
	return failures


if __name__ == "__main__":
	problems = [failure for path in sorted(PACKAGE.glob("*.sublime-syntax")) for failure in check_syntax(path)]
	for completions in sorted(PACKAGE.glob("*.sublime-completions")):
		try:
			sublime_json(completions.read_text())
		except json.JSONDecodeError as problem:
			problems.append(f"{completions.name}: {problem}")
	problems += run_syntax_tests()
	print("\n".join(problems) or "all checks passed")
	sys.exit(1 if problems else 0)
