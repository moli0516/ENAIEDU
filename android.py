__version__ = "1.0.0"
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty
from kivy.graphics import Color, Rectangle,RoundedRectangle
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

Window.clearcolor = (1,1,1,1)

Builder.load_string("""
<Label>
    markup: True
    color: 0,0,0,1
""")

Papers = {
    'Paper1':{
        'text':"""[1] Jesse Owens was born on 12th September 1913. He is
known for winning four Olympic gold medals in track and
field events. In 1935, Jesse took part in a total of 42 different sporting events and
won them all. This amazing achievement earned him a place at the 1936
Olympics in Berlin, Germany. During the 1936 Olympics, Germany was being 
ruled by Adolf Hitler. After his success, Jesse Owens was called a hero by many people.
However, lots of people believe that Jesse’s success was not
what Hitler wanted to happen. This is because he wanted to
use the Olympics to show how his group of white athletes
were better than everyone else and Jesse proved him wrong.
Today, there is a school in Berlin that has been named
after Jesse.
[2] Serena Williams is a famous tennis player who was born on 26th September
1981. In total, she has won more Grand Slam tennis tournaments than any
other player. Serena’s father started teaching her how to play tennis when she was three
years old. By the time she was ten, Serena was the number one tennis
player in the ten and under division. Serena has also won a total of four Olympic gold medals.
Three of these have been in doubles tournaments alongside
her sister, Venus. Throughout her career, Serena has suffered
many injuries. Each time, she has returned to the game and proven what
an incredible, talented player she is.
[3] Michael Jordan was born on 17th February 1963 and is a
successful basketball player. Throughout his career, he
won a total of six NBA (National Basketball Association)
championships with his team. When Michael was at university, 
he joined the basketballteam. In 1982, they won the championship and, a few
years later, Michael joined the NBA team, the Chicago Bulls.
Michael continued learning while playing basketball and
earned a degree in geography in 1985. Michael is 1.98 metres tall and can jump 
over a metre straight up into the air!
Before retiring in 2003, Michael played in 1,072 NBA games.
[4] Muhammad Ali was a successful boxer who has a total of 56 victories. He
was born on 17th January 1942 and was named Cassius Marcellus Clay Jr.
When he was 12, Muhammad’s bike was stolen. The police officer who
helped Muhammad also trained young boxers in his spare time. He invited
him along to the gym to join in and, by 1954, Muhammad had won his first
boxing match. In April 1967, Muhammad was summoned to join the military. He refused
and openly said that he did not support the Vietnam War. This objection led
to him being found guilty of refusing to serve in the military,
which was against the law. While Muhammad argued against
the decision, he was unable to box and missed over three
years of competitions.
In 1998, Muhammad was given an important award that
celebrated his work to promote peace.""",
        'questions':[
            {
                "question": "Who was born on 17th February 1963? ",
                "answer": "michael jordan",
                "advise": "You can't recongize the name",
                "score": "2",
                "type": "short",
                "keypoint": [" "]
            },
            {
                "question": "Where were the 1936 Olympics held? ",
                "answer": "germany",
                "advise": "You can't get the properly country name",
                "score": "2",
                "type": "short",
                "keypoint": [" "]
            },
            {
                "question": "Look at the section on Para 4. Find and copy one word that means the same as called. ",
                "answer": "summoned",
                "advise": "You can't find out the correct vocab",
                "score": "2",
                "type": "short",
                "keypoint": [" "]
            },
            {
                "question": "Summarise what you have learnt about Michael Jordan using 20 words or fewer. ",
                "answer": "",
                "advise": "You can't summerise the article",
                "score": "4",
                "type": "long",
                "keypoint": [
                    "good", "strong", "gay", "black"
                ]
            }
        ]
    },
    'Paper2':{
        'text':"""""",
        'questions':[]
    }
}

screenManager = ScreenManager()

def renderBG(elem,value):
    elem.canvas.before.clear()
    with elem.canvas.before:
        Color(elem.bgColor[0]/255,elem.bgColor[1]/255,elem.bgColor[2]/255,elem.bgColor[3])
        Rectangle(pos=elem.pos,size=elem.size)

class menuScreen(Screen):
    def __init__(self, **kwargs):
        super(menuScreen,self).__init__(**kwargs)
        self.paperScreen = None
        self.titleLabel = Label(text='[b]ENAI[/b]',font_size='30sp',pos_hint={'x':.0,'y':.9},size_hint=(1,.1))#,background_color=(1,1,1,1)=
        self.titleLabel.bgColor = (42,196,240,.8)
        self.titleLabel.bind(pos=renderBG)
        self.add_widget(self.titleLabel)
        paperHintY = 0.85
        for paper in Papers:
            paperHintY -=.17
            bg = Label(text='',pos_hint={'x':0,'y':paperHintY},size_hint=(1,.15))
            bg.bgColor = (167,176,178,.8)
            startBtn = Button(text="start",font_size='20sp',pos_hint={'x':.75,'y':paperHintY+.025},size_hint=(.2,.1))
            startBtn.paper = paper
            bg.bind(pos=renderBG)
            startBtn.bind(on_press=self.onstartBtnPressed)
            self.add_widget(bg)
            self.add_widget(Label(text=paper,font_size='20sp',pos_hint={'x':-.3,'y':paperHintY},size_hint=(1,.15)))
            self.add_widget(startBtn)
    def onstartBtnPressed(self,btn):
        if self.paperScreen:screenManager.remove_widget(self.paperScreen)
        del self.paperScreen
        self.paperScreen = paperScreen(name='paperScreen',paper=btn.paper)
        screenManager.add_widget(self.paperScreen)
        screenManager.switch_to(screen=self.paperScreen,direction='left')

class paperScreen(Screen):
    def __init__(self, **kwargs):
        self.paper = kwargs["paper"]
        del kwargs["paper"]
        super(paperScreen,self).__init__(**kwargs)
        self.titleLabel = Label(text=self.paper,font_size='30sp',pos_hint={'x':.0,'y':.9},size_hint=(1,.1))
        self.exitBtn = Button(text="<<Exit",font_size='25sp',pos_hint={'x':.02,'y':.9},size_hint=(.1,.08),background_normal='',background_down='',background_color=(1,1,1,1))
        self.textBox = TextInput(text=Papers[self.paper]['text'],font_size='20sp',readonly=True,pos_hint={'x':.1,'y':.45},size_hint=(.8,.45))
        self.previousBtn = Button(text="<=Previous",font_size='20sp',pos_hint={'x':.15,'y':.05},size_hint=(.18,.08),disabled=True)
        self.nextBtn = Button(text="Next=>",font_size='20sp',pos_hint={'x':.67,'y':.05},size_hint=(.18,.08),disabled=True)
        self.exitBtn.bind(on_press=self.returnMenu)
        self.previousBtn.bind(on_press=self.previousQuestion)
        self.nextBtn.bind(on_press=self.nextQuestion)
        self.add_widget(self.titleLabel)
        self.add_widget(self.exitBtn)
        self.add_widget(self.textBox)
        self.add_widget(self.previousBtn)
        self.add_widget(self.nextBtn)
        self.questionsElem = []
        for question in Papers[self.paper]['questions']:
            elems = []
            questionLabel = Label(text=question['question'],font_size='18sp',pos_hint={'x':.02,'y':-.15},halign="left",valign="middle",padding=(70,70))
            questionLabel.bind(size=questionLabel.setter('text_size'))
            elems.append(questionLabel)
            answerTextBox = None
            if question['type']=="short":
                answerTextBox = TextInput(hint_text="Short Answer",pos_hint={'x':.1,'y':.25},size_hint=(.4,.05),multiline=False)
            elif question['type']=="long":
                answerTextBox = TextInput(hint_text="Long Answer",pos_hint={'x':.1,'y':.15},size_hint=(.7,.13))
            if answerTextBox:
                answerTextBox.bind(text=self.answerTextBoxTyped)
                elems.append(answerTextBox)
            self.questionsElem.append(elems)
        self.answered = [False for i in range(len(self.questionsElem))]
        self.currentQuestion = 1
        for elem in self.questionsElem[0]:
            self.add_widget(elem)
    def answerTextBoxTyped(self,textBox,value):
        self.nextBtn.disabled = not value
        self.answered[self.currentQuestion-1] = bool(value)
    def previousQuestion(self,btn):
        if self.currentQuestion == 1:return
        self.nextBtn.disabled = False
        self.nextBtn.text = "Next=>"
        for elem in self.questionsElem[self.currentQuestion-1]: self.remove_widget(elem)
        self.currentQuestion -= 1
        for elem in self.questionsElem[self.currentQuestion-1]: self.add_widget(elem)
        if self.currentQuestion == 1: btn.disabled = True
    def nextQuestion(self,btn):
        if self.currentQuestion != len(self.questionsElem):
            self.previousBtn.disabled = False
            for elem in self.questionsElem[self.currentQuestion-1]: self.remove_widget(elem)
            self.currentQuestion += 1
            for elem in self.questionsElem[self.currentQuestion-1]: self.add_widget(elem)
            if not self.answered[self.currentQuestion-1]: btn.disabled = True
            if self.currentQuestion == len(self.questionsElem): btn.text = "^Submit^"
        else:
            self.mappingAns()
    def mappingAns(self):
        pass #tmr's work la zzZ
    def returnMenu(self,btn):
        screenManager.switch_to(menuS,direction="right")

menuS = menuScreen(name='menuScreen')
class androidApp(App):
    def build(self):
        screenManager.add_widget(menuS)
        return screenManager

if __name__ == '__main__':
    androidApp().run()
