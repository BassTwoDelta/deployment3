from django.db import models
import bcrypt
import re

# Create your models here.
class regManager(models.Manager):
    def validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address"
        if postData['password'] != postData['confirm_pw']:
            errors['confirm_pw'] = "Passwords do not match"
        return errors

    def validatorLogin(self, postData):
        errors = {}
        user = User.objects.filter(email=postData['email_login'])
        if len(user) == 0:
            errors["email_login"] = "Email not found! Please register"
        else: 
            logged_user = user[0]
            if not bcrypt.checkpw(postData['password_login'].encode(), logged_user.password.encode()):
                errors['password_login'] = "Password is incorrect"
        return errors

class quoteManager(models.Manager):
    def quoteValidator(self, postData):
        errors = {}
        if len(postData['author']) < 2:
            errors['author'] = "'Quoted by' must be at least 2 characters"
        if len(postData['message']) < 10:
            errors['message'] = "Message must be at least 10 characters"
        return errors

class User(models.Model):
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=100, default="name")
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = regManager()

class Quote(models.Model):
    author = models.CharField(max_length=100)
    message = models.TextField()
    user = models.ForeignKey(User, related_name="quotes", on_delete=models.CASCADE)
    favorites = models.ManyToManyField(User, related_name="users")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = quoteManager()
