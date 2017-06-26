#!/usr/bin/env python3

"""
Inject README.rst to __init__.py and cli.py

README.rst has to have a section "CLI" followed by "Python interface".
The section "CLI" has to be underlined by "-".

"""

from __future__ import print_function

import re


def stripout_docstring(file, keep_title):
    pre_lines = []
    post_lines = []
    for line in file:
        pre_lines.append(line)
        if re.match('^r?["\']{3}$', line):
            is_in_title = True
            for line in file:
                if re.match('^["\']{3}$', line):
                    post_lines.append(line)
                    break
                if keep_title and is_in_title:
                    pre_lines.append(line)
                    if line.strip() == '':
                        is_in_title = False
            break

    post_lines.extend(file)
    return pre_lines, post_lines


def inject_rst(path, rst, keep_title=False):
    with open(path) as file:
        pre_lines, post_lines = stripout_docstring(file, keep_title)
    rst_str = ''.join(rst)
    if keep_title:
        rst_str = rst_str.strip() + '\n'
    with open(path, 'w') as file:
        file.writelines(pre_lines)
        file.write(rst_str)
        file.writelines(post_lines)


def inject_readme(readme, init_py, cli_py):
    init_rst = []
    cli_rst = []
    with open(readme) as file:
        for line in file:
            if line.rstrip() == 'CLI':
                next_line = next(file)
                if not re.match('^-+$', next_line):
                    raise RuntimeError('Unrecognized line after CLI: {}'
                                       .format(next_line))
                for line in file:
                    if line.rstrip() == 'Python interface':
                        break
                    cli_rst.append(line)
            init_rst.append(line)

    inject_rst(init_py, init_rst)
    inject_rst(cli_py, cli_rst, keep_title=True)


def make_parser(doc=__doc__):
    import argparse
    parser = argparse.ArgumentParser(
        formatter_class=type('FormatterClass',
                             (argparse.RawDescriptionHelpFormatter,
                              argparse.ArgumentDefaultsHelpFormatter),
                             {}),
        description=doc)
    parser.add_argument('readme', nargs='?', default='README.rst')
    parser.add_argument('--init-py', default='src/dictsdiff/__init__.py')
    parser.add_argument('--cli-py', default='src/dictsdiff/cli.py')
    return parser


def main(args=None):
    parser = make_parser()
    ns = parser.parse_args(args)
    inject_readme(**vars(ns))


if __name__ == '__main__':
    main()
