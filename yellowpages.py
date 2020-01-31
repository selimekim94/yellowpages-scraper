import csv
import os
import re
import sys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver.webdriver import WebDriver
from captcha.captcha import Captcha
from scrapy.selector import Selector


class YellowPages(WebDriver):
    def __init__(self, api_key):
        opts = Options()
        opts.add_argument("--headless")
        opts.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US',
                                               'profile.managed_default_content_settings.images': 2})
        opts.add_argument(
            '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/57.0.2987.133 Safari/537.36')
        WebDriver.__init__(self, opts)
        self.api_key = api_key
        self.current_page = 2

    def scrape(self, clue):
        try:
            item_list = []
            url = f'https://www.yellowpages.com.au/search/listings?clue={clue}&locationClue=&lat=&lon' \
                  f'=&selectedViewMode=list '
            self.driver.get(url)
            self.wait_until_page_loaded()
            is_captcha_none = False
            while True:
                while 'dataprotection' in self.driver.current_url:
                    captcha = Captcha(self.api_key)
                    print('Detected unusual traffic. Captcha response waiting...')
                    sel = Selector(text=self.driver.page_source)
                    g_recaptcha_key = sel.css('div.g-recaptcha::attr(data-sitekey)').extract_first()
                    captcha_response = captcha.solve_recaptcha(g_key=g_recaptcha_key, page_url=
                    self.driver.current_url)
                    if captcha_response is not None:
                        print('Captcha solved successfully.')
                        self.driver.execute_script(
                            f'document.getElementsByName("g-recaptcha-response")[0].value = "{captcha_response}"')
                        submit = self.get_element(By.CLASS_NAME, 'submit')
                        submit.click()
                        self.wait_until_page_loaded()
                    else:
                        is_captcha_none = True
                        print('Captcha Error')
                        break
                if is_captcha_none:
                    break
                try:
                    self.driver.find_element_by_link_text('Next »')
                except NoSuchElementException:
                    b = f'Scrape finished. Total {len(item_list)} items scraped. Data saved to csv file.'
                    sys.stdout.write('\r' + b)
                    sys.stdout.flush()
                    print('')
                    clue = clue.replace(' ', '_')
                    self.save(file=f'{clue}.csv', items=item_list)
                    break
                sel = Selector(text=self.driver.page_source)
                items = sel.css('div.cell > div.listing')
                for item in items:
                    name = item.css('div.listing::attr(data-full-name)').extract_first()
                    address = item.css(
                        'p.listing-address::text').extract_first()
                    contact = item.css(
                        'div.call-to-action > a::attr(href)').extract()

                    item = {'tel': '', 'mail': '', 'website': '', 'name': '', 'address': ''}
                    for element in contact:
                        if 'tel:' in element:
                            item['tel'] = element.replace('tel:', '')
                        if 'mailto:' in element:
                            if re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
                                          element.replace('%40', '@')):
                                item['mail'] = \
                                    re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
                                               element.replace('%40', '@'))[0]
                        if 'http' in element and 'yellowpages.com' not in element:
                            item['website'] = element
                    item['name'] = name
                    item['address'] = address

                    item_list.append(item)
                b = f'Scraped {len(item_list)} items'
                sys.stdout.write('\r' + b)
                sys.stdout.flush()
                self.driver.get(
                    f'https://www.yellowpages.com.au/search/listings?clue={clue}&eventType=pagination&pageNumber={self.current_page}&referredBy=www.yellowpages.com.au')
                self.wait_until_page_loaded()
                self.current_page += 1
        except Exception as e:
            print(f'Error: {e}')
        finally:
            self.driver.quit()

    def save(self, file, items):
        file_exists = os.path.isfile(file)
        with open(file, mode='a', newline='') as csv_file:
            fieldnames = ['Telephone', 'Mail', 'Website', 'Name', 'Address']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            for item in items:
                writer.writerow(
                    {
                        'Telephone': item['tel'],
                        'Mail': item['mail'],
                        'Website': item['website'],
                        'Name': item['name'],
                        'Address': item['address']
                    }
                )
