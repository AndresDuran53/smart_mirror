from datetime import datetime

class EventInformation():
    def __init__(self,owner_name: str, title: str, start_time: datetime, end_time: datetime):
        self.owner_name = owner_name
        self.title = title
        self.start_time = start_time
        self.end_time = end_time

    def get_title(self, max_chars = 30):
        if(len(self.title)>30):
            return self.title[:max_chars]
        else:
            return self.title
        
    def get_time(self):
        if(self.start_time == self.end_time):
            return self.start_time.strftime("%A %b %d")
        elif(self.is_same_day()):
            return self.get_short_time()
        else:
            return self.get_complete_time()

    def get_complete_time(self):
        datetime_output_format="%A, %b %d - %I:%M%p"
        start_time = self.start_time.strftime(datetime_output_format)
        end_time = self.end_time.strftime(datetime_output_format)
        time_value = f"From {start_time} to {end_time}"
        return time_value

    def get_short_time(self):
        datetime_output_format="%A at %I:%M %p"
        time_value = self.start_time.strftime(datetime_output_format)
        return time_value
        
    def is_same_day(self):
        string_start_time = EventInformation.str_from_datetime(self.start_time,"%A, %b %d")
        string_end_time = EventInformation.str_from_datetime(self.end_time,"%A, %b %d")
        return (string_start_time==string_end_time)
    
    @staticmethod
    def str_from_datetime(datetime_info,datetime_output_format="%A, %b %d - %I:%M%p"):
        string_value = datetime_info.strftime(datetime_output_format)
        return string_value

    @staticmethod
    def datetime_from_str(date_str):
        date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z')
        return date_obj
