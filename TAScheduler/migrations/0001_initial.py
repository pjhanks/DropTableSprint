# Generated by Django 4.0.3 on 2022-04-23 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='classTAAssignments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('courseCode', models.CharField(default='12345', max_length=9, primary_key=True, serialize=False)),
                ('courseNumber', models.CharField(default='101', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('userID', models.CharField(max_length=9, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=40)),
                ('email', models.CharField(max_length=40)),
                ('phoneNumber', models.CharField(max_length=20)),
                ('role', models.CharField(max_length=11)),
                ('password', models.CharField(default='123', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='TA',
            fields=[
                ('TACode', models.CharField(default='42', max_length=20, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Sections',
            fields=[
                ('sectionCode', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('TA', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='TAScheduler.myuser')),
                ('parentCode', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='TAScheduler.course')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='TAname',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='TAScheduler.ta'),
        ),
        migrations.AddField(
            model_name='course',
            name='instructorID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='TAScheduler.myuser'),
        ),
    ]