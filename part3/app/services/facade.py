from app.services.userfacade import UserFacade
from app.services.amenityfacade import AmenityFacade
from app.services.placefacade import PlaceFacade
from app.services.reviewfacade import ReviewFacade


class HBnBFacade:
    def __init__(self):
        self.user_facade = UserFacade()
        self.amenity_facade = AmenityFacade()
        self.place_facade = PlaceFacade(self.user_facade, self.amenity_facade)
        self.review_facade = ReviewFacade(self.user_facade, self.place_facade)
