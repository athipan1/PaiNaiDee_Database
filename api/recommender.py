def recommend_for_user(db, user_id):
    from .models import Attraction, Review
    subq = db.query(Review.attraction_id).filter(Review.user_id == user_id)
    recs = db.query(Attraction).filter(~Attraction.id.in_(subq)).limit(5).all()
    return recs

