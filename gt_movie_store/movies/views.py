from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Avg
from django.views.decorators.http import require_POST

from .models import Movie, Report, Review, Rating
from .forms import RatingForm


def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()

    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(
        request,
        'movies/index.html',
        {'template_data': template_data},
    )

def show(request, id, rating_form = None):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)

    user_rating = None

    
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(
            movie = movie,
            user = request.user,
        ).first()

        if rating_form is None:
            rating_form = RatingForm(initial =
            {"score" : user_rating.stars} if user_rating else {})

        reports = Report.objects.filter(review__in=reviews, user=request.user)

        reported_reviews = [report.review for report in reports]
        shown_reviews = []
        for review in reviews:
            if review not in reported_reviews:
                shown_reviews.append(review)
    else:
        shown_reviews = reviews

    average_rating = Rating.objects.filter(movie = movie).aggregate(
                average = Avg("stars"))["average"]
    
    template_data = {}

    template_data["rating_form"] = rating_form
    template_data["average_rating"] = average_rating
    template_data["user_rating"] = user_rating
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = shown_reviews 
    return render(
        request,
        'movies/show.html',
        {'template_data': template_data},
    )

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment'].strip()
        review.movie = movie
        review.user = request.user
        review.save()
        movie.review_count = movie.review_count + 1
        movie.save()
    return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(
           request,
           'movies/edit_review.html',
           {'template_data': template_data},
        )
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment'].strip()
        review.save()
    return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    movie = Movie.objects.get(id=id)
    movie.review_count = movie.review_count - 1
    movie.save()
    return redirect('movies.show', id=id)

@login_required
def report_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Report Review'
        template_data['review'] = review
        template_data['movie'] = Movie.objects.get(id=id)
        return render(
            request,
            'movies/report_review.html',
            {'template_data': template_data},
        )
    elif request.method == 'POST' and request.POST['reason'] != '':
        report = Report()
        report.reason = request.POST['reason'].strip()
        report.review = review
        report.user = request.user
        report.save()

    return redirect('movies.show', id=id)

@login_required
@require_POST
def rate_movie(request, id):
    movie = get_object_or_404(Movie, id=id)
    form = RatingForm(request.POST)

    if (not form.is_valid()):
        return show(request, id, rating_form = form)

    Rating.objects.update_or_create(
        user = request.user,
        movie = movie,
        defaults= {"stars" : form.cleaned_data["score"]},
    )

    return redirect("movies.show", id=id)
