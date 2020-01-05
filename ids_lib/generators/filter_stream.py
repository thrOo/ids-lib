def exclude_filter(item, exclude_filters):
    """compares each column,filter pair in exclude_filters

        if one of them is true it returns False to exclude that item
        else it returns true

        Parameters
        ----------
        item : list
            current systemcall
        exclude_filters: dict
            column, exclude pairs

        Raises
        ------
        IndexError
            If index of column,filter pair is out of bounds
    """
    try:
        for column, exclude in exclude_filters.items():
            if item[column] == exclude:
                return False
        return True
    except IndexError:
        raise SystemExit('ERROR:  exclude_filter could not find specified index! check your filter_set')


def trim_filter(item, trim_filters):
    """removes given indices from item

        Parameters
        ----------
        item : list
            current systemcall
        trim_filters: list
            indices to delete
    """
    item_length = len(item)
    # sorting and reversing indices to prevent index shifts while deleting
    for index in sorted(trim_filters, reverse=True):
        if index < (item_length - 1):
            del item[index]
    return item


def filter_generator(item_generator, filter_set):
    """applies exclusion and trim filter if given

        Parameters
        ----------
        item_generator : generator
            yieldable systemcalls
        filter_set: dict
            filter_set with exclusions and/or trims

            format of filter_set = {
                'exclude': {
                    column: 'str',
                    ...
                },
                'trim': [ column, ... ]
            }
    """
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