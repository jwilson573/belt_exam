from __future__ import unicode_literals
import bcrypt
from django.db import models

class UserManager(models.Manager):
    
    def validate(self, form):
        
        errors = []
        user_record = User.objects.filter(username=form['username']).first()
        if user_record:
            errors.append("Username already exists.")
            return errors

        if len(form['name']) < 3 or len(form['username']) < 3:
            errors.append("Name fields must be at least 3 characters.")
            return errors
        
        if len(form['password']) < 8:
            errors.append("Password must be at least 8 characters.")
        
        if form['password'] != form['pwconfirm']:
            errors.append("Passwords do not match.")
            return errors
        
        return errors
    
    
    def register(self, form):

        errors = []
        
        password = str(form['password'])
        encryptedpw = bcrypt.hashpw(password, bcrypt.gensalt())
        
        user = User.objects.create(
                name = form['name'],
                username = form['username'],
                password = encryptedpw,

            )
        return user

    
    def validate_login(self, form):
        print "Inside the login_validate method"

        
        errors = []
        user_check = User.objects.filter(username=form['userlogin']).first()
        # print user_check

        if user_check == None:
            errors.append("User not in database")
            return errors
    
        if user_check:
            password = str(form['passlogin'])
            user_pass = str(user_check.password)

            encryptedpw = bcrypt.hashpw(password, user_pass)

            if encryptedpw == user_pass:
                return user_check
            
            errors.append("Invalid Password")
        
        return errors

class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s' %(self.name, self.username)

    objects = UserManager()

class TripManager(models.Manager):
    def create_trip(self, user, form):
        trip = Trip.objects.create(
            owner = user,
            destination = form['destination'],
            description = form['description'],
            start_date = form['date_from'],
            end_date = form['date_to']
        )
        
        return trip

class Trip(models.Model):
    owner = models.ForeignKey(User, related_name="created_trips")
    user = models.ManyToManyField(User, related_name='trips')
    destination = models.CharField(max_length=255)
    start_date = models.CharField(max_length=11)
    end_date = models.CharField(max_length=11)
    description = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s %s %s' %(self.description, self.destination, self.start_date, self.end_date)

    objects = TripManager()