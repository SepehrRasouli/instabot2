# my first project in a freelancer website
import instaloader
import requests.exceptions
import instaloader.exceptions
import time
import os
import pickle
L = None

def get_key(val,dictName):
    for key, value in dictName.items():
        if val == value:
            return key

    return "key doesn't exist"


def saveData(data,usernames):
    with open("data.pickle","wb") as f:
        savedData = {'data':data,'usernames':usernames}
        pickle.dump(savedData, f)
        print("Data Saved, Come back Later.")
        time.sleep(3)
        SystemExit





def getFollowersAndCompare(Compare,CompareWith):
    # Compare is the followers list gathered
    # Compare With is the id of main page
    listOfFollowers = [] # List of main page followings
    resultDict = {}
    print("- Anti-IP Ban - Going To Sleep For 10 Secounds... ")
    time.sleep(10)
    print("Scarping Main Page...")
    try:
        profile = instaloader.Profile.from_username(L.context, CompareWith)
    except instaloader.exceptions.ConnectionException:
        print("Connection Error.")
        mainApp()
    followersamount = 5000
    i = 10
    if profile.followers > 5000: 
        for follower in profile.get_followers():
            listOfFollowers.append(follower.username)
            if len(listOfFollowers) == followersamount:
                amount = len(listOfFollowers)
                print(f"Scapred {amount} So far...")
                print("Sleeping For 5 Minutes")
                followersamount += 5000
                time.sleep(300)
                listOfFollowers.append(follower.username)
            else:
                continue
    else:
        for follower in profile.get_followers():
            listOfFollowers.append(follower.username)
            amount = len(listOfFollowers)
            if amount == i:
                print(f"Scarped {amount} so far...")
                i += 50

    print("Comparing...")
    for value in Compare.values():
        FilterValue = filter(listOfFollowers.__contains__,value)
        nameOfKey = get_key(value,Compare)
        resultDict[nameOfKey] = len([i for i in FilterValue])


    return resultDict



def getPostsCommentsUsernames(user):
    global L
    try:
        profile = instaloader.Profile.from_username(L.context, user)
    except instaloader.exceptions.ProfileNotExistsException:
        print("Profile Does Not Exist.")
        mainApp()

    except instaloader.exceptions.ConnectionException:
        print("Bad Internet.")
        mainApp()
    postIds = []
    commentsUsernames = set()
    i = 0
    for post in profile.get_posts():
        #Get Post Ids
        postIds.append(post)
        i += 1 
        if i == 10:
            break
    for postId in postIds:
        #Get postIDs
        print(f"Scarping Comments... *On PostId {postId} *")
        post_comments = postId.get_comments()
        for comment in post_comments:
            #Get Comment Usernames
            commentsUsernames.add(comment.owner.username)


    return commentsUsernames


def getFollowers(usernames,useLostData,mainPage):
    global L
    if useLostData == 1:
        print("Recovering Data...")
        with open("data.pickle","rb") as f:
            loaded_data = pickle.load(f)
        #Remove Last Dict Item
        temp = loaded_data['data'].keys()
        loaded_data['data'].pop(list(temp)[len(list(temp))-1])
        usernames = loaded_data['usernames']
        for key_username in loaded_data['data'].keys():
            usernames.remove(key_username)
        
    else:
        pass


    usernamesFollowers = {}
    for username in usernames:
        #TODO : Move Line 101 - 104 Under Try.
        try:
            if username != mainPage:
                profile = instaloader.Profile.from_username(L.context, username)
                pass
            else:
                continue
            if profile.followers >= 5000:
                pass
            else:
                continue


        except ConnectionResetError:
            print("Connection Error...")
            mainApp()
        
        except instaloader.exceptions.ConnectionException:
            print("Connection Error...")
            mainApp()
        print("Adding Followers...")
        try:
            if username == mainPage:
                continue
            print(f"Going Through Usernames and Scarping Their Followers... *On Username {username}*")
            usernamesFollowers[username] = []
            print("- Anti-IP Ban - Going to sleep for 10 Seconds")
            time.sleep(10)
            followersamount = 5000
            i = 10
            if profile.followers > 2000:
                for follower in profile.get_followers():
                    usernamesFollowers[username].append(follower.username)
                    
                    if len(usernamesFollowers[username]) == followersamount:
                        amount = len(usernamesFollowers[username])
                        print(f"Scapred {amount} So far...")
                        print("Sleeping For 5 Minutes")
                        followersamount += 5000
                        time.sleep(300)
                    else:
                        if len(usernamesFollowers[username]) == i:
                            print(f"Scarped {i} so far...")
                            i += 100
                            continue
                        else:
                            continue
            else:
                for follower in profile.get_followers():
                    usernamesFollowers[username].append(follower.username)
                    


        except instaloader.exceptions.ConnectionException:
            print("Connection Error...")
            print("Saving Data...")
            saveData(usernamesFollowers,usernames)
            time.sleep(3)
            SystemExit
        except ConnectionResetError:
            print("Connection Error...")
            print("Saving Data...")
            saveData(usernamesFollowers,usernames)
            time.sleep(3)
            SystemExit

    return usernamesFollowers

    
def mainApp():
    global L
    useLostData = 0
    print("Hello.")
    if os.path.isfile("data.pickle"):
        print("Lost Data File Found, Do You Want To Use Lost Data? Y/N")
        yon = input("> ")
        if yon[0].lower() == "y":
            useLostData = 1
        else:
            os.remove("data.pickle")
            pass


    username = input("Your instagram page username > ")
    password = input("Your instagram page password > ")
    mainPage = input("Main Page id *To compare* > ")
    L = instaloader.Instaloader()
    try:
        print("Logging In...")
        L.login(username,password)
    except instaloader.exceptions.BadCredentialsException:
        print("Wrong Password.")
        mainApp()
    except instaloader.exceptions.TwoFactorAuthRequiredException:
        print("TwoFactor Auth Is Needed.")
        mainApp()
    except ConnectionResetError:
        print("Connection Reseted. Aborting.")
        mainApp()
    except instaloader.exceptions.ConnectionException as f:
        print(f"Instagram Auth Needed. {f}")
    except requests.exceptions.ConnectionError:
        print("Bad Internet. Aborting.")
        mainApp()
    except instaloader.exceptions.InvalidArgumentException:
        print("User Does not exist.")
        mainApp()
    if useLostData == 0:
        usernames = getPostsCommentsUsernames(mainPage) 
    else:
        usernames = []
        pass
    
    FollowerFromOtherPages = getFollowers(usernames,useLostData,mainPage)
    FollowersFromMainPage = getFollowersAndCompare(FollowerFromOtherPages,mainPage)
    sortedDict = sorted(FollowersFromMainPage.items(), key=lambda x: x[1],reverse=True)
    print("Results : ")
    print("-"*10)
    for i in range(0,5):
        try:
            if sortedDict[i][1] >= 1:
                print(f"User {sortedDict[i][0]} with {sortedDict[i][1]} followers")
            else:
                continue
        except IndexError:
            continue
    print("\n\n\n")
    mainApp()

mainApp()