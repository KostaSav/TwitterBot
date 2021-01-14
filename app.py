# A twitter bot with python using the selenium library and GeckoDriver
# Inspired by Dev Ed's video tutorial (https://www.youtube.com/watch?v=7ovFudqFB0Q) - the Twitter DOM tree has changed, so there are quite some changes

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

### Your login data and the keyword you want to search for in Twitter
### Make sure you don't share your credentials on GitHub or anywhere else!
username = ""
password = ""
searchTerm = "giveaway"
comment = "Nice"

### A class containing the various actions the bot can execute
class TwitterBot:
    ## Initialize our bot's data
    def __init__(self, username, password):
        print("Initializing bot and maximizing window now. Waiting 3 seconds...")
        self.username = username
        self.password = password
        self.bot = webdriver.Firefox()
        self.bot.maximize_window()
        time.sleep(3)

    ## Input bot's data and login to Twitter
    def login(self):
        # Get the website containing the login forms, wait for it to load and then get the html username and password fields
        print("Entering credentials, waiting 5 seconds.....")
        bot = self.bot
        bot.get("https://twitter.com/login")
        time.sleep(5)
        username = bot.find_element_by_name("session[username_or_email]")
        password = bot.find_element_by_name("session[password]")
        # If anything is written inside the login forms, erase it
        username.clear()
        password.clear()
        # Fill username and password with our data and press ENTER to login
        username.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
        time.sleep(5)
        loginError = bot.find_elements_by_xpath(
            "//span[contains(text(), 'match our records')]"
        )  # not the best solution, sometimes works with few words
        time.sleep(5)
        if not loginError:
            print("Login Successful!")
            return True
        else:
            print("Your credentials were incorrect...\nBot is dead!")
            bot.close()
            return False
        print(loginError)
        time.sleep(5)

    ## Scroll until the element we want to interact with (Like button, Retweet button, etc.) is inside the viewport
    def scroll_shim(self, passed_in_driver, object):
        x = object.location["x"]
        y = object.location["y"]
        scroll_by_coord = "window.scrollTo(%s,%s);" % (x, y)
        scroll_nav_out_of_way = "window.scrollBy(0, -120);"
        passed_in_driver.execute_script(scroll_by_coord)
        passed_in_driver.execute_script(scroll_nav_out_of_way)

    ## Give a like/heart to a tweet containing our term
    def like_tweet(self, term):
        links = list()
        counter = 1  # count the retrieved tweets
        bot = self.bot
        print('Searching for the term "' + term + '", waiting 5 seconds.....')
        bot.get("https://twitter.com/search?q=" + term + "&src=typd")
        time.sleep(5)

        # Loop how many times we scroll down and load more tweets
        for i in range(1, 3):
            # The tweet's url can be found in several positions in the DOM
            # tree, we fetch it once from the anchor tag containing the
            # word "status" (ex. https://twitter.com/tweet_author_name/status/some_digits)
            tweets = bot.find_elements_by_css_selector(
                'a[href*="status"]:not([href*=photo]):not([href*=retweets]):not([href*=likes]):not([href*=media_tags])'
            )
            print("Getting tweet links, waiting 2 seconds..")
            time.sleep(2)

            # Get the tweet's actual url and store them in a list
            tempLoopLinks = [elem.get_attribute("href") for elem in tweets]
            for x in tempLoopLinks:
                links.append(x)
            print("Storing tweets, waiting 2 seconds..")
            time.sleep(2)
            print("Scroll loop " + str(i) + " complete!")

            # Scroll down in order to load new tweets
            print("Scrolling, waiting 10 seconds..........")
            bot.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(10)

        ## Locate and click the Like and Retweet buttons
        links = list(dict.fromkeys(links))  # Remove duplicates
        for link in links:
            print("Found link, waiting 10 seconds..........")
            print(counter, link)
            bot.get(link)
            time.sleep(10)
            try:
                # Find the Like button
                print("Looking for like button, waiting 2 seconds..")
                toLike = bot.find_element_by_css_selector(
                    'div[aria-label="Like"][role="button"][data-testid="like"]'
                )
                time.sleep(2)

                # Scroll so that it is in our viewport
                print(
                    "Scrolling a bit to find the correct like/retweet buttons, waiting 2 seconds.."
                )
                if "firefox" in bot.capabilities["browserName"]:
                    self.scroll_shim(bot, toLike)

                # Click the Like button
                actions = ActionChains(bot)
                actions.move_to_element(toLike)
                actions.click()
                actions.perform()
                time.sleep(2)

                # Find the Retweet button
                print("Looking for retweet button arrows, waiting 2 seconds..")
                toRetweet = bot.find_element_by_css_selector(
                    'div[aria-label="Retweet"][role="button"][data-testid="retweet"]'
                )
                time.sleep(2)

                # Click the Retweet button
                actions = ActionChains(bot)
                actions.move_to_element(toRetweet)
                actions.click()
                actions.perform()
                time.sleep(2)

                # Find the Confirm Retweet button
                print('Looking for "Confirm Retweet", waiting 2 seconds..')
                toConfirmRetweet = bot.find_element_by_css_selector(
                    'div[aria-label="Retweet"][role="button"][data-testid="retweet"]'
                )
                time.sleep(2)

                # Click the Confirm Retweet button
                actions = ActionChains(bot)
                actions.move_to_element(toConfirmRetweet)
                actions.click()
                actions.perform()
                time.sleep(2)

                # Show a confirmation in console
                print(
                    "Gave a LIKE and a RT to tweet "
                    + str(counter)
                    + ". Waiting 5 seconds..."
                )
                print(
                    "********************************************************************************"
                )
                time.sleep(5)
            except Exception as ex:
                # At the moment, an exception will be thrown
                # when a tweet is already liked
                print(
                    "Exception, the tweet might already have a like/retweet. Sleeping for 5 seconds....."
                )
                print(ex)
                print(
                    "********************************************************************************"
                )
                time.sleep(5)

            counter = counter + 1
            time.sleep(1)
        print(
            "--------------------------------------------------------------------------------"
        )
        print("Finished liking/retweeting. Goodbye!")


# Our bot's name is bix
bix = TwitterBot(username, password)
loginSuccess = bix.login()
if loginSuccess:
    bix.like_tweet(searchTerm)
