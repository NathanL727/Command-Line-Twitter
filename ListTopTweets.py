import pymongo

def format_tweet_id(tweet_id):
    """
    This function formats a tweet ID as a string to prevent scientific notation.

    Args:
        tweet_id (int): The tweet ID to format.

    Returns:
        str: The formatted tweet ID.
    """
    # Format tweet ID as a string to prevent scientific notation
    return str(tweet_id)
#list the top users base on the tweetCount, or likeCount, or quoteCount
def list_top_tweets(collection, field, n):
    """
    This function lists the top 'n' tweets based on a specified field from a collection in the database.

    Args:
        collection (MongoClient): The collection where the tweets are located.
        field (str): The field to sort the tweets by.
        n (int): The number of top tweets to list.

    Returns:
        Set[str]: A set of the top 'n' tweet IDs.
    """
    cursor = collection.find()
    cursor.sort(field, pymongo.DESCENDING)
    cursor.limit(n)
    top_conversation_ids = set()
    # Display tweet details
    for i, tweet in enumerate(cursor, start=1):
        formatted_conversation_id = format_tweet_id(tweet['id'])
        print(f"Tweet {i}:")
        print(f"TweetID: {formatted_conversation_id}")
        print(f"Date: {tweet['date']}")
        print(f"Content: {tweet['content']}")
        print(f"Username: {tweet['user']['username']}")
        print("-------------------------------")
        top_conversation_ids.add(formatted_conversation_id)
    # Get user input to select a tweet for more details
    while True:
        selected_tweet_id = input("Enter the ID of the tweet for more details: ").strip()
        if selected_tweet_id in top_conversation_ids:
            # Display all fields of the selected tweet
            display_full_tweet(int(selected_tweet_id), collection)
        else:
            print("The selected conversation ID is not in the top N tweets.")
        ques = input("Do you want to exit? Type exit to exit or type any keyboard character to continue: ").lower().strip()
        if ques == 'exit':
            break
        else:
            print('The program shall continue')



#displays the all of the fields related to a tweet
def display_full_tweet(tweet_id,collection):
    """
    This function displays all of the fields related to a tweet with a specified ID from a collection in the database.

    Args:
        tweet_id (int): The ID of the tweet to display.
        collection (MongoClient): The collection where the tweet is located.

    Returns:
        None
    """
    # Search for the selected tweet
    tweet = collection.find_one({'id': tweet_id})
    # Display all fields of the selected tweet
    print("Full Tweet Details:")
    print(f"Conversation ID: {format_tweet_id(tweet['id'])}")
    print(f"Date: {tweet['date']}")
    print(f"Content: {tweet['content']}")
    print(f"Username: {tweet['user']['username']}")
    print(f"URL: {tweet['url']}")
    print(f"Reply Count: {tweet['replyCount']}")
    print(f"Retweet Count: {tweet['retweetCount']}")
    print(f"Like Count: {tweet['likeCount']}")
    print(f"Quote Count: {tweet['quoteCount']}")
    print("-------------------------------")
