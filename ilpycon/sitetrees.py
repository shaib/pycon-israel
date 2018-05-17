"""
Site trees defining the menus for the PyCon-Israel site
"""

from sitetree.utils import tree, item

sitetrees = (
  # A tree for English will serve as the default for now
  tree('main', 'main', items=[
      item('Home', 'home'),
      item('Blog', 'pinax_blog:blog'),
      item('Code of Conduct', 'pinax_pages:pages_page "en/code-of-conduct/"'),
      item('Schedule', 'schedule_conference'),
      item('Venue', 'pinax_pages:pages_page "en/venue/"'),
  ]),

  tree('main_he', title='ראשי', items=[
      item('עמוד הבית', 'home'),
      item('בלוג', 'pinax_blog:blog'),
      item('כללי התנהגות', 'pinax_pages:pages_page "he/code-of-conduct/"'),
      item('לוח זמנים', 'schedule_conference'),
      item('מקום', 'pinax_pages:pages_page "he/venue/"'),
  ]),

      # item('Title', 'url', children=[
      #     item('Book named "{{ book.title }}"', 'books-details', in_menu=False, in_sitetree=False),
      #     item('Add a book', 'books-add'),
      #     item('Edit "{{ book.title }}"', 'books-edit', in_menu=False, in_sitetree=False)
      # ])
  # ... You can define more than one tree for your app.
)
