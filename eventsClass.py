# The model that handles the events within the application
import re


class EventsManager(object):

    def __init__(self):
        self.event_list = []

    def return_events(self):
        return self.event_list

    def getOwner(self, user):
        user_event_list = [
            item for item in self.event_list if item['owner'] == user]
        return user_event_list

    def allEvents(self):
        all_events = [item for items in self.event_list]
        return all_events

    def createEvent(self, event, location, category, date, owner):
        if re.match("^[a-zA-Z0-9_]*$", event):
            
            events_dict = {
                "name": event,
                "user": owner,
                "category": category,
                "location": location,
                "date": date
            }
            self.event_list.append(events_dict)
            return "event_created"
        else:
            return "no_special_characters"
        return self.getOwner(user)
