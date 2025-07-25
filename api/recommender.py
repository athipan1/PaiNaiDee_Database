from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc, and_, text
from typing import List, Optional
from .models import Attraction, Review, Favorite, AttractionTag, User, Category
import random

def recommend_for_user(db: Session, user_id: int, limit: int = 10) -> List[Attraction]:
    """
    Enhanced recommendation algorithm that considers:
    1. User's rating history and preferences
    2. Popular attractions
    3. Similar user preferences
    4. Attractions in same categories as user favorites
    """
    
    # Get attractions user has already reviewed or favorited
    reviewed_subq = db.query(Review.attraction_id).filter(Review.user_id == user_id).subquery()
    favorited_subq = db.query(Favorite.attraction_id).filter(Favorite.user_id == user_id).subquery()
    
    # Base query for unvisited attractions
    base_query = db.query(Attraction).options(
        joinedload(Attraction.category_obj),
        joinedload(Attraction.attraction_tags).joinedload(AttractionTag.tag)
    ).filter(
        and_(
            ~Attraction.id.in_(reviewed_subq),
            ~Attraction.id.in_(favorited_subq)
        )
    )
    
    recommendations = []
    
    # 1. Category-based recommendations (40% weight)
    category_recommendations = _get_category_based_recommendations(db, user_id, base_query, limit//2)
    recommendations.extend(category_recommendations)
    
    # 2. Popularity-based recommendations (30% weight)
    if len(recommendations) < limit:
        remaining = limit - len(recommendations)
        popularity_recommendations = _get_popularity_based_recommendations(db, base_query, remaining)
        recommendations.extend(popularity_recommendations)
    
    # 3. Collaborative filtering recommendations (20% weight)
    if len(recommendations) < limit:
        remaining = limit - len(recommendations)
        collaborative_recommendations = _get_collaborative_recommendations(db, user_id, base_query, remaining)
        recommendations.extend(collaborative_recommendations)
    
    # 4. Random recommendations to fill up if needed (10% weight)
    if len(recommendations) < limit:
        remaining = limit - len(recommendations)
        random_recommendations = _get_random_recommendations(db, base_query, remaining)
        recommendations.extend(random_recommendations)
    
    # Remove duplicates and return
    seen = set()
    unique_recommendations = []
    for attraction in recommendations:
        if attraction.id not in seen:
            seen.add(attraction.id)
            unique_recommendations.append(attraction)
            if len(unique_recommendations) >= limit:
                break
    
    return unique_recommendations

def _get_category_based_recommendations(db: Session, user_id: int, base_query, limit: int) -> List[Attraction]:
    """Get recommendations based on user's favorite categories."""
    
    # Get user's preferred categories from favorites and high-rated reviews
    preferred_categories = db.query(
        Attraction.category_id,
        func.count().label('preference_score')
    ).join(Favorite, Attraction.id == Favorite.attraction_id).filter(
        Favorite.user_id == user_id
    ).group_by(Attraction.category_id).all()
    
    # Also consider categories from highly rated attractions
    high_rated_categories = db.query(
        Attraction.category_id,
        func.count().label('rating_score')
    ).join(Review, Attraction.id == Review.attraction_id).filter(
        and_(Review.user_id == user_id, Review.rating >= 4)
    ).group_by(Attraction.category_id).all()
    
    # Combine preference scores
    category_scores = {}
    for cat_id, score in preferred_categories:
        category_scores[cat_id] = category_scores.get(cat_id, 0) + score * 2  # Favorites weight more
    
    for cat_id, score in high_rated_categories:
        category_scores[cat_id] = category_scores.get(cat_id, 0) + score
    
    if not category_scores:
        return []
    
    # Sort categories by preference score
    preferred_category_ids = [cat_id for cat_id, _ in sorted(category_scores.items(), key=lambda x: x[1], reverse=True)]
    
    # Get attractions from preferred categories
    recommendations = base_query.filter(
        Attraction.category_id.in_(preferred_category_ids[:3])  # Top 3 categories
    ).order_by(desc(func.random())).limit(limit).all()
    
    return recommendations

def _get_popularity_based_recommendations(db: Session, base_query, limit: int) -> List[Attraction]:
    """Get recommendations based on overall popularity (ratings and favorites)."""
    
    # Subquery for average ratings
    avg_ratings = db.query(
        Review.attraction_id,
        func.avg(Review.rating).label('avg_rating'),
        func.count(Review.id).label('review_count')
    ).group_by(Review.attraction_id).subquery()
    
    # Subquery for favorite counts
    favorite_counts = db.query(
        Favorite.attraction_id,
        func.count(Favorite.id).label('favorite_count')
    ).group_by(Favorite.attraction_id).subquery()
    
    # Join with base query and calculate popularity score
    popularity_query = base_query.outerjoin(
        avg_ratings, Attraction.id == avg_ratings.c.attraction_id
    ).outerjoin(
        favorite_counts, Attraction.id == favorite_counts.c.attraction_id
    ).order_by(
        desc(
            func.coalesce(avg_ratings.c.avg_rating, 0) * func.coalesce(avg_ratings.c.review_count, 0) +
            func.coalesce(favorite_counts.c.favorite_count, 0) * 2
        )
    ).limit(limit)
    
    return popularity_query.all()

def _get_collaborative_recommendations(db: Session, user_id: int, base_query, limit: int) -> List[Attraction]:
    """Get recommendations based on similar users' preferences."""
    
    # Find users with similar preferences (users who favorited same attractions)
    similar_users = db.query(
        Favorite.user_id,
        func.count().label('common_favorites')
    ).join(
        Favorite.alias(), 
        and_(
            Favorite.attraction_id == Favorite.alias().attraction_id,
            Favorite.alias().user_id == user_id,
            Favorite.user_id != user_id
        )
    ).group_by(Favorite.user_id).having(
        func.count() >= 2  # At least 2 common favorites
    ).order_by(desc('common_favorites')).limit(10).all()
    
    if not similar_users:
        return []
    
    similar_user_ids = [user.user_id for user in similar_users]
    
    # Get attractions favorited by similar users
    recommendations = base_query.join(
        Favorite, Attraction.id == Favorite.attraction_id
    ).filter(
        Favorite.user_id.in_(similar_user_ids)
    ).order_by(desc(func.random())).limit(limit).all()
    
    return recommendations

def _get_random_recommendations(db: Session, base_query, limit: int) -> List[Attraction]:
    """Get random recommendations to ensure diversity."""
    return base_query.order_by(desc(func.random())).limit(limit).all()

def get_trending_attractions(db: Session, days: int = 30, limit: int = 10) -> List[Attraction]:
    """Get trending attractions based on recent activity."""
    
    # Get attractions with recent reviews and favorites
    recent_activity = db.query(
        Attraction.id,
        func.count(Review.id).label('recent_reviews'),
        func.count(Favorite.id).label('recent_favorites')
    ).outerjoin(
        Review, 
        and_(
            Attraction.id == Review.attraction_id,
            Review.created_at >= func.current_date() - text(f"INTERVAL '{days} days'")
        )
    ).outerjoin(
        Favorite, Attraction.id == Favorite.attraction_id
    ).group_by(Attraction.id).having(
        func.count(Review.id) + func.count(Favorite.id) > 0
    ).order_by(
        desc(func.count(Review.id) + func.count(Favorite.id) * 2)
    ).limit(limit).subquery()
    
    # Get full attraction objects
    trending = db.query(Attraction).options(
        joinedload(Attraction.category_obj),
        joinedload(Attraction.attraction_tags).joinedload(AttractionTag.tag)
    ).join(recent_activity, Attraction.id == recent_activity.c.id).all()
    
    return trending

def get_recommendations_by_location(db: Session, province: str, limit: int = 10) -> List[Attraction]:
    """Get recommendations for a specific province."""
    
    # Get highly rated attractions in the province
    avg_ratings = db.query(
        Review.attraction_id,
        func.avg(Review.rating).label('avg_rating'),
        func.count(Review.id).label('review_count')
    ).group_by(Review.attraction_id).subquery()
    
    recommendations = db.query(Attraction).options(
        joinedload(Attraction.category_obj),
        joinedload(Attraction.attraction_tags).joinedload(AttractionTag.tag)
    ).outerjoin(
        avg_ratings, Attraction.id == avg_ratings.c.attraction_id
    ).filter(
        Attraction.province.ilike(f"%{province}%")
    ).order_by(
        desc(func.coalesce(avg_ratings.c.avg_rating, 0) * func.coalesce(avg_ratings.c.review_count, 0))
    ).limit(limit).all()
    
    return recommendations