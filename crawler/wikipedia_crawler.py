import wikipediaapi

wiki_wiki = wikipediaapi.Wikipedia('en')

page_py = wiki_wiki.page('University of Oxford')

print("Page - Title: %s" % page_py.title)
    # Page - Title: Python (programming language)

print("Page - Summary: %s" % page_py.summary[0:1000])