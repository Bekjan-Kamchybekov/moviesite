from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'age',
                  'phone_number', 'status']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Profile.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'last_name', 'first_name', 'age', 'phone_number', 'status']


class ProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'status']


class CountrySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_name']


class DirectorSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['director_name']


class ActorSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['actor_name']


class MovieListLanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieLanguages
        fields = ['id', 'language']

class MovieDetailLanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieLanguages
        fields = ['id', 'language', 'video', 'movie', ]


class MovieLanguagesSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieLanguages
        fields = ['language', 'video']


class MomentsSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moments
        fields = ['movie_moments']


class MovieSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    year = serializers.DateField(format='%Y')


    class Meta:
        model = Movie
        fields = ['movie_name', 'movie_image', 'average_rating', 'year',
                  'status']

    def get_average_rating(self, obj):
        return obj.get_average_rating()


class RatingSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format='%d-%m-%Y-%H-%M')
    user = ProfileSimpleSerializer()
    movie = MovieSerializer()

    class Meta:
        model = Rating
        fields = ['id', 'user', 'movie', 'stars', 'parent', 'text', 'created_date']


class RatingSimpleSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format='%d-%m-%Y-%H-%M')

    class Meta:
        model = Rating
        fields = ['id', 'user', 'parent', 'text', 'created_date']


class RatingsSimpleSerializer(serializers.ModelSerializer):
    user = ProfileSimpleSerializer()

    class Meta:
        model = Rating
        fields = ['id', 'user', 'parent', 'text']


class HistorySerializer(serializers.ModelSerializer):
    movie = MovieSerializer()
    user = ProfileSimpleSerializer()
    viewed_at = serializers.DateTimeField(format='%d-%m-%Y-%H-%M')

    class Meta:
        model = History
        fields = ['id', 'user', 'movie', 'viewed_at']


class GenreSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['genre_name']


class MovieListSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    country = CountrySimpleSerializer(many=True)
    year = serializers.DateField(format='%Y')



    class Meta:
        model = Movie
        fields = ['id', 'movie_name', 'movie_image', 'average_rating', 'year',
                  'country', 'status']

    def get_average_rating(self, obj):
        return obj.get_average_rating()


class MovieDetailSerializer(serializers.ModelSerializer):
    country = CountrySimpleSerializer(many=True)
    average_rating = serializers.SerializerMethodField()
    ratings = RatingsSimpleSerializer(read_only=True, many=True)
    director = DirectorSimpleSerializer(many=True)
    genre = GenreSimpleSerializer(many=True)
    actor = ActorSimpleSerializer(many=True)
    movie_languages = MovieLanguagesSimpleSerializer(read_only=True, many=True)
    moments = MomentsSimpleSerializer(read_only=True, many=True)
    year = serializers.DateField(format='%Y')

    class Meta:
        model = Movie
        fields = ['id', 'movie_name', 'movie_image', 'average_rating', 'year', 'country', 'director', 'genre', 'types',
                  'movie_time', 'description', 'movie_trailer', 'status', 'actor', 'movie_languages', 'moments',
                  'ratings']

    def get_average_rating(self, obj):
        return obj.get_average_rating()


class GenreDetailSerializer(serializers.ModelSerializer):
    movie = MovieListSerializer(many=True)

    class Meta:
        model = Genre
        fields = ['id', 'genre_name', 'movie']


class GenreListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ['id', 'genre_name']


class FavoriteMovieSerializer(serializers.ModelSerializer):
    movie_id = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all(), write_only=True, source='movie')
    movie = MovieListSerializer()

    class Meta:
        model = FavoriteMovie
        fields = ['movie', 'movie_id']


class FavoriteSerializer(serializers.ModelSerializer):
    user = ProfileSimpleSerializer()
    favorite_movie = FavoriteMovieSerializer(read_only=True, many=True)
    created_date = serializers.DateTimeField(format='%d-%m-%Y %H:%M')

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'favorite_movie', 'created_date']


class ActorDetailSerializer(serializers.ModelSerializer):
    movie = MovieListSerializer(many=True)

    class Meta:
        model = Actor
        fields = ['id', 'actor_name', 'biography', 'age', 'actor_image', 'movie']

class ActorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'actor_name']


class DirectorDetailSerializer(serializers.ModelSerializer):
    movie = MovieListSerializer(many=True)

    class Meta:
        model = Director
        fields = ['id', 'director_name', 'biography', 'age', 'director_image', 'movie']

class DirectorListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Director
        fields = ['id', 'director_name']


class CountryDetailSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(many=True)

    class Meta:
        model = Country
        fields = ['id', 'country_name', 'movie']


class CountryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'country_name']

class MovieNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['movie_name']

    def get_average_rating(self, obj):
        return obj.get_average_rating()

class MomentsListSerializer(serializers.ModelSerializer):
    movie = MovieNameSerializer()
    class Meta:
        model = Moments
        fields = ['id', 'movie', 'movie_moments']

class MomentsDetailSerializer(serializers.ModelSerializer):
    movie = MovieSerializer()
    class Meta:
        model = Moments
        fields = ['id', 'movie', 'movie_moments']