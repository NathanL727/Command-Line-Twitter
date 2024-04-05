from datetime import datetime

def compose_tweet(db):
    """
    This function asks the user to compose a tweet to which it then inserts the tweet into the "tweet" collection within the database.

    Args:
        db (MongoClient): The database client where the 'tweets' collection is located.

    Returns:
        None
    """
    # Ask the user to compose a tweet
    content = input("Compose your tweet: ")

    # Create a new tweet with all fields set to None
    tweet = {
        "url": None,
        "date": datetime.now().isoformat(),
        "content": content,
        "renderedContent": None,
        "id": None,
        "user": {
            "username": "291user",
            "displayname": None,
            "id": None,
            "description": None,
            "rawDescription": None,
            "descriptionUrls": None,
            "verified": None,
            "created": None,
            "followersCount": None,
            "friendsCount": None,
            "statusesCount": None,
            "favouritesCount": None,
            "listedCount": None,
            "mediaCount": None,
            "location": None,
            "protected": None,
            "linkUrl": None,
            "linkTcourl": None,
            "profileImageUrl": None,
            "profileBannerUrl": None,
            "url": None
        },
        "outlinks": None,
        "tcooutlinks": None,
        "replyCount": None,
        "retweetCount": None,
        "likeCount": None,
        "quoteCount": None,
        "conversationId": None,
        "lang": None,
        "source": None,
        "sourceUrl": None,
        "sourceLabel": None,
        "media": None,
        "retweetedTweet": None,
        "quotedTweet": None,
        "mentionedUsers": None
    }

    # Insert the new tweet into the 'tweets' collection
    db.tweets.insert_one(tweet)

    print("Your tweet has been posted!")
