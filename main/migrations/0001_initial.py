# Generated by Django 4.1.4 on 2023-01-05 18:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='nomi')),
                ('slug', models.SlugField(max_length=128, verbose_name='slug')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='MontylyReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('income', models.IntegerField(verbose_name='kirim')),
                ('outcome', models.PositiveIntegerField(verbose_name='chiqim')),
                ('sells', models.PositiveIntegerField(verbose_name='sotildi')),
                ('stock', models.PositiveIntegerField(verbose_name='sotib olindi')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('measure', models.CharField(choices=[('Metr', 'metr'), ('kg', 'kg'), ('sonida', 'number')], max_length=256)),
                ('quantity', models.PositiveIntegerField()),
                ('buy', models.PositiveIntegerField()),
                ('sell', models.PositiveIntegerField()),
                ('is_calc', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group', to='main.group')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='HistoryProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode', models.CharField(choices=[('add', "qo'shish"), ('sale', 'Sotish')], max_length=128)),
                ('quantity', models.PositiveIntegerField()),
                ('price', models.IntegerField(blank=True)),
                ('is_calc', models.BooleanField(default=True)),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', related_query_name='product', to='main.product')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.PositiveIntegerField()),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('history', models.ManyToManyField(to='main.historyproduct')),
            ],
        ),
    ]
