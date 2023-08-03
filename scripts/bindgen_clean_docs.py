#!/usr/bin/env python3
"""Replace parameters """


# TODO: refactor into (1) extracting doc comments, then (2) doing replacements
# on their text

import re
import sys

from typing import TextIO

EMPTY_DOC = "#[doc = \"\"]"
PARAM_HEADER = "#[doc = \"# Parameters\"]"
DOC_PARAM_PATTERN = re.compile(
    r"^(?P<lead_ws>\s*)(?P<pfx>#\[doc\s*=\s*\")\s*@(?P<param>\w+)(?P<rest>.*)"
)
DOC_PARAM_CONT_PATTERN = re.compile(
    r"^(?P<lead_ws>\s*)(?P<pfx>#\[doc\s*=(\t|  ))"
)

def map_single_param(match: re.Match) -> str:
    lead_ws = match.group("lead_ws")
    pfx = match.group("pfx")
    param = match.group("param")
    rest = match.group("rest")
    return f"{lead_ws}{pfx} - `{param}`: {rest}"


def replace_doc_params(old_lines: [str]) -> [str]:
    new_lines = []
    idx = 0

    while idx < len(old_lines):
        line = old_lines[idx].strip("\n\r")
        match = DOC_PARAM_PATTERN.fullmatch(line)

        if "@" in line:
            print(f"line: `{line}`")

        if not bool(match):
            new_lines.append(line)
            idx += 1
            continue

        lead_ws = match.group("lead_ws")

        new_lines.append(f"{lead_ws}{EMPTY_DOC}")
        new_lines.append(f"{lead_ws}{PARAM_HEADER}")
        new_lines.append(map_single_param(match))

        sub_idx = 1

        while sub_idx < len(old_lines) - idx:
            # Extract all parameters in the same block
            print(sub_idx)

            sub_line=old_lines[idx + sub_idx].strip("\n\r")
            print(f"sub_line: `{sub_line}`")
            
            submatch = match = DOC_PARAM_PATTERN.fullmatch(sub_line)
            if submatch:
                # We have a matching group
                print("submatch")
                old_lines.append(map_single_param(submatch))
            elif DOC_PARAM_CONT_PATTERN.fullmatch(sub_line):
                # continuation of previous parameter
                old_lines.append(sub_line)
                print("submtab")
            else:
                break

            sub_idx += 1

        idx += sub_idx

    return new_lines

        


def main():
    if len(sys.argv) != 2:
        print ("expected a single path argument")
        sys.exit(1)
    
    with open(sys.argv[1], "r") as f:
        lines = f.readlines()
    
    with open("out.rs", "w") as f:
        f.writelines("\n".join(replace_doc_params(lines)))

        

        
        
    

if __name__ == "__main__":
    main()
