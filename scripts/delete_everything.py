import os

os.environ['DJANGO_SETTINGS_MODULE']='bookstore.settings'

from store.models import Genre, Book, Author, Publisher

print('THIS IS VERY DESTRUCTIVE, IT WILL DELETE EVERYTHING IN THE DATABASE.')
response = input('Are you sure you want to continue?[yes/n]')

if response == 'yes':
    print('Deleting...')
    Book.objects.all().delete()
    Genre.objects.all().delete()
    Publisher.objects.all().delete()
    Author.objects.all().delete()
    print('Database emptied...')

else:
    print('Keeping data... Not deleting anything.')
