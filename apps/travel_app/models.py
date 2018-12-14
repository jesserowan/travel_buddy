from django.db import models
import re, bcrypt
from datetime import date, datetime

class UserManager(models.Manager):
    def register(self, form):
        errors = {}
        if len(form['name']) < 3:
            errors['name'] = "Your name must be at least three characters"
        if len(form['username']) < 2:
            errors['user'] = "Your username must be at least two characters"
        if len(User.objects.filter(username=form['username'])) != 0:
            errors['in_use'] = "This username has already been taken"
        if form['pw'] != form['confirm']:
            errors['match'] = "Please enter the same password in both fields"
        if len(form['pw']) < 8:
            errors['pw_length'] = "Your password must be at least eight characters"
        return errors

    def login(self, form):
        errors = {}
        match = User.objects.filter(username=form['login_username'])
        if len(match) == 0:
            errors['login'] = "Your information is incorrect"
        elif not bcrypt.checkpw(form['login_pass'].encode(), match[0].pw_hash.encode()):
            errors['login'] = "Your information is incorrect"
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    pw_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # trips
    # trips_planned

    objects = UserManager()

class TripManager(models.Manager):
    def add_trip(self, form):
        errors = {}
        if len(form['destination']) < 1:
            errors['destination'] = "Please enter a destination"
        if len(form['description']) < 1:
            errors['description'] = "Please briefly describe your trip"
        if form['departure'] == "":
            errors['no_departure'] = "Please enter a departure date"
        if form['return_date'] == "":
            errors['no_return'] = "Please enter a return date"
        if form['departure'] != "":
            if form['departure'] < str(date.today()):
                errors['future'] = "Your trip should be scheduled in the future"
        if form['departure'] > form['return_date']:
            errors['dates'] = "Please select a return date after your departure date"
        return errors

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    travellers = models.ManyToManyField(User, related_name="trips")
    departure = models.DateField()
    return_date = models.DateField()
    planned_by = models.ForeignKey(User, related_name="trips_planned", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TripManager()