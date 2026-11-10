from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_contact'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='doctor',
            new_name='doctor_name',
        ),
    ]
