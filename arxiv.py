#! /usr/bin/python

# This code scans the ArXiv for the 25 most recent post with authors from UCSB.
# read_arxiv() returns the 25 most recent posts. 
# See comments below for how the output is formated

import urllib2

faculty = ['Blaes_O', 'Bildsten_L', 'Peng_O', 'Martin_C', 'Antonucci_R',
           'Lubin_P', 'Gwinn_C', 'Howell_D', 'Mazin_B', 'Monreal_B', 'Peale_S',
           ]
inst = ['UCSB', 'EXACT+UC_Santa_Barbara']
urlbase = 'http://arxiv.org'

# The class "article" has the following attributes
#   article.title (a string which is the title of the article)
#   article.authors (a list of strings, each member is a separate author.
#                    This list preserves the order found on the ArXiv.)
#   article.url (a string which is the url to the ArXiv entry for the article)
#   article.pdfurl (a sting which contains the url of the pdf for the article)
#   article.comments (a string containing the comment that the authors 
#                     included when submitting the paper)
#   article.subjects (a sting which list the subjects of the paper, 
#                     e.g. "Astrophysics of Galaxies (astro-ph.GA)")
class article:
  def __init__(self, listing):
    """Takes a listing from a single article and extracts important info."""
    # split to examine different fields/items
    items = listing.split('<span class="descriptor">')

    # first item contains urls
    tmp = items.pop(0).split('a href="')
    # extract ArXiv url
    self.url = urlbase + (tmp[1].split('"'))[0]
    # extract url to pdf file
    self.pdfurl = urlbase + (tmp[2].split('"'))[0]

    # 2nd item contains title
    self.title = ((items.pop(0).split("\n"))[0].split('> '))[1]

    # 3rd item contains list of authors
    tmp = items.pop(0).split('">')
    tmp.pop()
    tmp.pop(0)
    self.authors = [i.split('</a>')[0] for i in tmp]

    # 4th item contains comments
    self.comments = ((items.pop(0).split("\n"))[0].split('> '))[1]

    # 5th item contains subjects
    self.subjects = ((items.pop(0).split("</span>"))[1].split('">'))[1]

def read_arxiv(print_url=False):
  """Scans the ArXiv and returns a list containing the 25 most recent submissions from UCSB.

  The keyword "print_url" tels the function weather to print the url which is used to scan the ArXiv.

  Each member of the output list is an object with the following attributes:

    article.title (a string which is the title of the article)
    article.authors (a list of strings, each member is a separate author.
                     This list preserves the order found on the ArXiv.)
    article.url (a string which is the url to the ArXiv entry for the article)
    article.pdfurl (a sting which contains the url of the pdf for the article)
    article.comments (a string containing the comment that the authors 
                      included when submitting the paper)
    article.subjects (a sting which list the subjects of the paper, 
                      e.g. "Astrophysics of Galaxies (astro-ph.GA)")

  """

  # construct the url used to identify UCSB submissions to the ArXiv
  search = []
  # add searches for faculty members
  for i in faculty :
    search.append('au:+'+i)
  # add searches for different versions of the institution name
  for i in inst :
    search.append('all:+'+i)
  
  # start with the proper beginning for the url
  url = urlbase + '/find/astro-ph/1/'
  # use ORs so that any single match is accepted
  url += 'OR+' * (len(search) - 1)
  # insert all the items in "search" list
  url += '+'.join(search)
  # add proper url suffix
  url += '/0/1/0/all/0/1'
  if print_url : print url
  
  # read date on the web page specified by the url
  data = urllib2.urlopen(url).read()
  # the string '<dt>' seams to separate all the listings
  items = data.split('<dt>')
  # remove the stuff before the first listing
  items.pop(0)
  
  # extract the useful info from the listings
  papers = []
  for i in items:
      try:
          papers.append(article(i))
      except IndexError:
          pass
  # return a list of the most recent articles
  return papers
