# Generated by Django 4.1 on 2022-08-17 04:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=128)),
                ('phone', models.CharField(max_length=56)),
                ('summa', models.IntegerField()),
                ('person_type', models.CharField(choices=[('Jismoniy shaxs', 'Jismoniy shaxs'), ('Yuridik shaxs', 'Yuridik shaxs')], max_length=128)),
                ('status', models.CharField(choices=[('Yangi', 'Yangi'), ('Moderiyatsada', 'Moderiyatsada'), ('Tasdiqlangan', 'Tasdiqlangan'), ('Bekor qilingan', 'Bekor qilingan')], default='Yangi', max_length=128)),
                ('company_name', models.CharField(blank=True, max_length=128, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=128)),
                ('phone', models.CharField(max_length=56)),
                ('university', models.CharField(choices=[('Toshkent shahridagi INHA universiteti', 'Toshkent shahridagi INHA universiteti'), ('Westminister University', 'Westminister University'), ("O'zbekiston milliy universiteti", "O'zbekiston milliy universiteti"), ('Toshkent davlat iqtisodiyot universiteti', 'Toshkent davlat iqtisodiyot universiteti'), ("O'zbekiston davlat jahon tillari universiteti", "O'zbekiston davlat jahon tillari universiteti")], max_length=256)),
                ('student_type', models.CharField(choices=[('Bakalavr', 'Bakalavr'), ('Magistr', 'Magistr')], max_length=56)),
                ('contract_amount', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Funding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('sponsor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='funding', to='api.sponsor')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='funding', to='api.student')),
            ],
        ),
    ]
