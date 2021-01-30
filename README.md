# Facebook group scraper

A simple selenium-dependent python scraper for Facebook groups.

Requirements:
- Python 3.6 or newer
- Selenium (automatically installed)

Installing:

```
# pypi
pip3 install fbgs

# local
git clone https://github.com/lesander/facebook-group-scraper.git
cd facebook-group-scraper/
pip3 install -r requirements.txt
```

CLI usage:

```shell
# local & pypi
python3 -m fbgs \
--username user@example.com \
--password "example-password" \
--url https://m.facebook.com/groups/group-name \
--output ./path/for/output.json \
--no-shell  # toggle to disable default selenium interactive prompt
```

Module usage:

```python
from fbgs import FacebookScraper
from fbgs.exceptions import ScraperException
try:
    scraper = FacebookScraper(
        username="user@example.com", password="example-password")
    scraper.login()
    g = scraper.scrape_group(url="https://m.facebook.com/groups/group-name", out="output-example.json")
    scraper.interactive()
except ScraperException as e:
    print(f'ScraperException: {e}')
```
