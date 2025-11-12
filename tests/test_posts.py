import unittest
from app import create_app, db
from app.posts.models import Post, PostCategory 
from datetime import datetime
from sqlalchemy.orm import Mapped
from sqlalchemy.exc import IntegrityError 

class PostModelTestCase(unittest.TestCase):
    """
    Включає тести для операцій CRUD та перевірки цілісності (загалом 9 тестів).
    """

    def setUp(self):
        self.app = create_app(config_name="test")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

  

    def test_post_creation(self):
        """
        [US01-C] Тест: перевіряємо, чи створюється пост з усіма необхідними полями та Enum.
        """
        
        p = Post(
            title="Test Post", 
            content="This is the content of a test post.",
            category=PostCategory.tech 
        )
        
        db.session.add(p)
        db.session.commit()
        
        retrieved_post = db.session.scalar(
            db.select(Post).where(Post.title == "Test Post")
        )
        
        
        self.assertIsNotNone(retrieved_post)
        self.assertEqual(retrieved_post.title, "Test Post")
        self.assertEqual(retrieved_post.content, "This is the content of a test post.")
        self.assertEqual(retrieved_post.category, PostCategory.tech)
        self.assertIsInstance(retrieved_post.posted, datetime)

    def test_repr(self):
        """
        Тест: перевіряємо метод __repr__
        """
        
        p = Post(
            title="Test Repr", 
            content="body", 
            category=PostCategory.news 
        )
        db.session.add(p)
        db.session.commit()
        
        test_id = p.id 
        
        self.assertEqual(
            repr(p), 
            f"<Post(id={test_id}, title='Test Repr', author='Anonymous')>"
        )

    def test_default_values(self):
        """
        Тест: перевіряємо, чи працюють 'default' у моделі
        """
        
        p = Post(title="Default Test", content="body", category=PostCategory.news)
        db.session.add(p)
        db.session.commit()
        
        retrieved_post = db.get_or_404(Post, p.id)
        
        
        self.assertEqual(retrieved_post.author, 'Anonymous')
        self.assertEqual(retrieved_post.is_active, True)
        self.assertIsInstance(retrieved_post.posted, datetime)

    

    def test_failed_creation_missing_category(self):
        """
        [US01-Error] Тест: перевіряємо, чи виникає помилка при відсутності обов'язкового поля 'category'.
        """
        
        p = Post(title="Error Test", content="Missing category body")
        db.session.add(p)
        
        
        with self.assertRaises(IntegrityError):
            db.session.commit()
        
        
        db.session.rollback()

    def test_read_all_posts(self):
        """
        [US02-R] Тест: перевіряємо читання кількох постів.
        """
        
        db.session.add_all([
            Post(title="Post 1", content="C1", category=PostCategory.tech),
            Post(title="Post 2", content="C2", category=PostCategory.news),
            Post(title="Post 3", content="C3", category=PostCategory.tech) 
        ])
        db.session.commit()

       
        posts = db.session.scalars(db.select(Post)).all()

        
        self.assertEqual(len(posts), 3)
        self.assertIn("Post 2", [p.title for p in posts])

    def test_filter_by_category(self):
        """
        [US03-R] Тест: перевіряємо фільтрацію постів за категорією.
        """
        
        db.session.add_all([
            Post(title="Tech Post 1", content="T1", category=PostCategory.tech),
            Post(title="News Post 1", content="N1", category=PostCategory.news),
            Post(title="Tech Post 2", content="T2", category=PostCategory.tech)
        ])
        db.session.commit()

       
        tech_posts = db.session.scalars(
            db.select(Post).where(Post.category == PostCategory.tech)
        ).all()


        self.assertEqual(len(tech_posts), 2)
        self.assertEqual(tech_posts[0].category, PostCategory.tech)
        self.assertEqual(tech_posts[1].category, PostCategory.tech)
        self.assertNotIn("News Post 1", [p.title for p in tech_posts])

    def test_update_content(self):
        """
        [US04-U] Тест: перевіряємо оновлення поля 'content'.
        """
        p = Post(title="Original", content="Old Content", category=PostCategory.news)
        db.session.add(p)
        db.session.commit()

        original_id = p.id
        new_content = "This is the updated content."

        
        p.content = new_content
        db.session.commit()

        
        updated_post = db.get_or_404(Post, original_id)

        
        self.assertEqual(updated_post.content, new_content)
        self.assertEqual(updated_post.title, "Original") 

    def test_update_category(self):
        """
        [US05-U] Тест: перевіряємо оновлення поля 'category'.
        """
        p = Post(title="Category Change", content="Content", category=PostCategory.tech)
        db.session.add(p)
        db.session.commit()

        original_id = p.id
        
        
        p.category = PostCategory.news 
        db.session.commit()

        
        updated_post = db.get_or_404(Post, original_id)

       
        self.assertEqual(updated_post.category, PostCategory.news)
        self.assertNotEqual(updated_post.category, PostCategory.tech)

    def test_delete_post(self):
        """
        [US06-D] Тест: перевіряємо видалення посту.
        """
        p = Post(title="To Be Deleted", content="Delete me!", category=PostCategory.news)
        db.session.add(p)
        db.session.commit()
        
        post_id = p.id

        self.assertIsNotNone(db.session.get(Post, post_id))

    
        db.session.delete(p)
        db.session.commit()

    
        self.assertIsNone(db.session.get(Post, post_id))

if __name__ == '__main__':
    unittest.main()