from django.contrib import admin

from .models import Movie,Rating, Review, Report
from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import path
from .models import Movie, Rating, Review, Report

class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

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
