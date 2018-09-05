from flask import render_template,request,redirect,url_for , abort
from . import main
from ..requests import get_movies,get_movie,search_movie
from .forms import ReviewForm ,UpdateProfile
from ..models import Review , User

from .. import db , photos

from flask_login import login_required



@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''

    # Getting popular movie
    popular_movies = get_movies('popular')
    # upcoming_movie = get_movies('upcoming')
    title = 'Home - Welcome to The best Movie Review Website Online'
    search_movie = request.args.get('movie_query')
    
    if search_movie:
        return redirect(url_for('main.search',movie_name=search_movie))
    else:
        return render_template('index.html', title = title, popular = popular_movies)

@main.route('/movie/<int:id>')
def movie(id):
    '''
    View movie page function that returns the movie details page and its data
    '''
    movie = get_movie(id)
    title = f'{movie.title}'
    reviews = Review.get_reviews(movie.id)

    return render_template('movie.html',title = title,movie = movie, reviews = reviews)

@main.route('/search/<movie_name>')
def search(movie_name):
    '''
    View function to display the search results
    '''
    movie_name_list = movie_name.split(" ")
    movie_name_format = "+".join(movie_name_list)
    searched_movies = search_movie(movie_name_format)
    title = f'search results for {movie_name}'
    return render_template('search.html',movies = searched_movies)

@main.route('/movie/review/new/<int:id>', methods = ['GET','POST'])
@login_required
def new_review(id):
    form = ReviewForm()
    movie = get_movie(id)

    if form.validate_on_submit():
        title = form.title.data
        review = form.review.data
        new_review = Review(movie.id,title,movie.poster,review)
        new_review.save_review()
        return redirect(url_for('.movie',id = movie.id ))

    title = f'{movie.title} review'
    return render_template('new_review.html',title = title, review_form=form, movie=movie)



@main.route('/profile/<username>/upload/pic',methods =["POST"])
@login_required
def profile_pic(username):

    user = User.query.filter_by(username = username).first()

    if 'photos' in request.files:
        filename = photos.save(request.files['photos'])
        path = f"photos/{filename}"
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for("main.profile",username=username))
    

'''
A route to redirect you to a user's profile
'''
@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


'''
A route to take you to edit user's profile 
'''

@main.route('/user/<username>/update')
@login_required
def update_profile(username):
    user = User.query.filter_by(username = username).first()

    if username is None:
        abort(404)
    
    if form.validate_on_submit():
        user.bio = form.bio.data 
        db.session.add(user)
        db.commit(user)

        return redirect(url_for('.profile',uname=username))

    return render_template()
