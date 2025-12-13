import unittest
from unittest.mock import patch, MagicMock
from services.providers.apollo_provider import ApolloLeadProvider

class TestApolloProvider(unittest.TestCase):
    def setUp(self):
        self.provider = ApolloLeadProvider(api_key="test_key")

    @patch('services.providers.apollo_provider.requests.post')
    def test_fetch_leads_success(self, mock_post):
        # Mock API Response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "people": [
                {
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "john@example.com",
                    "organization": {"name": "Test Corp"},
                    "phone_numbers": ["123-456-7890"]
                }
            ]
        }
        mock_post.return_value = mock_response

        # Call method
        leads = self.provider.fetch_leads("Tech", "NY")

        # Assertions
        self.assertEqual(len(leads), 1)
        self.assertEqual(leads[0]['company_name'], "Test Corp")
        self.assertEqual(leads[0]['email'], "john@example.com")
        self.assertEqual(leads[0]['score'], 90) # 50 base + 20 email + 20 phone

        # Verify API called with correct payload
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs['headers']['X-Api-Key'], "test_key")
        self.assertEqual(kwargs['json']['q_organization_keyword_tags'], ["Tech"])

if __name__ == '__main__':
    unittest.main()
