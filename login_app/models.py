from django.db import models
import bcrypt
import re
import lyricsgenius
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, form):
        errors = {}
        email_checker = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(form['first_name']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters"
        if len(form['last_name']) < 3:
            errors["last_name"] = "Last Name should be at least 2 characters"
        if len(form['email']) < 8:
            errors["email"] = "Email should be at least 10 characters"
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = 'Invalid Email Address'
        email_check = self.filter(email=form['email'])
        if email_check:
            errors['email'] = "Email already in use"
        if len(form['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if form['password'] != form['confirm']:
            errors['password'] = 'Passwords do not match'
        if form['search'] == '':
            errors['search'] = 'Not a valid search'
        return errors

    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False

        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def register(self, form):
        pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            first_name = form['first_name'],
            last_name = form['last_name'],
            email = form['email'],
            password = pw,
        )

class User(models.Model):
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=225)
    birthday = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Favs(models.Model):
    song_id = models.CharField(max_length=45)
    fav = models.ManyToManyField(User, related_name='user_favs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    comment = models.CharField(max_length=225)
    poster = models.ForeignKey(User, related_name="user_message",on_delete = models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Reply(models.Model):
    reply = models.CharField(max_length=225)
    comment = models.ForeignKey(Comment, related_name='post_comments', on_delete=models.CASCADE)
    poster = models.ForeignKey(User, related_name='user_reply',on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Lyric(models.Model):
    lyric = models.TextField()
    artist = models.CharField(max_length=225)
    title = models.CharField(max_length=225)
    album = models.CharField(max_length=225)
    #image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    like = models.ManyToManyField(User, related_name='user_fav')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Genius(models.Model):
    lyricsgenius
    like = models.ManyToManyField(User, related_name='fav')



# Create your models here.
