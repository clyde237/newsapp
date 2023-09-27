import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
@anvil.server.callable
def add_article(article_dict):
  # Get the logged in user
  current_user = anvil.users.get_user()
  # Check that someone is logged in
  if current_user is not None:
    app_tables.articles.add_row(
	  created=datetime.now(),
	  # Store the logged in user in the 'user' column
	  user=current_user,
	  **article_dict
	)

@anvil.server.callable
def get_articles():
  # Get the logged in user
  current_user = anvil.users.get_user()
  # Check that someone is logged in
  if current_user is not None:
    # Get a list of articles that belong to the logged-in user,
    # sorted by 'created' column, in descending order
    return app_tables.articles.search(
      tables.order_by("created", ascending=False),
      user=current_user
    )

@anvil.server.callable
def update_article(article, article_dict):
  # check that the article given is really a row in the ‘articles’ table
  if app_tables.articles.has_row(article):
    article_dict['updated'] = datetime.now()
    article.update(**article_dict)
  else:
    raise Exception("Article does not exist")

@anvil.server.callable
def delete_article(article):
  # check that the article being deleted exists in the Data Table
  if app_tables.articles.has_row(article):
    article.delete()
  else:
    raise Exception("Article does not exist")

