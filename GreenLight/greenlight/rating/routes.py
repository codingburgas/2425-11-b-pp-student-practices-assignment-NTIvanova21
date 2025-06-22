from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from . import rating
from greenlight.models import Rating, UserRating
from greenlight import db
from sqlalchemy import func


@rating.route('/rate', methods=['GET', 'POST'])
@login_required
def rate_website():
    if request.method == 'POST':
        rating_value = request.form.get('rating')
        comment = request.form.get('comment', '').strip()
        
        if not rating_value:
            flash('Please select a rating', 'error')
            return redirect(url_for('rating.rate_website'))
        
        try:
            rating_value = int(rating_value)
            if rating_value < 1 or rating_value > 5:
                raise ValueError("Invalid rating value")
        except ValueError:
            flash('Please select a valid rating (1-5 stars)', 'error')
            return redirect(url_for('rating.rate_website'))
        
        # Create new rating
        new_rating = Rating(
            userId=current_user.userId,
            rating=rating_value,
            comment=comment
        )
        db.session.add(new_rating)
        db.session.flush()

        user_rating_link = UserRating(
            userId=current_user.userId,
            ratingId=new_rating.ratingId
        )
        db.session.add(user_rating_link)
        flash('Thank you for your rating!', 'success')
        
        db.session.commit()
        return redirect(url_for('rating.rate_website'))
    
    # Get user's most recent rating to display, if any
    user_rating = Rating.query.filter_by(userId=current_user.userId).order_by(Rating.created_at.desc()).first()
    
    # Get overall statistics
    total_ratings = Rating.query.count()
    avg_rating = db.session.query(func.avg(Rating.rating)).scalar() or 0
    avg_rating = round(float(avg_rating), 1)
    
    # Get rating distribution
    rating_distribution = db.session.query(
        Rating.rating,
        func.count(Rating.rating).label('count')
    ).group_by(Rating.rating).order_by(Rating.rating.desc()).all()
    
    # Convert to dictionary for easier template usage
    rating_stats = {rating: count for rating, count in rating_distribution}
    
    # Get recent comments (last 5)
    recent_comments = Rating.query.filter(
        Rating.comment.isnot(None),
        func.trim(Rating.comment) != ''
    ).order_by(Rating.created_at.desc()).limit(5).all()
    
    return render_template('ratingPage.html',
                         user_rating=user_rating,
                         total_ratings=total_ratings,
                         avg_rating=avg_rating,
                         rating_stats=rating_stats,
                         recent_comments=recent_comments)


@rating.route('/api/rating-stats')
def get_rating_stats():
    """API endpoint to get rating statistics for AJAX requests"""
    total_ratings = Rating.query.count()
    avg_rating = db.session.query(func.avg(Rating.rating)).scalar() or 0
    avg_rating = round(float(avg_rating), 1)
    
    rating_distribution = db.session.query(
        Rating.rating,
        func.count(Rating.rating).label('count')
    ).group_by(Rating.rating).order_by(Rating.rating.desc()).all()
    
    rating_stats = {rating: count for rating, count in rating_distribution}
    
    return jsonify({
        'total_ratings': total_ratings,
        'avg_rating': avg_rating,
        'rating_distribution': rating_stats
    }) 