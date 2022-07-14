<!-- Please update value in the {}  -->

<h1 align="center">TODO App</h1>

<!-- TABLE OF CONTENTS -->

## Table of Contents

- [Overview](#overview)
- [Built With](#built-with)
- [Features](#features)
- [How to use](#how-to-use)
- [Acknowledgements](#acknowledgements)
- [Contact](#contact)

<!-- OVERVIEW -->

## Overview


![screenshot](https://user-images.githubusercontent.com/16707738/92399059-5716eb00-f132-11ea-8b14-bcacdc8ec97b.png)

### Built With

<!-- This section should list any major frameworks that you built your project using. Here are a few examples.-->

- HTML
- CSS
- Django

## How To Use

<!-- This is an example, please update according to your application -->

To clone and run this application, you'll need [Git](https://git-scm.com) 
You can also find preclass version archived in folder if you want to start over.
# Clone this repository
$ git clone https://github.com/savasgormus/django-todo-app.git

# Install dependencies
    $ python -m venv env
    > env/Scripts/activate (for win OS)
    $ source env/bin/activate (for macOs/linux OS)
    $ pip install -r requirements.txt

# Run the app
$ python manage.py runserver
```

## Acknowledgements
- Practice Django to implement CRUD (Create, Read, Update, Delete) operations.
- The root url will be a Todo form. Users can submit a new todo using this form.
- After submission, the user will be linked to "list" page. Or they can go to the list page with a direct link.
- In list page, users will see the "Title", "Description", "Priority", and "isCompleted" of the TODO. Here there will be "Add New", "Update", and "Delete" buttons.
- "Add New" will go to the "TODO" form.
- "Update" will go to the related TODO filled form, which can be updated.
- "Delete" will erase the related TODO, and continue to show the list page.

## Contact

- GitHub (https://github.com/savasgormus/)

- Linkedin (https://www.linkedin.com/in/savasgormus/)
- Twitter (https://twitter.com/savasgormus1/)
