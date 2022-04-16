'''
TITLE: Tome To Read
AUTHORS: James Thomason, Colby Chambers, Sarah Valine, and Cole Dryer
'''

from tkinter import ttk
from tkinter import *
import tkinter as tk
from tkinter.filedialog import askopenfile, askopenfilename
from PIL import Image, ImageTk
import customtkinter
import pandas as pd
import requests
import pygame
import os
import os.path
import time
import sys
import pdfplumber

pygame.mixer.init()
pygame.mixer.music.set_volume(0.5)
channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)
channel3 = pygame.mixer.Channel(2)
bg_music_channel = pygame.mixer.Channel(3)
dark_mode = ["dark slate gray", "slate gray", "slate blue", "light slate blue"]
light_mode = ["color_one", "color_two", "color_three", "color_four"]
tan_mode = ["color_one", "color_two", "color_three", "color_four"]
user_settings = { 'font' : "Times", 'theme' : dark_mode }


url='https://raw.githubusercontent.com/colbychambers25/immersive-ebook/main/Domain_Free_eBook.csv'
book_library = pd.read_csv(url) #print to see what the panda looks like
url= 'https://raw.githubusercontent.com/colbychambers25/immersive-ebook/page_audio_map/Sound_audio_map.csv'
audio_map = pd.read_csv(url)
url= 'https://raw.githubusercontent.com/colbychambers25/immersive-ebook/page_audio_map/soundeffects_map.csv'
sound_effects_map = pd.read_csv(url)
prev_song = ['none']
library_map = {}
volume=50


class story_file:
    '''
    
    '''
    def __init__(self, book_library):
        
        self.userStory = []
        
        # Handling if the user story file already exists within the ereadCSV folder
        if os.path.exists("ereadCSV/tometoread_Stories.csv"):
            df = pd.read_csv("ereadCSV/tometoread_Stories.csv", header=None)
            self.userStory = df
            for index, row in self.userStory.iterrows():
                book_library.loc[len(book_library.index)] = [row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]]

    def set_user_story(self):
        self.userStory = book_library.loc[book_library['Provider'] == "User"]
        
    def save_stories(self):
        self.userStory.to_csv("ereadCSV/tometoread_Stories.csv", header=False,index=False)
        print("Story has been saved to csv file!")
        

class sounds_file:
    def __init__(self):
        self.sounds = []
        self.userSounds = []
        if os.path.exists("ereadCSV/tometoread_sounds.csv"):
            df = pd.read_csv("ereadCSV/tometoread_sounds.csv")
            self.sounds = df['0'].tolist()

        else:
            path = "./ereadSounds"
            self.curdir = os.getcwd()
            os.chdir(path)
            for file in os.listdir():
                if not file.startswith("C:"):
                    self.sounds.append("ereadSounds/" + file)
                else:
                    self.userSounds.append(file)
            self.sounds = self.sounds + self.userSounds
            os.chdir(self.curdir)
            

    def save_sounds(self):
        self.sound_df = pd.DataFrame(self.sounds)

        os.chdir(self.curdir)

        if not os.path.exists("ereadCSV/tometoread_sounds.csv"):
            self.sound_df.to_csv("ereadCSV/tometoread_sounds.csv", header='column_names', index=False)
        else:
            df_check = pd.read_csv('ereadCSV/tometoread_sounds.csv')['0'].tolist()

            self.new_sounds = []
            for sound in self.sounds:
                if sound not in df_check:
                    self.new_sounds.append(sound)
            self.new_sounds_df = pd.DataFrame(self.new_sounds)
            self.new_sounds_df.to_csv("ereadCSV/tometoread_sounds.csv", mode='a', header=False, index=False)
        print("Sound has been saved!")

    def add_sound(self, filename):
        self.sounds.append(filename)
        print("Sound has been added!")
    
class music_file:
    def __init__(self):
        
        self.files = []
        self.userFiles = []
        # checking to see if the tometoread.csv file exists
        # if it exists, reads the file, and appends the name of each song or path to self.files
        if os.path.exists("ereadCSV/tometoread_music.csv"):
            df = pd.read_csv('ereadCSV/tometoread_music.csv')            
            self.files = df['0'].tolist()
            
        else:
            # If tometoread_music.csv does not exist, reads the ereadmp3 folder
            # and grabs all the names and appends them into self.files
            path = "./ereadmp3"
            self.curdir = os.getcwd()
            os.chdir(path)
            for file in os.listdir():
                if not file.startswith("C:"):
                    self.files.append("ereadmp3/" + file)
                else:
                    self.userFiles.append(file)
            self.files = self.files + self.userFiles
            os.chdir(self.curdir)
        
        
    def save_files(self):
        # creates a dataframe from the self.files list
        self.song_dataframe = pd.DataFrame(self.files)

        # changes the directory back into the main folder
        os.chdir(self.curdir)

        # check to see if tometoread.csv exists
        if not os.path.exists("ereadCSV/tometoread_music.csv"):
            self.song_dataframe.to_csv("ereadCSV/tometoread_music.csv", header='column_names', index=False)
        else:
        # If tometoread.csv exists, simply appends the NEWEST contents of self.song_dataframe

            # Making a Dataframe from tometoread_music for checking purposes
            df_check = pd.read_csv('ereadCSV/tometoread_music.csv')['0'].tolist()

            # Loop over each song in self.files
            #   if song not in df_check
            #       add the NEW song into a separate structure
            # Add separate structure into the csv file
            self.new_songs = []
            for song in self.files:
                if song not in df_check:
                    self.new_songs.append(song)
            self.new_songs_df = pd.DataFrame(self.new_songs)
            self.new_songs_df.to_csv('ereadCSV/tometoread_music.csv',mode = 'a', header=False, index= False)
        print("Songs have been saved.")

    def add_file(self,filename):
        self.files.append(filename)
        print("Song has been added!")

class tome_to_read(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        pygame.mixer.music.load("main_bg_music.mp3")
        pygame.mixer.music.play(loops=0)

        tk.Tk.__init__(self, *args, **kwargs)
        
        self.container = tk.Frame(self)

        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight = 1)
        self.container.grid_columnconfigure(0, weight = 1)

        self.frames = {}
        
        for F in (start_page,main_menu, settings_page, upload_page,library_page, Configure, FAQ): 
            frame = F(self.container,self)

            self.frames[F] = frame

            frame.grid(row = 0, column = 0, sticky="nsew")

        self.show_frame(start_page)

    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()
        
    def upload_file(self,type_of_upload):
        if type_of_upload in ["Music","Sound"]:
            file_type = [("Mp3 Files","*.mp3")]
        if type_of_upload == "Story":
            file_type = [("Pdf file","*.pdf"), ("text files","*.txt")]
        file = askopenfile(parent=self,mode="rb", title=f'Choose {type_of_upload} to upload!', filetype=file_type)

        # Handles adding Music files
        if type_of_upload == "Music" and file:
            # do something with the music file 
            music.add_file(file.name)
        
            sound_obj = pygame.mixer.Sound(file)
            pygame.mixer.find_channel().play(sound_obj)
            # pygame.mixer.music.load(file.name)
            # pygame.mixer.music.play(loops=0)
            music.save_files()
        
        # Handles adding Story files !!! NOT DONE NOT DONE NOT DONE NOT DONE !IMPORTANT
        if type_of_upload == "Story" and file:
            self.story.add_story(file)
            self.story.save_files()

        # Handles adding Sound files 
        if type_of_upload == "Sound" and file:
            soundFiles.add_sound(file.name)
            # TESTING PURPOSES
            sound_obj = pygame.mixer.Sound(file)
            pygame.mixer.find_channel().play(sound_obj)
            # ]
            soundFiles.save_sounds()

    def mute_bg_music(self):
        pygame.mixer.music.pause()
    
    def change_font_options_global(self, font_options, var):
        if font_options == "Style":
            self.option_add('*Font', var)
        if font_options == "Size":
            self.option_add('*Font', var)
        
        
class start_page(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)
        img = ImageTk.PhotoImage(Image.open("extra_background.jpg").resize((1200,800)), Image.ANTIALIAS)
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

        instructions = customtkinter.CTkButton(self, text="Click here to begin!", text_font=("Raleway", 32), command=lambda: controller.show_frame(main_menu), corner_radius=3)
        instructions.place(relx=.55,rely=.95, anchor= S)

# Music is supposed to play when this screen is shown, 
class main_menu(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)        
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
            text="Library",
            text_font = ("Raleway", 15),
            command = lambda: controller.show_frame(library_page)
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

        configure_button = customtkinter.CTkButton(
            self,
            width=100, height = 50,
            border_width=0, corner_radius=2,
            text="Configure Books",
            text_font = ("Raleway",15),
            command = lambda: controller.show_frame(Configure)
        )
        configure_button.pack(anchor=CENTER)
        configure_button.place(relx=.5,rely=.85,anchor=CENTER)

        faq_btn = customtkinter.CTkButton(
            self,
            width=100,height=25,
            border_width=0,
            corner_radius=2,
            text="FAQ",
            text_font = ("Raleway",12),
            command = lambda: controller.show_frame(FAQ)
        )
        faq_btn.pack(anchor=CENTER)
        faq_btn.place(relx=.5,rely=.925,anchor=CENTER)

        # logo in main menu
        logo = Image.open("TomeToRead_Logo.png")
        logo = logo.resize((350,380))
        logo = ImageTk.PhotoImage(logo)
        logo_label = Label(self,image=logo)
        logo_label.image = logo
        logo_label.place(relx=.5, rely=.3, anchor= CENTER)

        mute_btn = customtkinter.CTkButton(
            self,
            width=25,
            height=25,
            border_width=0,
            corner_radius=2,
            text="Mute Music",
            command = lambda: controller.mute_bg_music()
        )
        mute_btn.place(relx=0,rely=.97)

class upload_page(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)
        # top portion of the user upload page
        upload_header = Frame(self, width = 10000, height = 100, bg = "white")
        upload_header.grid(columnspan=3,rowspan=2,row=0)
        upload_label = Label(self, text = "Add in your own story, music, or sound!", font = ("Raleway", 32), fg="black", bg="white")
        upload_label.place(relx=.5,y=50,anchor=CENTER)
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

        # upload story button
        upload_btn = customtkinter.CTkButton(
            self,
            width=100,
            height=50,
            border_width=0,
            corner_radius=2,
            text="Add to Library",
            text_font = ("Raleway", 15),
            command = lambda: self.submit_story(self.story_file_path,self.cover_image_path)
        )

        self.author_var = tk.StringVar()
        self.year_pub_var = tk.StringVar()
        self.genre_var = tk.StringVar()
        self.book_title = tk.StringVar()

        title_entry = Entry(self,textvariable=self.book_title)
        title_entry.place(relx=.25,rely=.15)
        title_label = Label(self,text="Title:",font=("Raleway",10))
        title_label.place(relx=.21,rely=.15)


        author_entry = Entry(self, textvariable=self.author_var)
        author_entry.place(relx=.25,rely=.2)
        author_entry_label = Label(self,text="Author:", font=("Raleway",10))
        author_entry_label.place(relx=.2,rely=.2)

        year_published_entry = Entry(self, textvariable=self.year_pub_var)
        year_published_entry.place(relx=.25,rely=.25)
        year_published_label = Label(self,text="Year Published:", font=("Raleway",10))
        year_published_label.place(relx=.16,rely=.25)

        genre_entry = Entry(self, textvariable=self.genre_var)
        genre_entry.place(relx=.25,rely=.3)
        genre_entry_label = Label(self, text="Genre:", font=("Raleway", 10))
        genre_entry_label.place(relx=.2, rely=.3)

        self.cover_image_path = "None Given"
        self.story_file_path = "fileCheck"

        cover_image_upload = customtkinter.CTkButton(
            self,
            width=100,
            height=25,
            border_width=0,
            corner_radius=2,
            text="Add Book Cover",
            command = lambda: self.upload_book_cover()
        )
        cover_image_upload.place(relx=.25,rely=.35)
        
        actual_book_upload = customtkinter.CTkButton(
            self,
            width=100,
            height=25,
            border_width=0,
            corner_radius=2,
            text="Add Story File",
            command = lambda : self.add_story()
        )
        actual_book_upload.place(relx=.255,rely=.42)

        upload_btn.place(relx=.3, rely=.53, anchor= CENTER)
    
        # Upload Music button, only allows upload of mp3 files
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
        music_upload.place(relx=.7,rely=.53,anchor = CENTER)

        # Upload Sound button, only allows upload of mp3 files
        sound_upload = customtkinter.CTkButton(
            self,
            width=100,
            height=50,
            border_width=0,
            corner_radius=2,
            text="Add to Sounds",
            text_font = ("Raleway", 15),
            command = lambda: controller.upload_file("Sound")
        )
        sound_upload.place(relx=.5,rely=.53,anchor=CENTER)

        # frame that showcases all the songs that are stored
        all_songs = Label(self,font=("Raleway",16), text = "All Songs", anchor=CENTER)
        all_songs.place(relx=.66,rely=.15)
        self.songlistbox = Listbox(self,width=25,height=10,background="light grey", selectmode=BROWSE)
        self.songlistbox.place(relx=.7,rely=.3,anchor=CENTER)
        for i, song in enumerate(music.files):
            self.songlistbox.insert(i,song)

        all_sounds = Label(self,font=("Raleway",16), text="All Sounds", anchor=CENTER)
        all_sounds.place(relx=.45, rely=.15)
        self.soundlistbox = Listbox(self,width=25, height= 10, background="light grey", selectmode=BROWSE)
        self.soundlistbox.place(relx=.5,rely=.3, anchor=CENTER)
        for i,song in enumerate(soundFiles.sounds):
            self.soundlistbox.insert(i,song)

        preview_song_btn = customtkinter.CTkButton(
            self,
            width=100,
            height=25,
            border_width=0,
            corner_radius=2,
            text="Preview Song",
            command = lambda: self.preview_sound_song_file("Song")
        )
        preview_song_btn.place(relx=.655,rely=.6)

        preview_sound_btn = customtkinter.CTkButton(
            self,
            width=100,
            height=25,
            border_width=0,
            corner_radius=2,
            text="Preview Sound",
            command = lambda: self.preview_sound_song_file("Sound")
        )
        preview_sound_btn.place(relx=.455,rely=.6)

        mute_btn = customtkinter.CTkButton(
            self,
            width=25,
            height=25,
            border_width=0,
            corner_radius=2,
            text="Mute Music",
            command = lambda: controller.mute_bg_music()
        )
        mute_btn.place(relx=0,rely=.97)

    def upload_book_cover(self):
        book_cover = askopenfilename(filetypes=[('image files','.png'),('image files','.jpg')])

        if book_cover:
            self.cover_image_path = book_cover
            cover_success = Label(self, text="Success!", font=("Raleway",10))
            cover_success.place(relx=.27,rely=.385)
            print(f'New Book Cover is: {self.cover_image_path}')

    def add_story(self):
        storyfile = askopenfilename(filetypes=(("text files", '.txt'),("text files",'.pdf')))
        if storyfile:
            self.story_file_path = storyfile
            story_success = Label(self,text="Success!", font=("Raleway",10))
            story_success.place(relx=.27,rely=.455)
            print(f'New Story is: {self.story_file_path}')
    
    def submit_story(self,book_path="fileCheck",book_cover="None Given"):
        if book_path == "fileCheck":
            story_add_success_or_fail = Label(self, text="Please upload a story file to add new story.", font=("Raleway", 10), fg="red")
            story_add_success_or_fail.place(relx=.2,rely=.58)
        else:
            if book_cover == "None Given":
                book_cover = "ereadpngs/tome2.png"
            provider = "User"
            views = 0
            print(book_path) 
            title = self.book_title.get()
            author = self.author_var.get()
            year = self.year_pub_var.get()
            genre = self.genre_var.get()
            # add new row with information
            book_library.loc[len(book_library.index)] = [book_path,title,author,year, provider, views, genre, book_cover]
            story_add_success_or_fail = Label(self,text="Story has been added!", font=("Raleway",10))
            story_add_success_or_fail.place(relx=.22,rely=.58)
            # make call to update library page with new book
            stories.set_user_story()
            stories.save_stories()

    def preview_sound_song_file(self,song_or_sound):
        if song_or_sound == "Song":
            song = self.songlistbox.get(self.songlistbox.curselection())
            song_Sound_obj = pygame.mixer.Sound(song)
            channel3.play(song_Sound_obj)
        if song_or_sound == "Sound":
            sound = self.soundlistbox.get(self.soundlistbox.curselection())
            ttr_sound_Sound_obj = pygame.mixer.Sound(sound)
            channel3.play(ttr_sound_Sound_obj)
        
        
class settings_page(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)
        # Top portion of the settings page
        settings_header = Frame(self, width= 10000, height=100, bg="white")
        settings_header.grid(columnspan=3,rowspan=2,row=0)
        settings_label = Label(self, text = "Settings", font = ("Raleway", 32), fg="black", bg="white")
        settings_label.place(relx=.5,y=50,anchor=CENTER)
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
        

        # sec1 frame
        sec1 = Frame(self,width=585,height=70,bg='white')
        sec1.place(relx=.5,rely=.2,anchor=N)

        # labels
        interface_lbl = Label(sec1, text="Interface Settings",font=("Raleway", 14), fg="black",bg="white")
        interface_lbl.place(relx=.5,rely=.2,anchor=CENTER)
        light_dark_lbl = Label(sec1, text="Interface Style:", font=("Raleway",12), fg="black",bg="white")
        light_dark_lbl.place(relx=.2,rely=.7,anchor=CENTER)

        # sec2 frame
        sec2 = Frame(self,width=585,height=225,bg="white")
        sec2.place(relx=.5,rely=.4,anchor=N)

        volume_lbl = Label(sec2, text="Volume Settings", font = ("Raleway", 14), fg="black", bg="white")
        volume_lbl.place(relx=.5, rely=.1,anchor=CENTER)
        music_lbl = Label(sec2, text="Music:", font = ("Raleway", 12), fg="black", bg="white")
        music_lbl.place(relx=.23, rely=.4,anchor=CENTER)
        soundfx_lbl = Label(sec2, text="Sound FX:", font = ("Raleway", 12), fg="black", bg="white")
        soundfx_lbl.place(relx=.2, rely=.6,anchor=CENTER)

        # sec3 frame
        sec3= Frame(self,width= 585, height=225, bg="white")
        sec3.place(relx=.5,rely=.75, anchor=N)


        font_lbl = Label(sec3, text="Font Settings:", font = ("Raleway", 14), fg="black", bg="white")
        font_lbl.place(relx=.5, rely=.1,anchor=CENTER)
        fstyle_lbl = Label(sec3, text="Font Style:", font = ("Raleway", 12), fg="black", bg="white")
        fstyle_lbl.place(relx=.2, rely=.4,anchor=CENTER)
        fsize_lbl = Label(sec3, text="Font Size:", font = ("Raleway", 12), fg="black", bg="white")
        fsize_lbl.place(relx=.2, rely=.6,anchor=CENTER)
        
        fstyle_value_inside = StringVar()
        fstyle_value_inside.set("Select an Option")
        fstyle_options = ["Arial","Lato","MS Sans Serif","Times New Roman","Courier", "Raleway"]
        fstyle_dropdown = ttk.Combobox(sec3, textvariable = fstyle_value_inside)
        fstyle_dropdown['values'] = fstyle_options
        fstyle_dropdown.place(relx=.37,rely=.365)
        fstyle_set_btn = customtkinter.CTkButton(
            sec3,
            width=25,height=25,
            border_width=0,
            corner_radius=2,
            command = lambda: controller.change_font_options_global("Style",fstyle_dropdown.get()),
            text="Set"
        )
        fstyle_set_btn.place(relx=.65,rely=.36)

        font_size_inside = StringVar()
        font_size_inside.set("Select an Option")
        font_size_options = [10,12,14,16,18,20]
        font_size_dropdown = ttk.Combobox(sec3, textvariable=font_size_inside)
        font_size_dropdown['values'] = font_size_options
        font_size_dropdown.place(relx=.37,rely=.565)
        font_size_btn = customtkinter.CTkButton(
            sec3,
            width=25,height=25,
            border_width=0, corner_radius=2,
            command = lambda: controller.change_font_options_global("Size", font_size_dropdown.get()),
            text="Set"
        )
        font_size_btn.place(relx=.65,rely=.56)

        mute_btn = customtkinter.CTkButton(
            self,
            width=25,
            height=25,
            border_width=0,
            corner_radius=2,
            text="Mute Music",
            command = lambda: controller.mute_bg_music()
        )
        mute_btn.place(relx=0,rely=.97)

class library_page(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)
        # Top portion of the settings page
        library_header = Frame(self, bg="white", width=1200,height=100)
        library_label = Label(library_header, text = "Library", font = ("Raleway", 32), fg="black", bg="white")
        library_label.pack(anchor=CENTER,fill="none",expand=False)
        library_label.place(relx=.5,y=50,anchor=CENTER)
        back_arrow_img = PhotoImage(file="ereadpngs/chevron-left.png")
        back_arrow_img = back_arrow_img.subsample(15)

        refresh_img = PhotoImage(file="ereadpngs/refresh_.png")

        back_arrow = customtkinter.CTkButton(
        library_header,
        width=50,
        height=50,
        border_width=0,
        corner_radius=2,
        image=back_arrow_img,
        text = '',
        command= lambda: controller.show_frame(main_menu)
        )
        back_arrow.pack(side=LEFT,expand=False,pady=25,padx=25)
        library_header.pack(fill=BOTH)

        to_configure = customtkinter.CTkButton(
            library_header,
            width=55,height=50,
            border_width=0, corner_radius=2,
            text="Configure Books",
            command = lambda: controller.show_frame(Configure)
        )
        to_configure.pack(side=LEFT,expand=False,pady=25,padx=10)
        
        refresh_button = customtkinter.CTkButton(
            library_header,
            width = 50,
            height = 50,
            border_width=0,
            corner_radius=2,
            image=refresh_img,
            text='',
            command = lambda: self.render_books()
        )
        refresh_button.pack(side=RIGHT, expand=False,pady=25,padx=25)


        # Creating the canvas
        self.scrollable_canvas = Canvas(self)
        self.scrollable_canvas.config(width=950, height = 4000)
        self.scrollable_canvas.place(relx=.5)
        self.scrollable_canvas.pack(side=LEFT,fill="y",expand=1)

        # Creating a scrollbar
        library_scrollbar = Scrollbar(self, orient = VERTICAL, command = self.scrollable_canvas.yview)
        library_scrollbar.pack(side = RIGHT, fill = Y)

        # Configuring Canvas with scrollbar
        self.scrollable_canvas.configure(yscrollcommand=library_scrollbar.set)

        # Binding configure
        self.scrollable_canvas.bind('<Configure>', lambda e: self.scrollable_canvas.configure(scrollregion = self.scrollable_canvas.bbox("all")))

        # Creating another frame inside canvas
        self.canvas_frame = Frame(self.scrollable_canvas)
        self.canvas_frame.bind("<Configure>", self.reset_scrollregion)

        # adding new frame to window in canvas
        self.scrollable_canvas.create_window((0,125), window=self.canvas_frame, anchor="nw")

        # Renders all books into the canvas
        
        self.render_books()

        mute_btn = customtkinter.CTkButton(
            self,
            width=25,
            height=25,
            border_width=0,
            corner_radius=2,
            text="Mute Music",
            command = lambda: controller.mute_bg_music()
        )
        mute_btn.place(relx=0,rely=.97)
    
    def reset_scrollregion(self, event):
        self.scrollable_canvas.configure(scrollregion=self.scrollable_canvas.bbox("all"))

    def action(self, item):
        temp = book_library.loc[book_library['Title'] == item]
        #temp['Cover'].item()
        logo = Image.open(temp['Cover'].item())
        logo = logo.resize((170,280))
        logo = ImageTk.PhotoImage(logo)
            
        return customtkinter.CTkButton(self.canvas_frame, width=200,height=300,border_width=2, 
        corner_radius=8,image = logo, text = '',command = lambda: self.func(item), fg_color = "gray"
        )
    def name(self, item):
        return customtkinter.CTkLabel(self.canvas_frame, width=196, height=30,text=item, text_font= ("Railway",12),corner_radius=0,fg_color='gray')

    def func(self, item):
        create_book(item,'on','',self.scrollable_canvas)

    def render_books(self):
        rows = 0
        columns = 0
        col_adv = 0
        for i, item  in enumerate(book_library['Title']):
            b = self.action(item)
            c = self.name(item)
                #create_book(item,'on','',tk.Frame)
                #btn2.pack(side="right")
                # if line % 5 == 0:
                
                # First 3 buttons should be placed in (0,0),(0,1),(0,2)
            b.grid(row = rows, column = columns, padx = 20, pady = 10)

            c.grid(row = rows, column = columns)
                # Then condition hits and then the next set of buttons should be placed in 
                # (1,0),(1,1),(1,2), and so forth for every 3 or 4 buttons
            print("("+str(rows)+","+str(columns)+")")
            if columns % 3 == 0 and columns > 0:
                rows += 1
                columns=-1
            if columns != 3:
                columns+=1

    def refresh_library(self):
        self.render_books() 

class Configure(tk.Frame):

    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)
        self.all_books_in_df = book_library["Title"].tolist() # getting all book names in book_library df so we can display it for configuring
        configure_header = Frame(self, bg="white", width=1200,height=100)
        configure_label = Label(configure_header, text = "Configure Books", font = ("Raleway", 32), fg="black", bg="white")
        configure_label.pack(anchor=CENTER,fill="none",expand=False)
        configure_label.place(relx=.5,y=50,anchor=CENTER)
        
        to_library = customtkinter.CTkButton(
            configure_header,
            width=50,
            height=50,
            border_width=0,
            corner_radius=2,
            text = 'To Library',
            command= lambda: controller.show_frame(library_page)
        )
        to_library.pack(side=LEFT,expand=False,pady=25,padx=10)

        to_main = customtkinter.CTkButton(
            configure_header,
            width=50,height=50,
            border_width=0,
            corner_radius=2,
            text = 'To Main Menu',
            command = lambda: controller.show_frame(main_menu)
        )
        to_main.pack(side=LEFT,expand=False,pady=25,padx=10)

        configure_header.pack(fill=BOTH)
        

        mute_btn = customtkinter.CTkButton(
            self,
            width=25,
            height=25,
            border_width=0,
            corner_radius=2,
            text="Mute Music",
            command = lambda: controller.mute_bg_music()
        )
        mute_btn.place(relx=0,rely=.97)

class FAQ(tk.Frame):

     def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)
        faq_header = Frame(self, bg="white", width=1200,height=100)
        faq_label = Label(faq_header, text = "Frequently Asked Questions", font = ("Raleway", 32), fg="black", bg="white")
        faq_label.pack(anchor=CENTER,fill="none",expand=False)
        faq_label.place(relx=.5,y=50,anchor=CENTER)

        back_arrow_img = PhotoImage(file="ereadpngs/chevron-left.png")
        back_arrow_img = back_arrow_img.subsample(15)
        
        
        back_arrow = customtkinter.CTkButton(
        faq_header,
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

        faq_header.pack(fill=BOTH)


        mute_btn = customtkinter.CTkButton(
            self,
            width=25,
            height=25,
            border_width=0,
            corner_radius=2,
            text="Mute Music",
            command = lambda: controller.mute_bg_music()
        )
        mute_btn.place(relx=0,rely=.97)



class Book:
    def __init__(self,book_title, sound,theme,window):
        #self.window = window
        self.window = window
        self.book_title = book_title
        self.sound = sound
        self.theme = theme
        self.status = 'play'
        self.frame_4_1 =None
        self.frame_4 = None
        self.frame_3 = None
        self.canvas = None
        self.canvas_2 = None
        self.canvas_3 = None
        self.info = None
        self.music_info = None
        self.advbutton = None
        self.backbutton = None
        self.mute = None
        self.volup = None
        self.slider = None
        self.search_button = None
        self.search_directions = None
        self.bookmark1 = None
        self.bookmark2 = None
        if __name__ == "__main__":
            self.main_book_run()

    def sound_switch(self,var):
        if var == "off":
            self.sound = var
            channel2.pause()
            channel1.pause()
        elif var == 'on':
            self.sound = var
            channel2.unpause()
            channel1.unpause()
        return

    def sound_switch_button(self):
        photo = PhotoImage(file = 'ereadpngs/mute.png')
        btn2 = customtkinter.CTkButton( width=45,height=45,border_width=0, 
        corner_radius=8,text = '',image = photo,text_color='black', fg_color=user_settings["theme"][2],
        command = lambda: self.sound_switch('off')
        )
        self.mute = btn2
        btn2.pack(side="right")
        btn2.place(relx=.5, rely=.5,y=300,x=270, anchor=CENTER)
        return
    
    def sound_switch_button2(self):
        photo = PhotoImage(file = 'ereadpngs/volume.png')
        btn2 = customtkinter.CTkButton( width=45,height=45,border_width=0,
        corner_radius=8,text = '',image = photo,text_color='black',fg_color=user_settings["theme"][2],
        command = lambda: self.sound_switch('on')
        )
        self.volup = btn2
        btn2.pack(side="right")
        btn2.place(relx=.5, rely=.5,y=300,x=550, anchor=CENTER)
        return

    def get_from_library(self,file_url,target_url):
        '''
        This function finds the url to our database in github.
        '''
        if file_url == "file":
            response  = open(target_url,encoding="utf-8")
            #read whole file to a string
            data = response.read()
            
            response.close()   
        else:
            response = requests.get(target_url)
            data = response.text
        return(data)

    def read_user_story(self, file_path): # !IMPORTANT
        # ask rich if he knows how to process pdf files or txt files. How can we know when there is a next page, especially for pdf files, Important for reading pdf files.
        # semi works
        processed = []
        extracted = []
        pdf_str = ''
        if file_path[-4:] == ".pdf":
            pdf = pdfplumber.open(file_path)
            for i in range(len(pdf.pages)):
                processed.append(pdf.pages[i])
            for page in processed:
                pdf_str += page.extract_text()
            return pdf_str
        

    def music(self,n,song):
        if n == 1:
            song = pygame.mixer.Sound('ereadmp3/'+song)
            channel1.play(song,loops=3000)
        elif self.status == "paused":
            channel1.unpause()
        else:
            i = 'do nothing'

    def sound_effects(self,n,sound):
        if n == 1:
            song = pygame.mixer.Sound('ereadSounds/'+sound)
            song.set_volume(.2)
            channel2.play(song,loops=0)
        elif self.status == "paused":
            channel2.unpause()
        else:
            i = 'do nothing'


    def music_player(self,window,title):
        #if title != 'continue':
        #   music(0,title)
        #   return
        if title in audio_map:
            if window.counter >= len(audio_map[title]):
                song = prev_song[0]
            else:
                song = audio_map[title].iloc[(window.counter)]
        else:
            song = audio_map["The Raven"][1]
            
        if title in sound_effects_map.columns and window.counter < len(sound_effects_map[title]) and  sound_effects_map[title].iloc[(window.counter)] != 'None':
            print(sound_effects_map[title].iloc[(window.counter)])
            self.sound_effects(1,sound_effects_map[title].iloc[(window.counter)])
        print(song)
        if self.sound == 'off':
            #do nothing
            self.status = 'paused'
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
        # The line below is how the book is found in the dictionary. vl
        if book_library['URL'][index][0] == 'h':
            story = self.get_from_library('url',target_url = book_library['URL'][index]) 
        elif book_library['URL'][index][-1] == 't':
            story = self.get_from_library('file',target_url = book_library['URL'][index]) 
        elif book_library['URL'][index][-1] == 'f':                                                                                                                                                                                                                   
            story = self.read_user_story(book_library['URL'][index])
            
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
        channel2.fadeout(5)
        print(self.sound)
        pages_total = len(final_pages)
        if forward_back == "back" and window.counter > 0:
            window.counter -= 1
        if forward_back == "adv" and window.counter != len(final_pages):
            window.counter += 1
        moderator = len(final_pages) <= window.counter
        if moderator == False:
            self.music_player(window,title)
        if self.canvas_2 != None:
            self.canvas_2.destroy()
        self.canvas_2 = Canvas(bg=user_settings["theme"][1], width=595, height=770)
        self.canvas_2.place(relx=.5, rely=.5,x=-60,anchor=CENTER)
        self.canvas_2.config(highlightthickness=0)
        self.music_information(window)
        self.information(pages_total)
        text = self.canvas_2.create_text(30, 20, text=str(window.counter) if moderator == False else self.thanks(), fill="black", font=('Times 16'),width=540, )
        text = self.canvas_2.create_text(300, 400, text=final_pages[window.counter] if moderator == False else self.thanks(), fill="black", font=('Times 16'),width=540, anchor=CENTER)

    def thanks(self):
        '''
        Currently the last page of the book. It just prints thank you.
        '''
        self.music(0,'none')
        if self.canvas_3 != None:
            self.canvas_3.destroy()
        self.canvas_3 = Canvas(bg=user_settings["theme"][1], width=595, height=770)
        self.canvas_3.place(relx=.5, rely=.5,x=-60, anchor=CENTER)
        self.canvas_3.config(highlightthickness=0)
        text = self.canvas_3.create_text(300, 400, text="Thank you For Reading", fill="black", font=('Times 25'),width=430)
        text = self.canvas_3.create_text(300, 550, text="Music by Eric Matyas\nwww.soundimage.org", fill="black", font=('Times 18'),width=430)


    def information(self,pages_total):
        '''
        Information on book
        '''
        temp = book_library.loc[book_library['Title'] == self.book_title]
        #temp['Cover'].item()
        if self.info!= None:
            self.info.destroy()
        self.info = customtkinter.CTkLabel(width=225, height=500,text_color='black',text="Title:\n"+self.book_title+"\n\nAuthor:\n"+temp['Author'].item()+"\n\nYear:\n"+ str(temp['Year Published'].item())+"\n\nGenre:\n"+str(temp['Genre'].item())+"\n\n"+"Page Count: \n"+str(pages_total), text_font= ("Railway",14),fg_color=user_settings["theme"][1])
        self.info.place(relx=.5, rely=.5,x=465,y=-100, anchor=CENTER)
        self.info.config(highlightthickness=0,)

    def music_information(self,window):
        '''
        Information on song
        '''
        title = self.book_title
        if title in audio_map:
            if window.counter >= len(audio_map[title]):
                song = prev_song[0]
            else:
                song = audio_map[title].iloc[(window.counter)]
        else:
            song = audio_map["The Raven"][1]
        if self.music_info != None:
            self.music_info.destroy()
        self.music_info = customtkinter.CTkLabel(width=280, height=80,text_color='black',text="Song Title: "+song+"\nBy: Eric Matyas\nwww.soundimage.org",fg_color=user_settings["theme"][1])
        self.music_info.place(relx=.5, rely=.5,x=410,y=230, anchor=CENTER)
        self.music_info.config(highlightthickness=0)

    def menu_bar(self,window,final_pages):
        frame_4 = customtkinter.CTkFrame(width=80, height=500,fg_color=user_settings["theme"][1])
        frame_4.place(rely=.5, anchor=W)
        frame_4.configure()
        self.library_button(frame_4)
        self.find_button(frame_4,window,final_pages)
        self.settings_button(frame_4,window)
        self.upload_button(frame_4)
        frame_4.tkraise()
        self.frame_4_1 = frame_4
    
    def library_return(self):
        self.mute.destroy()
        self.volup.destroy()
        self.slider.destroy()
        self.advbutton.destroy()
        self.backbutton.destroy()
        self.frame_3.destroy()
        self.frame_4.destroy()
        self.canvas.destroy()
        self.frame_4_1.destroy()
        if self.canvas_2 != None:
            self.canvas_2.destroy()
        if self.info != None:
            self.info.destroy()
        if self.music_info != None:
            self.music_info.destroy()
        if self.canvas_3 != None:
            self.canvas_3.destroy()
        if self.search_button != None:
            self.search_button.destroy()
        if self.search_directions != None:
            self.search_directions.destroy()
        if self.bookmark1 != None:
            self.bookmark1.destroy()
        if self.bookmark2 != None:
            self.bookmark2.destroy()
        channel1.stop()
        channel2.stop()

    def finder(self,window,final_pages):
        if self.search_button != None:
                self.search_button.destroy()
        if self.search_directions != None:
            self.search_directions.destroy()
        self.page_name = tk.IntVar()
        title_entry = Entry(window,width=3, textvariable= self.page_name)
        directions = Label(text="Select the go button\nto jump.", font=("Raleway",10))
        title_entry.pack(side="right")
        title_entry.place(relx=.5, rely=.5,x= -480, y=-180, anchor=CENTER)
        directions.place(relx=.5, rely=.5,x= -450, y=-210, anchor=CENTER)
        btn = customtkinter.CTkButton(width=40,height=20,border_width=2,fg_color=("white", user_settings["theme"][1]),
        corner_radius=8,text = 'Go',text_color='black',
        command = lambda: self.page_jump(title_entry,window,final_pages) 
        )
        self.search_button = btn
        self.search_directions= directions
        btn.place(relx=.5, rely=.5,x= -420, y=-180, anchor=CENTER)
        print(title_entry.get())
        #window.counter = int(title_entry.get())

    def page_jump(self, val, window,final_pages):
        window.counter = int(val.get())-1
        adv = 'adv'
        self.pages(window,final_pages,adv,self.book_title)
        

    def settings_link(self,window):
        if self.bookmark1 != None:
            self.bookmark1.destroy()
        if self.bookmark2 != None:
            self.bookmark2.destroy()
        df = pd.read_csv('ereadbookmarks/bookmarks.csv')
        if self.book_title in df.columns:
            directions2 = Label(text="You left off on page "+str(df.iloc[0][self.book_title].item())+'.', font=("Raleway",10))
            directions2.place(relx=.5, rely=.5,x= -440, y=60, anchor=CENTER)
        df[self.book_title] = window.counter
        #df = df.to_csv(index=False)
        #os.makedirs('/ereadbookmarks', exist_ok=True)  
        df.to_csv('ereadbookmarks/bookmarks.csv') 
        
        directions1 = Label(text="Page "+str(df.iloc[0][self.book_title].item())+" Bookmarked!", font=("Raleway",10))
        directions1.place(relx=.5, rely=.5,x= -440, y=80, anchor=CENTER)
        self.bookmark2 = directions1
        self.bookmark1= directions2


        
    def upload_link(self):
        exit()

    def find_button(self,frame,window,final_pages):
        photo = PhotoImage(file = 'ereadpngs/book-research.png')
        btn2 = customtkinter.CTkButton(master = frame, width=200,height=80,border_width=2,fg_color=("white", user_settings["theme"][1]),
        corner_radius=8,text = '',image = photo,text_color='black',
        command = lambda: self.finder(window,final_pages)
        )
        btn2.pack(side="right")
        btn2.place(relx=.5, rely=.5,y=-180, anchor=CENTER)

    def library_button(self,frame):
        photo = PhotoImage(file = 'ereadpngs/home.png')
        btn2 = customtkinter.CTkButton(master = frame,width=200,height=80,border_width=2,fg_color=("white", user_settings["theme"][1]),
        corner_radius=8,text = '',image = photo,text_color='black',
        command = lambda: self.library_return()
        )
        btn2.pack(side="right")
        btn2.place(relx=.5, rely=.5,y=-60, anchor=CENTER)

    def upload_button(self,frame):
        photo = PhotoImage(file = 'ereadpngs/exit.png')
        btn2 = customtkinter.CTkButton(master = frame,width=200,height=80,border_width=2,fg_color=("white", user_settings["theme"][1]),
        corner_radius=8,text = '',image = photo,text_color='black',
        command = lambda: self.upload_link()
        )
        btn2.pack(side="right")
        btn2.place(relx=.5, rely=.5,y=180, anchor=CENTER)

    def settings_button(self,frame,window):
        photo = PhotoImage(file = 'ereadpngs/bookmark.png')
        btn2 = customtkinter.CTkButton(master = frame,width=200,height=80,border_width=2,fg_color=("white", user_settings["theme"][1]),
        corner_radius=8,text = '',image = photo,text_color='black',
        command = lambda: self.settings_link(window)
        )
        btn2.pack(side="right")
        btn2.place(relx=.5, rely=.5,y=60, anchor=CENTER)
    
    
    def vol_slider(self,window):
        def volume(self):
            val = round(slider.get()/100,1)
            print(val)
            channel1.set_volume(val)
            channel2.set_volume(val)
            return

        slider = customtkinter.CTkSlider(
        width=230,
        height=25,
        border_width=5.5,
        from_=0,
        to=100,
        fg_color=user_settings["theme"][2],
        button_color=user_settings["theme"][1],
        command=volume)
        self.slider = slider
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
        fg_color=user_settings["theme"][2],
        border_color="dark slate gray",
        command = lambda: self.pages(window,final_pages,adv,title)
        )
        self.advbutton = btn2
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
        fg_color=user_settings["theme"][2],
        text = '',
        image = photo,
        text_color='black',
        command = lambda: self.pages(window,final_pages,back,title)
        )
        self.backbutton = btn2
        btn2.pack(side="right")
        btn2.place(relx=.5, rely=.5,x=-410, anchor=CENTER)

    def split_function(self,story):
        story = story.splitlines(True)
        if len(story[1]) > 20:
            print('got it')
            new_story = ''
            i = 0
            n=0
            for line in story:
                i = 0
                for word in line.split(' '):
                    if i == 11:
                        new_story += '\n'
                        i=0
                    else:
                        new_story+=word+' '
                    i+=1
            story = new_story.splitlines()

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

    def main_book_run(self):
        ''' 
        Creates the window, and calls this diction function to get a key value pair linked by page number.
        Currently only supports .txt files because pdf files lack the functionality 
        to be manipulated and most domain stories use .txt or .epub not pdf.
        '''
        frame_3 = Frame(width=10000, height=10000)
        frame_3.place(relx=.5, rely=.5, anchor=CENTER)
        frame_3.configure()
        frame_3.tkraise()
        self.frame_3 = frame_3
        frame_4 = Frame(width=1200, height=800)
        frame_4.place(relx=.5, rely=.5, anchor=CENTER)
        frame_4.configure()
        frame_4.tkraise()
        #customtkinter.set_default_color_theme("darkblue")
        
        self.frame_4 = frame_4
        window = frame_4
        window.counter = -1 #this is universal counter funtion that allows a user to traverse a story.
        pygame.mixer.music.pause()
        final_pages, title = self.diction(self.book_title)
        self.vol_slider(window)
        self.adv_button(window, final_pages, title)
        self.back_button(window, final_pages, title) 
        self.sound_switch_button()
        self.sound_switch_button2()
        self.music(0,'none')
        self.canvas = Canvas(bg="dark gray", width=595, height=770)
        self.canvas.place(relx=.5, rely=.5,x=-60, anchor=CENTER)
        self.canvas.config(highlightthickness=0)
        temp = book_library.loc[book_library['Title'] == self.book_title]
        logo = Image.open(temp['Cover'].item())
        logo = logo.resize((595,770))
        logo = ImageTk.PhotoImage(logo)
        logo_label = Label(self.canvas,image=logo)
        logo_label.image = logo
        logo_label.place(relx=.5, rely=.5, anchor= CENTER)
        #canvas.create_text(300, 400, text="Good Luck On Your Fictional Journey!", fill="white", font=('Times 25'),width=430)
        #canvas.create_text(300, 550, text="Music by Eric Matyas\nwww.soundimage.org", fill="white", font=('Times 10'),width=430)
        self.menu_bar(window,final_pages)
        #window.mainloop() #basically refreshes the window


def create_book(title,two,three,frame):
    Book(title,two,three,frame)

music = music_file()
stories = story_file(book_library)
soundFiles = sounds_file()

def main():
    # Main window that pops up
    app = tome_to_read()
    app.title("Tome to Read")
    app.resizable(False,False)
    app.geometry("1200x800")
    app.counter = -1
    '''final_pages, title = ereader_page.diction(ereader_page.book_title)
    ereader_page.vol_slider(app)
    ereader_page.adv_button(app, final_pages, title)
    ereader_page.back_button(app,final_pages, title)
    ereader_page.information()
    ereader_page.music_information()
    ereader_page.menu_bar(app)''' 
    app.mainloop()
    
if __name__ == "__main__":
    main()