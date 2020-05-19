# TwitterBot

A twitter bot with python using the selenium library and GeckoDriver

Based on Dev Ed's video tutorial (https://www.youtube.com/watch?v=7ovFudqFB0Q)

_the tutorial code is not entirely functional any more, because of Twitter's changes in their DOM tree_

## Bugs:

- if a tweet is already liked, an exception is thrown and a message is printed, but it does not break
- again, if a tweet is already liked, the bot might like a comment instead
- even if the sign in is unsuccessful, the program still searches the given word and tries to like tweets

## TODO:

1. [ ] retweet
2. [ ] comment
3. [ ] follow
4. [ ] ChromeDriver
