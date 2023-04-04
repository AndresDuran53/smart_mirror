import ephem
import pytz
from datetime import datetime,timedelta

class CelestialBodyViewer:

    def __init__(self):
        self.timezone = pytz.timezone('America/Costa_Rica')
        self.sun = ephem.Sun()

    def get_local_now(self):
        now = datetime.utcnow()
        now = pytz.utc.localize(now).astimezone(self.timezone)
        return now

    def create_observer(self, days_diff=0):
        observer = ephem.Observer()
        observer.lat = '9.7489'
        observer.lon = '-83.7534'
        observer.elevation = 0
        local_now = self.get_local_now() + timedelta(days=days_diff)
        observer.date = ephem.date(local_now)
        return observer
    
    def get_next_sun_event(self):
        observer = self.create_observer()
        sunset = observer.next_setting(self.sun)
        sunset = sunset.datetime().replace(tzinfo=pytz.utc).astimezone(self.timezone)
        sunrise = observer.next_rising(self.sun, start=observer.date)
        sunrise = sunrise.datetime().replace(tzinfo=pytz.utc).astimezone(self.timezone)
        if sunrise < sunset:
            return ("sunrise",sunrise.strftime("%H:%M%p"))
        else:
            return ("sunset",sunset.strftime("%H:%M%p"))

    def get_days_diff(self, ephem_date):
        actual_date = self.get_local_now().date()
        date_aux = ephem_date.datetime().date()
        days_diff = (actual_date - date_aux).days
        if(days_diff<0): days_diff = days_diff*-1
        return days_diff    

    def is_crescent_moon(self):
        observer_now = self.create_observer()
        observer_tomorrow = self.create_observer(1)
        moon_now = ephem.Moon(observer_now)
        moon_now.compute(observer_now)
        phase_now = moon_now.moon_phase
        moon_tomorrow = ephem.Moon(observer_tomorrow)
        moon_tomorrow.compute(observer_tomorrow)
        phase_tomorrow = moon_tomorrow.moon_phase
        return phase_now<phase_tomorrow
    
    def get_name_moonphase(self, phase):
        is_crescent = self.is_crescent_moon()
        if phase >= 0.97:
            state = "Luna Llena"
        elif phase <= 0.02:
            state = "Luna Nueva"
        elif 0.02 < phase <= 0.34:
            state = "Lúnula Creciente" if is_crescent else "Lúnula Menguante"
        elif 0.34 < phase <= 0.65:
            state = "Cuarto Creciente" if is_crescent else "Cuarto Menguante"
        elif 0.65 < phase <= 0.96:
            state = "Gibosa Creciente" if is_crescent else "Gibosa Menguante"
        return state
    
    def get_moon_phase(self):
        observer = self.create_observer()
        moon = ephem.Moon(observer)
        moon.compute(observer)
        phase = moon.moon_phase
        return phase
    
    def get_next_full_moon(self):
        observer = self.create_observer()
        next_full_moon = ephem.next_full_moon(observer.date)
        return self.ephem_date_to_string(next_full_moon)

    @staticmethod
    def ephem_date_to_string(date):
        return date.datetime().strftime("%d %b")