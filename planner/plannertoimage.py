from PIL import Image, ImageDraw, ImageFont
import globals
import datetime
from datetime import datetime as dt

class PlannerToImage():

    __WIDTH     = 1754
    __HEIGHT    = 1240

    def __init__(self, planner, day):
        self.__planner      = planner
        self.__first_day    = self.__get_monday(day)
        self.__time_start   = planner.get_time_begin_day()
        self.__time_end     = planner.get_time_end_day()
        self.__header_font      = ImageFont.truetype("Ubuntu-B.ttf", size=int(PlannerToImage.__HEIGHT/20))
        self.__subtitle_font    = ImageFont.truetype("Ubuntu-B.ttf", size=int(PlannerToImage.__HEIGHT/49.6))
        self.__top_font         = ImageFont.truetype("Ubuntu-B.ttf", size=int(PlannerToImage.__HEIGHT/60))
        self.__top_font_R       = ImageFont.truetype("Ubuntu-R.ttf", size=int(PlannerToImage.__HEIGHT/60))
        self.__regular_font     = ImageFont.truetype("Ubuntu-R.ttf", size=int(PlannerToImage.__HEIGHT/82))
        self.__event_name_font  = ImageFont.truetype("Ubuntu-R.ttf", size=int(PlannerToImage.__HEIGHT/82))
        self.__time_font        = ImageFont.truetype("Ubuntu-R.ttf", size=int(PlannerToImage.__HEIGHT/82))
        self.__spaceing = PlannerToImage.__HEIGHT / 80


    def __get_monday(self, day):
        return day-datetime.timedelta(days=day.weekday())


    def __advance_day(self, day):
        return day+datetime.timedelta(days=1)


    def draw_image(self, file_name):
        img = Image.new('RGBA', (PlannerToImage.__WIDTH, PlannerToImage.__HEIGHT), color = 'white')
        draw = ImageDraw.Draw(img)

        self.img_left    = PlannerToImage.__WIDTH/14
        self.img_right   = PlannerToImage.__WIDTH - self.img_left
        self.img_top     = PlannerToImage.__HEIGHT/14
        self.img_bottom  = PlannerToImage.__HEIGHT - self.img_top

        self.plan_top    = self.img_top + self.__header_font.getsize(".")[1] + 5*self.__spaceing + self.__subtitle_font.getsize(".")[1]

        now = dt.today()

        draw.text((self.img_left,self.img_top), "JANUS Planning", font=self.__header_font, fill="black")
        draw.text( (self.img_left,self.img_top + self.__header_font.getsize(".")[1] + self.__spaceing),
            "Generated on " + now.strftime("%d/%m/%Y") + " at " + now.strftime("%I:%M %p"),
            font=self.__subtitle_font, fill="black")

        draw.rectangle([(self.img_left,self.plan_top), (self.img_right,self.img_bottom)],
            fill="white", outline="gray", width=2)

        self.__draw_grid(draw)
        self.__draw_events(draw)

        img.save(file_name)


    def __draw_grid(self, draw):
        self.events_top     = self.plan_top + 3*self.__spaceing + self.__top_font.getsize(".")[1]
        self.events_left    = self.img_left+6*self.__spaceing

        time_diff = self.__time_end - self.__time_start
        diff_h, diff_m = globals.to_hours(time_diff)

        if diff_h > 0 and diff_m > 0:
            num_lines = diff_h
        else:
            num_lines = diff_h

        hour_height     = (self.img_bottom - self.events_top) / (num_lines)
        hour_start,_    = globals.to_hours(self.__time_start)

        for line_y in range(0,num_lines):
            curr_hour = hour_start+line_y
            if curr_hour < 10:
                curr_hour = "0" + str(curr_hour)

            draw.text((self.img_left+2*self.__spaceing, self.events_top+line_y*hour_height - self.__top_font.getsize(".")[1]/2),
                str(curr_hour)+":00",
                font=self.__time_font, fill="gray")

            if line_y == 0:
                width = 2
            else:
                width = 1

            draw.line([(self.events_left,self.events_top+line_y*hour_height),
                (self.img_right,self.events_top+line_y*hour_height)],
                fill="gray", width=width)

        self.events_left = self.events_left + 2*self.__spaceing
        self.events_width = (self.img_right - self.events_left) / 7

        curr_date = self.__first_day
        weekdays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

        for line_x in range(0,7):
            curr_day = weekdays[line_x]
            date_str = curr_date.strftime("%d/%m/%y")
            row_x = self.events_left + line_x*self.events_width

            if line_x > 0:
                draw.line([(row_x,self.plan_top),
                    (row_x,self.img_bottom)],
                    fill="gray", width=1)

            row_text_width  = self.__top_font.getsize(curr_day)[0]
            row_text_height = self.__top_font.getsize(curr_day)[1]
            date_text_size  = self.__top_font_R.getsize(date_str)
            row_top_height  = self.events_top - self.plan_top

            draw.text( (row_x + self.events_width/2-row_text_width/2, self.plan_top + row_top_height/2 - (row_text_height+date_text_size[1])/2),
                curr_day,
                font=self.__top_font, fill="gray")
            draw.text( (row_x + self.events_width/2-date_text_size[0]/2, self.plan_top + row_top_height/2 - (row_text_height+date_text_size[1])/2 + row_text_height),
                date_str,
                font=self.__top_font_R, fill="gray")

            curr_date = self.__advance_day(curr_date)


    def __draw_events(self, draw):
        curr_date = self.__first_day

        for day_num in range(0,7):
            day = self.__planner.get_day(curr_date.day,curr_date.month, curr_date.year)[0]

            for event in day.get_next_event():
                self.__draw_event(draw, event, day_num)

            curr_date = self.__advance_day(curr_date)


    def __draw_event(self, draw, event, day_num):
        ev_name  = event.get_name()
        ev_start = event.get_start()
        ev_end   = event.get_end()

        planner_height = self.img_bottom - self.events_top
        ev_start_y  = ((ev_start-self.__time_start)/(self.__time_end-self.__time_start)) * planner_height + self.events_top
        ev_end_y    = ((ev_end-self.__time_start)/(self.__time_end-self.__time_start)) * planner_height + self.events_top

        if event.is_travelling() or "[... travelling" in ev_name:
            fill_color      = (180,180,180)
            outline_color   = (50,50,50)
            ev_name = None
        elif event.is_specific():
            fill_color      = (255,120,120)
            outline_color   = (200,50,50)
        else:
            fill_color      = (120,255,120)
            outline_color   = (50,200,50)

        draw.rectangle([(self.events_left+day_num*self.events_width,ev_start_y),
            (self.events_left+day_num*self.events_width+self.events_width,ev_end_y)],
            fill=fill_color, outline=outline_color, width=1)

        if ev_name:
            while self.__event_name_font.getsize(ev_name)[0] > self.events_width:
                ev_name = ev_name[:-4] + "..."

            draw.text( (self.events_left+day_num*self.events_width + self.events_width/2 - self.__event_name_font.getsize(ev_name)[0]/2,
                ev_start_y+(ev_end_y-ev_start_y)/2-self.__event_name_font.getsize(".")[1]/2),
                ev_name,
                font=self.__event_name_font, fill="white")
