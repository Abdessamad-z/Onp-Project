# Generated by Django 4.0.2 on 2022-08-06 15:27

from django.db import migrations, models
import django.db.models.deletion
import gestion_clients.models
import gestion_clients.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(null=True, upload_to=gestion_clients.models.user_directory_path, validators=[gestion_clients.validators.validate_file_extension])),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='documents', to='gestion_clients.client')),
            ],
        ),
        migrations.CreateModel(
            name='ActeCessionMareyeur',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='gestion_clients.document')),
            ],
            bases=('gestion_clients.document',),
        ),
        migrations.CreateModel(
            name='ActeCessionNavire',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='gestion_clients.document')),
            ],
            bases=('gestion_clients.document',),
        ),
        migrations.CreateModel(
            name='ActeNationaliteNavire',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='gestion_clients.document')),
            ],
            bases=('gestion_clients.document',),
        ),
        migrations.CreateModel(
            name='ArmateurRcNavire',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='gestion_clients.document')),
            ],
            bases=('gestion_clients.document',),
        ),
        migrations.CreateModel(
            name='CarteAutorisationMareyeur',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='gestion_clients.document')),
            ],
            bases=('gestion_clients.document',),
        ),
        migrations.CreateModel(
            name='CinMareyeur',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='gestion_clients.document')),
            ],
            bases=('gestion_clients.document',),
        ),
        migrations.CreateModel(
            name='DiversMareyeur',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='gestion_clients.document')),
            ],
            bases=('gestion_clients.document',),
        ),
        migrations.CreateModel(
            name='DiversNavire',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='gestion_clients.document')),
            ],
            bases=('gestion_clients.document',),
        ),
        migrations.CreateModel(
            name='Mareyeur',
            fields=[
                ('client_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='gestion_clients.client')),
                ('code_national', models.CharField(max_length=30, primary_key=True, serialize=False)),
            ],
            bases=('gestion_clients.client',),
        ),
        migrations.CreateModel(
            name='Navire',
            fields=[
                ('client_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='gestion_clients.client')),
                ('matricule', models.CharField(max_length=30, primary_key=True, serialize=False)),
            ],
            bases=('gestion_clients.client',),
        ),
        migrations.CreateModel(
            name='RcStatutMareyeur',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='gestion_clients.document')),
            ],
            bases=('gestion_clients.document',),
        ),
    ]
