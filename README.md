# TwitterBot

A twitter bot with python using the selenium library and GeckoDriver.<br/>
Using a keyword, the bot uses it to perform a search on Twitter and interacts with the results(tweets). For the moment, it likes and retweets these tweets.<br/>

Based on Dev Ed's [video tutorial](https://www.youtube.com/watch?v=7ovFudqFB0Q).<br/>
_(the tutorial code is not entirely functional any more, because of Twitter's changes in their DOM tree)_

## Installation

- [geckodriver](https://github.com/mozilla/geckodriver)<br/>
  _Extract executable in C://Users//{username}//AppData//Local//Programs//Python//Python{version}_
- Use the package manager [pip](https://pip.pypa.io/en/stable/) to install [Selenium](https://www.selenium.dev/).

```cmd
pip install selenium
```

## Bugs:

- if a tweet is already liked, an exception is thrown and a message is printed, but it does not break
- **ATTENTION:** if Twitter detects suspicious activity after many login attempts, login fails but no exception is thrown, the bot tries (unsuccessfully) to like/retweet without an account
- ~~again, if a tweet is already liked, the bot might like a comment instead~~
- ~~even if the sign in is unsuccessful, the program still searches the given word and tries to like tweets~~

## TODO:

1. [x] like
2. [x] retweet
3. [ ] comment
4. [ ] follow
5. [ ] ChromeDriver
