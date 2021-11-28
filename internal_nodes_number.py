def find_internal_nodes_num(tree: list[int]) -> int:
    """ find total number of internal nodes of a tree
        the tree is composed of consecutive integers start from 0 and including 0
        if node is root, -1 is used to denoted as its parent node

    Args:
        tree (list[int]): the list which contains the parent node of each tree node

    return:
        the total number of internal nodes
    """
    num: int = 0
    if tree is not None and -1 in tree:
        root: int = tree.index(-1)
        for i in tree:
            if i != root and i != -1:
                num += 1
    else:
        print("input tree is invalid!")

    return num

def find_internal_nodes_num_refined(tree: list[int]) -> int:
    """ find total number of internal nodes of a tree
        the tree is composed of consecutive integers start from 0 and including 0
        if node is root, -1 is used to denoted as its parent node

    Args:
        tree (list[int]): the list which contains the parent node of each tree node

    return:
        the total number of internal nodes
    """
    if tree is not None and -1 in tree:
        root: int = tree.index(-1)
        internal_nodes = set()
        for i in tree:
            if i != root and i != -1:
                internal_nodes.add(i)

        return len(internal_nodes)
    else:
        print("input tree is invalid!")
        return 0

if __name__ == '__main__':
    my_tree = [4, 4, 1, 5, -1, 4, 5]
    print(find_internal_nodes_num(my_tree))
    print(find_internal_nodes_num_refined(my_tree))