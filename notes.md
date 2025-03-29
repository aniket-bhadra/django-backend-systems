
```bash
django-admin startproject folderName
```
This creates a new Django project inside a folder named **folderName**.

inside that folder, Django creates:  
1. A **project folder** (contains project files).  
2. **manage.py** (used to interact with the project, e.g., starting the server).  

Inside the project folder:  
- **`__init__.py`** → Makes the folder a Python package.  
- **`settings.py`** → Stores project configurations (similar to `package.json`).  
- **`urls.py`** → Defines URL patterns for handling requests.  
- **`wsgi.py`** → Used for deploying the project with WSGI servers.
A WSGI server runs Django applications in production by handling HTTP requests and passing them to the Django app.