from dataclasses import dataclass
from datetime import datetime

@dataclass
class AddBookModel:
    title: str
    author: str
    genre: str
    summary: str
    published_year: datetime

@dataclass
class AddReviewModel:
    user_id: int
    rating: int
    review_text: str

@dataclass
class Headers:
    x_API_KEY: str
    x_optional: int

@dataclass
class UpdateBookModel:
    id: int
    title: str
    author: str
    genre: str
    summary: str
    published_year: datetime