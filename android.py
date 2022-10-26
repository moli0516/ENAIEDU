__version__ = "1.0.0"
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label

Window.clearcolor = (1,1,1,1)

Builder.load_string("""
<Label>
    markup: True
    color: 0,0,0,1
""")

Papers = {
    'Paper1':{
        'text':"""""",
        'questions':[]
    },
    'Paper2':{}
}

class androidApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(menuScreen(name='menuScreen'))
        return sm

class label(Label):
    def __init__(self,**kwargs):
        self.bgc = kwargs['bgColor']
        del kwargs['bgColor']
        return super(label,self).__init__(**kwargs)
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(self.bgc[0]/255,self.bgc[1]/255,self.bgc[2]/255,self.bgc[3])
            Rectangle(pos=self.pos,size=self.size)

class menuScreen(Screen):
    def __init__(self, **kwargs):
        super(menuScreen,self).__init__(**kwargs)
        self.elementsList = {
            'titleLabel': ({'text':"ENAI",'pos_hint':{}})
        }
        self.titleLabel = label(text='[b]ENAI[/b]',bgColor=(42,196,240,.8),font_size='30sp',pos_hint={'x':.0,'y':.9},size_hint=(1,.1))#,background_color=
        self.titleLabel.bind(pos=self.titleLabel.on_size)
        self.add_widget(self.titleLabel)
        paperHintY = 0.85
        for paper in Papers:
            paperHintY -=.17
            bg = label(text='',bgColor=(167,176,178,.8),font_size='20sp',pos_hint={'x':0,'y':paperHintY},size_hint=(1,.15))
            bg.bind(pos=bg.on_size)
            self.add_widget(bg)
            self.add_widget(Label(text=paper,font_size='20sp',pos_hint={'x':-.3,'y':paperHintY},size_hint=(1,.15)))


if __name__ == '__main__':
    androidApp().run()