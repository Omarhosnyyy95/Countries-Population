import scrapy
import json

class SeatsSpider(scrapy.Spider):
    name = 'seats'
    allowed_domains = ['www.majorcineplex.com']

    #https://www.majorcineplex.com/cinema/ajax_get_quickbranch
    #POST
    #cinema_id = //div[@class='cinema_filter']/a/@data-filter-cinema-id
    #cinema_name = //div[@class='cinema_filter']/a/@data-filter-cinema-name-en
    cinema_id = 1
    
    #start request to get the showtimes
    def start_requests(self):
        url = "https://www.majorcineplex.com/ajaxbooking/ajax_showtime"

        form_data = {'movie_text': '',
        'cinema_text': json.dumps(self.cinema_id)
        }
        
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }

        yield scrapy.FormRequest(
            url=url,
            formdata=form_data,
            method="POST",
            headers=headers,
            callback=self.cinema_page
        )

    # Now we are in the cinema page
    def cinema_page(self, response):
       
        cinema_name = response.xpath("//div[@class='book_branch_textinside']//text()").get()
        
        #get all sessions in a cinema page
        sessions_ids = response.xpath("//div[@class='book_st_time']/a[contains(@class, 'nextst')]/@data-showtime") 
        

        for session_id in sessions_ids:               
            
            theatre = session_id.xpath(".//preceding::div[@class='book_st_theatre']//text()").get()
            movie_name = session_id.xpath(".//preceding::div[@class='book_st_mvname']//text()").get()
            
            yield scrapy.Request(
                url = f"https://www.majorcineplex.com/apivistaticketing/get_seats?session_id={session_id.get()}",
                method="GET",                
                headers={
                    "accept": "application/json"
                },
                callback=self.parse,
                meta={

                    'cinema_name': cinema_name,
                    'session_id': session_id.get(),
                    'movie_name': movie_name,
                    'theatre': theatre
                }
            )
         

    def parse(self, response):
        

        # get the meta data
        cinema_name = response.meta['cinema_name']
        session_id = response.meta['session_id']
        movie_name = response.meta['movie_name']
        theatre = response.meta['theatre']
        
        #load the json response
        response_dict = json.loads(response.body)
        
        # get the seats list
        seats = response_dict.get('result').get('seats')
        
        # define needed variables
        unreserved_seats = 0
        purchased_seats = 0
        fake_reservations = 0
        social_distancing_seats = 0

        # get to rows 
        for seat in seats:
            columns = seat['Columns']    
            
            # get to columns
            for column in columns:
            
                status = (dict(column)).get('Status')
                
                if status == 0:
                    unreserved_seats += 1        
                elif status == 1:
                    purchased_seats += 1
                elif status == 2:
                    fake_reservations += 1
                elif status == 5:
                    social_distancing_seats += 1
        
        # calculations
        total_seats = purchased_seats + unreserved_seats + fake_reservations
        occupancy_rate = (purchased_seats/total_seats) * 100
        available_seats = unreserved_seats + purchased_seats + fake_reservations
                    

        yield{
            'cinema_id': self.cinema_id,
            'cinema_name': cinema_name,
            'theatre': theatre,
            'movie_name': movie_name,
            'session_id': session_id,
            'available_seats': available_seats,
            'unreserved_seats': unreserved_seats,
            'purchased_seats': purchased_seats,
            'fake_reservations': fake_reservations,
            'social_distancing_seats': social_distancing_seats,
            'occupancy_rate': occupancy_rate,
        }

            