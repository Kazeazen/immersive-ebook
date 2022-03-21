'''
TITLE: Tome To Read
AUTHOR: James Thomason
DESCRIPTION: So far this is the welcome page. Probably will integrate most things from this file into the main file. \
            However, this is just the skeleton for the main page that displays the Logo as well as a welcome.
            The welcome screen itself will have the functionality of being able to click anywhere on screen to switch
            over to the main screen. 

'''
from tkinter import *
import tkinter as tk
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
import customtkinter
import pandas as pd
import requests
import pygame
import os

pygame.mixer.init()

url='https://raw.githubusercontent.com/colbychambers25/immersive-ebook/main/Domain_Free_eBook.csv'
book_library = pd.read_csv(url) #print to see what the panda looks like
url= 'https://raw.githubusercontent.com/colbychambers25/immersive-ebook/page_audio_map/Sound_audio_map.csv'
audio_map = pd.read_csv(url)
prev_song = ['none']

class story_file:
    def __init__(self):
        self.story = []
        # path = "./ereadpngs"
        '''os.chdir(path)
        for file in os.listdir():
            self.story.append(file)'''
        
    def save_files(self):
        file = open('story.txt','w')
        for stories in self.story:
            if stories not in file:
                file.write(stories +'\n')
        file.close()

    def add_story(self,filename):
        self.story.append(filename)


class music_file:
    def __init__(self):

        self.files = []

        path = "./ereadmp3"
        os.chdir(path)
        for file in os.listdir():
            self.files.append(file)
        os.chdir("...")
        


    def save_files(self):
        self.song_dataframe = pd.DataFrame(self.files)
        self.song_dataframe.to_csv('tometoread_music.txt',encoding='utf-8',index=False)

    def add_file(self,filename):
        self.files.append(filename)


class tome_to_read(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.container = tk.Frame(self)

        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight = 1)
        self.container.grid_columnconfigure(0, weight = 1)

        self.frames = {}
        
        for F in (start_page,main_menu, settings_page, upload_page): # and ereader page, about us page, library page
            frame = F(self.container,self)

            self.frames[F] = frame

            frame.grid(row = 0, column = 0, sticky="nsew")

        self.show_frame(start_page)
        self.music_songs = music_file()
        self.story = story_file()
        
        # pygame.mixer.music.load(self.music.files[3])
        # pygame.mixer.music.play(loops=0)
    
    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()

        
    def upload_file(self,type_of_upload):
        if type_of_upload == "Music":
            file_type = [("Mp3 Files","*.mp3")]
        if type_of_upload == "Story":
            file_type = [("Pdf file","*.pdf"), ("text files","*.txt")]
        file = askopenfile(parent=self,mode="rb", title=f'Choose {type_of_upload} to upload!', filetype=file_type)
        if type_of_upload == "Music" and file:
            # do something with the music file 
            self.music_songs.add_file(file.name)
            pygame.mixer.music.load(file.name)
            pygame.mixer.music.play(loops=0)
            self.music_songs.save_files()
            
        if type_of_upload == "Story" and file:
            self.story.add_story(file)
            self.story.save_files()

class start_page(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)
        img = ImageTk.PhotoImage(Image.open("start_page_background.jpg").resize((1200,800)), Image.ANTIALIAS)
        labl = tk.Label(self, image=img)
        labl.img = img
        labl.place(relx=0.5, rely=0.5, anchor= CENTER)

        # main logo creation, implementation, placing into frame
        logo = Image.open("TomeToRead_Logo.png")
        logo = logo.resize((350,380))
        logo = ImageTk.PhotoImage(logo)
        logo_label = Label(self,image=logo)
        logo_label.image = logo
        logo_label.place(relx=.55, rely=.4, anchor= CENTER)
        # end of main logo creation, implementation, placing into frame

        instructions = Button(self, text="Click here to begin!", font=("Raleway", 32), command=lambda: controller.show_frame(main_menu), borderwidth=0)
        instructions.place(relx=.55,rely=.95, anchor= S)
        

# Music is supposed to play when this screen is shown, 
class main_menu(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)        
        label = Label(self, text="Welcome to Tome to Read!")
        label.pack(padx=10,pady=10)
        label.place(relx=.5, anchor=N)

        # button layout
        # library button, upload button
        # about us button, settings button

        # button for about us page | Page not implemented 
        about_us_btn = customtkinter.CTkButton(
            self,
            width = 100,
            height = 50,
            border_width=0,
            corner_radius=2,
            text="About Us",
            text_font = ("Raleway", 15)
            # implement command once about us page is done

        )
        about_us_btn.pack(side="left")
        about_us_btn.place(relx=.45, rely=.775, anchor=CENTER)
        
        # button for library page | Page not implemented
        library_btn = customtkinter.CTkButton(
            self,
            width = 100,
            height = 50,
            border_width=0,
            corner_radius=2,
            text="Read",
            text_font = ("Raleway", 15)
            # implement command once library page is done
        )
        library_btn.pack(anchor=CENTER)
        library_btn.place(relx=.45,rely=.7,anchor=CENTER)

        # button for upload page
        
        upload_btn = customtkinter.CTkButton(
            self,
            width = 100,
            height = 50,
            border_width=0,
            corner_radius=2,
            text="Upload",
            text_font=("Raleway", 15),
            command = lambda: controller.show_frame(upload_page)
        )
        upload_btn.pack(anchor=CENTER)
        upload_btn.place(relx=.55,rely=.7,anchor=CENTER)

        # button for settings page
        settings_btn = customtkinter.CTkButton(
            self,
            width = 100,
            height = 50,
            border_width=0,
            corner_radius=2,
            text="Settings",
            text_font= ("Raleway", 15),
            command = lambda: controller.show_frame(settings_page)
        )
        settings_btn.pack(anchor=CENTER)
        settings_btn.place(relx=.55, rely=.775, anchor=CENTER)

        # logo in main menu
        logo = Image.open("TomeToRead_Logo.png")
        logo = logo.resize((350,380))
        logo = ImageTk.PhotoImage(logo)
        logo_label = Label(self,image=logo)
        logo_label.image = logo
        logo_label.place(relx=.5, rely=.3, anchor= CENTER)

class upload_page(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)
        # top portion of the user upload page
        upload_header = Frame(self, width = 1200, height = 100, bg = "white")
        upload_header.grid(columnspan=3,rowspan=2,row=0)
        upload_label = Label(upload_header, text = "Write in your own story and sound!", font = ("Raleway", 32), fg="black", bg="white")
        upload_label.place(relx=.5,rely=.5, anchor=CENTER)
        # Placing button into the top section of settings page
        back_arrow_img = PhotoImage(file="ereadpngs/chevron-left.png")
        back_arrow_img = back_arrow_img.subsample(15)

        back_arrow = customtkinter.CTkButton(
        upload_header,
        width=50,
        height=30,
        border_width=0,
        corner_radius=2,
        image=back_arrow_img,
        text = '',
        command= lambda: controller.show_frame(main_menu)
        )
        back_arrow.pack(side="left")
        back_arrow.place(x=50, y= 50, anchor=W)

        # Upload Story button, only allows upload of txt and pdf files
        '''upload_text = tk.StringVar()
        upload_btn = customtkinter.CTkButton(
            self,
            textvariable=upload_text,
            command = lambda: upload_file(upload_text,self)

        )''' # need to experiment and see how uploading files should be stored/saved, pickle module might be a good option.
        # placeholder upload button
        upload_btn = customtkinter.CTkButton(
            self,
            width=100,
            height=50,
            border_width=0,
            corner_radius=2,
            text="Add to Library",
            text_font = ("Raleway", 15),
            command = lambda: controller.upload_file("Story")
        )
        
        upload_btn.place(relx=.3, rely=.75, anchor= CENTER)
    
        # Upload Music button, only allows upload of mp3 files
        # placeholder upload music button
        music_upload = customtkinter.CTkButton(
            self,
            width=100,
            height=50,
            border_width=0,
            corner_radius=2,
            text="Add to Music",
            text_font = ("Raleway", 15),
            command = lambda: controller.upload_file("Music")
        )
        music_upload.place(relx=.7,rely=.75,anchor = CENTER)

        # frame that showcases all the songs that are stored
        # currently not working. cant access controller.music_songs.files
        '''song_showcase = Frame(self,width=300,height=400,bg="grey")
        song_showcase.place(relx=.7,rely=.4,anchor=CENTER)
        
        for song in controller.music_songs.files:
            song_btn = customtkinter.CTkButton(
                song_showcase,
                width=300,
                height=25,
                text=song
            )
            song_btn.pack(song_showcase,fill="x")'''
            
        # song_scrollbar = Scrollbar(song_showcase,orient="vertical")
        # song_scrollbar.pack(side="right",fill="y")

class settings_page(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)
        # Top portion of the settings page
        settings_header = Frame(self, width= 1200, height=100, bg="white")
        settings_header.grid(columnspan=3,rowspan=2,row=0)
        settings_label = Label(settings_header, text = "Settings", font = ("Raleway", 32), fg="black", bg="white")
        settings_label.place(relx=.5,rely=.5,anchor=CENTER)
        # Placing button into the top section of settings page
        back_arrow_img = PhotoImage(file="ereadpngs/chevron-left.png")
        back_arrow_img = back_arrow_img.subsample(15)
        
        
        back_arrow = customtkinter.CTkButton(
        settings_header,
        width=50,
        height=30,
        border_width=0,
        corner_radius=2,
        image=back_arrow_img,
        text = '',
        command= lambda: controller.show_frame(main_menu)
        )
        back_arrow.pack(side="left")
        back_arrow.place(x=50, y= 50, anchor=W)


# ereader page currently does NOT work. 
'''
Need to fix getting and inputting book_title, sound, and theme to pass as args into the init for ereader page to work.
'''
class ereader_page(tk.Frame):
    def __init__(self,parent, controller, book_title, sound, theme):
        tk.Frame.__init__(self,parent)
        self.book_title = book_title
        self.sound = sound
        self.theme = theme
        
    
    def sound_switch(self):
        if self.sound == "on":
            self.sound = "off"
        else:
            self.sound = 'on'
        return

    def sound_switch_button(self):
        return

    def get_from_library(self,target_url):
        '''
        This function finds the url to our database in github.
        '''
        response = requests.get(target_url)
        data = response.text
        return(data)

    def music(self,n,song):
        if n == 1:
            pygame.mixer.music.load('ereadmp3/'+song)
            pygame.mixer.music.play(loops=3000)
        else:
            i = 'do nothing'

    def music_player(self,window,title):
        #if title != 'continue':
        #   music(0,title)
        #   return
        if window.counter >= len(audio_map[title]):
            song = prev_song[0]
        else:
            song = audio_map[title].iloc[(window.counter)]
        print(song)
        if self.sound == 'off':
            #do nothing
            sound = 'off'
        elif window.counter == 0:
            prev_song[0] = song
            self.music(1,song)
        elif song != prev_song[0] and window.counter != 0:
            prev_song[0] = song
            self.music(1,song)
        else:
            prev_song[0] = song
            self.music(0,song)
    
    def diction(self,book):
        '''
        Basically this function creates dictionary
        that links the pages of the story with an index number.
        print(diction) will show you what I am referring too.
        '''
        
        diction = {}
        i = 0
        for row in book_library['Title']:
            diction[book_library['Title'][i]] = i
            print(diction)
            i+=1
        index = diction[book]
        # The line below is how the book is found in the dictionary. 
        story = self.get_from_library(target_url = book_library['URL'][index]) 
        if book != "The Raven":
            story = self.split_function(story)
        else:
            print('working')
        final_pages=story.split('---split---') #this is the page splitting decider.
        # We will either need to write a function to change pdfs into txt files
        return final_pages, book
    
    def diction(self,book):
        '''
        Basically this function creates dictionary
        that links the pages of the story with an index number.
        print(diction) will show you what I am referring too.
        '''
        
        diction = {}
        i = 0
        for row in book_library['Title']:
            diction[book_library['Title'][i]] = i
            print(diction)
            i+=1
        index = diction[book]
        # The line below is how the book is found in the dictionary. 
        story = self.get_from_library(target_url = book_library['URL'][index]) 
        if book != "The Raven":
            story = self.split_function(story)
        else:
            print('working')
        final_pages=story.split('---split---') #this is the page splitting decider.
        # We will either need to write a function to change pdfs into txt files
        return final_pages, book


    def pages(self,window,final_pages, forward_back,title):
        '''
        This creates the pages of the tkinter pop up. Currently only works for
        the story Drifting Towards Purpose as the others text files are not formatted
        yet. 
        '''
        #think of adding mp3 call functions based on page here. 
        #Something like mp3_play(window, window.counter, volume_on == true)
        pages_total = len(final_pages)
        if forward_back == "back" and window.counter > 0:
            window.counter -= 1
        if forward_back == "adv" and window.counter != len(final_pages):
            window.counter += 1
        moderator = len(final_pages) <= window.counter
        if moderator == False:
            self.music_player(window,title)
        canvas = Canvas(bg="dark gray", width=595, height=770)
        canvas.place(relx=.5, rely=.5,x=-60,anchor=CENTER)
        canvas.config(highlightthickness=0)
        text = canvas.create_text(30, 20, text=str(window.counter)+'/'+str(pages_total) if moderator == False else self.thanks(window), fill="black", font=('Times 17'),width=510, )
        text = canvas.create_text(300, 400, text=final_pages[window.counter] if moderator == False else self.thanks(window), fill="black", font=('Times 17'),width=530, )

    def thanks(self):
        '''
        Currently the last page of the book. It just prints thank you.
        '''
        self.music(0,'none')
        canvas = Canvas(bg="dark gray", width=595, height=770)
        canvas.place(relx=.5, rely=.5, anchor=CENTER)
        canvas.config(highlightthickness=0)
        text = canvas.create_text(300, 400, text="Thank you For Reading", fill="black", font=('Times 25'),width=430)
        text = canvas.create_text(300, 550, text="Music by Eric Matyas\nwww.soundimage.org", fill="black", font=('Times 18'),width=430)


    def information(self):
        '''
        Information on book
        '''
        canvas = customtkinter.CTkLabel(width=225, height=500,text="Title:\n"+self.book_title+"\nAuthor:\n\nYear:\n\nInfo:\n\n")
        canvas.place(relx=.5, rely=.5,x=465,y=-100, anchor=CENTER)
        canvas.config(highlightthickness=0)

    def music_information(self):
        '''
        Information on song
        '''
        canvas = customtkinter.CTkLabel(width=250, height=80,text="Song Title:\nExample -By: Example")
        canvas.place(relx=.5, rely=.5,x=410,y=230, anchor=CENTER)
        canvas.config(highlightthickness=0)

    def menu_bar(self,window):
        frame_4 = customtkinter.CTkFrame(master=window, width=80, height=500)
        frame_4.place(relx=.5, rely=.5,x=-520, anchor=CENTER)
        frame_4.configure(fg_color=("lightgray"))
        self.library_button(frame_4)
        self.find_button(frame_4)
        self.settings_button(frame_4)
        self.upload_button(frame_4)
    
    def library_return(self):
        None
    def finder(self):
        None
    def settings_link(self):
        None
    def upload_link(self):
        None

    def find_button(self,frame):
        photo = PhotoImage(file = 'ereadpngs/book-research.png')
        btn2 = customtkinter.CTkButton(master = frame, width=200,height=80,border_width=2,fg_color=("white", "lightgray"),
        corner_radius=8,text = '',image = photo,text_color='black',
        command = lambda: self.finder()
        )
        btn2.pack(side="right")
        btn2.place(relx=.5, rely=.5,y=-180, anchor=CENTER)

    def library_button(self,frame):
        photo = PhotoImage(file = 'ereadpngs/binder-file.png')
        btn2 = customtkinter.CTkButton(master = frame,width=200,height=80,border_width=2,fg_color=("white", "lightgray"),
        corner_radius=8,text = '',image = photo,text_color='black',
        command = lambda: self.library_return()
        )
        btn2.pack(side="right")
        btn2.place(relx=.5, rely=.5,y=-60, anchor=CENTER)
    def upload_button(self,frame):
        photo = PhotoImage(file = 'ereadpngs/cloud-upload.png')
        btn2 = customtkinter.CTkButton(master = frame,width=200,height=80,border_width=2,fg_color=("white", "lightgray"),
        corner_radius=8,text = '',image = photo,text_color='black',
        command = lambda: self.upload_link()
        )
        btn2.pack(side="right")
        btn2.place(relx=.5, rely=.5,y=180, anchor=CENTER)

    def settings_button(self,frame):
        photo = PhotoImage(file = 'ereadpngs/settings-gear.png')
        btn2 = customtkinter.CTkButton(master = frame,width=200,height=80,border_width=2,fg_color=("white", "lightgray"),
        corner_radius=8,text = '',image = photo,text_color='black',
        command = lambda: self.settings_link()
        )
        btn2.pack(side="right")
        btn2.place(relx=.5, rely=.5,y=60, anchor=CENTER)
    
    def volume(self):
        return

    def vol_slider(self,window):
        slider = customtkinter.CTkSlider(master=window,
        width=230,
        height=25,
        border_width=5.5,
        from_=0,
        to=100,
        command=self.volume())
        slider.place(relx=0.5, rely=0.5,x=410,y=300, anchor=CENTER)

    def adv_button(self,window,final_pages,title):
        photo = PhotoImage(file = 'ereadpngs/chevron-right.png')
        photo = photo.subsample(15)
        adv = "adv"
        btn2 = customtkinter.CTkButton(
        width=80,
        height=80,
        border_width=0,
        corner_radius=8,
        text = '',
        image = photo,
        text_color='black',
        command = lambda: self.pages(window,final_pages,adv,title)
        )
        btn2.pack(side="right")
        btn2.place(relx=.5, rely=.5,x=290, anchor=CENTER)

    def back_button(self,window,final_pages,title):
        photo = PhotoImage(file = 'ereadpngs/chevron-left.png')
        photo = photo.subsample(15)
        back = "back"
        btn2 = customtkinter.CTkButton(
        width=80,
        height=80,
        border_width=0,
        corner_radius=8,
        text = '',
        image = photo,
        text_color='black',
        command = lambda: self.pages(window,final_pages,back,title)
        )
        btn2.pack(side="right")
        btn2.place(relx=.5, rely=.5,x=-410, anchor=CENTER)

    def split_function(self,story):
        story = story.splitlines(True)
        new_story = ''
        i = 0
        n=0
        for line in story:
            if i == 18:
                new_story += '\n---split--- '
                i=0
            if line == '---chapter---\n':
                new_story += '\n---split---\n '
                i=3
            elif line[-2:] != '\n':
                new_story+=line+' \n'
            else:
                new_story+=line.strip('\n')
            i+=1
            n+=1
        return new_story
    
def main():
    # Main window that pops up
    app = tome_to_read()
    app.title("Tome to Read")
    app.geometry("1200x800")
    app.counter = -1
    '''final_pages, title = ereader_page.diction(ereader_page.book_title)
    ereader_page.vol_slider(app)
    ereader_page.adv_button(app, final_pages, title)
    ereader_page.back_button(app,final_pages, title)
    ereader_page.information()
    ereader_page.music_information()
    ereader_page.menu_bar(app)''' # fix up ereader class
    app.mainloop()
    
    
    
    

if __name__ == "__main__":
    main()