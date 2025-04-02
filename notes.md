
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
- **`urls.py`** → Defines URL patterns for handling requests.  
- **`wsgi.py`** → Used for deploying with WSGI servers (traditional synchronous requests).  
- **`asgi.py`** → Used for deploying with ASGI servers (supports async features like WebSockets).  


### **When are `wsgi.py` and `asgi.py` used?**  
- These files are only needed **when deploying** Django to a server.  
- They act as an entry point for the server to communicate with your Django app.  

Both servers **run Django**, but ASGI supports additional features like WebSockets 

Here's the corrected version of your text:  

---

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