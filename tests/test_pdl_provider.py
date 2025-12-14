import unittest
from unittest.mock import patch, MagicMock
from services.providers.pdl_provider import PDLLeadProvider

class TestPDLProvider(unittest.TestCase):
    def setUp(self):
        self.provider = PDLLeadProvider(api_key="test_pdl_key")

    @patch('services.providers.pdl_provider.requests.get')
    def test_fetch_leads_success(self, mock_get):
        # Mock API Response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "full_name": "Jane Doe",
                    "job_company_name": "Tech Corp",
                    "emails": [{"address": "jane@techcorp.com"}],
                    "phone_numbers": ["555-0199"],
                    "linkedin_url": "http://linkedin.com/in/jane"
                }
            ]
        }
        mock_get.return_value = mock_response

        # Call method
        leads = self.provider.fetch_leads("Software", "San Francisco")

        # Assertions
        self.assertEqual(len(leads), 1)
        self.assertEqual(leads[0]['company_name'], "Tech Corp")
        self.assertEqual(leads[0]['contact_name'], "Jane Doe")
        self.assertEqual(leads[0]['email'], "jane@techcorp.com")
        self.assertEqual(leads[0]['phone'], "555-0199")
        # Score check: 60 base + 15 mobile (assumed from phone) + 10 linkedin = 85?
        # Actually logic says 'mobile_phone' key needed for +15, 'work_email' for +15.
        # Our mock didn't provide 'work_email' or 'mobile_phone' explicitly in keys,
        # just 'emails' and 'phone_numbers'.
        # Let's check the score logic in code:
        # if person.get('work_email'): score += 15
        # if person.get('mobile_phone'): score += 15
        # if person.get('linkedin_url'): score += 10
        # So score should be 60 + 10 = 70.
        self.assertEqual(leads[0]['score'], 70)

        # Verify API called with correct SQL
        args, kwargs = mock_get.call_args
        self.assertEqual(kwargs['headers']['X-Api-Key'], "test_pdl_key")
        self.assertIn("SELECT * FROM person", kwargs['params']['sql'])
        self.assertIn("LIKE '%Software%'", kwargs['params']['sql'])
        self.assertIn("LIKE '%San Francisco%'", kwargs['params']['sql'])

if __name__ == '__main__':
    unittest.main()
