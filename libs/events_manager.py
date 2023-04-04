import requests
from .ha_services.homeassistant_services import HomeAssistantServices
from .ui_views.event_object import EventInformation

class EventHandler():
    def __init__(self,config_data):
        self.homeassistant_service = HomeAssistantServices.from_json(config_data)

    def get_event_list(self):
        list_calendars = self.homeassistant_service.get_calendars_events()
        list_event = []
        for calendar in list_calendars:
            list_event = list_event + self.events_from_calendar(calendar)
        return list_event
    
    def events_from_calendar(self,calendar):
        list_events = []
        owner = calendar.get_owner_name()
        for event in calendar.events:
            title = event.name
            start_time = event.start_time
            end_time = event.end_time
            new_event = EventInformation(owner,title,start_time,end_time)
            list_events.append(new_event)
        return list_events
    
    def format_event_list(self,list_event):
        formatted_events = []
        for evento in list_event:
            formatted_events.append(f"{evento.get_title()}")
        return formatted_events