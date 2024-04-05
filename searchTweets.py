import sys


def search_tweets(db):
    """
    Prompt the user to input keywords and search for tweets that contain all of the keywords.

    Parameters:
    db: MongoDB database.

    Returns:
    results : The search results from tweets collection.
    """
    
    keywords = input("Enter keywords to search or enter to exit:")
    if not keywords:
        print("Null input. Enter Valid Input")
        results = search_tweets(db)
        print_results(db, results)
    

    if keywords.lower() == "exit":
        print("Exiting")
        sys.exit(1)
    keywords = keywords.split()
    query = {'$and': [{'content': {'$regex': f'\\b{keyword}\\b', '$options': 'i'}} for keyword in keywords]}
    results = db.tweets.find(query, {'_id': 0, 'id': 1, 'date': 1, 'content': 1, 'user.username': 1})
    return results

def print_results(db, results):
    """
    Print all results which match the keywords search, prompting user to enter a tweet ID to all fields of the tweet.

    Parameters:
    db: MongoDB database.
    results : The search results from tweets collection.
    """
    count = 0 
    tweet_id= []
    for result in results:
        #Displaying the tweet ID, username, date and content of the tweet. Displaying the total result number of the search.
        count += 1
        tweet_id.append(result['id'])
        print()
        print(f"Tweet ID: {result['id']}")
        print(f"Username: {result['user']['username']}")
        print(f"Date: {result['date']}")
        print(f"Content: {result['content']}")
    print(f"Total Results: {count}")
    if count == 0:
        results = search_tweets(db)
        print_results(db, results)
    input_id = input("Enter a  Tweet ID to see more details, or press enter to exit: ")
    while input_id != "exit":
        if input_id == "exit":
            print("Exiting")
            break
        if not input_id.isdigit():
            print('Please enter a valid ID')
            input_id = input("Enter a  Tweet ID to see more details, or press enter to exit: ")
        if input_id.isdigit():
            input_id = int(input_id)
            if input_id in tweet_id:
                all_fields = db.tweets.find_one({'id': input_id}, {'_id': 0})
                print()
                for field, value in all_fields.items():
                    #Displaying all fields of the tweet
                    print(f'{field}: {value}')
                input_id = input("Enter a  Tweet ID to see more details, or press enter to exit: ")
                
            elif input_id not in tweet_id:
                print("Invalid Tweet ID")
                input_id = input("Enter a  Tweet ID to see more details, or press enter to exit: ")
