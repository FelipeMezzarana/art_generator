"""
app to create cool and completely unique works of art
"""
import sys
import toga
from artgenerator.ArtGenerator import ArtGenerator,create_geometric_art,create_chaotic_art
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import logging
from typing import Optional
import os
import re

logging.basicConfig(
    stream=sys.stdout, 
    format='%(levelname)s - Line %(lineno)d (%(name)s %(asctime)s) - %(message)s',
    datefmt= '%Y-%m-%d %H:%M', 
    level=logging.DEBUG)

class App(toga.App):

    def startup(self):
        """Construct and show the Toga application.
        """
        self.style = 'light'
        self.icons_path = str(self.paths.app) + "/resources/command_icons/"
        # Lazy initialization
        self.draw_steps = []
        self.view = None 
        self.draw_view = None
        self.save_cmd = None
        self.random_art_box = None
        self.draw_art_box = None

        # Initialize main_menu
        self.main_menu()

    def main_menu(self,widget:[Optional]=None):
        """Create the main menu content in self.main_box
        """

        self.main_window = toga.MainWindow(title=self.formal_name,size = (540,960))
        self.main_box = toga.Box(
            style=Pack(
                direction=COLUMN,
                background_color= '#D9DDC4'
                )
            )

        button_random_art = toga.Button(
            "Create Random Art!",
            on_press=self.random_art_windows,
            style=Pack(
                padding=(0,120,25,120),
                alignment = 'center',
                direction = ROW,
                #font_family = 'fantas
                #font_weight = 'bold',
                font_size = 14,
                flex =1,
                background_color = 'white'
                )
        )
        
        button_draw_art = toga.Button(
            "Draw Your Own Art!",
            on_press=self.draw_art_windows,
            style=Pack(
                padding=(0,120,200,120),
                alignment = 'center',
                direction = ROW,
                #font_family = 'fantas
                #font_weight = 'bold',
                font_size = 14,
                flex =1,
                background_color = 'white'
                )
        )
        background_img = toga.Image(str(self.paths.app) + "/resources/background/artgenerator.png")
        self.background = toga.ImageView(background_img,style=Pack(
            padding=(10,20,30,20),
            direction=COLUMN,
            alignment = 'top',
            flex =2))
        
        # toolbox
        self.save_cmd = toga.Command(
            self.save,
            text="Save",
            icon=self.icons_path + 'save.png'
        )
        self.home_cmd = toga.Command(
            self.main_menu,
            text="Menu",
            icon=self.icons_path + 'home.png'
        )

        self.main_window.toolbar.add(self.home_cmd,self.save_cmd)

        self.main_box.add(self.background)
        self.main_box.add(button_random_art)
        self.main_box.add(button_draw_art)
        self.main_window.content = self.main_box
        #if self.save_cmd:
         #   self.main_window.toolbar = None
        self.main_window.show()

    def draw_art_windows(self,widget):
        
        self.style = 'light'
        # Initialize ArtGenerator Object
        size = self.main_window.size
        self.art_obj = ArtGenerator(
            bg_type = 'white',
            img_size =(int(size[0])+55,int(size[1]))
            )
        self.art_obj.save_img(str(self.paths.app )+ "/img/step_00.jpeg")
        # Save current state
        self.draw_steps.append(self.art_obj)

        self.draw_art_box = toga.Box(
            children = [],
            style=Pack(
                direction=COLUMN,
                background_color= 'white',
                alignment='bottom',
                )
        )

        draw_pack = Pack(
            padding=10,
            font_family='serif',
            font_weight='bold',
            font_size=14,
            alignment = 'bottom',
            background_color = 'white',
            width = 100)
        
        self.switch_style = toga.Switch(
                    'Dark Mode',
                    on_change=lambda widget: self.change_style(widget),
                    style=Pack(
                        padding=7,
                        font_size=10,
                        alignment = 'right',
                        color = '#9da39e',
                        width = 80)
                    )
        #toga.Slider(range=(-5, 10), value=7, on_change=my_callback)

        self.draw_buttons = toga.Box(
            children = [        
                toga.Button(
                    "Background",
                    on_press=lambda widget:self.change_background(widget),
                    style=draw_pack
                ),
                toga.Selection(
                    items=[
                        'Lines','Vortex','Polygon', 'Arc','Ellipse'],
                    style=draw_pack, 
                    on_select=None
                    ),
                self.switch_style, 
            ],
            style=Pack(
                direction=ROW,
                background_color= 'white'
                )
            )
     
        self.draw_art_box.add(self.draw_buttons)
        self.main_window.content = self.draw_art_box

        if self.draw_view:
            self.draw_art_box.remove(self.draw_view)
        my_image = toga.Image(self.paths.app / "img/step_00.jpeg")
        self.draw_view = toga.ImageView(my_image,style=Pack(direction=COLUMN))
        self.draw_art_box.add(self.draw_view)

    def random_art_windows(self, widget):

        self.style = 'light'
        self.random_art_box = toga.Box(
            children = [],
            style=Pack(
                direction=COLUMN,
                background_color= 'white',
                alignment='bottom',
                )
        )

        button_pack = Pack(
            padding=2,
            font_family='serif',
            font_weight='bold',
            font_size=12,
            alignment = 'bottom',
            background_color = 'white',
            width = 100)

        self.switch_style = toga.Switch(
                    'Dark Mode',
                    on_change=lambda widget: self.change_style(widget),
                    style=Pack(
                        padding=7,
                        font_size=10,
                        alignment = 'right',
                        color = '#9da39e',
                        width = 80)
                    )
        self.buttons = toga.Box(
            children = [        
                toga.Button(
                    "Geometric",
                    on_press=lambda widget:self.create_random_art(widget,'geometric'),
                    style=button_pack
                ),
                toga.Button(
                    "Chaotic",
                    on_press=lambda widget:self.create_random_art(widget,'chaotic'),
                    style=button_pack
                ),
                self.switch_style, 
            ],
            style=Pack(
                direction=ROW,
                background_color= 'white'
                )
            )
     
        self.random_art_box.add(self.buttons)
        self.main_window.content = self.random_art_box

    def save(self,widget):

        if self.main_window.content == self.main_box:
            print('Nothing to save')
        else:
            print('save')
    
    def change_style(self,widget):

        if not self.switch_style.value:
            if self.random_art_box:
                self.random_art_box.style.update(background_color='white')
                self.buttons.style.update(background_color='white')
            if self.draw_art_box:
                self.draw_art_box.style.update(background_color='white')
                self.draw_buttons.style.update(background_color='white')
            self.style = 'light'
        else:
            if self.random_art_box:
                self.random_art_box.style.update(background_color='black')
                self.buttons.style.update(background_color='black')
            if self.draw_art_box:
                self.draw_art_box.style.update(background_color='black')
                self.draw_buttons.style.update(background_color='black')
            self.style = 'dark'

    def create_random_art(self, widget,type:str):
        """Display a random geometric_art
        Generate a .jpeg img and assign to an ImageView
        """

        # Get the main screen's dimensions
        size = self.main_window.size
        # Generate Art
        if type == 'chaotic':
            _ = create_chaotic_art(
                save_path = str(self.paths.app) + "/test",
                img_size =(int(size[0])+55,int(size[1])),
                style = self.style
                )
        elif type == 'geometric':
            _ = create_geometric_art(
                save_path = str(self.paths.app) + "/test",
                img_size =(int(size[0])+55,int(size[1])),
                style = self.style
                )
        if self.view:
            self.random_art_box.remove(self.view)
        my_image = toga.Image(self.paths.app / "test.jpeg")
        self.view = toga.ImageView(my_image,style=Pack(direction=COLUMN))
        self.random_art_box.add(self.view)
        
    def change_background(self, widget):

        self.art_obj.alter_background()
        self.find_last_stpe() # update last self.last_step
        self.art_obj.save_img(str(self.paths.app )+ "/img/step_" + self.next_step + ".jpeg")
        # Save current state
        self.draw_steps.append(self.art_obj)
        self.background_step = True 

    def find_last_stpe(self):
        """Returns str value referring to the last step
        """
        draw_files = os.listdir(str(self.paths.app )+ "/img")
        draw_files_jpeg = [file for file in draw_files if re.search('.jpeg',file)]
        print(draw_files_jpeg)

        draw_files_steps = [re.findall(r'\d+',file)[0] for file in draw_files_jpeg]
        self.last_step = max(draw_files_steps)

        next_step_int = int(self.last_step ) + 1
        if len(str(next_step_int))==1:
            self.next_step = '0' + str(next_step_int)
        else:
            self.next_step = str(next_step_int)



class ExitHandler():
    def __call__(self, app):
        # Place your closing actions here
        # For example, save data, close connections, etc.
        print("Closing the application")

        # Return True to allow the application to exit
        return True

    

def main():
    app = App()
    app.on_exit = ExitHandler() 
    return app
