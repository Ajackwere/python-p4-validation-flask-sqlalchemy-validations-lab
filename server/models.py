from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

    @validates('phone_number')
    def validate_phone_number(self, key, value):
        # Ensure phone_number is exactly ten digits
        if not re.match(r'^\d{10}$', value):
            raise ValueError('Phone number must be exactly ten digits')
        return value


class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'

    @validates('title')
    def validate_title(self, key, value):
        # Custom validation for clickbait title
        clickbait_keywords = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(keyword in value for keyword in clickbait_keywords):
            raise ValueError('Title must be sufficiently clickbait-y')
        return value

    @validates('content')
    def validate_content_length(self, key, value):
        # Ensure that content is at least 250 characters long
        if len(value) < 250:
            raise ValueError('Content must be at least 250 characters long')
        return value

    @validates('category')
    def validate_category(self, key, value):
        # Ensure that category is either "Fiction" or "Non-Fiction"
        valid_categories = ["Fiction", "Non-Fiction"]
        if value not in valid_categories:
            raise ValueError('Category must be "Fiction" or "Non-Fiction"')
        return value
