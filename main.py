from yellowpages import YellowPages

if __name__ == '__main__':
    clue = input('Please enter a keyword to scrape: ')
    y_pages = YellowPages(api_key='Your 2captcha API Key')
    y_pages.scrape(clue=clue)
