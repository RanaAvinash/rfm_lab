def next_best_offer(segment):

    offers = {

        "Champions":"Premium loyalty rewards",

        "Loyal":"Cross sell complementary products",

        "Potential":"Welcome discount",

        "At Risk":"Win-back campaign",

        "Lost":"Reactivation coupon"

    }

    return offers.get(segment,"General promotion")
