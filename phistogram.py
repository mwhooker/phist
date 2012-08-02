#!/usr/bin/env python

import math

from collections import defaultdict, Mapping


class Histogram(object):

    SCALES = ('linear', 'log', 'ratio')
    SORTS = ('keys', 'values')

    def __init__(self, dataset):
        """return visual histogram of d."""

        if isinstance(dataset, Mapping):
            self.dataset = dataset
        self.dataset = self._from_list(dataset)

    def format(self, scale='linear', sort='keys', **kwargs):

        assert scale in self.SCALES
        assert sort in self.SORTS

        sorting_bin = []
        output = []

        for key in self.dataset:
            sorting_bin.append((self.dataset[key], key))

        if sort == 'keys':
            sorting_bin.sort(key=lambda k: k[1])
        else:
            sorting_bin.sort()

        for val, name in sorting_bin:
            output.append("%s (%s)" % (
                getattr(self, "_scale_%s" % scale)(val, **kwargs),
                name
            ))

        return '\n'.join(output)

    def _scale_linear(self, val):
        return int(val) * '*'

    def _scale_log(self, val, base=10):
        if base == 10:
            log_val = math.log10(val)
        else:
            log_val = math.log(val, base)

        return int(log_val) * '*'

    def _scale_ratio(self, val, line_width=80):
        max_val = max(self.dataset.values())
        factor = line_width / max_val
        return self._scale_linear(int(val * factor))

    def __str__(self):
        return self.format()

    def _from_list(self, l):
        """compile list into histogram."""
        d = defaultdict(int)

        for i in l:
            d[i] += 1

        return d


def test():
    import operator
    print Histogram({
        'a': 1,
        'b': 10,
        'c': 100,
        'j': 1000,
        'e': 10000
    }).format(scale='log', sort='keys')
    for scale in Histogram.SCALES:
        print "[%s]" % scale
        print Histogram(
            reduce(operator.add, [range(i) for i in range(20)])
        ).format(scale=scale)


if __name__ == '__main__':
    import sys
    from itertools import imap

    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            hist = Histogram(imap(str.strip, f.readlines()))
    else:
        hist = Histogram(sys.stdin)
    sys.stdout.write(hist.format())
    sys.stdout.write("\n")