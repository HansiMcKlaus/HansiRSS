# Bot Token
TOKEN = "YOUR_BOT_TOKEN"

# Channel ID
CHANNEL_ID = 123456789123456789

# Update interval for how often the bot is supposed to check if a new entry in the RSS feed exists (in Minutes)
UPDATE_INTERVAL = 5

# How far a new entry in the RSS feed can can be published in the past before being ignored (in Days)
LAST_ARTICLE_RANGE = 5

# Add the RSS feeds here. Each object consists of the RSS feed URL and an optional Discord User-ID, whose user will be tagged in the message
RSS_FEEDS = [
    {
        "url": "LINK_TO_RSS_FEED",
        "user": "USER_ID"
    }
]