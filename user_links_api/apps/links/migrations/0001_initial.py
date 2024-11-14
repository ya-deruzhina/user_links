# Generated by Django 5.0 on 2024-11-14 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('collections', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinksModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField()),
                ('description', models.TextField()),
                ('url_page', models.URLField()),
                ('kind_link', models.CharField(choices=[('WEBSITE', 'WEBSITE'), ('BOOK', 'BOOK'), ('ARTICLE', 'ARTICLE'), ('MUSIC', 'MUSIC'), ('VIDEO', 'VIDEO')], default='WEBSITE')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('collection', models.ManyToManyField(null=True, to='collections.collectionmodel')),
            ],
        ),
    ]
