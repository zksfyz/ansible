#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys


def main():
    skip = set([
        'test/sanity/code-smell/%s' % os.path.basename(__file__),
        'docs/docsite/rst/dev_guide/testing/sanity/no-smart-quotes.rst',
        'test/integration/targets/unicode/unicode.yml',
        'test/integration/targets/lookup_properties/lookup-8859-15.ini',
    ])

    for path in sys.argv[1:] or sys.stdin.read().splitlines():
        if path in skip:
            continue

        with open(path, 'rb') as path_fd:
            for line, text in enumerate(path_fd.readlines()):
                try:
                    text = text.decode('utf-8')
                except UnicodeDecodeError as ex:
                    print('%s:%d:%d: UnicodeDecodeError: %s' % (path, line + 1, ex.start + 1, ex))
                    continue

                match = re.search(u'([‘’“”])', text)

                if match:
                    print('%s:%d:%d: use ASCII quotes `\'` and `"` instead of Unicode quotes' % (
                        path, line + 1, match.start(1) + 1))


if __name__ == '__main__':
    main()
