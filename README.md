# Email Ninja

Takes in a URL and returns an array of emails found within the domain

## Dependencies

Install them however you like. I recommend using pip :)

- python 3.4
- urllib
- BeautifulSoup4
- lxml

## Run it

There's an example URL built in, so you can run the script without anything breaking:

    python3 jana.py
    
Or you can pass a URL string to `go_go_gadget_emails()` on line 110

## Assumptions + limitations

- Stays within the input domain
- Only locates the `mailto:` links
- Doesn't work with JS framework sites
- Doesn't fail gracefully (if it hits a 404, you'll notice)