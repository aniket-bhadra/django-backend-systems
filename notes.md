
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