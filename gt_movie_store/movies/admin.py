from django.contrib import admin
from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import path

from .models import Movie, Rating, Review, Report

class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

    
class MovieEngagementAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('most-purchased', self.admin_view(self.most_purchased_view), name='engagement.most_purchased'),
        ]
        return custom_urls + urls

    def most_purchased_view(self, request: HttpRequest) -> HttpResponse:

        most_purchased = Movie.objects.get(id=1)
        most_reviewed = Movie.objects.get(id=1)
        
        most_purchased = []
        most_reviewed = []
        most_purchased_amt = 0
        most_reviewed_amt = 0
        for movie in Movie.objects.all():
            print("movie, ", movie)
            if movie.purchase_count > most_purchased_amt:
                most_purchased.clear()
                most_purchased.append(movie.name)
                most_purchased_amt = movie.purchase_count
                print("Updating most purchased ", movie.name)
                print('most purchased amt: ', most_purchased_amt)
            elif movie.purchase_count == most_purchased_amt:
                most_purchased.append(movie.name)

            
            print("movie review count ", movie.review_count)
            if movie.review_count > most_reviewed_amt:
                
                print("this has gotten here")
                most_reviewed.clear()
                most_reviewed.append(movie.name)
                most_reviewed_amt = movie.purchase_count                
            elif movie.review_count == most_reviewed_amt:
                most_reviewed.append(movie.name)


        template_data = {
            **self.each_context(request),
        }
        template_data['title'] = "Engagement"
        template_data['most_purchased'] = most_purchased
        template_data['purchase_amount'] = most_purchased_amt
        template_data['most_reviewed'] = most_reviewed
        template_data['review_amount'] = most_reviewed_amt
        return render(request, 'movies/engagement.html', template_data)

movie_engagement_admin_site = MovieEngagementAdminSite(name="movie_engagement_admin_site")


admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
admin.site.register(Report)


from typing import override

class ReviewEngagementAdminSite(admin.AdminSite):
    @override
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('most-reviews', self.admin_view(self.most_reviews_view), name='reviews-engagement.most_reviews'),
        ]
        print(custom_urls)
        return custom_urls + urls

    def most_reviews_view(self, request: HttpRequest) -> HttpResponse:
        users = get_user_model().objects.all()

        high_user = None
        high_review_count = 0
        for user in users:
            reviews = Review.objects.filter(user=user)

            review_count = len(reviews)

            if review_count > high_review_count or high_user is None:
                high_user = user
                high_review_count = review_count

        template_data = {
            **self.each_context(request),
        }
        template_data['title'] = "User Most Reviews"
        template_data['user'] = request.user
        template_data['highest_review_count_user'] = high_user
        template_data['review_count'] = high_review_count
        return render(request, 'movies/most_reviews.html', template_data)

review_engagement_admin_site = ReviewEngagementAdminSite(name="reviews_engagement_admin")
admin.site.register(Rating)
