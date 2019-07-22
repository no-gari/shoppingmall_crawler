# Generated by Django 2.2.3 on 2019-07-19 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='카테고리 이름')),
            ],
            options={
                'verbose_name': '카테고리',
                'verbose_name_plural': '카테고리',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.CharField(max_length=2000, verbose_name='질문 내용')),
                ('date', models.DateTimeField(verbose_name='등록 시간')),
                ('category', models.ForeignKey(on_delete='CASCADE', to='core.Category', verbose_name='카테고리')),
            ],
            options={
                'verbose_name': '질문',
                'verbose_name_plural': '질문',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=2000, verbose_name='답변 내용')),
                ('date', models.DateTimeField(verbose_name='등록 시간')),
                ('title', models.ForeignKey(on_delete='CASCADE', to='core.Question', verbose_name='질문')),
            ],
            options={
                'verbose_name': '답변',
                'verbose_name_plural': '답변',
            },
        ),
    ]
