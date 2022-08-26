import datetime

from django.db import models

from account.models import UserProfile


class Category(models.Model):
    title = models.CharField(max_length=100)
    icon_image = models.ImageField(max_length=100)

    def __str__(self):
        return self.title


class Subcategory(models.Model):
    category = models.ForeignKey(Category, related_name='Subcategory_Category', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name='Subcategory')

    def __str__(self):
        return self.title


class City(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class PhoneNumber(models.Model):
    phone_number_0 = models.CharField(max_length=10)

    def __str__(self):
        return self.phone_number_0


STATUS = (
        ('in_progress', 'in_pprigress'),
        ('verified', 'verified'),
        ('rejected', 'rejected')
    )

class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    category = models.ForeignKey(Category, related_name='Post_category', on_delete=models.RESTRICT)
    subcategory = models.ForeignKey(Subcategory, related_name='Post_subcategory', on_delete=models.CASCADE)
    city = models.ForeignKey(City, related_name='Post_City', on_delete=models.CASCADE)
    phone_number = models.ForeignKey(PhoneNumber, related_name='Post_PhoneNumber', on_delete=models.PROTECT)
    user = models.ForeignKey(UserProfile, related_name='Post_User', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name='Фотография')
    from_price = models.IntegerField()
    to_price = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=100)
    is_activated = models.BooleanField()
    status = models.CharField(max_length=100, choices=STATUS, default=('in_progress', 'in_progress'))


    def __str__(self):
        return self.title


class Views(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField()
    post = models.ForeignKey(Post, related_name='Views_Post', on_delete=models.CASCADE)


class Image(models.Model):
    post = models.ForeignKey(Post, related_name='Image_Post', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name='Фотография')


class Favorite(models.Model):
    post = models.ManyToManyField(Post, related_name='Favorite_Post')
    user = models.ForeignKey(UserProfile, related_name='Favorite_User', on_delete=models.CASCADE)


LIST = (
    ('VIP', 'VIP'),
    ('ordinary', 'ordinary'),
    ('urgent', 'urgent')
)


class Subscription(models.Model):
    post = models.ForeignKey(Post, related_name='Subscription', on_delete=models.CASCADE)
    choice = models.CharField(max_length=100, choices=LIST, default=('ordinary', 'ordinary'))
    date_created = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)


from django.db import models

# Create your models here.
