import os
import unittest
from database import DbClass, Sport, Event, Selection

test_db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/TestSportsBook.db')

class TestDatabase(unittest.TestCase):
    """Unit test class for DbClass class"""

    @classmethod
    def setUpClass(cls):
        """Set up necessary parameter's values """
        cls.db = DbClass(test_db_file)
        cls.db.connection()
        cls.number_sports = 0
        cls.number_events = 0
        cls.number_selections = 0

    def test_get_sports(self):
        """Test get_sports() function"""
        rows = TestDatabase.db.get_sports()
        self.assertEqual(len(rows), TestDatabase.number_sports)

    def test_insert_sport(self):
        """Test insert_sport() function"""
        sport = Sport(None, "sport1", "sport1_slug", None)
        TestDatabase.db.insert_sport(sport)
        rows = TestDatabase.db.get_sports()
        self.assertEqual(len(rows), TestDatabase.number_sports + 1)
        newrowindex = TestDatabase.number_sports
        self.assertEqual(rows[newrowindex][0], newrowindex + 1)
        self.assertEqual(rows[newrowindex][1], "sport1")
        self.assertEqual(rows[newrowindex][2], "sport1_slug")
        self.assertEqual(rows[newrowindex][3], 0)
        TestDatabase.number_sports += 1

        sport = Sport(10, "sport2", "sport2_slug", 1)
        TestDatabase.db.insert_sport(sport)
        rows = TestDatabase.db.get_sports()
        self.assertEqual(len(rows), TestDatabase.number_sports + 1)
        newrowindex = TestDatabase.number_sports
        self.assertEqual(rows[newrowindex][0], newrowindex + 1)
        self.assertEqual(rows[newrowindex][1], "sport2")
        self.assertEqual(rows[newrowindex][2], "sport2_slug")
        self.assertEqual(rows[newrowindex][3], 1)
        TestDatabase.number_sports += 1

    @classmethod
    def tearDownClass(cls):
        cls.db.disconnection()
        os.remove(test_db_file)


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestDbClass)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
