# Generated by Django 4.0.1 on 2022-02-03 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stores_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery', models.CharField(max_length=25, null=True)),
                ('city', models.CharField(max_length=25, null=True)),
                ('address', models.TextField(max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('final_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.IntegerField(null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_products', to='orders_app.order')),
                ('seller_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_products', to='stores_app.sellerproduct')),
            ],
        ),
    ]
