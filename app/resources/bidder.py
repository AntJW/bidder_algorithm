from flask import Response, request
import random
from app import app
from app.models import Campaign


@app.route('/api/bidder', methods=['POST'])
def get_campaigns():
    try:
        post_body = request.form
        user_search_terms = set(str(post_body["search_terms"]).split())

        campaigns = Campaign.query.all()

        result = choose_best_campaign_for_user(user_search_terms, campaigns)

        return Response(result, content_type="application/text")
    except Exception:
        return Response("Sorry, something went wrong with our system. :(", content_type="application/text")


def choose_best_campaign_for_user(user_search_terms, campaigns):
    """Returns the best campaign to serve for a given user or None if
    no campaigns are applicable. A user can be served a campaign if they
    have searched for at least one keyword configured for the campaign.

    The "best" campaign to serve is the one with the most search term
    matches.

    If two or more campaigns have the same number of matches then the
    one with the highest bid_price should be served.

    If two or more campaigns have the same number of matches and the
    same bid_price, then either one may be returned.

    :param user_search_terms: list of search terms. assume normalized
    :param campaigns: a collection of Campaign objects
    :return: A single campaign object considered the 'best' campaign to show
            for the search terms provided or None if no campaigns are eligible
    """

    try:
        # *Optimized algorithm*
        camp_dict = \
            {(c.name, c.bid_price): len(set(user_search_terms) &
                                        set(c.target_keywords.replace(", ", ",").replace(" ,", ",").split(",")))
             for c in campaigns}

        if sum(set(camp_dict.values())) == 0:
            return None

        max_matches = max(camp_dict.values())
        best_matches = [key for key, value in camp_dict.items() if value == max_matches]

        if len(best_matches) > 1:
            # Sorts (descending) list of campaign (tuples) by bid_price, assigns highest bid_price to variable max_bid
            max_bid = sorted(best_matches, key=lambda tup: -tup[1])[0][1]
            highest_bid_campaign = [item[0] for item in best_matches if item[1] == max_bid]
            return random.choice(highest_bid_campaign)
        else:
            return best_matches[0][0]

        # # *Unoptimized algorithm*
        # camp_dict = {c.name: 0 for c in campaigns}
        #
        # for term in user_search_terms:
        #     for camp in campaigns:
        #         target_keywords = [k.strip() for k in camp.target_keywords.split(",")]
        #
        #         if term in target_keywords:
        #             camp_dict[camp.name] += 1
        #
        # if all(value == 0 for value in camp_dict.values()):
        #     return None
        #
        # max_matches = max(camp_dict.values())
        # best_matches = []
        # for key, value in camp_dict.items():
        #     if value == max_matches:
        #         best_matches.append(key)
        #
        # if len(best_matches) > 1:
        #     bid_dict = {c.name: c.bid_price for c in campaigns if c.name in best_matches}
        #     max_bid = max(bid_dict.values())
        #     highest_bid_campaign = [key for key, value in bid_dict.items() if value == max_bid]
        #     return random.choice(highest_bid_campaign)
        # else:
        #     return best_matches[0]
    except Exception:
        raise Exception("Error occurred in bid algorithm function.")
