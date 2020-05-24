import unittest
from webtest import TestApp
from COVID_19_Monitor import app
test_app=TestApp(app)
resp= test_app.get("/")


class test_form(unittest.TestCase):
    def test_response(self):
        self.assertEqual(resp.status,'200 OK')
    
        
if __name__=='__main__':
    unittest.main()