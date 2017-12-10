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
    size_hint = (1, 1)
    orientation = 'vertical'
    padding = [20, 20, 20, 20]
    spacing = 20

    container = ObjectProperty(None)

class VillagerWidget(BoxLayout):
    '''Widget to load villager edit screen.'''

    container = ObjectProperty(None)


class ButtonGrid(GridLayout):
    '''Grid of control buttons.'''

    size_hint = [1, None]
    cols = 3
    padding = [20, 20, 20, 20]
    spacing = [20, 20]

    def __init__(self):
        super(ButtonGrid, self).__init__()

        add_villager_button = Button(text='Add Villager', size_hint=[0.25, 0.1], font_size=25, background_color=(0, 0.5, 1, 1), background_normal='src/white16x.png')
        self.add_widget(add_villager_button)
        add_villager_button.bind(on_release=lambda x: VTA.add_villager(villager_name_input.text))

        rm_villager_button = Button(text='Remove Villager', size_hint=[0.25, 0.1], font_size=25, background_color=(0, 0.5, 1, 1), background_normal='src/white16x.png')
        self.add_widget(rm_villager_button)
        rm_villager_button.bind(on_release=lambda x: VTA.rm_villager(villager_name_input.text))

        villager_name_input = TextInput(hint_text='Name..', hint_text_color=(1, 1, 1, 1), size_hint=[0.25, 0.1], font_size=35, background_color=(0, 0.5, 1, 1), foreground_color=(1, 1, 1, 1), multiline=False)
        self.add_widget(villager_name_input)
        villager_name_input.bind(on_text_validate=lambda x: VTA.add_villager(villager_name_input.text))


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
        VTA.main(VTA.project, instance.text)


class TradingGrid(GridLayout):
    '''Grid for the villagers in the main menu.'''
    cols = 6
    padding = [10, 10, 10, 10]
    spacing = [10, 10]
    size_hint = (None, None)
    row_force_default = True
    row_default_height = 50

    def __init__(self):
        super(TradingGrid, self).__init__()
        self.amout_demands = []
        self.demands = []
        self.supplys = []
        self.amout_supplys = []
        self.remove_buttons = []

        for i in range(len(VTA.village[VTA.project]['villagers'][VTA.villager]['tradings'])):

            self.amout_demands.append(TextInput(hint_text='Amount', text=VTA.village[VTA.project]['villagers'][VTA.villager]['tradings'][i]['amount_demand'], hint_text_color=(1, 1, 1, 1), font_size=35, background_color=(0, 0.5, 1, 1), multiline=False, size_hint=(70, 100), size=(70, 100), font_color=(1, 0.98, 0, 1), border=(4, 4, 4, 4), foreground_color=(1, 1, 1, 1)))
            self.add_widget(self.amout_demands[i])
            self.amout_demands[i].bind(on_text_validate=partial(self.transmitter_amount_demand, i))
            self.amout_demands[i].bind(focus=partial(self.transmitter2_amount_demand, i))

            self.demands.append(TextInput(hint_text='Item', text=VTA.village[VTA.project]['villagers'][VTA.villager]['tradings'][i]['demand'], hint_text_color=(1, 1, 1, 1), font_size=35, background_color=(0, 0.5, 1, 1), multiline=False, size_hint=(70, 100), size=(70, 100), font_color=(1, 0.98, 0, 1), border=(4, 4, 4, 4), foreground_color=(1, 1, 1, 1)))
            self.add_widget(self.demands[i])
            self.demands[i].bind(on_text_validate=partial(self.transmitter_demand, i))
            self.demands[i].bind(focus=partial(self.transmitter2_demand, i))

            self.add_widget(Label(text='-', font_size=35))

            self.supplys.append(TextInput(hint_text='Item', text=VTA.village[VTA.project]['villagers'][VTA.villager]['tradings'][i]['supply'], hint_text_color=(1, 1, 1, 1), font_size=35, background_color=(0, 0.5, 1, 1), multiline=False, size_hint=(70, 100), size=(70, 100), font_color=(1, 0.98, 0, 1), border=(4, 4, 4, 4), foreground_color=(1, 1, 1, 1)))
            self.add_widget(self.supplys[i])
            self.supplys[i].bind(on_text_validate=partial(self.transmitter_supply, i))
            self.supplys[i].bind(focus=partial(self.transmitter2_supply, i))

            self.amout_supplys.append(TextInput(hint_text='Amount', text=VTA.village[VTA.project]['villagers'][VTA.villager]['tradings'][i]['amount_supply'], hint_text_color=(1, 1, 1, 1), font_size=35, background_color=(0, 0.5, 1, 1), multiline=False, size_hint=(70, 100), size=(70, 100), font_color=(1, 0.98, 0, 1), border=(4, 4, 4, 4), foreground_color=(1, 1, 1, 1)))
            self.add_widget(self.amout_supplys[i])
            self.amout_supplys[i].bind(on_text_validate=partial(self.transmitter_amount_supply, i))
            self.amout_supplys[i].bind(focus=partial(self.transmitter2_amount_supply, i))

            self.remove_buttons.append(Button(text='-', size_hint=(None, None), size=(40, 50), font_size=25, background_normal='src/white16x.png', background_color=(1, 0.28, 0, 1)))
            self.add_widget(self.remove_buttons[i])
            self.remove_buttons[i].bind(on_release=partial(self.transmitter_remove, i))


    def transmitter_amount_demand(self, i, instance):
        '''Shows the number of the button pressed.'''
        VTA.change_demand_amount(i, instance.text)

    def transmitter_demand(self, i, instance):
        '''Shows the number of the button pressed.'''
        VTA.change_demand(i, instance.text)

    def transmitter_supply(self, i, instance):
        '''Shows the number of the button pressed.'''
        VTA.change_supply(i, instance.text)

    def transmitter_amount_supply(self, i, instance):
        '''Shows the number of the button pressed.'''
        VTA.change_supply_amount(i, instance.text)

    def transmitter2_amount_demand(self, i, instance, istrue):
        '''Shows the number of the button pressed.'''
        if not istrue:
            VTA.change_demand_amount(i, instance.text)

    def transmitter2_demand(self, i, instance, istrue):
        '''Shows the number of the button pressed.'''
        if not istrue:
            VTA.change_demand(i, instance.text)

    def transmitter2_supply(self, i, instance, istrue):
        '''Shows the number of the button pressed.'''
        if not istrue:
            VTA.change_supply(i, instance.text)

    def transmitter2_amount_supply(self, i, instance, istrue):
        '''Shows the number of the button pressed.'''
        if not istrue:
            VTA.change_supply_amount(i, instance.text)

    def transmitter_remove(self, i, instance):
        '''Shows the number of the button pressed.'''
        VTA.rm_trading(i)


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
        self.main('vale', None)
        ####################


    def main(self, project_name, villager):
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

        if villager is None:
            try:
                villager = self.villagers[0]
            except IndexError:
                pass

        Builder.unload_file(self.file)
        self.root.clear_widgets()
        '''self.file = 'kv/main.kv'
        screen = Builder.load_file(self.file)
        villager_grid = VillagerGrid()
        villager_grid.bind(minimum_height=villager_grid.setter('height'))
        layout = ScrollView(pos_hint={'center_x': .5, 'center_y': .5}, do_scroll_x=False)
        layout.add_widget(villager_grid)
        screen.add_widget(layout)
        self.root.add_widget(screen)'''
        screen = MainWidget()

        topbox = BoxLayout(size_hint=(1, 1), orientation='horizontal', padding=20, spacing=20)

        quickview = GridLayout(cols=1, padding=[5, 5, 5, 5], spacing=5, size_hint=(1, None))
        if villager is not None:
            quickview.add_widget(TextInput(text=villager, font_size=30, readonly=True, multiline=False, size_hint=(70, 100), size=(70, 100), background_color=(0, 0.5, 1, 1), foreground_color=(1, 1, 1, 1)))
            quickview.add_widget(TextInput(text=self.village[self.project]['villagers'][villager]['profession'].capitalize(), font_size=30, readonly=True, multiline=False, size_hint=(70, 100), size=(70, 100), background_color=(0, 0.5, 1, 1), foreground_color=(1, 1, 1, 1)))
            quickview.add_widget(TextInput(text=self.village[self.project]['villagers'][villager]['career'].capitalize(), font_size=30, readonly=True, multiline=False, size_hint=(70, 100), size=(70, 100), background_color=(0, 0.5, 1, 1), foreground_color=(1, 1, 1, 1)))
            edit_button = Button(text='Edit', font_size=30, size_hint=(70, 100), size=(70, 100), background_color=(0, 0.5, 1, 1), background_normal='src/white16x.png')
            edit_button.bind(on_release=lambda x: self.load_villager(villager))
            quickview.add_widget(edit_button)
        else:
            quickview.add_widget(TextInput(text='None', font_size=30, readonly=True, multiline=False, size_hint=(70, 100), size=(70, 100), background_color=(0, 0.5, 1, 1), foreground_color=(1, 1, 1, 1)))
            quickview.add_widget(TextInput(text='None', font_size=30, readonly=True, multiline=False, size_hint=(70, 100), size=(70, 100), background_color=(0, 0.5, 1, 1), foreground_color=(1, 1, 1, 1)))
            quickview.add_widget(TextInput(text='None', font_size=30, readonly=True, multiline=False, size_hint=(70, 100), size=(70, 100), background_color=(0, 0.5, 1, 1), foreground_color=(1, 1, 1, 1)))
        topbox.add_widget(quickview)

        villager_grid = VillagerGrid()
        villager_grid.bind(minimum_height=villager_grid.setter('height'))
        villager_scroll = ScrollView(pos_hint={'center_x': .5, 'center_y': .5}, do_scroll_x=False)
        villager_scroll.add_widget(villager_grid)
        topbox.add_widget(villager_scroll)


        screen.add_widget(topbox)


        button_grid = ButtonGrid()
        screen.add_widget(button_grid)

        self.root.add_widget(screen)


    def add_villager(self, name):
        '''Adding a villager to the village.'''

        if name != '':
            self.village[self.project]['villagers'][name] = dict()
            self.village[self.project]['villagers'][name]['name'] = name
            self.village[self.project]['villagers'][name]['profession'] = 'none'
            self.village[self.project]['villagers'][name]['career'] = 'none'
            self.village[self.project]['villagers'][name]['tradings'] = list()

            JsonHandler.exporter(self.project, self.village)
            self.main(self.project, None)


    def rm_villager(self, name):
        '''Adding a villager to the village.'''

        try:
            del self.village[self.project]['villagers'][name]
            JsonHandler.exporter(self.project, self.village)
            self.main(self.project, None)
        except KeyError:
            pass

    def load_villager(self, name):
        '''Loading the villager edit screen.'''

        self.villager = name
        Builder.unload_file(self.file)
        self.root.clear_widgets()
        self.file = 'kv/villager.kv'
        screen = Builder.load_file(self.file)


        layout = GridLayout(cols=1, padding=[20, 20, 20, 20], spacing=5, size_hint=(1, 1), pos=(150, 10), size=(self.root.width - 300, self.root.height - 20))
        input_name = TextInput(text=name, multiline=False, size_hint_y=None, height=80, font_size=40, font_color=(1, 0.98, 0, 1), foreground_color=(1, 1, 1, 1), background_color=(0, 0.5, 1, 1))
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


        add_button = Button(text='+', size_hint=(None, None), size=(40, 40), font_size=25, background_normal='src/white16x.png', background_color=(1, 0.28, 0, 1))
        add_button.bind(on_release=lambda x: self.add_trading())
        layout.add_widget(add_button)

        trading_scroll = ScrollView(do_scroll_x=False)  #TODO Repair scrollview
        trading_grid = TradingGrid()
        trading_grid.bind(minimum_height=layout.setter('height'))
        trading_scroll.add_widget(trading_grid)
        layout.add_widget(trading_scroll)

        layout.add_widget(Button(text='Back', size_hint_y=None, height=50, font_size=25, background_normal='src/white16x.png', background_color=(1, 0.28, 0, 1), on_release=lambda x: self.main(self.project, None)))

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

    def add_trading(self):
        '''Adding trade to villager's trade list.'''
        empty_trading = dict()
        empty_trading['amount_demand'] = str()
        empty_trading['amount_supply'] = str()
        empty_trading['demand'] = str()
        empty_trading['supply'] = str()
        self.village[self.project]['villagers'][self.villager]['tradings'].append(empty_trading)
        JsonHandler.exporter(self.project, self.village)
        self.load_villager(self.villager)

    def rm_trading(self, index):
        '''Remove trade from villager's trade list.'''
        try:
            self.village[self.project]['villagers'][self.villager]['tradings'].remove(self.village[self.project]['villagers'][self.villager]['tradings'][index])
            JsonHandler.exporter(self.project, self.village)
            self.load_villager(self.villager)
        except ValueError as e:
            print(e)

    def change_demand_amount(self, index, amount):
        '''Change the amount of items for the demand.'''
        try:
            self.village[self.project]['villagers'][self.villager]['tradings'][index]['amount_demand'] = amount
            JsonHandler.exporter(self.project, self.village)
        except ValueError:
            pass


    def change_supply_amount(self, index, amount):
        '''Change the amount of items for the supply.'''
        try:
            self.village[self.project]['villagers'][self.villager]['tradings'][index]['amount_supply'] = amount
            JsonHandler.exporter(self.project, self.village)
        except ValueError:
            pass


    def change_demand(self, index, item):
        '''Change the items for the demand.'''
        try:
            self.village[self.project]['villagers'][self.villager]['tradings'][index]['demand'] = item
            JsonHandler.exporter(self.project, self.village)
        except ValueError:
            pass


    def change_supply(self, index, item):
        '''Change the items for the supply.'''
        try:
            self.village[self.project]['villagers'][self.villager]['tradings'][index]['supply'] = item
            JsonHandler.exporter(self.project, self.village)
        except ValueError:
            pass







if __name__ == '__main__':
    VTA = VillageToolApp()
    VTA.run()
