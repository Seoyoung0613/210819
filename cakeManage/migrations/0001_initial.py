# Generated by Django 3.2.5 on 2021-08-15 09:56

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cake',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cakename', models.CharField(default='', max_length=200)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('body', models.TextField(default='')),
                ('cake_image', models.ImageField(null=True, upload_to='cakeimages/')),
                ('맛', models.CharField(max_length=200)),
                ('모양', models.CharField(max_length=200)),
                ('사이즈', models.CharField(max_length=200)),
                ('크림종류', models.CharField(max_length=200)),
                ('레터링색', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='주문 날짜')),
                ('reviewing', models.IntegerField(default=1)),
                ('희망픽업일', models.CharField(default=datetime.date.today, max_length=30, null=True)),
                ('희망픽업시간', models.CharField(choices=[('10:00', '10:00'), ('10:30', '10:30'), ('11:00', '11:00'), ('11:30', '11:30'), ('12:00', '12:00'), ('12:30', '12:30'), ('13:00', '13:00'), ('14:30', '14:30'), ('15:00', '15:00'), ('15:30', '15:30'), ('16:00', '16:00'), ('16:30', '16:30'), ('17:00', '17:00'), ('17:30', '17:30'), ('18:00', '18:00'), ('18:30', '18:30')], default='10:00', max_length=30, null=True)),
                ('레터링위치', models.CharField(choices=[('판 위에 레터링', '판 위에 레터링'), ('케이크에 직접 레터링', '케이크에 직접 레터링')], default='케이크에 직접 레터링', max_length=30, null=True)),
                ('is_accepted', models.BooleanField(default=False, verbose_name='가게 승인')),
                ('is_active', models.BooleanField(default=True, verbose_name='진행중')),
                ('is_paid', models.BooleanField(default=False, verbose_name='결제완료')),
                ('맛', models.CharField(max_length=15)),
                ('모양', models.CharField(max_length=15)),
                ('사이즈', models.CharField(max_length=15)),
                ('크림종류', models.CharField(max_length=15)),
                ('레터링색', models.CharField(max_length=15)),
                ('원하시는도안사진첨부', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='사진 첨부(도시락케이크 선택시)')),
                ('referred_cake', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cakeManage.cake', verbose_name='선택 케이크')),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('store_image', models.ImageField(upload_to='storeimages/')),
                ('text', models.TextField(blank=True, default='')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('contact', models.CharField(max_length=15)),
                ('location', models.CharField(choices=[('종로구', '종로구'), ('중구', '중구'), ('용산구', '용산구'), ('성동구', '성동구'), ('광진구', '광진구'), ('동대문구', '동대문구'), ('중랑구', '중랑구'), ('성북구', '성북구'), ('강북구', '강북구'), ('도봉구', '도봉구'), ('노원구', '노원구'), ('은평구', '은평구'), ('서대문구', '서대문구'), ('마포구', '마포구'), ('양천구', '양천구'), ('강서구', '강서구'), ('구로구', '구로구'), ('금천구', '금천구'), ('영등포구', '영등포구'), ('동작구', '동작구'), ('관악구', '관악구'), ('서초구', '서초구'), ('강남구', '강남구'), ('송파구', '송파구'), ('강동구', '강동구')], default='마포구', max_length=10)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('users_liked', models.ManyToManyField(blank=True, related_name='users_liked_store', related_query_name='users_liked_store', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('comment', models.TextField(blank=True, default='')),
                ('rate', models.IntegerField(default=0)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cakeManage.order')),
                ('referred_cake', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cakeManage.cake')),
                ('referred_store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cakeManage.store')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='referred_store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cakeManage.store', verbose_name='가게'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='주문자'),
        ),
        migrations.AddField(
            model_name='cake',
            name='referred_store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cakeManage.store'),
        ),
        migrations.AddField(
            model_name='cake',
            name='users_liked',
            field=models.ManyToManyField(blank=True, related_name='users_liked_cake', related_query_name='users_liked_cake', to=settings.AUTH_USER_MODEL),
        ),
    ]
