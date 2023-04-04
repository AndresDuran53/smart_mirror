import requests
from datetime import datetime,timedelta
from .calendar import Calendar

class HomeAssistantServices:    
    def __init__(self,url,token,list_calendar):
        self.url = url
        self.token = token
        self.filling_list_devices(list_calendar)

    def filling_list_devices(self,list_calendar):
        self.important_calendars = []
        for calendar_aux in list_calendar:
            self.important_calendars.append(Calendar(calendar_aux["id"],calendar_aux["owner"]))
    
    def get_calendars_events(self):
        self.update_events_by_calendar()
        return self.important_calendars       
    
    def requests_calendar_events(self,calendar_id,future_days=3):
        now = datetime.now()
        actual_time_string = now.strftime("%Y-%m-%d")
        future_time = (now + timedelta(days=future_days))
        future_time_string = future_time.strftime("%Y-%m-%d")
        events_filter = f"start={actual_time_string}&end={future_time_string}"
        local_calendar_url = f"{self.url}/calendars/{calendar_id}?{events_filter}"    
        headers = {
            'Authorization': f"Bearer {self.token}",
            'Content-Type': 'application/json'
        }
        # Realizar la petición HTTP GET
        response = requests.get(local_calendar_url, headers=headers)
        list_events_data = response.json()
        list_events = []
        for event in list_events_data:
            list_events.append(Calendar.create_event_from_json(calendar_id,event))
        return list_events
    
    def update_events_by_calendar(self):
        for calendar in self.important_calendars:
            calendar_id = calendar.calendar_id
            calendar.set_events(self.requests_calendar_events(calendar_id))

    @classmethod
    def from_json(cls, json_config):
        config = json_config["homeAssistant"]
        url = config['url']
        ha_token = config['ha_token']
        calendars = config['calendars']
        return HomeAssistantServices(url, ha_token, calendars)