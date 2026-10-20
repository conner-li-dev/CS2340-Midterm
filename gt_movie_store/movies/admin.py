from django.contrib import admin
from .models import Movie, Review, Report
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import path

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