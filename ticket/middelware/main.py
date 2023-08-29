from datetime import datetime,timedelta
from database.models import Times,Dates,Booked
from django.urls import reverse
from django.http import HttpResponseRedirect

class MiddeleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def next_show_time(self):
        current_time = datetime.now().time()
        next_show = None
        for time in Times.objects.filter(time__gt=current_time).order_by("time"):
            next_show= time.time
            return next_show
    
    def __call__(self, request):
        response = self.get_response(request)
        demo_path = "movie"
        path_elements = request.path.split("/")
        today_date = datetime.today().date()
        current_time = datetime.now().time()
        dates =[date.date for date in  Dates.objects.all() ]
        if len(path_elements) > 3 and path_elements[1] == demo_path:
            path_movie = path_elements[2]
            path_date = datetime.strptime(path_elements[3], "%Y-%m-%d").date()
            path_time = datetime.strptime(path_elements[4], "%H:%M:%S").time()
            last_show_time =  datetime.strptime("22:00:00", "%H:%M:%S").time()

            if today_date == path_date and current_time > path_time:
                next_show_time = self.next_show_time()
                if next_show_time:
                    return HttpResponseRedirect(reverse("book", kwargs={"movie": path_movie, "date": path_date, "time": next_show_time}))
                
            elif path_date > dates[-1]:
                return HttpResponseRedirect(reverse("book", kwargs={"movie": path_movie, "date":dates[-1], "time":path_time}))
            
            elif not (path_date >= today_date):
                next_show_time = self.next_show_time()
                return HttpResponseRedirect(reverse("book", kwargs={"movie": path_movie, "date":today_date, "time": next_show_time}))
            
            elif path_date == today_date and current_time > last_show_time:
                next_day = today_date +timedelta(days=1)
                return HttpResponseRedirect(reverse("book", kwargs={"movie": path_movie, "date":next_day, "time":"10:00:00"}))

        return response

