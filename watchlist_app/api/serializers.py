from rest_framework import serializers
from watchlist_app.models import WatchList,StreamPlatform,Review

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        # fields = "__all__"
        exclude = ('watchlist',)

class WatchlistSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many = True,read_only = True)
    # rating = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    platform_name = serializers.SerializerMethodField()
    class Meta:
        model = WatchList
        fields = "__all__"
        #fields = ["name", "description','id']
        #exclude=['description']    
    def get_platform_name(self,object):
        pk = object.platform_id
        name1 = StreamPlatform.objects.get(id=pk)
        return name1.name
    def get_average_rating(self,object):
        pk = object.id
        reviews = Review.objects.filter(watchlist_id=pk)
        # print('this are reviews',reviews)
        # print(type(reviews))
        # print(len(reviews))
        # print(reviews.count())
        # print([i.rating for i in reviews])
        if reviews.count() >0:
            avg_rat = sum([i.rating for i in reviews])/reviews.count()
        else:
            avg_rat = {'error':'No reviews available'}
        return avg_rat

    def get_total_reviews(self,object):
        pk = object.id
        reviews = Review.objects.filter(watchlist_id=pk)
        return reviews.count()

    # def get_rating(self,object):
    #     try:
    #         pk = object.id
    #         name1 = Review.objects.filter(watchlist_id=pk)
    #         name2 = { {"rating":i.rating} for i in name1}
    #         return name2
    #     except:
    #         abc = {'error':'No Rating found'}
    #         return abc

class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchlistSerializer(many = True,read_only = True)
    class Meta:
        model = StreamPlatform
        fields ="__all__"

        
# def name_length(value):
#      if len(value)<2:
#             raise serializers.ValidationError('Name is too short')

# class MoiveSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active= serializers.BooleanField()

#     def create(self,validated_data):
#         return Movie.objects.create(**validated_data)
    
#     def update(self,instance,validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance

#     def validate(self,data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError('name and description should not be the same')
#         else:
#             return data

    # def validate_name(self,value):
    #     if len(value)<2:
    #         raise serializers.ValidationError('Name is too short')
    #     else:
    #         return va