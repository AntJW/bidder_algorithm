import unittest

from app.models import Campaign
from app.resources.bidder import choose_best_campaign_for_user


# Sample campaigns for testing - the apple_mac and apple_ios campaigns have one keyword
# in common 'apple'
apple_mac_campaign = Campaign(
    name="Apple Mac Products",
    bid_price=1.00,
    target_keywords="apple,macbook, macbook pro, imac, power mac, mavericks"
)

apple_ios_campaign = Campaign(
    name="Apple IOS Products",
    bid_price=1.50,
    target_keywords="apple, ipad, iphone, ios, appstore, siri"
)

marvel_comics_campaign = Campaign(
    name="Marvel Comics",
    bid_price=0.50,
    target_keywords="spiderman, hulk, wolverine, ironman, captain america, action"
)

dc_comics_campaign = Campaign(
    name="DC Comics",
    bid_price=0.50,
    target_keywords="batman, joker, flash, green latern, superman, action"
)


class BidderTest(unittest.TestCase):

    def test_it_picks_no_campaign_if_no_keywords_match(self):
        chosen_campaign = choose_best_campaign_for_user(
            user_search_terms=["batman"],
            campaigns=[marvel_comics_campaign],
        )
        self.assertIsNone(chosen_campaign)

    def test_it_chooses_a_campaign_if_search_terms_match_keywords(self):
        chosen_campaign = choose_best_campaign_for_user(
            user_search_terms=["spiderman"],
            campaigns=[marvel_comics_campaign],
        )
        self.assertEqual(marvel_comics_campaign.name, chosen_campaign)

    def test_it_chooses_campaign_with_most_overlapping_keywords(self):
        chosen_campaign = choose_best_campaign_for_user(
            user_search_terms=["apple", "macbook"],
            campaigns=[apple_mac_campaign, apple_ios_campaign],
        )
        self.assertEqual(apple_mac_campaign.name, chosen_campaign)

    def test_it_chooses_campaign_with_higher_bid_given_same_number_of_matching_keywords(self):
        chosen_campaign = choose_best_campaign_for_user(
            user_search_terms=["apple"],
            campaigns=[apple_mac_campaign, apple_ios_campaign],
        )
        self.assertEqual(apple_ios_campaign.name, chosen_campaign)

    def test_it_chooses_campaign_with_same_bid_and_same_number_of_matching_keywords(self):
        chosen_campaign = choose_best_campaign_for_user(
            user_search_terms=["action"],
            campaigns=[marvel_comics_campaign, dc_comics_campaign],
        )
        self.assertIn(chosen_campaign, [marvel_comics_campaign.name, dc_comics_campaign.name])

if __name__ == '__main__':
    unittest.main()
