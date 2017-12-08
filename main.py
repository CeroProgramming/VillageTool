#!/usr/bin/python3
'''Module for a minecraft villager app in python3'''

#pylint: disable=E0611,W0611,W0201,W0640,C0301,C0200,W0613,R0201

from time import sleep
from functools import partial

from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.dropdown import DropDown
from kivy.properties import ObjectProperty

from modules.cjson import JsonHandler

class VillagesWidget(BoxLayout):
    '''Widget to load start screen.'''

    container = ObjectProperty(None)

class MainWidget(BoxLayout):
    '''Widget to load main screen.'''

    container = ObjectProperty(None)

class VillagerWidget(BoxLayout):
    '''Widget to load villager edit screen.'''

    container = ObjectProperty(None)

class VillagerGrid(GridLayout):
    '''Grid for the villagers in the main menu.'''
    cols = 1
    padding = [5, 5, 5, 5]
    spacing = [5, 5]
    size_hint = (1, None)

    def __init__(self):
        super(VillagerGrid, self).__init__()
        self.buttons = []

        for i in range(len(VTA.villagers)):
            self.buttons.append(Button(id=VTA.villagers[i], text=VTA.villagers[i], size_hint_y=None, height=80, font_size=25, background_normal='src/white16x.png', background_color=(1, 0.28, 0, 1)))
            self.add_widget(self.buttons[i])
            self.buttons[i].bind(on_release=partial(self.transmitter, i))

    def transmitter(self, i, instance):
        '''Shows the number of the button pressed.'''
        VTA.load_villager(VTA.villagers[i])


class ProfessionDropDown(DropDown):
    '''DropDown of all professions.'''

    def __init__(self):
        super(ProfessionDropDown, self).__init__()
        self.buttons = []

        for i in range(len(VTA.data['professions'])):
            self.buttons.append(Button(id=VTA.data['professions'][i].capitalize(), text=VTA.data['professions'][i].capitalize(), size_hint_y=None, height=40, font_size=25, background_normal='src/white16x.png', background_color=(1, 0.28, 0, 1)))
            self.add_widget(self.buttons[i])
            self.buttons[i].bind(on_release=partial(self.transmitter, i))

    def transmitter(self, i, instance):
        '''Shows the number of the button pressed.'''
        VTA.change_profession(VTA.villager, VTA.data['professions'][i])


class CareerDropDown(DropDown):
    '''DropDown of all careers.'''

    def __init__(self):
        super(CareerDropDown, self).__init__()
        self.buttons = []

        for i in range(len(VTA.data['careers'])):
            self.buttons.append(Button(id=VTA.data['careers'][i].capitalize(), text=VTA.data['careers'][i].capitalize(), size_hint_y=None, height=40, font_size=25, background_normal='src/white16x.png', background_color=(1, 0.28, 0, 1)))
            self.add_widget(self.buttons[i])
            self.buttons[i].bind(on_release=partial(self.transmitter, i))

    def transmitter(self, i, instance):
        '''Shows the number of the button pressed.'''
        VTA.change_career(VTA.villager, VTA.data['careers'][i])

class DemandAmountDropDown(DropDown):
    '''DropDown a list to choose the amount of items for trading (demands).'''

    def __init__(self):
        super(DemandAmountDropDown, self).__init__()
        self.buttons = []

        for i in range(64):
            self.buttons.append(Button(id=VTA.data['careers'][i].capitalize(), text=VTA.data['careers'][i].capitalize(), size_hint_y=None, height=40, font_size=25, background_normal='src/white16x.png', background_color=(1, 0.28, 0, 1)))
            self.add_widget(self.buttons[i])
            self.buttons[i].bind(on_release=partial(self.transmitter, i))

    def transmitter(self, i, instance):
        '''Shows the number of the button pressed.'''
        VTA.set_demand(VTA.villager, i)

class SupplyAmountDropDown(DropDown):
    '''DropDown a list to choose the amount of items for trading (supplys).'''

    def __init__(self):
        super(SupplyAmountDropDown, self).__init__()
        self.buttons = []

        for i in range(64):
            self.buttons.append(Button(id=VTA.data['careers'][i].capitalize(), text=VTA.data['careers'][i].capitalize(), size_hint_y=None, height=40, font_size=25, background_normal='src/white16x.png', background_color=(1, 0.28, 0, 1)))
            self.add_widget(self.buttons[i])
            self.buttons[i].bind(on_release=partial(self.transmitter, i))

    def transmitter(self, i, instance):
        '''Shows the number of the button pressed.'''
        VTA.set_demand(VTA.villager, i)




class VillageToolApp(App):
    '''All functions of the app.'''

    def build(self):
        '''Loading start screen.'''

        self.icon = 'src/minecraft32px.png'
        self.project = str()
        self.file = 'kv/village.kv'
        self.data = JsonHandler.importer('data')

        self.root = Builder.load_file(self.file)
        Window.maximize()


        ####################
        self.main('vale')
        ####################


    def main(self, project_name):
        '''Loading main screen.'''

        if project_name == '':
            return

        self.title = project_name.lower()
        self.project = project_name.lower()


        try:
            self.village = JsonHandler.importer(self.project)
        except FileNotFoundError:
            JsonHandler.exporter(self.project, {self.project: {'name': self.project, 'villagers': {}}})
            self.village = JsonHandler.importer(self.project)

        self.villagers = list(self.village[self.project]['villagers'].keys())


        Builder.unload_file(self.file)
        self.root.clear_widgets()
        self.file = 'kv/main.kv'
        screen = Builder.load_file(self.file)
        villager_grid = VillagerGrid()
        villager_grid.bind(minimum_height=villager_grid.setter('height'))
        layout = ScrollView(pos_hint={'center_x': .5, 'center_y': .5}, do_scroll_x=False)
        layout.add_widget(villager_grid)
        screen.add_widget(layout)
        self.root.add_widget(screen)

    def add_villager(self, name):
        '''Adding a villager to the village.'''

        if name != '':
            self.village[self.project]['villagers'][name] = dict()
            self.village[self.project]['villagers'][name]['name'] = name
            self.village[self.project]['villagers'][name]['profession'] = 'none'
            self.village[self.project]['villagers'][name]['career'] = 'none'
            self.village[self.project]['villagers'][name]['supplys'] = 'none'
            self.village[self.project]['villagers'][name]['demands'] = 'none'

            JsonHandler.exporter(self.project, self.village)
            self.main(self.project)


    def rm_villager(self, name):
        '''Adding a villager to the village.'''

        try:
            del self.village[self.project]['villagers'][name]
            JsonHandler.exporter(self.project, self.village)
            self.main(self.project)
        except KeyError:
            pass

    def load_villager(self, name):
        '''Loading the villager edit screen.'''

        self.villager = name
        Builder.unload_file(self.file)
        self.root.clear_widgets()
        self.file = 'kv/villager.kv'
        screen = Builder.load_file(self.file)


        layout = GridLayout(cols=1, padding=5, spacing=5, size_hint=(1, 1), pos=(150, 10), size=(self.root.width - 300, self.root.height - 20))
        input_name = TextInput(text=name, multiline=False, size_hint_y=None, height=80, font_size=40, font_color=(1, 0.98, 0, 1), border=(4, 4, 4, 4), foreground_color=(1, 1, 1, 1), background_color=(0, 0.5, 1, 1))
        input_name.bind(on_text_validate=lambda x: self.rename_villager(name, input_name.text))
        layout.add_widget(input_name)

        self.profession_dropdown = ProfessionDropDown()
        profession_button = Button(text=self.village[self.project]['villagers'][name]['profession'].capitalize(), size_hint_y=None, height=50, font_size=25, background_normal='src/white16x.png', background_color=(1, 0.28, 0, 1))
        profession_button.bind(on_release=self.profession_dropdown.open)
        layout.add_widget(profession_button)

        self.career_dropdown = CareerDropDown()
        career_button = Button(text=self.village[self.project]['villagers'][name]['career'].capitalize(), size_hint_y=None, height=50, font_size=25, background_normal='src/white16x.png', background_color=(1, 0.28, 0, 1))
        career_button.bind(on_release=self.career_dropdown.open)
        layout.add_widget(career_button)

        trading_box = BoxLayout(size_hint=(1, 1), orientation='vertical', padding=[10, 10, 10, 10], spacing=[10, 10, 10, 10])

        supply_amount = SupplyAmountDropDown()
        supply_amount_text = TextInput(text=self.village[self.project]['villagers'][name]['supplys'], multiline=False, size_hint_y=None, height=80, font_size=40, font_color=(1, 0.98, 0, 1), border=(4, 4, 4, 4), foreground_color=(1, 1, 1, 1), background_color=(0, 0.5, 1, 1))
        #TODO Changing architecture to supprt multiple tradings
        layout.add_widget(trading_box)

        layout.add_widget(Button(text='Back', size_hint_y=None, height=50, font_size=25, background_normal='src/white16x.png', background_color=(1, 0.28, 0, 1), on_release=lambda x: self.main(self.project)))

        screen.add_widget(layout)
        self.root.add_widget(screen)

    def rename_villager(self, legacy_name, new_name):
        '''Renames a villager in the edit screen and reloads the screen.'''

        if new_name != '' and new_name != legacy_name:
            self.village[self.project]['villagers'][new_name] = dict()
            self.village[self.project]['villagers'][new_name]['name'] = new_name
            self.village[self.project]['villagers'][new_name]['profession'] = self.village[self.project]['villagers'][legacy_name]['profession']
            self.village[self.project]['villagers'][new_name]['career'] = self.village[self.project]['villagers'][legacy_name]['career']
            self.village[self.project]['villagers'][new_name]['supplys'] = self.village[self.project]['villagers'][legacy_name]['supplys']
            self.village[self.project]['villagers'][new_name]['demands'] = self.village[self.project]['villagers'][legacy_name]['demands']

            self.rm_villager(legacy_name)
            self.load_villager(new_name)

    def change_profession(self, name, profession):
        '''Changes the profession of a villager.'''
        self.village[self.project]['villagers'][name]['profession'] = profession
        JsonHandler.exporter(self.project, self.village)
        self.profession_dropdown.dismiss()
        self.load_villager(name)

    def change_career(self, name, career):
        '''Changes the career of a villager.'''
        self.village[self.project]['villagers'][name]['career'] = career
        JsonHandler.exporter(self.project, self.village)
        self.career_dropdown.dismiss()
        self.load_villager(name)







if __name__ == '__main__':
    VTA = VillageToolApp()
    VTA.run()
