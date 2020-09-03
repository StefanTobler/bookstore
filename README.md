# CSCI 4050 Bookstore

Hi everyone, I hope you found this page well. I am going to summarize a few things that you might find useful when setting up the environment that we will be working in.

## Virtual Environment

I **highly** suggest everyone set up a fresh virtual environment on your computer to work on this project, especially if you have ever installed other python packages before. It can be a headache to try and trouble shoot some error that is outside of the scope of the project directory, and setting up a virtual environment is fairly easy!

First make sure that you have Python 3.7+ or above on your system. You can find the download link [here](https://www.python.org/downloads/). The next few steps will differ from unix based systems and Windows systems, but just skip to the one you have. You can also look at the official documentation [here](https://docs.python.org/3/library/venv.html).

Quick note: This project should run the same on both systems. Python is platform independent so if you have a virtual environment on a Mac and Windows machine they should run the same if you just pull the repo.

### Windows

NOTE: I will be using PowerShell in this demo.

If you are on Windows then you probably will only have Python 3.7+ installed on your machine, unless you installed an earlier version on purpose. Just to be safe use the command `python --version`. If a version lower than 3.7 shows up I suggest you update it incase we get get into any async calls.

Now setting up a virtual environment is very straight forward. We use the `venv` command to create virtual environments.

```
python -m venv bookstore
```

This will create a new virtual environment in the directory that you ran the command in called `bookstore`. After you `cd` into the new `bookstore` directory we need to activate the environment.

In Windows PowerShell we can use the following command:

```
PS C:\\Users\you\Documents\bookstore> .\Scripts\Activate.ps1
```

If the activation was successful you should see the virtual environment's name preceding the shell prompt.

```
(bookstore) PS C:\\Users\you\Documents\bookstore>
```

After activating the virtual environment run the command `pip install --upgrade pip` to upgrade the python package installer.

Now clone the git repo using `git clone --depth 1 https://github.com/StefanTobler/bookstore` and `cd` into the repo. Now that you are in the git repo use the command `pip install -r requirements.txt`.

If this is all successful you should be ready to go!

#### Git

If you don't have git on Windows you can install it [here](https://git-scm.com/download/). Follow the instructions then you will need to generate a [personal access token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token) when logging in (if you have 2FA enabled). Confirm that you can get the repo by using the following command in your virtual environment `git clone --depth 1 https://github.com/StefanTobler/bookstore`. If this doesn't work you can message me (Stefan) and I can help you figure it out or you can [Google-fu](https://en.wiktionary.org/wiki/Google-fu) your way to a solution.

### Unix/MacOS

If you are on Unix or MacOS then you will already have Python 2.7, this is not the right version and will cause a lot of issues if this is your only version. Please install Python 3.7+. You can verify that Python3.7+ is installed if you use the command `python3 --version`. If a version lower than 3.7 shows up I suggest you update it incase we get get into any async calls.

Now setting up a virtual environment is very straight forward. We use the `venv` command to create virtual environments.

```
python3 -m venv bookstore
```

This will create a new virtual environment in the directory that you ran the command in called `bookstore`. After you `cd` into the new `bookstore` directory we need to activate the environment.

In a bash shell you can use the following command:

```
$ source bin/activate
```

If the activation was successful you should see the virtual environment's name preceding the shell prompt.

```
(bookstore) $
```

After activating the virtual environment run the command `pip install --upgrade pip` to upgrade the python package installer.

Now clone the git repo using `git clone --depth 1 https://github.com/StefanTobler/bookstore` and `cd` into the repo. Now that you are in the git repo use the command `pip install -r requirements.txt`.

If this is all successful you should be ready to go!

## Trello

We will use Trello to keep track of what we need to do and the due dates. I will also help us stay accountable by assigning user stories to ourselves so that we know what we are working on. The link to join is [here](https://trello.com/invite/b/eIG0UMi4/1573761132922f9ac523709e8e0c8d28/bookstore-csci-4050-fall-2020). If there are any issues with the permissions let me know, this is my first time setting up a Trello card.

## Django

Django is an awesome python web framework with a built in ORM. This makes it super easy to access information and build forms. For many of you this is your first time using Django and honestly it is mine too. I made a small project a few weeks ago to get my bearings with it and I picked it up very quickly. Below I will include some links to playlists that I found useful when learning, but I will give a general run down of Django here.

### Starting with Django

First off we need to create a project (this will already be done):

```
$ django-admin startproject bookstore
```

This project is the repository, so no need to create one.

You can view the site with the following command:

```
$ python manage.py runserver
```

This will start the Django server on `localhost:8000` by default. If you have a conflicting service running on port 8000 you can specify the port after the `runserver` command. You might notice a warning about unapplied migrations, but we will talk about that later.

`startproject` creates a directory that looks like this

```
bookstore/
    manage.py
    bookstore/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
```

Next we need to create an app. Apps are like micro services that can be reused across different Django projects. We can have many apps but only one project. In this example we will start the `users` app.

```
$ django-admin startapp users
```

Now that the app has been created it will create a new directory that looks like this.

```
users/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py
```

Now that we created our first app, let's add something to the [view](#views).

In `users/views.py` add the following

```python
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the users index.")
```

Next we need to map the url in `users/urls.py`, if this file is not created, create it now.

```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

And finally in `bookstore/urls.py` add

```python
from django.urls import include, path

urlpatterns = [
    path('users/', include('users.urls')),
    path('admin/', admin.site.urls),
]
```

Now if you run the server and go to `localhost:8000/users` you should see "Hello, world. You're at the users index.".

### [Models](https://docs.djangoproject.com/en/3.1/topics/db/models/)

Models are database objects. We can create classes that represent database objects. Take a look at this code

```python
class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
```

Above defines a Model named `User`. This `User` has a `first_name` and a `last_name`. After preforming a [migration](#migration) this table will be created in the database and we will be able to query for any existing `User`. Django also has something called `Forms` that allow for `POST` requests on pages that include a `Form` to validate and create the `Model` it is referring.

The model above translates to the following SQL

```sql
CREATE TABLE bookstore_user (
    "id" serial NOT NULL PRIMARY KEY,
    "first_name" varchar(30) NOT NULL,
    "last_name" varchar(30) NOT NULL
);
```

### [Views](https://docs.djangoproject.com/en/3.1/topics/class-based-views/)

Views are how pages are rendered. For this project we will be using class-based views because they offer more flexibility and allow for much easier to read code. In the `views.py` file of each app we can create methods and classes that define how pages react when they get a `POST` or `GET` request.

Here is an example of a class-based view

```python
# users/views.py
from django.views.generic import View
from django.http import HttpResponse

class AboutView(View):

    def get(self, request, id_url, *args, **kargs):
      return HttpResponse('This is my about view.')
```

Then in the `urls.py` file we reference the class in a different way

```python
# users/urls.py
from django.urls import path
from users.views import AboutView

urlpatterns = [
    path('about/', AboutView.as_view(), name='users-about'),
]
```

This essentially has the same function as the example in [Starting With Django](#starting-with-django), however when we create more complex views you will be thanking yourself.

### [Migration](https://docs.djangoproject.com/en/3.1/topics/migrations/)

**Potentially Destructive**

Migrations are the way to add our models to the database. If we create a new model or change any attribute of any current model we need to migrate those changes to the database. To make a migration we need to do a few commands in the shell.

```
$ python manage.py makemigrations
```

This command will get your migrations ready to migrate. If it is your first migration it will create a file called `0001_initial.py`, otherwise it will create a file in `migrations` called `xxxx_auto.py`.

After the `makemigrations` command we can migrate.

```
$ python manage.py migrate
```

After the migrations are applied then the database will adapt the new Model structure. If something messes up and worse comes to worse you can delete the `db.sqlite3` file and all the files in the `migrations` directory. Then just remake the migrations. **This will destroy the database and any data in it.**

I am not a professional at migrations, if you want to learn more read the documentation page.

#### Other Notes

All this being said, I highly suggest following along with Corey Schafer's tutorial about Django, he does not use class-based views but there is a 5 minute video online about how to make regular views class-based views. If you have any questions feel free to reach out.

#### Links

* [Python Download](https://www.python.org/downloads/)
* [Python Virtual Environment](https://docs.python.org/3/library/venv.html)
* [Git Download](https://git-scm.com/download/)
* [Setting up a GitHub Personal Access Token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token)
* [Trello Invite](https://trello.com/invite/b/eIG0UMi4/1573761132922f9ac523709e8e0c8d28/bookstore-csci-4050-fall-2020)
* [Corey Schafer Django Tutorial](https://www.youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p)
* [Corey Schafer Python Tutorial](https://www.youtube.com/playlist?list=PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU)
* [Django Quick Start](https://docs.djangoproject.com/en/3.1/intro/tutorial01/)
* [Class Based Views](https://docs.djangoproject.com/en/3.1/topics/class-based-views/)
