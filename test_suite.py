"""
PromptCraft AI - Comprehensive Test Suite
Validates all Flask endpoints, categories, error handling, heuristic scoring, and edge cases.
"""

import unittest
import json
from app import app, evaluate_prompt_quality, GENERATORS, STYLE_PRESETS

class PromptCraftTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_health_endpoint(self):
        """Test the healthcheck endpoint."""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data.get('status'), 'ok')
        self.assertEqual(data.get('app'), 'PromptCraft AI')

    def test_index_page(self):
        """Test that the main page loads with 200 OK and contains essential titles."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn("PromptCraft AI", html)
        self.assertIn("One Idea. Any Prompt.", html)
        self.assertIn("Universal Prompt Generator", html)
        self.assertIn("Quick Examples", html)
        self.assertIn("Introduction to Prompt Engineering", html)
        self.assertIn("style.css", html)
        self.assertIn("script.js", html)

    def test_api_examples(self):
        """Test fetching curated examples."""
        response = self.app.get('/api/examples')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data.get('status'), 'success')
        self.assertEqual(len(data.get('examples')), 6)

    def test_generate_all_categories(self):
        """Test generating prompts across all 7 supported categories."""
        categories = ['image', 'video', 'website', 'code', 'study', 'writing', 'custom']
        for cat in categories:
            payload = {
                "category": cat,
                "idea": f"Test prompt creation for {cat} domain with realistic scenario",
                "style": "futuristic",
                "instructions": "Ensure clean execution and 16:9 ratio where applicable",
                "variation": 0
            }
            response = self.app.post('/api/generate',
                                    data=json.dumps(payload),
                                    content_type='application/json')
            self.assertEqual(response.status_code, 200, f"Failed for category: {cat}")
            data = json.loads(response.data)
            self.assertEqual(data.get('status'), 'success')
            res = data.get('data', {})
            self.assertEqual(res.get('category'), cat)
            self.assertTrue(len(res.get('generated_prompt')) > 50)
            self.assertIn('quality', res)
            self.assertGreaterEqual(res['quality']['total_score'], 35)

    def test_generate_all_styles(self):
        """Test all 6 styles."""
        styles = ['cinematic', 'minimal', 'professional', 'futuristic', 'technical', 'creative']
        for style in styles:
            payload = {
                "category": "image",
                "idea": f"A serene mountain peak at twilight, {style} style",
                "style": style,
                "instructions": "",
                "variation": 1
            }
            response = self.app.post('/api/generate',
                                    data=json.dumps(payload),
                                    content_type='application/json')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data.get('status'), 'success')
            self.assertEqual(data['data']['style'], style)

    def test_empty_input_validation(self):
        """Empty idea input should return 400 Bad Request with helpful error message."""
        payload = {
            "category": "image",
            "idea": "   ",
            "style": "futuristic"
        }
        response = self.app.post('/api/generate',
                                data=json.dumps(payload),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data.get('status'), 'error')
        self.assertIn("Please enter an idea", data.get('message', ''))

    def test_long_input_validation(self):
        """Input exceeding 3000 chars should return 400."""
        payload = {
            "category": "code",
            "idea": "a" * 3500,
            "style": "technical"
        }
        response = self.app.post('/api/generate',
                                data=json.dumps(payload),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data.get('status'), 'error')
        self.assertIn("Input is too long", data.get('message', ''))

    def test_special_characters_and_unicode(self):
        """Test handling of quotes, HTML brackets, emojis, and symbols."""
        payload = {
            "category": "website",
            "idea": "Create a portal for <AI & Robotics> with emojis 🚀✨ & 'quotes' & \"double-quotes\" & Japanese: 東京",
            "style": "futuristic",
            "instructions": "HTML entities <script>alert(1)</script> shouldn't break anything"
        }
        response = self.app.post('/api/generate',
                                data=json.dumps(payload),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("東京", data['data']['generated_prompt'])

    def test_quality_analysis_endpoint(self):
        """Test on-demand quality evaluation endpoint."""
        payload = {
            "prompt": "# Master Prompt\n**Role:** Senior Architect\n**Task:** Create high performance API\n- Step 1: Design schema\n- Step 2: Implement handlers",
            "idea": "High performance API",
            "category": "code",
            "style": "technical"
        }
        response = self.app.post('/api/analyze',
                                data=json.dumps(payload),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data.get('status'), 'success')
        self.assertIn('quality', data)
        q = data['quality']
        self.assertGreater(q['total_score'], 50)
        self.assertIn('breakdown', q)
        self.assertIn('suggestions', q)


if __name__ == '__main__':
    unittest.main()
