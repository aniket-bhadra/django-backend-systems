
```bash
django-admin startproject folderName

# if environment variable not set
python -m django startproject folderName
```
This creates a new Django project inside a folder named **folderName**.

inside that folder, Django creates:  
1. A **project folder** (contains project files).  
2. **manage.py** (used to interact with the project, e.g., starting the server).  

Inside the project folder:  


### **Updated List:**  
- **`__init__.py`** → Makes the folder a Python package.  
- **`settings.py`** → Stores project configurations (similar to `package.json`).  
- **`urls.py`** → Defines URL patterns for handling incoming requests.  
- **`wsgi.py`** → Used for deploying with WSGI servers (traditional synchronous requests).  
- **`asgi.py`** → Used for deploying with ASGI servers (supports async features like WebSockets).  

These files are needed when deploying Django with production servers. We deploy Django apps on WSGI or ASGI servers. WSGI/ASGI servers handle HTTP requests and convert them into Python function calls that Django understands. The wsgi.py and asgi.py files are the entry points that tell these servers how to load and run your Django application.

Django follows the **MVT (Model-View-Template)** architecture:  

- **Model** → Handles database (data structure).  
- **View** → Handles logic (processes requests, fetches data).  
- **Template** → Handles UI (HTML, frontend rendering).  
 
### Why are SSR web apps built with Django a little slower than web apps built with Express or Next.js?
Django SSR can be slower than Express/Next.js because while Node.js handles HTTP requests directly, Django uses WSGI servers that do conversion work (HTTP ↔ Python function calls) - though this isn't a major bottleneck since it's just a lightweight calling convention. The real performance difference comes from JavaScript's V8 engine being faster than Python's interpreter and Node.js's event loop handling concurrent requests more efficiently than Python's traditional threading model, though Django now supports ASGI for async operations and the performance gap has narrowed with modern Python web servers.

# VIEW

### Apps in Django  
In a Django project, apps represent different sections. For example:  
- **Food section → `food` app**  
- **Order section → `order` app**  

### Creating an App  
To create an app, run:  
```bash
python manage.py startapp food
```

When an app is created, it contains multiple default files.  

### Key File: `views.py`  
- Defines what content the user will see.  
- Processes user requests, analyzes them, and sends responses.  
- Written using functions, where the function name becomes the view name.  

### Connecting Views to URLs  
After defining a view, it must be linked to a URL so it gets triggered when a user visits a specific path.  

1. **Create `urls.py` inside the same app folder (`food/urls.py`)**  
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
]
```

2. **Add the app's URL configuration to the project's `urls.py` (root `urls.py`)**  
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("food/", include("food.urls")),
]
```

### How Django Handles URL Requests  
If a user enters:  
```
http://localhost:8000/food/hello
```  
Django follows these steps:  
1. Checks `ROOT_URLCONF` in `settings.py`, which points to `ProjectFolder.urls`.  
2. so, it Opens the project folder root `urls.py` and looks for a matching pattern (`food/`).  
3. If `food/` matches, it moves to `food/urls.py` and looks for the next part (`hello`).  
4. If a match is found, Django executes the corresponding view function (e.g., `index`).  
5. The view function processes the request and returns an HTTP response, like `"Hello, User!"`.  

This is how users see `"Hello, User!"` when they enter the URL.

The WSGI server takes the entire HTTP request and calls Django's main application function (defined in wsgi.py) just once with the request data. Then Django does all of those steps internally, and whatever Django returns becomes the return value of that application function call, to the WSGI server. The WSGI server then sends that return value as an HTTP response to the client.
it's one function call in, one return value out, with Django handling all the internal processing.
Why it works locally without WSGI/ASGI:
python manage.py runserver includes a built-in development server that has WSGI functionality built into it. It's doing the same job as Gunicorn but is simpler and only for development.

# MODEL
## Django Models and Database Handling

## Introduction
- Models in Django define the schema of each database table.
- Django comes with a pre-installed and pre-configured SQLite3 database.
- To use another database, install it and configure it inside `settings.py`.

## Django Migrations
- Django comes with pre-installed apps, some of which use database tables.
- To create database tables for them, run:
  ```sh
  python manage.py migrate
  ```
- The `migrate` command:
  - Looks at all installed apps inside `settings.py`.
  - Creates necessary database tables according to `DATABASES` settings in `settings.py`.

## Creating Custom Models and Database Tables
1. Define the schema inside `models.py` of each app (e.g., `food`).
   ```python
   from django.db import models

   class Item(models.Model):
       item_name = models.CharField(max_length=200)
       item_desc = models.CharField(max_length=200)
       item_price = models.IntegerField()
   ```
2. Add the custom app to `INSTALLED_APPS` in `settings.py`:
   ```python
   INSTALLED_APPS = [
       'food.apps.FoodConfig',
       'django.contrib.admin',
   ]
   ```
3. Create database migrations:
   ```sh
   python manage.py makemigrations food
   ```
   - This command creates migration files but does **not** create the actual database table.
4. To see the SQL query behind migration:
this is optional. It just shows the SQL query for checking, but it doesn’t affect the database. You can skip it and go directly from step 3 (makemigrations) to step 5 (migrate).
   ```sh
   python manage.py sqlmigrate food 0001
   ```
   - Example output:
     ```sql
     CREATE TABLE "food_item" (
         "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
         "item_name" varchar(200) NOT NULL,
         "item_desc" varchar(200) NOT NULL,
         "item_price" integer NOT NULL
     );
     ```
5. Apply migrations to create actual database tables:
   ```sh
   python manage.py migrate
   ```

### If migrate creates the database table in step 5, why do we need to run makemigrations and sqlmigrate before that? and why for installed apps we dont need to execute those steps?

1. **Step 3 (`makemigrations`)** → Prepares the **blueprint** (migration files) for your model changes but doesn’t create the table yet.  
2. **Step 4 (`sqlmigrate`)** →optional
3. **Step 5 (`migrate`)** → Actually **builds** the table in the database using the blueprint.  

Why the extra steps for custom apps? Django’s built-in apps already have migrations, so `migrate` knows what to create. But for **your** app, Django needs you to define the **blueprint first** before it can create the table.
- `migrate` **actually runs** the SQL query and creates the database table.

## summary
- **`makemigrations`** → Creates a **blueprint** (migration file) of what needs to be done.  
- **`migrate`** → **Builds** the actual table in the database using that blueprint.

## Adding Data to the Database
Django provides a **Database Abstraction API** to create, update, and delete objects.

### **Method 1: Using Python Shell**
```sh
python manage.py shell
```
```python
from food.models import Item

# Retrieve all data from the table
Item.objects.all()

# Create an object
a = Item(item_name="Pizza", item_desc="Cheesy pizza", item_price=99)  # Not stored in DB yet

a.save()  # Now saved in DB

# Access a column
print(a.item_name)  # Output: Pizza
```

#### **Q: Is Django’s Database Abstraction API an ORM?**
- Yes, Django's **Database Abstraction API is an ORM** (Object-Relational Mapper).
- It allows interaction with the database using objects instead of raw SQL.

### Mongoose vs Django Model Creation

#### Q: How does Django’s model creation compare to Mongoose?
In Mongoose, we create data in two ways:

- Calling methods directly on the model:

 User.find()
- Creating an instance from the model class:

const user1 = new User({ name: "Robin", age: 35 });
user1.save();

In Django, we use the 2nd method (creating an instance from the model class and saving it):

user1 = User(name="Robin", age=35)
user1.save()

This is similar to the second method in Mongoose.

### **Method 2: Using Admin Panel**
1. Create a **superuser**:
   ```sh
   python manage.py createsuperuser
   ```
   - Set username and password.
2. Register the model in `admin.py`:
   ```python
   from django.contrib import admin
   from .models import Item

   admin.site.register(Item)
   ```
3. Access Django Admin Panel (`/admin` in the browser) to add, update, or delete objects.

In Django models actually define DB schema, so when we create schema or edit that schema, basically edit that model, then we have to run `makemigrations` command which actually creates a blueprint, then we run `migrate` to execute the real SQL command and create DB table or apply changes to that DB table.

But when we add data to that table there are 2 options:
1. **Python shell** - there we instantiate object from model class, add/update and then save it
2. **Admin panel** - there we add data with UI, but both of these methods use Django's database abstraction API to interact with the DB

**Key difference:**
- **To create/change table structure (schema)**: We need `makemigrations` (creates blueprint) → `migrate` (executes SQL)
- **For CRUD operations (data)**: We use UI or shell commands - SQL commands are executed directly through Django's ORM without needing migration steps

So schema changes require the migration process, but data operations happen immediately through Django's database abstraction API.

 When you modify models.py, you must run `makemigrations` then `migrate` because you're changing the database schema structure.
 Django provides this two-command approach so you can review schema changes before applying them to ensure you're absolutely sure.
 **CRUD operations are direct**: For regular CRUD operations (create, read, update, delete data), no migrations are needed since you're only manipulating data, not changing the database structure.

in models.py-
class Item(models.Model):
   def __str__(self):
      return self.item_name
   item_name= models.CharField(max_length=200)
   item_desc= models.CharField(max_length=200)
   item_price= models.IntegerField()

## why are we not calling __init__ here?
In Python, __init__ (Constructor) runs when an object is created.
In Django models, we don’t explicitly define __init__ because:Django models inherit from models.Model, which already has __init__.
When an object is created, Django calls __init__ internally and handles object creation automatically.

 The `__str__` method gets called whenever a new instance is displayed on the console, in the Django admin, or when rendered in a template (`{{ item1 }}`). The object from this class will be displayed in those places with the return value from `__str__`. If we remove `__str__`, the object will be rendered as a generic object representation in all those places.

The `__str__` method only changes how the object is displayed, but it does not replace the actual object with a string. The new instance from that class, still exists as an object, and you can access all its properties like `pizza.item_price`. 
The `__str__` method just controls how the object appears when printed or shown in Django admin/templates.

## Querying Data from the Database

In Mongoose we can query directly on the model:
```javascript
Item.find()
```
But in Django we cannot directly query on the model. Every model has a default manager called `objects`, so we query on them:

```python
Item.objects.all()
```
And whatever this returns is called a **QuerySet**, which is a collection of data stored in the database.

 we use the manager to retrieve data, and we get QuerySets as the output.

 Django models can have multiple managers and you can create custom managers.All managers, inherit from Django's Manager class, so they all have the same default methods like .all(), .filter(), .create(), .get(), etc.so in custom managers we get their own custom methods plus all the default methods.

### **Example:** Retrieve Data in Views
```python
def index(request):
    Item_list = Item.objects.all() 
    #Item.objects.all() returns the----> QuerySet
    return HttpResponse(Item_list)
```
- This will display all items stored in the database on the webpage.

Both Python shell (`python manage.py shell`) and Django admin panel use Django's ORM abstraction API (using the same model classes and methods like `.save()`, `.create()`, `.filter()`) to interact with the database. The only difference is the interface - shell uses code, admin uses a web UI.
when you view data in Django admin panel, it calls Item.objects.all() (or similar ORM methods) behind the scenes.

In both Mongoose and Django, you can create items in two ways:
1. **Direct method**: `Item.create()` (Mongoose) / `Item.objects.create()` (Django)
2. **Instance + save**: Create model instance, then call `.save()` method

# Does python manage.py runserver start the database server along with Django's web server?

**SQLite** → **File-based database**
* **No server process needed**
* Just a file on your hard drive (usually `db.sqlite3`)
* When your Django app needs database access:
   1. Django opens the SQLite file (`db.sqlite3`)
   2. Reads/writes data directly to the file
   3. Closes the file

**If we use Django with MySQL/PostgreSQL/MongoDB locally**, these are server-based databases, so we ourselves have to:
1. **Run these servers separately**
2. **Configure Django** to connect to them in `settings.py`
3. **Then run** `python manage.py runserver`
4. **Then Django will work** with those database servers

**Important**: `python manage.py runserver` **does NOT start any database server** - it only starts Django's web server. 

- In case of **SQLite3**, we don't need a separate server
- But even if we need to run a database server, **we have to start that server separately ourselves** - Django will NOT start that server
- **Django will only talk to the database** after successful connection and after the server is started

So Django's job is just to connect to and communicate with databases - never to start database servers!

# Template

## Django Template System

### 📁 Setting Up Templates

1. Inside your Django app, create a folder named `templates`.
2. Put all your HTML files inside this `templates` folder so that Django can locate them automatically.

---

### 📦 Template Context

Templates need a **context** — this is the data we get from the database.

Django takes the HTML file and combines it with the context (data from the database) to render the final output. dynamically

---

### 💡 How It Works

Templates allow us to combine:
- Static parts → HTML
- Dynamic parts → Data from the database  
And render a single complete web page.

---

### 🧑‍💻 Example View Function

```python
from django.shortcuts import render
from .models import Item

def index(request):
    item_list = Item.objects.all()
    context = {
        "item_list": item_list
    }
    return render(request, "food/index.html", context)
```
now index.html can access this context,so inside index.html we can do -->
---

### 📄 `index.html`

```html
<ul>
  {% for item in item_list %}
    <li>{{ item.id }} -- {{ item.item_name }}</li>
  {% endfor %}
</ul>
```
---
### 🛠 Django Template Language (DTL)

Django comes with its own template engine called **DTL** (Django Template Language).

#### Syntax Overview:

- **Variables**: `{{ variable_name }}`
- **Control structures** (`if`, `for`, etc.): `{% ... %}`

Example:

```html
{% if item_list %}
  <!-- Render list -->
{% else %}
  <p>No items available.</p>
{% endif %}
```

---
Django natively cannot work with NoSQL databases - Django ORM only supports SQL databases.templates rendered through views get auth context, which is enabled by default but not literally "every" template.
Adding an app to INSTALLED_APPS is essential because Django needs to make your app discoverable by Django's system to do anything with it. Whether it's for migrations, template rendering, or any other functionality, your app must be in INSTALLED_APPS to work.
### static files
files like css,js,images are static files

how to use them in index.html template?
{% load static %} this actually allows us to use {% static 'food/style.css' %} tag.
So when django sees this href="{% static 'food/style.css' %}", here for the static keyword it goes to settings.py STATIC_URL = 'static/', so django replaces this value for the static keyword.
This becomes: href="/static/food/style.css"> then Django finds the actual file in `your_app/static/food/style.css` and serves it.
And all of this is handled by django's preinstalled app django.contrib.staticfiles.

how to create a base template for all pages (Ex- navbar)
Create a .html file inside templates, write down the base template code then at the end or anywhere where you want to keep the rest of the website content, add this:
    {% block body %}
    {% endblock %}
Then go to the pages where you need this template and add this above:
{% extends 'food/base.html' %} and then wrap the whole page code with {% block body %}
    {% endblock %}

So now whenever django encounters that extends line it goes to that location, parses that html file, then when django spots `{% block body %} {% endblock %}` it comes to the actual page and renders the rest of the content in place of those tags.

When Django encounters `{% url 'food:create_item' %}` in a template, it identifies the `food` namespace and `create_item` URL name, then looks up the corresponding URL pattern in the food app's urls.py file. During server-side template rendering, Django replaces all template tags with their actual values - converting `{% url 'food:create_item' %}` to something like `/food/add-item/` and `{% static 'css/style.css' %}` to `/static/css/style.css`. The browser receives the final processed HTML with real URLs, never seeing the original template tags.

### forms
class ItemForm(forms.ModelForm):
   class Meta:
      model=Item
      fields=["item_name", "item_desc", "item_price"]

**Create forms.py inside the app you want to create forms.** Create a form class with a Meta class inside it to tell Django from this model you want to accept these specific fields. The Meta class is a special inner class that tells Django how to build the form - which model to use, which fields to include, etc. Django specifically looks for a class named Meta inside ModelForm classes. now When we create an instance object from the ItemForm class inside view and pass that whole instance to the template, Django creates a form with specified fields for this model and renders basic HTML form fields. When that form is submitted, the same view function gets called again. The `is_valid()` method is called - if true, we can save that form which result all the data is saved to the DB (For create operations, it creates a new record. For update operations, it updates the existing record) and redirect the user to our index page. We can use this same form to create and update items.

def create_item(request):
   form = ItemForm(request.POST or None)

   if form.is_valid():
      form.save()
      return redirect("food:index")
   
   return render(request,'food/item-form.html',{'form':form})

<form action="POST">
   {% csrf_token %}
   {{form}}
   <button type="submit">Save</button>
</form>

**Step-by-Step Process:**

**CREATE:**
- **First visit**: `form = ItemForm(None)` - empty form instance
- **User submits**: Same view function runs again, `form = ItemForm(request.POST)` - NEW form instance with user data
- User doesn't see this filled form because `form.is_valid()` is true → redirected to index

**UPDATE:**
- **First visit**: `form = ItemForm(None, instance=item)` - form instance pre-filled with existing item data
- **User submits**: Same view function runs again, `form = ItemForm(request.POST, instance=item)` - NEW form instance with user's modified data
- User doesn't see this form because `form.is_valid()` is true → redirected to index

Each time the view runs, it creates a fresh form instance. You only see the form when validation fails or on first visit.

In Django templates, when a form is submitted, the same view function that rendered that template gets called again when the submit button is pressed.

When we create or update an item, we call form.save() if form.is_valid() is true. But when we delete an item, we call item.delete() - we call delete on the item object itself. Both perform operations in the database.
form.is_valid() checks all the fields in the form for validation errors.

### Authentication

Create a new app and add that app to INSTALLED_APPS.

For authentication, we use Django's built-in forms. Django comes with authentication logic and built-in forms.

```python
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Welcome {username}, your account is created")
            return redirect("food:index")
    else:
        form = UserCreationForm()
    return render(request, 'user/register.html', {"form": form})
```
UserCreationForm is a built-in form which is by default connected to the built-in User model.
So this UserCreationForm creates a basic HTML form and also whatever user inputs after submit, it stores to the user table. We don't need to create a users table by ourselves - all of that is handled by Django.

We don't need to run migrate command here because we're not changing the database schema - we're just storing form data to Django's already existing user table. When the request is POST and form is valid, we simply save the inputs to this pre-existing table. Django always comes with a default user table (stored in SQLite3) where admin data is kept, so UserCreationForm doesn't need a model specified since it's already connected to this built-in table.

Django's pre-installed apps ('django.contrib.admin' and 'django.contrib.auth') automatically create a user table in whatever database you connect (MySQL, SQLite3, PostgreSQL) so the admin panel works properly.but it happens through the migration system rather than being completely automatic upon database connection.

If you want to use a custom user model instead, you'd need to create a separate model and configure UserCreationForm to use it - otherwise, form data saves to Django's default user table. This way Django always provides a built-in user model regardless of your database choice.


## How to add an additional field on built-in form?

1. Create your own form in forms.py
2. Inherit the built-in form (UserCreationForm)
3. Add your own fields
4. Then define the Meta class to tell Django what model to choose and what fields we want for that model

Now we can create an instance from this form and render that instance into the template. Now those additional fields will be there in that form, but if those fields don't exist on the model then input on those fields will do nothing.

```python
class RegisterForm(UserCreationForm):
    # add custom fields
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "phone"]
```

## How to add additional fields on built-in model (like User)?

1. Create a model class
2. Create a field which is linked with that existing model
3. Create the additional fields
4. Run `makemigrations`
5. Run `migrate`
6. Add that model to admin.py to see in admin panel
7. Done

```python
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
```

This way we create a new model that extends the User model, so another table will be created which is separate from but connected to the user table and has those additional fields that I provided.

For login and logout we use Django's built-in views.

So to use built-in views we need to attach them with URL in root project urls.py and setup templates to function properly. And since these views pass `form` as context, so inside the template which is linking with these views can also accept `form`.

```python
path("login/", authentication_views.LoginView.as_view(template_name="user/login.html"), name="login"),
path("logout/", authentication_views.LogoutView.as_view(template_name="user/logout.html"), name="logout"),
```

## How does Django handle login/logout? Where does it store the login state - in RAM or in DB? How does it determine if the request is coming from a logged-in user or not?

Django uses **session-based authentication** by default. Here's how it works:

Whenever a user successfully logs in, Django creates a session ID and stores that session ID in the browser cookie, and stores session data in the database session table not in RAM. On each request, Django checks the session ID from the cookie against the session from db - if valid, then Django provides request.user to all view functions and also provides the user details as context to templates rendered through views.
Django checks session ID cookie against the database session table for every request once the session middleware is enabled (which it is by default). This happens regardless of whether your app has login features or not - Django's session middleware runs on every request 

 Django can manage login state with sessions regardless of whether you use the built-in User model or a custom user model. As long as you set AUTH_USER_MODEL in settings.py to point to your custom model, Django's session-based authentication works exactly the same way.

## Template Context and Custom User Models

Every template Django sends some built-in context. Like every template Django sends `user` - we can see logged-in user details by just accessing `{{user}}` on any template rendered through views.

But the question is: if we store the login user into my custom table instead of Django's built-in user table, in that case can Django still send the proper user details to every template? If yes, then how?

**Answer:** Yes, Django will still send the proper user details to every template even with a custom user model. Here's how:

- When you set `AUTH_USER_MODEL` in settings.py to point to your custom user model, Django automatically uses that model for authentication
- Django's authentication middleware will load your custom user model instance
- The `{{user}}` context variable in templates will contain your custom user model instance with all its fields and methods
- Everything works the same way - Django just uses your custom model instead of the default User model

So whether you use Django's built-in User model or your custom user model, the `{{user}}` template context will always work properly.

So one thing we can add additional fields to already existing model or table which is user, we do that by creating separate model and we link with that foreign key field and then add our additional fields in this model, but another thing we can do is we can create separately different model and configure that model in settings.py and make django work its authentication session middleware everything using that model instead of that default user model.

### How to restrict a particular page?

Using decorator:

```python
@login_required
def profile(request):
    return render(request, 'user/profile.html')
```

Now this view can & that profile.html page will only be rendered if user is logged in.

Then in settings.py add:
```python
LOGIN_URL = "login"
```
So if user is not logged in and tries to access that template then he is automatically redirected to the URL which is named as "login".

