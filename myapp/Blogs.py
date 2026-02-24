from mongoengine import (
    Document, StringField, DateTimeField,
    IntField, ListField, EmbeddedDocument, EmbeddedDocumentField
)
from datetime import datetime


class Comment(EmbeddedDocument):
    user = StringField(required=True)
    content = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)


class Blog(Document):
    title = StringField(required=True, max_length=200)
    content = StringField(required=True)

    author = StringField(required=True)  # store username/email

    created_at = DateTimeField(default=datetime.utcnow)
    likes = IntField(default=0)  
    liked_by = ListField(StringField())
    comments = ListField(EmbeddedDocumentField(Comment))
    meta = {
        "collection": "blogs"  # MongoDB collection name
    }

    def __str__(self):
        return self.title