import os

# check if dependencies are installed
try:
    import django
except ImportError:
    print('Django not installed. Installing...')
    os.system('pip install -r requirements.txt')

# créer la db si elle n'existe pas
if not os.path.exists('db.sqlite3'):
    os.system('sqlite3 db.sqlite3')

# appliquer les migrations
os.system('python manage.py makemigrations')
os.system('python manage.py migrate')

# demander à l'utilisateur de créer un superuser si le fichier test_data n'existe pas
if not os.path.exists('test_data'):
    prompt = input('Voulez-vous créer un superuser ? (y/n) ')
    if prompt == 'y':
        os.system('python manage.py createsuperuser')
        open('test_data', 'x')
    else:
        print("Un superuser est nécessaire pour les fonctions d'administration.\nVous pourrez en créer un plus tard en relançaant ce script.\nou avec la commande 'python manage.py createsuperuser'.\nNotez que la presence du fichier 'tets_data' indique que vous avez créé le superuser via ce script.")

os.system('python manage.py runserver')

