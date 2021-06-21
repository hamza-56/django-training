How To:

1) Create and activate python virtual env using pyenv
2) `pip install -r requirements.txt`
3) `python manage.py runserver`

Assumptions:

1) No database mentioned: using sqlite3

Approach:

1) Using django's built-in login and logout views with custom templates
2) Using bootstrap for basic front-end styles
3) Bootstrap is defined in base.html and other templates extend base
4) As first_name and last_name are already stored in User's table. Modified the Profile model form to set first_name, last_name when profile is updated
5) only logged in users can update profile
