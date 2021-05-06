from .basics import searchtree


def is_iru(tree, noun):
    ''' Determine the AI path for the noun. If it matches on of the relations
        return True
    '''
    successful_paths = ['living thing:person', 'living thing:animal',
                        'living thing:spirit', 'living thing:occupation']
    my_path = []
    searchtree(noun, my_path, tree, None)
    my_path.reverse()
    my_path = ':'.join(my_path)
    return my_path in successful_paths
