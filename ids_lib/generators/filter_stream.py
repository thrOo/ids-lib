def exclude_filter(item, filter):
    try:
        for column, exclude in filter.items():
            if item[column] == exclude:
                return False
            else:
                return True
    except IndexError:
        raise SystemExit('ERROR:  exclude_filter could not find specified index! check your filter_set')


def trim_filter(item, filter):
    item_length = len(item)
    for index in sorted(filter, reverse=True):
        if index < (item_length - 1):
            del item[index]
    return item


def filter_generator(item_generator, filter_set):
    for item in item_generator:
        if 'exclude' in filter_set:
            if exclude_filter(item, filter_set['exclude']):
                if 'trim' in filter_set:
                    yield trim_filter(item, filter_set['trim'])
                else:
                    yield item
        elif 'trim' in filter_set:
            yield trim_filter(item, filter_set['trim'])
        else:
            yield item