from app import db


class Campaign(db.Model):
    """An ad campaign we can serve to users."""
    name = db.Column(db.String(150), primary_key=True)
    bid_price = db.Column(db.Float, unique=False)
    target_keywords = db.Column(db.Text, unique=False)

    def __init__(self, name, bid_price, target_keywords):
        """
        :param name: unique name for this campaign, e.g. "Nike Shoes Summer 2014"
        :param bid_price: amount to bid on any auctions when serving this campaign, e.g. 0.5
        :param target_keywords: list of keywords we are targeting for this campaign
        """
        self.name = name
        self.bid_price = bid_price
        self.target_keywords = target_keywords
        pass

    def __repr__(self):
        return "<Campaign {}>".format(str(self.name))
