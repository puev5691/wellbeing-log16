import unittest

class TestImports(unittest.TestCase):
    def test_import_modules(self):
        import log16.config
        import log16.storage.cards
        import log16.storage.layout
        import log16.review.decisions

        self.assertTrue(log16.config.runtime_root())
