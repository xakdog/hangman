# Generated by Django 2.1.7 on 2019-02-19 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sessions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameBoard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.SmallIntegerField(choices=[(10, 'started'), (20, 'goes-on'), (30, 'won'), (40, 'failed')])),
                ('word', models.CharField(max_length=14)),
                ('opened', models.CharField(max_length=14)),
                ('mistakes', models.CharField(max_length=5)),
                ('session', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sessions.Session')),
            ],
        ),
        migrations.CreateModel(
            name='GameScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('mistakes', models.IntegerField()),
                ('time_spent', models.IntegerField()),
                ('word_length', models.IntegerField()),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sessions.Session')),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=14, unique=True)),
            ],
        ),
    ]
