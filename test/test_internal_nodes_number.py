import unittest
from internal_nodes_number import find_internal_nodes_num, find_internal_nodes_num_refined


class TestInternalNodesNumber(unittest.TestCase):
    """Unit test class for internal nodes number functions"""

    def setUp(self):
        """Set up necessary parameter's values """

    def test_find_internal_nodes_num(self):
        """Test find_internal_nodes_num() function """
        empty_tree = []
        self.assertEqual(find_internal_nodes_num(empty_tree), 0)
        tree_without_minus_one = [ 1, 2, 3, 4, 5]
        self.assertEqual(find_internal_nodes_num(tree_without_minus_one), 0)
        tree = [4, 4, 1, 5, -1, 4, 5]
        self.assertEqual(find_internal_nodes_num(tree), 3)

    def test_find_internal_nodes_num_refined(self):
        """Test find_internal_nodes_num_refined() function """
        empty_tree = []
        self.assertEqual(find_internal_nodes_num_refined(empty_tree), 0)
        tree_without_minus_one = [ 1, 2, 3, 4, 5]
        self.assertEqual(find_internal_nodes_num_refined(tree_without_minus_one), 0)
        tree = [4, 4, 1, 5, -1, 4, 5]
        self.assertEqual(find_internal_nodes_num_refined(tree), 2)

    def tearDown(self):
        """The unit test tearDown() function """


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestInternalNodesNumber)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
