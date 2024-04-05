from pymongo import MongoClient
import sys
from list_top_user import *
from compose_tweet import *
from ListTopTweets import *
from searchTweets import *
from SearchUsers import *



def main():

    if len(sys.argv) != 2:
        print("Incorrect Input, Should be: <script_name>.py <mongodb_port>")
        sys.exit(1)

    port_number = int(sys.argv[1])

    db = MongoClient('localhost', port_number)['291db']

    while True:
        print("\nMenu:")
        print("1. List top users")
        print("2. Compose Tweet")
        print("3. List Top Tweets")
        print("4. Search Tweets")
        print("5. Search Users")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            while True:
                n = input("Enter the number of top users you want to list (or 'exit' to go back to menu): ")
                if n.lower() == 'exit':
                    print("\nExiting to menu.")
                    break

                # Check if the input is a string
                try:
                    n = int(n)
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
                    continue

                # Get the number of documents in the collection
                num_docs = db["tweets"].count_documents({})

                # Check if the input is a negative number or a number above the maximum document size
                if n < 0:
                    print("Invalid input, your input may be a negative number Please enter a valid number.")
                    continue

                list_top_users(db, n)
        elif choice == '2':
            compose_tweet(db)
        elif choice == '3':
            collection_name = "tweets"
            collection = db[collection_name]
            while True:
                field = input("Enter the field (retweetCount, likeCount, quoteCount): ").strip()
                if field == 'retweetCount' or field == 'likeCount' or field == 'quoteCount':
                    break
                else:
                    print(" please try entering retweetCount, likeCount, quoteCount")
            temper = collection.count_documents({})
            while True:
                # Get user input for the field and n
                n = input("Enter the value of n: ")

                try:
                    n = int(n)
                    if n > 0: #and n <= temper:
                        break
                    elif n == 0:
                        print("no users will be displayed")
                    else:
                        print("invalid input for n trying using another digit")
                except ValueError:
                    print("Enter a valid number.")

            print("-------------------------------\n")
            list_top_tweets(collection,field, n)
        elif choice == '4':
            results = search_tweets(db)
            print_results(db, results)
        elif choice == '5': 
            searchUsers(db)
        elif choice == '6':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, 5, or 6.")

if __name__ == "__main__":
    main()
