# Generated by Django 2.2.3 on 2019-07-30 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_question_product_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='product_code',
            field=models.IntegerField(default=0, verbose_name='상품 코드'),
        ),
    ]