import unittest
from datetime import datetime
from app import app, db
from app.models import Building, StudySpace, User, Post

def uniqueEmailException():
    try:
        User.query.all()
    except:
        raise Exception('Emails not unique')

def uniqueUsernameException():
    try:
        User.query.all()
    except:
        raise Exception('Usernames not unique')

def uniqueBuildingNameException():
    try:
        Building.query.all()
    except:
        raise Exception('Building names not unique')

class BuildingAndStudySpace(unittest.TestCase):
    
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_BuildingFields(self):
        building = Building(name = 'Cornell Library')
        self.assertTrue(building.name == 'Cornell Library')
    
    def test_UniqueBuildingName(self):
        building1 = Building(name = 'Parrish')
        building2 = Building(name = 'Parrish')
        db.session.add(building1)
        db.session.add(building2)
        with self.assertRaises(Exception) as context:
            uniqueBuildingNameException()
        self.assertTrue('Building names not unique' in str(context.exception))
    
    def test_StudySpaceFields(self):
        space = StudySpace(name = '101', building_id = 0, lat = 12.34, long = -75.12)
        self.assertTrue(space.name == '101')
        self.assertTrue(space.building_id == 0)
        self.assertTrue(space.lat == 12.34)
        self.assertTrue(space.long == -75.12)
    
    def test_BuildingAndStudySpaceRelationship(self):
        building = Building(name = 'Parrish')
        space = StudySpace(name = 'Shane Lounge', lat = 12.34, \
            long = -75.12, building = building)
        space2 = StudySpace(name = 'Parlor West', lat = 12.34, \
            long = -75.12, building = building)

        self.assertTrue(building.studySpaces.all()[0].name == 'Shane Lounge')
        self.assertTrue(space.building.name == 'Parrish')

        self.assertTrue(building.studySpaces.all()[1].name == 'Parlor West')
        self.assertTrue(space2.building.name == 'Parrish')
     
class UserAndPost(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_UserFields(self):
        u = User(username='susan', email = "susan@email.com")
        self.assertTrue(u.username == 'susan')
        self.assertTrue(u.email == 'susan@email.com')
    
    def test_UniqueUsername(self):
        u1 = User(username='susan', email = "susan@email.com")
        u2 = User(username='susan', email = "susan@susan.com")
        db.session.add(u1)
        db.session.add(u2)
        with self.assertRaises(Exception) as context:
            uniqueUsernameException()
        self.assertTrue('Usernames not unique' in str(context.exception))

    def test_UniqueEmail(self):
        u1 = User(username='susan', email = "susan@email.com")
        u2 = User(username='bob', email = "susan@email.com")
        db.session.add(u1)
        db.session.add(u2)
        with self.assertRaises(Exception) as context:
            uniqueEmailException()
        self.assertTrue('Emails not unique' in str(context.exception))
        
    def test_password_hashing(self):
        u = User(username='susan', email = "susan@email.com")
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))
    
    def test_PostFields(self):
        post = Post(body = "hi", building = "Sci", user_id = 0, \
            studySpace_id = 1)
        self.assertTrue(post.body == 'hi')
        self.assertTrue(post.building == 'Sci')
        self.assertTrue(post.user_id == 0)
        self.assertTrue(post.studySpace_id == 1)

    def test_UserAndPostRelationship(self):
        u = User(username='susan', email = "susan@email.com")
        post = Post(body = "hi", building = "Sci", author = u, \
            studySpace_id = 1)
        post2 = Post(body = "hello", building = "Sci", author = u, \
            studySpace_id = 1)
        self.assertTrue(u.posts.all()[0].body == 'hi')
        self.assertTrue(u.posts.all()[1].body == 'hello')

        self.assertTrue(post.author.username == 'susan')
        self.assertTrue(post.author.email == 'susan@email.com')

        self.assertTrue(post2.author.username == 'susan')
        self.assertTrue(post2.author.email == 'susan@email.com')

class StudySpaceAndPost(unittest.TestCase):

    def test_PostAndStudySpaceRelationship(self):
        building = Building(name = 'Parrish')
        space = StudySpace(name = 'Shane Lounge', lat = 12.34, \
            long = -75.12, building = building)
        u = User(username='susan', email = "susan@email.com")
        post = Post(body = "hi", building = "Parrish", author = u, studySpace = space)
        post2 = Post(body = "hello", building = "Parrish", author = u, studySpace = space)
        
        self.assertTrue(post.studySpace.name == "Shane Lounge")
        self.assertTrue(post2.studySpace.name == "Shane Lounge")

        self.assertTrue(len(space.post.all()) == 2)
        
if __name__ == '__main__':
    unittest.main(verbosity=2)