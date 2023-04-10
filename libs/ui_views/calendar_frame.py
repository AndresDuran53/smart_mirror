from tkinter import *
from .custom_frame import CustomFrame,small_text_size,title_event_text_size,event_text_size

class Calendar(Frame):
    calendar_icon = None
    formatted_events=None
    last_owner = ""

    def __init__(self, parent, calendar_icon, **kwargs):
        CustomFrame.__init__(self, parent, kwargs)
        self.calendarEventContainer = Frame(self, bg=self.background)
        self.calendarEventContainer.pack(side=BOTTOM, anchor=W)
        self.calendar_icon = calendar_icon
        

    def create_calendar_event(self,event):
        calendar_event = CalendarEvent(self.calendarEventContainer,self.calendar_icon,
                                        background_parent = self.background, 
                                        fontColor_parent = self.fontColor, 
                                        fontStyle_parent = self.fontStyle)
        calendar_event.eventTitleLbl.config(text=event.get_title())
        calendar_event.eventNameLbl.config(text=event.get_time())
        return calendar_event

    def remove_all_events(self):
        for widget in self.calendarEventContainer.winfo_children():
            widget.destroy()
        self.last_owner=""
    
    def show_event_list(self):
        list_frame_events = []
        for event in self.formatted_events:
            calendarLbl = self.change_calendar_owner(event.owner_name)
            if(calendarLbl is not None): list_frame_events.append((calendarLbl,(8, 0)))
            calendar_event = self.create_calendar_event(event)
            list_frame_events.append((calendar_event,8))
        for frame_event,padding_y in list_frame_events:
                    frame_event.pack(side=TOP, anchor=W, pady=padding_y)

    def update_ui_events(self,new_formatted_events):
        if(self.formatted_events != new_formatted_events or len(self.calendarEventContainer.winfo_children())==0):
            self.formatted_events = new_formatted_events
            self.remove_all_events()
            if(len(self.formatted_events)>0):
                self.show_event_list()
            else:
                calendar_event = CalendarEvent(self.calendarEventContainer,self.calendar_icon,
                                        background_parent = self.background, 
                                        fontColor_parent = self.fontColor, 
                                        fontStyle_parent = self.fontStyle)
                calendar_event.eventTitleLbl.config(text="Sin acceso al calendario de eventos")
                calendar_event.pack(side=TOP, anchor=W, pady=8)

    def change_calendar_owner(self,owner):
        if(self.last_owner==owner): return None
        self.last_owner=owner
        text = F"{owner} events:"
        calendarLbl = Label(self.calendarEventContainer, text=text, font=(self.fontStyle, small_text_size), fg="#79D9D4", bg=self.background)
        return calendarLbl

class CalendarEvent(Frame):
    def __init__(self, parent, calendar_icon, event_name="Ningun evento registrado", **kwargs):
        CustomFrame.__init__(self, parent, kwargs)
        self.iconLbl = Label(self, bg=self.background, image=calendar_icon)
        self.iconLbl.image = calendar_icon
        self.iconLbl.pack(side=LEFT, anchor=N)
        self.eventName = event_name
        self.eventTitleLbl = Label(self, text="Prueba de titulo", font=(self.fontStyle, title_event_text_size), fg=self.fontColor, bg=self.background)
        self.eventTitleLbl.pack(side=TOP, anchor=W)
        self.eventNameLbl = Label(self, text=self.eventName, font=(self.fontStyle, event_text_size), fg="#AAAAAA", bg=self.background)
        self.eventNameLbl.pack(side=TOP, anchor=W)