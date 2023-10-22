import unittest
from app import app  # Import your Flask application and other necessary components
from models import db, User


class BloglyTestCase(unittest.TestCase):

    def setUp(self):
        with app.app_context():
            self.client = app.test_client()
            app.config['TESTING'] = True
            app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'

            db.create_all()

            user = User(first_name="Test", last_name="User", image_url="test.jpg")
            db.session.add(user)
            db.session.commit()

            self.user_id = user.id

    def tearDown(self):
        with app.app_context():
            db.session.rollback()
            db.drop_all()
            

    def test_list_users(self):
        
        
        response = self.client.get('/')
        self.assertIn(b'Test User', response.data)

    def test_new_user_form(self):
        
        
        response = self.client.get('/users/new')
        self.assertIn(b'First Name', response.data)

    def test_user_detail(self):
        
        
        response = self.client.get(f'/users/{self.user_id}')
        self.assertIn(b'Test User', response.data)
        
    def test_edit_user_form(self):
        
        
        response = self.client.get(f'/users/{self.user_id}/edit')
        self.assertIn(b'Edit a User', response.data)
        
if __name__ == "__main__":
    unittest.main()
