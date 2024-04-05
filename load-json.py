import json
import sys
from pymongo import MongoClient

def parse_json(file, db, max_tweets=10000):
    """
    Parse a JSON file and insert the data into the MongoDB collection.

    Parameters:
    file (str): The path to the JSON file.
    db: MongoDB database.
    max_tweets (int): The maximum number of tweets to insert at once
    """
    with open(file, "r") as file:
        arr = []
        # Read each line in the file
        for line in file:
            tweet = json.loads(line)
            arr.append(tweet)
            # If the array size reaches max_tweets
            if len(arr) >= max_tweets:
                db.tweets.insert_many(arr)
                arr.clear()
        # If there is any data left in the array insert the remaining data into the MongoDB collection        
        if arr:  
            db.tweets.insert_many(arr)
    

def main():
    """
    The main function of the script used to call the functions and ensure correct input.
    """
    # Check if the number of command-line arguments is correct
    if len(sys.argv) != 3:
        print("Incorrect Input, Should be: load-json.py <json_file> <mongodb_port>")
        sys.exit(1)

    # Get the command-line arguments
    json_file = sys.argv[1]
    port_number = int(sys.argv[2])

    # Connect to the MongoDB server and select the database
    db = MongoClient('localhost', port_number)['291db']

    # If the 'tweets' collection already exists, drop it
    if 'tweets' in db.list_collection_names():
        db.drop_collection('tweets')

    parse_json(json_file, db)

if __name__ == "__main__":
    main()
