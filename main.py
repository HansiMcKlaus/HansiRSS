import feedparser
from datetime import datetime, timedelta, timezone
import sqlite3
import discord
from discord.ext import commands, tasks

from config import TOKEN, CHANNEL_ID, UPDATE_INTERVAL, LAST_ARTICLE_RANGE, RSS_FEEDS


connection = sqlite3.connect('articles.db')
c = connection.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS articles (title TEXT, link TEXT)''')
connection.commit()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


def article_in_db(entry):
	c.execute("SELECT link FROM articles WHERE link=?", (entry.link,))
	if c.fetchone() is None:
		c.execute("INSERT INTO articles (title, link) VALUES (?, ?)", (entry.title, entry.link))
		connection.commit()
		return False
	else:
		return True


def get_new_articles():
	new_articles = []

	for rss_feed in RSS_FEEDS:
		entries = feedparser.parse(rss_feed["url"]).entries
		for entry in entries:
			if not article_in_db(entry):
				pub_date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z").replace(tzinfo=timezone.utc)
				if datetime.now(timezone.utc) - pub_date <= timedelta(days=LAST_ARTICLE_RANGE):
					new_articles.append({"article": entry, "user": rss_feed["user"], "feedTitle": feedparser.parse(rss_feed["url"]).feed.title})

	return new_articles


def format_to_message(article):
	article_title = article["article"].title
	article_user = article["user"]
	article_feed_title = article["feedTitle"]
	article_link = article["article"].link

	message = f"**{article_title}** by "
	if article_user:
		message += f"<@{article_user}>"
	else:
		message += f"{article_feed_title}"
	message += f"\n{article_link}"

	return message


@bot.event
async def on_ready():
	print(f'{bot.user} has connected to Discord!')
	post_new_articles.start()


@tasks.loop(minutes=UPDATE_INTERVAL)
async def post_new_articles():
	channel = bot.get_channel(CHANNEL_ID)

	new_articles = get_new_articles()
	for article in new_articles:
		message = format_to_message(article)
		await channel.send(message)


if __name__ == "__main__":
	bot.run(TOKEN)
