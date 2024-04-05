import json

def list_top_users(db, n):
    """
    This function lists the top 'n' users with the most followers from the 'tweets' collection in the database.

    Args:
        db (MongoClient): The database client where the 'tweets' collection is located.
        n (int): The number of top users to list.

    Returns:
        None
    """
    # Aggregate the tweets to get the maximum followersCount for each user
    users = db.tweets.aggregate([
        {"$group": {
            "_id": "$user.username",
            "displayname": {"$first": "$user.displayname"},
            "followersCount": {"$max": "$user.followersCount"}
        }},
        {"$sort": {"followersCount": -1}},
        {"$limit": n}
    ])

    # Print the top n users
    for i, user in enumerate(users, start=1):
        print(f"{i}. Username: {user['_id']}, Display Name: {user['displayname']}, Followers Count: {user['followersCount']}")

    show_user_info(db)


def show_user_info(db):
    """
    This function asks the user to enter a username and then displays more information about the user from the 'tweets' collection in the database.

    Args:
        db (MongoClient): The database client where the 'tweets' collection is located.

    Returns:
        None
    """
    while True:
        # Ask the user to enter a username
        username = input("Enter the username of the user you want to see more information about (or 'exit' to go back to menu): ")

        # Check if the user wants to exit the program
        if username.lower() == 'exit':
            print("\nExiting to menu.")
            break

        # Find the tweet with the maximum followersCount for the selected user
        tweet = db.tweets.find_one({"user.username": username}, sort=[("user.followersCount", -1)])

        # Check if a tweet was found
        if tweet is not None:
            # Print the full information about the selected user
            print("Full information about the selected user:")
            print(json.dumps(tweet["user"], indent=4, ensure_ascii=False))
            break
        else:
            print(f"No tweets found from the user with the username '{username}'. Please try again.")
