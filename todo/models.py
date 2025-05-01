from django.db import models
from mongoengine import Document, StringField, BooleanField, DateTimeField, ReferenceField
import datetime
from auth_user.models import User

class Todo(Document):
    title = StringField(required=True, max_length=255)
    description = StringField(default='')
    completed = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)
    user = ReferenceField(User, required=True)

def __str__ (self):
    return self.title