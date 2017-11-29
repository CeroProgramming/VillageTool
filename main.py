from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.accordion import Accordion, AccordionItem



class PAPApp(App):

    def build(self):

        self.icon = 'src/dice20_128.png'

        root = Accordion()
        for i in range(2):
            item = AccordionItem(title='Title %d' % i)
            item.add_widget(Label(text='Very big content\n' * 10))
            root.add_widget(item)
        return root

if __name__ == '__main__':
    PAPApp().run()
