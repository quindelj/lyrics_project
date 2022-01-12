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

class Snippit(models.Model):
    snippit = models.TextField()
    artist = models.CharField(max_length=225)
    title = models.CharField(max_length=225)
    album = models.CharField(max_length=225)
    image = models.CharField(max_length=225)
    poster = models.ForeignKey(User, related_name='user_snippit',on_delete = models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='snip_comm', on_delete= models.CASCADE, blank=True, null=True)
    liked = models.ManyToManyField(User, default = None, blank = True, related_name='user_like')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)

    @property
    def num_likes(self):
        return self.liked.all().count()

LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    snip = models.ForeignKey(Snippit, on_delete=models.CASCADE)
    value = models.CharField(choices = LIKE_CHOICES, default='Like', max_length=10)
    #created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.snip)

# Create your models here.
