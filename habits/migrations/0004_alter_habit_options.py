# Generated by Django 4.2 on 2024-10-14 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("habits", "0003_alter_habit_options_alter_habit_execution_time_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="habit",
            options={"verbose_name": "Привычка", "verbose_name_plural": "Привычки"},
        ),
    ]
