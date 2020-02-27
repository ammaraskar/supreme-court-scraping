import scrapy
import datetime
import re

from sc_scraper import case_code


def cleanup_text(text):
    return text.replace("\xA0", " ").strip().strip(")*#")


class GrantedCasesSpider(scrapy.Spider):
    name = "granted-cases"
    start_urls = [
        "https://www.supremecourt.gov/orders/grantednotedlists.aspx",
    ]

    def parse(self, response):
        per_year = response.xpath(
            '//a[contains(@href, "../grantednotedlist")]/@href'
        ).getall()
        for year in per_year:
            yield response.follow(year, self.parse_year_page)

    def parse_year_page(self, response):
        case_headings = response.xpath('//div[@class="WordSection1"]//a/..')

        for heading in case_headings:
            # The link to the pdf has the docket id.
            docket_id = heading.xpath("a/text()").get()
            if not docket_id:
                continue
            # Make sure we have a title.
            title = heading.xpath("text()").get()
            if not title:
                continue
            title = cleanup_text(title)
            title = title.split()
            if len(title) == 0:
                continue

            # Try to split out the case code identifier from the title, e.g:
            #   CFX      BABB V. WILKIE, SEC. OF VA
            #            FULTON V. CITY OF PHILADELPHIA, PA
            try:
                code = case_code.parse_case_code(title[0])
                # The first word is the case code identifier
                title = " ".join(title[1:])
            except ValueError:
                code = None
                # No case code identifier.
                title = " ".join(title)

            date_granted = heading.xpath(
                "./ancestor::p/following-sibling::p/span/text()"
            ).get()
            date_granted = cleanup_text(date_granted).lower()
            m = re.search('(\d\d?/\d\d?/\d\d)', date_granted)
            if m:
                date_granted = datetime.datetime.strptime(m.group(0), "%m/%d/%y")
            else:
                date_granted = None

            # Turn the enums into something json serializable.
            if code:
                code = {
                    "jurisdiction": code.jurisdiction.name,
                    "court_below": code.court_below.name,
                    "nature": code.nature.name,
                }

            final_info = {
                "docket_id": docket_id,
                "case_code_info": code,
                "title": title,
                "date_granted": date_granted,
            }
            yield final_info
