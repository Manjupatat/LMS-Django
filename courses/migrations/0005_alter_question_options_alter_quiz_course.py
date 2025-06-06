# Generated by Django 5.2 on 2025-05-04 16:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_alter_lesson_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='options',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='course',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='quiz', to='courses.course'),
        ),
    ]
