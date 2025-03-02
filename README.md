# GlobeTrotters
This is **GlobeTrotters**, a full-stack web app where users get cryptic clues about a famous place and must guess which destination it refers to. Once they guess, they’ll unlock fun facts, trivia, and surprises about the destination!
This web-app is deployed over railways [here](https://globetrotters-production.up.railway.app/accounts/login/#).

## Rules and Regulations-

- During each game, you'll be provided 2 clues about the *new destination* that you need to guess.
- You'll be provided with 4 options, and you have to correctly guess the city from the clues provided.
- For each correct guess, you win **3 points**, and for each incorrect guess, you win **0 points**!
- Regardless of whether your guess is right or wrong, you'll get to learn two new fun facts about the destination in question.
- You've an option to challenge your friends (or enemies) to this game, by creating a unique invite that you can share, so compete away!.

## Built with-

- [Django](https://www.djangoproject.com/)- Backend Framework
- Plain Vanilla HTML, CSS and JS- For the front-end rendering
- [Bootstrap](https://getbootstrap.com/)- To add a little color
- [JQuery](https://jquery.com/)- Event listeners (here and there)
- [SQLite3](https://www.sqlite.org/index.html)- Database (on local sys)

## Directions for Setting up Environment-

To install the source, pre-requisites include-

- Python 3.6 or above
- Dependencies from requirements.txt

First, clone this repository onto your system. Then, create a virtual environment (I'm using pyenv but you can use anything):

```
cd path/to/folder
pyenv virtualenv 3.6.0 myenv
pyenv activate myenv
```

Now, install the python dependencies from requirements.txt:

```
pip install -r requirements.txt
```

Build the database by making migrations:
```
python manage.py makemigrations
python manage.py migrate
```

Finally, to pre-populate the "Destinations" table, run the following management command-
```
python manage.py load_destinations
```

## Directions to execute-

Inside the main project directory (the directory with the 'manage.py' file), run the following command to start the server-
```
python manage.py runserver
```

Now open the link shown in the terminal in any browser of your choice.
