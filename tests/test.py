import unittest

from hivemind import create_app
from hivemind.config import TestingConfig
from hivemind.core.extensions import db


class WatchlistTestCase(unittest.TestCase):
    
    # Setup run before every test
    def setUp(self):
        self.app = create_app(TestingConfig)

        # Create test client and test CLI runner
        self.client = self.app.test_client()
        self.runner = self.app.test_cli_runner()

    # Cleanup run after every test
    def tearDown(self):
        with self.app.test_request_context():
            db.drop_all()
            db.session.close()
            db.session.remove()
    
    # Testing app creation
    def test_app_exist(self):
        self.assertIsNotNone(self.app)
    
    def test_app_is_testing(self):
        self.assertTrue(self.app.config['TESTING'])

# Run tests
if __name__ == '__main__':
    unittest.main()