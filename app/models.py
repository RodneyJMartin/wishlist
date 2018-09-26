from django.db import models
import re, bcrypt
from datetime import datetime, date
from time import strftime

# Create your models here.
class UserManager(models.Manager):
    def register(self,data):
        print("in our models", data)
        errors = {}

        if len(data['name']) < 1:
            errors['name'] = 'Name is required!'
        elif len(data['name']) < 3: 

            errors['username'] = 'Name much be 3 characters or more!'
        if len(data['username']) < 1:
            errors['username'] = 'Username is required!'
        elif len(data['username']) < 3: 
            errors['username'] = 'Username much be 3 characters or more!'

        if len(data['date_hired']) < 8:
            errors['date_hired'] = "Date of hire is required!"
        else:
            d = data['date_hired']
            day = datetime.strptime(d, "%Y-%m-%d")
            if day > datetime.now():
                errors['date_hired'] = "invalid date of hire!"

        if len(data['password']) < 1:
            errors['password'] = "Password is required!"
        elif len(data['password']) < 8:
            errors['password'] = "Password must be 8 characters or more!"        
        if data['password'] != data['password_confirm']:
            errors['password_confirm'] = "Confirm password must match the Password!"
        if len(errors) == 0:
            return User.objects.create(
                name = data['name'],
                username = data['username'],
                password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode(),
                date_hired = data['date_hired'],
            )
        else:
            return errors
    def login(self,data):
        print("in our models", data)
        errors = {}

        if len(data['username']) < 1:
            errors['username'] = "Username is required!"
        else:
            list_of_users_with_this_username = User.objects.filter(username=data['username'])
            if len(list_of_users_with_this_username) < 1:
                errors['username'] = "Username is not found!"
        if len(data['password']) < 1:
            errors['password'] = "Password is required!"
        elif len(data['password']) < 8:
            errors['password'] = "Password must be 8 characters or more!"
        if len(errors) == 0:
            stored_password = list_of_users_with_this_username[0].password
            if not bcrypt.checkpw(data['password'].encode(), stored_password.encode()):
                errors['password'] = "Incorrect Password!"
                return errors
            else:
                return list_of_users_with_this_username[0]
        else:
            return errors

class User(models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    date_hired = models.DateField(max_length = 8)
    objects = UserManager()

class ProductManager(models.Manager):
    def addproduct(self, data, user_id):
        if len(data['name']) < 1:
            return{'name': 'Cannot be empty'}
        elif len(data['name']) < 2:
            return {"name": "Product name must be 3 characters or longer"}
        else:
            return Product.objects.create(
                name=data['name'],
                user_id = user_id
            )

class Product(models.Model):
    name = models.CharField(max_length = 255)
    date_added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="products", on_delete=models.CASCADE)
    added = models.ManyToManyField(User, related_name="added_products")
    objects = ProductManager()