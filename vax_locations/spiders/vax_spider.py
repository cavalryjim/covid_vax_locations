import scrapy
import csv
import datetime, pytz

class VaxSpider(scrapy.Spider):
    name = "vax_locations"

    start_urls = [
        'https://shotfor100.com/locations', #
    ]

    def parse(self, response):
        now = pytz.timezone("America/Chicago").localize(datetime.datetime.now())
        file_name = 'vax_locations_' + now.strftime("%Y-%m-%d")  + '.csv'
        locations = response.css("div.campus")

        out_file = open(file_name, 'w')
        csv_writer = csv.writer(out_file)
        csv_writer.writerow( [ 'location_id', 'location', 'address', 'times' ])

        for location in locations:
            location_id = ''
            name = location.css("h4::text").get()
            address = location.css("p::text").get()
            times = location.css("p.tracking::text").get()
            csv_writer.writerow( [location_id, name, address, times] )

        out_file.close()
