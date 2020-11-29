# Generated by Django 3.1.1 on 2020-11-25 06:21

from django.db import migrations, models
import django.db.models.deletion
import store.models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20201114_1714'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookSearch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search', models.CharField(blank=True, max_length=120)),
                ('sort_by', models.CharField(choices=[('TITLE', 'Title'), ('GENRE', 'Genre'), ('ISBN', 'ISBN'), ('AUTHOR', 'Author')], default=store.models.SortBy['TITLE'], max_length=10)),
                ('genre', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='store.genre')),
            ],
        ),
    ]