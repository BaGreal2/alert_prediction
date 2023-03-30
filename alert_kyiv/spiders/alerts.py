import scrapy


class AlertsSpider(scrapy.Spider):
    name = "alerts"
    start_urls = ["https://kyiv.digital/storage/air-alert/stats.html"]

    def parse(self, response):
        yield {
            "date": response.xpath("//tr/td[1]/text()").getall(),
            "state": response.xpath("//tr/td[2]/text()").getall(),
            "duration": response.xpath("//tr/td[3]/text()").getall(),
        }

        # for row in response.css("tbody"):
        #     for col in row.css('tr'):
        #         column_data = row.css('td::text').getall()
        #         yield {
        #             "data": column_data,
        #         }
