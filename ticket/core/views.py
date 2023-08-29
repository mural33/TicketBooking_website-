from datetime import datetime,timedelta
from typing import Any, Dict
import random
# genal import 
from django.shortcuts import render,get_list_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
# classView
from django.views.generic import TemplateView,ListView
from django.views import View
# model import 
from database.models import UserData,Times,Demo,Booked,Dates
from django.db.models import Q
# Create your views here.

class TicketView(TemplateView):
    template_name = "ticket.html"
    
    def updating_database(self,*args, **kwargs):
        today_date= datetime.today().date()
        end_time = datetime.strptime("22:00:00", "%H:%M:%S").time()
        dates =[date.date for  date  in Dates.objects.all().order_by("date")]
        for date in dates:
            if not date >= today_date: 
                obj = Dates.objects.get(date = date)
                try:
                    booked_data = Booked.objects.get(date = obj)
                    booked_data.delete()
                except:
                    pass
                obj.delete()
                tommarrow = dates[len(dates)-1]+timedelta(days=1)
                new_obj = Dates.objects.create(date = tommarrow)
                print("new",new_obj)
                new_obj.save()
                dates.append(tommarrow)
        return dates
    
    def fake_seat_book(self,*args, **kwargs):
        seat_indices = list(range(0,26*30))
        booking_indexes = []
        for _ in range(500):
           booking_indexes.append(random.choice(seat_indices))
        return ",".join([str(i) for i in booking_indexes])
            
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # taking data from slug
        slug_movie = self.kwargs["movie"]
        slug_date = self.kwargs["date"] 
        slug_time = self.kwargs["time"]
        slug_time = datetime.strptime(slug_time, "%H:%M:%S").time()
        # send path date
        
        
        # convertig
        slug_date = datetime.strptime(slug_date, "%Y-%m-%d").date()
       
        today_date = datetime.today().date()
        current_time = datetime.now().time()
        end_time = datetime.strptime("22:00:00", "%H:%M:%S").time()
        
        context["path_time"] = slug_time
        context["path_date"] = slug_date

        self.updating_database()
        dates =Dates.objects.all().order_by("date")
        context["dates"] = dates
        if slug_date > today_date:
            times = Times.objects.all()
            context["time"] = times[0]
        else:
            try:
                times = [time for time in Times.objects.all() if time.time > current_time]
                context["next_show_time"] = times[0]
            except:
                context["next_show_time"] = datetime.strptime("10:00:00", "%H:%M:%S").time()
            context["time"] = times[0]
        
        # context["next_show_time"] = [time.time if time.time > current_time else datetime.strptime("22:00:00", "%H:%M:%S").time() for time in Times.objects.all() ][0]
        context["times"] = times
        context["today_date"] = today_date
        movie_time= Times.objects.get(time = slug_time)
        movie_name= Demo.objects.get(slug=slug_movie)
        movie_date = Dates.objects.get(date = slug_date)
        
        try:
            seat_indexs = Booked.objects.get(Q(movie=movie_name) & Q(time=movie_time) & Q(date=movie_date))
            total_seats_booked = len(seat_indexs.seats_index.split(','))
            max_seats = 26*30
            print(total_seats_booked/max_seats)
            if(total_seats_booked/max_seats) < 0.4:
                seat_indexs = seat_indexs.seats_index
                context["fake"] =self.fake_seat_book()
            else:
                seat_indexs = seat_indexs.seats_index
                context["fake"] ="1,2"
        except:
            seat_indexs ="0,1,2,3"
            context["fake"] =self.fake_seat_book()

        context ["index"] = seat_indexs

        return context
    
    def post(self, request, *args, **kwargs):
            book_data = request.POST.get("booked_seats")[1:-1]
            print(book_data)
            movie = self.kwargs["movie"]
            time = self.kwargs["time"]
            day = self.kwargs["date"]
            time = Times.objects.get(time = time)
            movie= Demo.objects.get(slug = movie)
            date=Dates.objects.get(date = day)
            try:
                obj = Booked.objects.get(Q(movie=movie) & Q(time=time) & Q(date = date))
                print(obj.seats_index)
                print(book_data)
                obj.seats_index = book_data + ","
            except:
                obj = Booked.objects.create(movie = movie,seats_index = book_data ,time= time ,date = date)
            obj.save()
            return JsonResponse({"message": "Data received and processed"})
    
class HomeView(ListView):
    template_name = "home.html"
    model = Demo
    context_object_name = "movies"
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        current_time = datetime.now().time()
        context["today_date"] = datetime.today().date()
        for i in Times.objects.all().order_by("time"):
            # print(i.time,current_time)
            if i.time > current_time:
                context["next_show_time"] = i.time
                break
        return context






