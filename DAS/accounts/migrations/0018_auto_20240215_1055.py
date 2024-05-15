from django.db import migrations


def create_django_admin_log(apps, schema_editor):
    schema_editor.execute(
        """
        CREATE TABLE django_admin_log (
    id serial NOT NULL PRIMARY KEY,
    action_time timestamp with time zone NOT NULL,
    object_id text NULL,
    object_repr text NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer NULL,
    user_id integer NOT NULL,
    FOREIGN KEY (content_type_id) REFERENCES django_content_type (id),
    FOREIGN KEY (user_id) REFERENCES auth_user (id)
);
        """
    )


def reverse_create_django_admin_log(apps, schema_editor):
    schema_editor.execute("DROP TABLE django_admin_log;")


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0017_alter_accountusers_managers'),
    ]

    operations = [
        migrations.RunPython(create_django_admin_log, reverse_code=reverse_create_django_admin_log),
    ]
