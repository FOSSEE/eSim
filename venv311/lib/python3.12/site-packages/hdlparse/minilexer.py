# -*- coding: utf-8 -*-
# Copyright © 2017 Kevin Thibedeau
# Distributed under the terms of the MIT license
import re
import logging

"""Minimalistic lexer engine inspired by the PyPigments RegexLexer"""

__version__ = '1.0.7'

log = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
log.addHandler(handler)


class MiniLexer(object):
    """Simple lexer state machine with regex matching rules"""

    def __init__(self, tokens, flags=re.MULTILINE):
        """Create a new lexer

        Args:
          tokens (dict(match rules)): Hierarchical dict of states with a list of regex patterns and transitions
          flags (int): Optional regex flags
        """
        self.tokens = {}

        # Pre-process the state definitions
        for state, patterns in tokens.items():
            full_patterns = []
            for p in patterns:
                pat = re.compile(p[0], flags)
                action = p[1]
                new_state = p[2] if len(p) >= 3 else None

                # Convert pops into an integer
                if new_state and new_state.startswith('#pop'):
                    try:
                        new_state = -int(new_state.split(':')[1])
                    except ValueError:
                        new_state = -1
                    except IndexError:
                        new_state = -1

                full_patterns.append((pat, action, new_state))
            self.tokens[state] = full_patterns

    def run(self, text):
        """Run lexer rules against a source text

        Args:
          text (str): Text to apply lexer to

        Yields:
          A sequence of lexer matches.
        """

        stack = ['root']
        pos = 0

        patterns = self.tokens[stack[-1]]

        while True:
            for pat, action, new_state in patterns:
                m = pat.match(text, pos)
                if m:
                    if action:
                        log.debug(f"Match: {m.group().strip()} -> {action}")

                        yield (pos, m.end() - 1), action, m.groups()

                    pos = m.end()

                    if new_state:
                        if isinstance(new_state, int):  # Pop states
                            del stack[new_state:]
                        else:
                            stack.append(new_state)

                        patterns = self.tokens[stack[-1]]

                    break

            else:
                try:
                    if text[pos] == '\n':
                        pos += 1
                        continue
                    pos += 1
                except IndexError:
                    break
