def getRecMovies(userPref,itemPref):
    # find the user ratings items
    # find similar items from pref
    userRatings = userPref
    sum_sim={}
    total_sim={}

    # loop over items,rating rated by user
    for (item,rating) in userRatings.items():
        # loop over similar items to this item
        for (similarity,item2) in itemPref[item]:

            if item2 in userRatings:
                continue

            total_sim.setdefault(item2,0)
            total_sim[item2] += similarity*rating

            sum_sim.setdefault(item2,0)
            sum_sim[item2] += similarity

    rank = [((total_sim[item]/sum_sim[item]),item) for item in total_sim]
    rank.sort()
    rank.reverse()

    return rank[:25]
