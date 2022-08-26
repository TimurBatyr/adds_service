from rest_framework import serializers

from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', 'icon_image')


class Subscription(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['choice']


class SubscriptionSerializer(serializers.ModelSerializer):
    Subscription = Subscription(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'from_price', 'image', 'subcategory', 'Subscription')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'from_price', 'image', 'subscription')


class AddPostSerializer(serializers.ModelSerializer):
    # Image_Post = ImageSerializer(many=True, read_only=True)  # Вложенный Сериализатор
    Image_Post = serializers.StringRelatedField(many=True)

    class Meta:
        model = Post
        fields = ('id', 'category', 'subcategory',
                  'title', 'from_price', 'to_price',
                  'description', 'image', 'Image_Post', 'city',
                  'email', 'phone_number'
                  )

    exclude = ('status',)

# class DetailPostSerializer(serializers.ModelSerializer):
#     category = CategorySerializer
#
#     class Meta:
#         model = Post
#         fields = '__all__'
#
#     exclude = ('status',)


class NewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'from_price', 'image', 'subcategory', 'date_created')

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields =('title','image','from_price','subcategory')