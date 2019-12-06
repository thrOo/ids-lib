import itertools
from _collections import deque


def n_gram_generator(item_generator, n, step_size=1):
    buffer = deque([], maxlen=n)
    try:
        for _ in itertools.repeat(None, n):
            buffer.append(item_generator.__next__())
        yield tuple(buffer)
    except StopIteration:
        return
    while True:
        try:
            for _ in itertools.repeat(None, step_size):
                buffer.append(item_generator.__next__())
            if len(buffer) == n:
                yield tuple(buffer)
        except StopIteration:
            break


""""
array = [('a', 'a2', 'a3'),
         ('b', 'b2', 'b3'),
         ('c', 'c2', 'c3'),
         ('d', 'd2', 'd3'),
         ('e', 'e2', 'e3'),
         ('f', 'f2', 'f3'),
         ('g', 'g2', 'g3'),
         ('h', 'h2', 'h3'),
         ('i', 'i2', 'i3'),
         ('j', 'j2', 'j3')]

for x in n_gram_generator((x for x in array), 3, step_size=3):
    print(x)
"""
