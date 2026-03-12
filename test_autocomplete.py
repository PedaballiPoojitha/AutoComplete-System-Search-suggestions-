import unittest

from autocomplete import AutocompleteSystem


class TestAutocompleteSystem(unittest.TestCase):
    def setUp(self):
        self.ac = AutocompleteSystem()
        # insert some initial words
        self.ac.insert("hello", 10)
        self.ac.insert("hell", 5)
        self.ac.insert("heaven", 3)
        self.ac.insert("heavy", 1)

    def test_top_k_basic(self):
        self.assertEqual(self.ac.top_k("he", 2), [("hello", 10), ("hell", 5)])
        self.assertEqual(self.ac.top_k("hel", 5), [("hello", 10), ("hell", 5)])
        self.assertEqual(self.ac.top_k("hea", 2), [("heaven", 3), ("heavy", 1)])

    def test_insert_and_update(self):
        # inserting word that already exists should increase frequency
        self.ac.insert("hell", 2)
        self.assertEqual(self.ac.top_k("hel", 2), [("hello", 10), ("hell", 7)])

        # explicit update
        self.ac.update("heaven", 8)
        self.assertEqual(self.ac.top_k("hea", 2), [("heaven", 8), ("heavy", 1)])

    def test_nonexistent_prefix(self):
        self.assertEqual(self.ac.top_k("xyz", 3), [])

    def test_update_nonexistent(self):
        with self.assertRaises(KeyError):
            self.ac.update("unknown", 1)


if __name__ == "__main__":
    unittest.main()
