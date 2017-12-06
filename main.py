#!/usr/bin/python3
'''Module for a minecraft villager app in python3'''

#pylint: disable=E0611,W0611,W0201

from time import sleep

from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.accordion import Accordion, AccordionItem

from modules.cjson import JsonHandler

class VillagesWidget(BoxLayout):
    '''Widget to load start screen.'''

    container = ObjectProperty(None)

class MainWidget(BoxLayout):
    '''Widget to load main screen.'''

    container = ObjectProperty(None)


class VillageToolApp(App):
    '''All functions of the app.'''

    def build(self):
        '''Loading start screen.'''

        self.icon = 'src/minecraft32px.png'
        self.project = str()
        self.file = 'kv/village.kv'

        self.root = Builder.load_file(self.file)
        Window.maximize()


    def main(self, project_name):
        '''Loading main screen.'''

        if project_name == '':
            return

        self.title = project_name
        self.project = project_name


        try:
            self.village = JsonHandler.importer(self.project)
        except FileNotFoundError:
            JsonHandler.exporter(self.project, {self.project: {'name': self.project, 'villagers': {}}})
            self.village = JsonHandler.importer(self.project)

        Builder.unload_file(self.file)
        self.root.clear_widgets()
        self.file = 'kv/main.kv'
        screen = Builder.load_file(self.file)
        layout = GridLayout(cols=1, padding=10, spacing=10, size_hint=(1, None))
        layout.bind(minimum_height=layout.setter('height'))
        for villager in self.village[self.project]['villagers'].keys():
            layout.add_widget(Button(text=villager, size_hint_y=None, height=100, font_size=25))
        toplayout = ScrollView(pos_hint={'center_x': .5, 'center_y': .5}, do_scroll_x=False)
        toplayout.add_widget(layout)
        screen.add_widget(toplayout)
        self.root.add_widget(screen)

    def add_villager(self, name):
        '''Adding a villager to the village.'''
        if name != '':
            self.village[self.project]['villagers'][name] = dict()
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




if __name__ == '__main__':
    VillageToolApp().run()
