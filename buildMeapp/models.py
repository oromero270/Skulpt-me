from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class usermanager (models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['fname']) < 2:
            errors["fname"] = "First name should be at least 2 characters"
        if len(postData['lname']) < 2:
            errors["lname"] = "Last name should be at least 2 characters"
        if len(postData['pw']) < 8:
            errors["pw"] = "Password should be at least 8 characters"
        if postData['pw'] != postData ['cpw']:
            errors["confirm"] = "Password and confirm password must match"
        if len( postData ['mail'] )< 1:
            errors['email'] = 'Email is required'
        else:
            activeemails=users.objects.filter(email=postData['mail'])
            if len (activeemails)>0:
                errors['taken']='This email has been taken, please try another email address'
        if len( postData ['acctname'] )< 1:
            errors['username'] = 'username required'
        else:
            activeusernames=users.objects.filter(username =postData['acctname'])
            if len (activeusernames)>0:
                errors['nametaken']='This username has been taken, please try another name'
            elif not EMAIL_REGEX.match(postData['mail']):
                errors['emailformat']= 'email is not valid'

        return errors

    def login_validator(self,postData):
        errors = {}
        if len( postData ['acctname'] )< 1:
            errors['acct'] = 'Username is required'
        active_usernames = users.objects.filter( username = postData['acctname'])
        if len (active_usernames) ==0:
            errors['acct not found']= 'Username not found'
        else:
            user=active_usernames[0]
            if not bcrypt.checkpw(postData['pw'].encode(),user.password.encode()):
                errors['pw']='Wrong password'
        if len(postData['pw']) < 1:
            errors["pw0"] = "Password required"
        return errors

    def test_validator(self,postData):
        errors = {}
        if len( postData ['sittest'] )< 1:
            errors['missing'] = 'Number is required'
        
        return errors

class users (models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    username =models.CharField(max_length=25)
    password = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = usermanager()

class fitness(models.Model):
    situps = models.CharField(max_length=255)
    pushups = models.CharField(max_length=255)
    plank_time= models.CharField(max_length=255)
    squats = models.CharField(max_length=255)
    # userfitness becomes a key to allow users to check 
    userfitness=models.ManyToManyField(users,related_name='myfitness')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class workout(models.Model):
    name=models.CharField(max_length=255)
    gear= models.CharField(max_length=255)
    focus= models.CharField(max_length=255)
    difficulty= models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

