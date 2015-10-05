# webpage email extractor
# by mary schmidt
# 31 july 2015
#


from urllib.parse import urlparse, urljoin, urlunparse
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


def go_go_gadget_emails(input_url = 'https://anthonystuff.wordpress.com/'):

    email_list = [] # list of emails we've found
    visited_urls = [] # don't want to get stuck on self-linking pages
    original_url = input_url

    email_list = email_ninja(input_url, email_list, visited_urls, original_url)

    return email_list


def email_ninja(input_url, email_list, visited_urls, original_url):

    visited_urls.append(input_url.rstrip('/'))

    page = urlopen(input_url)
    soup = BeautifulSoup(page, 'lxml')

    links = soup.find_all('a')

    for link in soup.find_all('a'):
        # if link is an email and is not already in email_list, append
        # else if it has an href and we haven't been there yet, vamos
        if link.get('href'):

            # handle email addresses
            if 'mailto:' in link.get('href'):

                email_address = link.get('href').replace('mailto:', '')

                if not email_address in email_list:
                    email_list.append(email_address)

            # handle rogue phone numbers
            elif 'tel:' in link.get('href'):

                continue

            # handle non-email links
            else:

                # make sure link_address is semi-valid web adrress
                link_address = link_sanitizer(link.get('href'), input_url)

                if not link_address in visited_urls:

                    # let's stay within the original domain
                    original_domain = urlparse(original_url).netloc
                    link_domain = urlparse(link_address).netloc

                    if original_domain in link_domain:
                        email_list = email_ninja(link_address, email_list, visited_urls, original_url)

    return email_list


def link_sanitizer(unsanitized_link, input_url):

    # parse the link
    parsed_unsanitized_link = urlparse(unsanitized_link)

    # remove trailing slash
    unsanitized_link = unsanitized_link.rstrip('/')

    # no query params or fragments allowed
    sanitized_link = handle_potential_query_params_and_fragment(parsed_unsanitized_link, input_url)

    # there's no netloc in the link, but there is a path: relative link
    if parsed_unsanitized_link.netloc == '' and parsed_unsanitized_link.path != '':
        sanitized_link = handle_relative_link(sanitized_link, input_url)

    return sanitized_link.rstrip('/')


def handle_potential_query_params_and_fragment(parsed_link, input_url):

    parsed_link_list = list(parsed_link)

    # by handle I mean ignore
    # remove params, query, fragment
    parsed_link_list[3] = ''
    parsed_link_list[4] = ''
    parsed_link_list[5] = ''

    sanitized_link = urlunparse(parsed_link_list)

    return sanitized_link


def handle_relative_link(link, input_url):

    # join the path with the input url
    sanitized_link = urljoin(input_url, link)

    return sanitized_link


output_emails = go_go_gadget_emails()
print(output_emails)
