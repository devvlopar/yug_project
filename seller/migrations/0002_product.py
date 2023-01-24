# Generated by Django 4.1.4 on 2023-01-24 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=150)),
                ('des', models.CharField(max_length=150)),
                ('price', models.DecimalField(decimal_places=2, default=500, max_digits=6)),
                ('pic', models.FileField(default='sad.jpg', upload_to='products_images')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.seller')),
            ],
        ),
    ]