def dataset_generator(list_generator):
    """returns generator for each item in list_generator"""
    for x in list_generator:
        yield x
