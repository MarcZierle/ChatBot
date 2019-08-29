from PIL import Image, ImageDraw, ImageFont
import globals
import datetime
from datetime import datetime as dt
import os

class PlannerToImage():

    __WIDTH     = 1754
    __HEIGHT    = 1240

    bot_name = "JANUS"
    additional_info_text = [
        bot_name+". An event planning ChatBot with respect to travel times and durations.",
        "Created as part of the semester project \"Dialoge mit Computern\" at Humboldt University of Berlin."
    ]

    def __init__(self, planner, day):
        self.__planner      = planner
        self.__first_day    = self.__get_monday(day)
        self.__time_start   = planner.get_time_begin_day()
        self.__time_end     = planner.get_time_end_day()
        self.__path = os.path.dirname(__file__)+"/../assets"
        self.__header_font      = ImageFont.truetype(self.__path+"/fonts/Dosis-Bold.ttf", size=int(PlannerToImage.__HEIGHT/20))
        self.__subtitle_font    = ImageFont.truetype(self.__path+"/fonts/Ubuntu-B.ttf", size=int(PlannerToImage.__HEIGHT/49.6))
        self.__top_font         = ImageFont.truetype(self.__path+"/fonts/Ubuntu-B.ttf", size=int(PlannerToImage.__HEIGHT/60))
        self.__top_font_R       = ImageFont.truetype(self.__path+"/fonts/Ubuntu-R.ttf", size=int(PlannerToImage.__HEIGHT/60))
        self.__add_info_font    = ImageFont.truetype(self.__path+"/fonts/Ubuntu-R.ttf", size=int(PlannerToImage.__HEIGHT/82))
        self.__event_name_font  = ImageFont.truetype(self.__path+"/fonts/Ubuntu-R.ttf", size=int(PlannerToImage.__HEIGHT/82))
        self.__time_font        = ImageFont.truetype(self.__path+"/fonts/Ubuntu-R.ttf", size=int(PlannerToImage.__HEIGHT/82))
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
        self.img_top     = PlannerToImage.__HEIGHT/16
        self.img_bottom  = PlannerToImage.__HEIGHT - self.img_top

        self.plan_top    = self.img_top + self.__header_font.getsize(PlannerToImage.bot_name)[0] + self.__header_font.getsize(PlannerToImage.bot_name)[1] + 3*self.__spaceing

        self.__draw_header(img, draw)
        self.__draw_grid(draw)
        self.__draw_events(draw)
        self.__draw_additional_infos(img, draw)

        img.save(file_name)


    def __draw_header(self, img, draw):
        logo_txt_w = int(self.__header_font.getsize(PlannerToImage.bot_name)[0])
        logo_spaceing_left = 2*self.__spaceing

        red_logo = Image.open(self.__path+"/../assets/images/logo_red_transparent.png")
        red_logo = red_logo.resize((logo_txt_w, logo_txt_w), Image.ANTIALIAS)

        pixel_data = red_logo.load()
        if red_logo.mode == "RGBA":
          for y in range(red_logo.size[1]):
            for x in range(red_logo.size[0]):
              if pixel_data[x, y][3] < 255:
                pixel_data[x, y] = (255, 255, 255, 255)

        img.paste(red_logo,
            (int(self.img_left+logo_spaceing_left), int(self.img_top))
        )

        draw.text((self.img_left+logo_spaceing_left,self.img_top+logo_txt_w),
            PlannerToImage.bot_name,
            font=self.__header_font, fill="black")

        #now = dt.today()
        #draw.text( (self.img_left,self.img_top + self.__header_font.getsize(".")[1] + self.__spaceing),
        #    "Generated on " + now.strftime("%d/%m/%Y") + " at " + now.strftime("%I:%M %p"),
        #    font=self.__subtitle_font, fill="black")


    def __draw_additional_infos(self, img, draw):
        logo_size = int(0.7 *(PlannerToImage.__HEIGHT - self.img_bottom))

        hu_logo = Image.open(self.__path+"/../assets/images/hu_logo.png")
        hu_logo = hu_logo.resize((logo_size,logo_size), Image.ANTIALIAS)

        pixel_data = hu_logo.load()
        if hu_logo.mode == "RGBA":
          for y in range(hu_logo.size[1]):
            for x in range(hu_logo.size[0]):
              if pixel_data[x, y][3] < 255:
                pixel_data[x, y] = (255, 255, 255, 255)

        hu_w, hu_h = hu_logo.size
        bg_w, bg_h = img.size

        logo_x = int(self.img_right-logo_size)
        logo_y = int(self.img_bottom+(PlannerToImage.__HEIGHT - self.img_bottom)/2-logo_size/2)

        img.paste(hu_logo,
            (logo_x,logo_y)
        )


        for i in range(len(PlannerToImage.additional_info_text)):
            txt = PlannerToImage.additional_info_text[i]
            txt_w, txt_h = self.__add_info_font.getsize(txt)

            line_h = txt_h+self.__spaceing/4
            num_lines = len(PlannerToImage.additional_info_text)

            xpos = self.img_right-logo_size-self.__spaceing-txt_w
            ypos = logo_y+logo_size/2 + i*line_h - (num_lines*line_h)/2

            draw.text( (xpos, ypos),
                txt,
                font=self.__add_info_font, fill="gray")


    def __draw_grid(self, draw):
        draw.rectangle([(self.img_left,self.plan_top), (self.img_right,self.img_bottom)],
            fill="white", outline="gray", width=2)

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
            fill_color      = (120,200,120)
            outline_color   = (50,170,50)

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
