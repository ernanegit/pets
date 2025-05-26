from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('pets', '0001_initial'),  # Ajuste conforme sua última migração
    ]

    operations = [
        migrations.AddField(
            model_name='morador',
            name='tipo_residencia',
            field=models.CharField(
                choices=[('apartamento', 'Apartamento'), ('casa', 'Casa'), ('cobertura', 'Cobertura'), ('loft', 'Loft')],
                default='apartamento',
                max_length=20,
                verbose_name='Tipo de Residência'
            ),
        ),
        migrations.AddField(
            model_name='morador',
            name='numero_residencia',
            field=models.CharField(
                default='',
                help_text='Número do apartamento/casa',
                max_length=10,
                verbose_name='Número'
            ),
            preserve_default=False,
        ),
    ]
