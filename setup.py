from distutils.core import setup
setup(
        name = 'edgar',
        packages = ['edgar'], # this must be the same as the name above
        version = '0.2.0',
        description = 'Scrape data from SEC\'s EDGAR',
        author = 'Joey Sham',
        author_email = 'sham.joey@gmail.com',
        url = 'https://github.com/joeyism/py-edgar', # use the URL to the github repo
        download_url = 'https://github.com/joeyism/py-edgar/archive/0.1.tar.gz',
        keywords = ['edgar', 'sec'], 
        classifiers = [],
        )
