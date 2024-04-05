# search for users
import json
from pymongo import MongoClient



# Search for users using a keyword which is an input given from the user
# Searches in display names and locations
def searchUsers(db):
    """
    Search for users using a keyword in display names and locations.
    Parameters:
    - db-> The MongoDB database.
    Returns:
    None
    """
    while True:
        # ask for an input
        keyword = input("Enter a keyword to search in users and cities: ").strip()
        if not keyword:
            query = {'$or': [{'user.displayname': ''}, {'user.location': ''}]}
        else:
            query = {'$or': [{'user.displayname': {'$regex': f'\\b{keyword}\\b', '$options': 'i'}}, {'user.location': {'$regex': f'\\b{keyword}\\b', '$options':'i'}}]}

        # the query to get the user info for the selected users
        results = db.tweets.find(query, {'_id' : 0 ,'user.username': 1, 'user.displayname': 1, 'user.location': 1,'user.followersCount': 1 , 'id': 1})
        if db.tweets.count_documents(query) == 0:
            print("Invalid input, please provide a valid input, try again. \n")
        else:
            break
    # initialize arrays
    usernames = []
    displays = []
    locations = []
    followers = []
    tids = []
    # loop through and put the information we need into arrays for easy access and to filter duplicates
    for s in results:
        if (s['user']['username'] not in usernames):
            usernames.append(s['user']['username'])
            displays.append(s['user']['displayname'])
            locations.append(s['user']['location'])
            followers.append(int(s['user']['followersCount']))
            tids.append(s['id'])
        else: 
            index = usernames.index(s['user']['username'])
            if (followers[index] < s['user']['followersCount']):
                displays[index] = s['user']['displayname']
                locations[index] = s['user']['location']
                followers[index] = int(s['user']['followersCount'])
                tids[index] = s['id']
    # printing the user infos out   
    for i in range(len(usernames)):
        print("Username: ", usernames[i], ", DisplayName: ", displays[i], ", Location: ", locations[i], ", Followers: ", followers[i])
    # print num of users found
    print(len(usernames))
    expandUser(db)
    return
        
# function to expand the user's details when selected
def expandUser(db):
    """
    Expand the user's details when selected.

    Parameters:
    db -> The MongoDB database.

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
            
    

