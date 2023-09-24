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
        self.app_path = str(self.paths.app) # For ExitHandler
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
        """Create the draw art windows in self.draw_art_box.
        """
        # Lazy initialization
        self.create_art_view = None 
        self.last_step = 0

        self.style = 'light'
        # Initialize ArtGenerator Object
        size = self.main_window.size
        self.art_obj = ArtGenerator(
            bg_type = 'white',
            img_size =(int(size[0])+79,int(size[1]))
            )

        self.draw_art_box = toga.Box(
            children = [],
            style=Pack(
                direction=COLUMN,
                #background_color= 'white',
                background_color= '#D9DDC4',
                alignment='bottom',
                )
        )
        # Standard style
        draw_pack = Pack(
            padding=7,
            font_family='serif',
            font_weight='bold',
            font_size=14,
            alignment = 'bottom',
            background_color = 'white',
            width = 50)
    
        self.draw_buttons = toga.Box(
            children = [      
                toga.Label(
                    "Choose a Background",
                    style=Pack(
                        padding=(7,0,10,10),
                        font_size=18,
                        alignment = 'right',
                        background_color= '#D9DDC4',
                        width = 200)
                ),
            toga.Button(
                    "+",
                    on_press=lambda widget:self.change_background(widget),
                    style=draw_pack
                ),
            toga.Button(
                    "⏎",
                    on_press=lambda widget:self.get_last_state(widget),
                    style=draw_pack
                ),
            toga.Button(
                    "Next!",
                    on_press=lambda widget:self.get_last_state(widget),
                    style=draw_pack
                )            ],
            style=Pack(
                direction=ROW,
                background_color= '#D9DDC4'
                )
            )
        
        self.intensity_slider = toga.Slider(
            range=(0, 10),
            value=5,
            on_change=self.change_intensity,
            style=Pack(
                padding=(0,0,4,0)))
        self.draw_art_box.add(self.draw_buttons)
        self.draw_art_box.add(self.intensity_slider)

        self.main_window.content = self.draw_art_box

    def random_art_windows(self, widget):
        """Create the random art windows in self.random_art_box.
        """

        self.style = 'light'
        self.random_art_box = toga.Box(
            children = [],
            style=Pack(
                direction=COLUMN,
                background_color= 'white',
                alignment='bottom',
                )
        )

        # Standard style
        random_pack = Pack(
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
                    style=random_pack
                ),
                toga.Button(
                    "Chaotic",
                    on_press=lambda widget:self.create_random_art(widget,'chaotic'),
                    style=random_pack
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
                img_size =(int(size[0])+79,int(size[1])),
                style = self.style
                )
        elif type == 'geometric':
            _ = create_geometric_art(
                save_path = str(self.paths.app) + "/test",
                img_size =(int(size[0])+79,int(size[1])),
                style = self.style
                )
        if self.view:
            self.random_art_box.remove(self.view)
        my_image = toga.Image(self.paths.app / "test.jpeg")
        self.view = toga.ImageView(my_image,style=Pack(direction=COLUMN))
        self.random_art_box.add(self.view)
        
    def change_background(self, widget):
        """Alter background. 
        Color based on slider value.
        """
        self.current_steap = "background"
        self.art_obj.alter_background(intensity = self.intensity_slider.value)
        self.add_step() # update last self.last_step
        self.art_obj.save_img(str(self.paths.app )+ "/img/background" + self.next_step + ".jpeg")
        # Save current state
        self.draw_steps.append(self.art_obj)

        if self.create_art_view:
            self.draw_art_box.remove(self.create_art_view)
        my_image = toga.Image(str(self.paths.app )+ "/img/background" + self.next_step + ".jpeg")
        self.create_art_view = toga.ImageView(my_image,style=Pack(direction=COLUMN))
        self.draw_art_box.add(self.create_art_view)

    def get_last_state(self,widget):
        """Return create_art_view to last state.
        """
        logging.debug(self.last_step)
        if self.create_art_view and self.last_step > 0:
            self.draw_art_box.remove(self.create_art_view)
            last_file_name = self.current_steap + self.last_step_str + ".jpeg"
            my_image = toga.Image(str(self.paths.app )+ "/img/" + last_file_name)
            self.create_art_view = toga.ImageView(my_image,style=Pack(direction=COLUMN))
            self.draw_art_box.add(self.create_art_view)
            self.remove_step()
        elif self.create_art_view:
            self.draw_art_box.remove(self.create_art_view)
            #self.remove_step()

        logging.debug(self.last_step)
        
    
    def remove_step(self):
        """Returns str value referring to the last step
        """

        # Update art obj
        current_file_name = self.current_steap + self.next_step + ".jpeg"
        os.remove(str(self.paths.app )+ "/img/" + current_file_name)
        logging.debug(f'File deleted: {current_file_name}')

        self.art_obj = self.draw_steps[self.last_step]
        # Update last step 
        self.last_step -=1
        if len(str(self.last_step))==1:
            self.last_step_str = '0' + str(self.last_step)
        else:
            self.last_step_str = str(self.last_step)
        # Update next step
        self.next_step_int-=1
        if len(str(self.next_step_int))==1:
            self.next_step = '0' + str(self.next_step_int)
        else:
            self.next_step = str(self.next_step_int)

    def add_step(self):
        """Returns str value referring to the last step
        """
        draw_files = os.listdir(str(self.paths.app )+ "/img")
        draw_files_jpeg = [file for file in draw_files if re.search('.jpeg',file)]
        draw_files_steps = [re.findall(r'\d+',file)[0] for file in draw_files_jpeg]
        if draw_files_steps:
            draw_files_steps = [int(i) for i in draw_files_steps]
            self.last_step = max(draw_files_steps)
            
        if len(str(self.last_step))==1:
            self.last_step_str = '0' + str(self.last_step)
        else:
            self.last_step_str = str(self.last_step)

        # Next step
        self.next_step_int = int(self.last_step ) + 1
        if len(str(self.next_step_int))==1:
            self.next_step = '0' + str(self.next_step_int)
        else:
            self.next_step = str(self.next_step_int)

    def change_intensity(self,widget):
        #print(self.intensity_slider.value)
        pass

class ExitHandler():
    def __call__(self, app):
        # Place your closing actions here
        # For example, save data, close connections, etc.
        print("Closing the application")

        # Clean img dir
        for file in os.listdir(str(app.paths.app )+ "/img/"):
            if re.search('.jpeg',file):
                os.remove(str(app.paths.app )+ "/img/" + file)
        # Return True to allow the application to exit
        return True

    

def main():
    app = App()
    app.on_exit = ExitHandler() 
    return app
