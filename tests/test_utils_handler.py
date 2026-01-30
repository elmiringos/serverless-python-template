import unittest
from src.application.handler.utils_handler import health_handler

class TestUtilsHandler(unittest.TestCase):
    def test_health_handler(self):
        # Mock event and context
        mock_event = {}
        mock_context = {}

        # Call the health_handler
        response = health_handler(mock_event, mock_context)

        # Check the response
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['body'], '{"status": "healthy", "message": "Service is running smoothly."}')

if __name__ == '__main__':
    unittest.main()
