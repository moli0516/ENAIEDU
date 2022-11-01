__version__ = "1.0.0"
import kivy,language_tool_python,threading
from kivymd.app import MDApp
from kivy.clock import ClockBase
from functools import partial
from kivy.utils import platform
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.filemanager import MDFileManager
from kivy.properties import ObjectProperty, NumericProperty
from kivy.graphics import Color, Rectangle,RoundedRectangle
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
#from android.permissions import request_permissions, Permission

grammarChecker = language_tool_python.LanguageTool('en-US')

Window.clearcolor = (1,1,1,1)

Builder.load_string("""
<Label>
    markup: True
    color: 0,0,0,1
""")

Papers = {
    'Reading':{
        'Mock':{
            "Paper1":{
                'text':"""[1] When Helen Keller was almost two years old, she got sick with a high fever.
Because of that, she could not see or hear. Soon, she could not talk. Her parents
were so sad.
[2] When Helen was seven years old, a teacher called Anne Sullivan came to see
Helen’s parents. Helen’s mum told Anne, “Helen can’t see or hear for five years. She
is dumb too so she can’t tell us what she wants or how she feels. She has had many
teachers before but they couldn’t understand her and Helen was like a wild animal in
class. One by one they left.”
[3] The next morning, Anne had breakfast with Helen’s family. Helen was walking
around the table and eating everyone’s food with her hands. Anne said to Helen’s
parents, “I will teach Helen right now but I need a private place.”
[4] The servant took Anne and Helen to the nearby house and she left. At the next
meal at the house, Helen ate very noisily and messily again. So, Anne took away
Helen’s food. Finally, Helen sat down at the table. Anne returned Helen’s plate of
food. But Anne did not let her eat until Helen sat still and used a spoon.
[5] A few days later, Helen and Anne came to her parents’ home for dinner. Helen
could sit still at the table and eat with a spoon. They were so surprised.
“Unbelievable! I have never thought Helen would learn again!” Helen’s mum
cried.""",
                'questions':[
                    {
                        "question": "1. Chloe is reading a __________. ",
                        "answer": "a",
                        "advise": "You can't get the type of article",
                        "score": "1",
                        "type": "MC",
                        "keypoint": [" "],
                        "choice": ["A. biography",
                                "B. poem", 
                                "C. notice", 
                                "D. report"]
                    },
                    {
                        "question": "2. Which of the following was true about Helen Keller? ",
                        "answer": "b",
                        "advise": "You can't understand what happend in the article",
                        "score": "1",
                        "type": "MC",
                        "keypoint": [" "],
                        "choice": ["A. She was blind when she was born.",
                                "B. Anne was her only teacher.",
                                "C. She learnt how to eat properly from her first teacher.",
                                "D. She could not see, hear or talk when she met Anne Sullivan."]
                    },
                    {
                        "question": "3 In line 17 , what does ‘they’ refer to? ",
                        "answer": "the teachers",
                        "advise": "You can't find out the refer thing",
                        "score": "1",
                        "type": "short",
                        "keypoint": [" "],
                        "choice": [" "]
                    },
                    {
                        "question": "4. According to Paragraph 4, what did Anne want Helen to do when eating? ",
                        "answer": "",
                        "advise": "You can't summerise the article",
                        "score": "2",
                        "type": "long",
                        "keypoint": [
                            "sit", "still"
                        ],
                        "choice": [" "]
                    }
                ]
            }
        },
        'Assignment':{
            "Paper1":{
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
            }
        }
    },
    "Writing":{
        "Mock":{
            "Paper1":None
        },
        "Assignment":{
            "Paper1":None
        }
    }
}

screenManager = ScreenManager()

def word_tokenize(string):# Cant import nltk word_tokenize in android qwq
    res = ['']
    chars = [*string]
    for c in chars:
        if c in "~!@#$%^&*()_+{}|:\"<>?`-=[]\;',./" and res[-1] != '': res.extend([c,''])
        elif c == ' ':res.append('') if res[-1] != '' else ''
        else:res[-1] += c
    return res[:(-1 if res[-1] == '' else 0)]

def renderBG(elem,value,radius=None):
    elem.canvas.before.clear()
    with elem.canvas.before:
        Color(elem.bgColor[0]/255,elem.bgColor[1]/255,elem.bgColor[2]/255,elem.bgColor[3])
        RoundedRectangle(pos=elem.pos,size=elem.size,radius=radius) if radius else Rectangle(pos=elem.pos,size=elem.size)

class menuScreen(Screen):
    def __init__(self, **kwargs):
        super(menuScreen,self).__init__(**kwargs)
        self.titleLabel = Label(text='[b]ENAI EDU[/b]',font_size='30dp',pos_hint={'x':.0,'y':.9},size_hint=(1,.1))#,background_color=(1,1,1,1)=
        self.titleLabel.bgColor = (42,196,240,.8)
        self.titleLabel.bind(pos=renderBG)
        self.renderMenu()
    def renderMenu(self):
        self.clear_widgets()
        self.questionScreen = None
        self.add_widget(self.titleLabel)
        paperHintY = 0.85
        for ttype in Papers:
            paperHintY -=.17
            bg = Label(text='',pos_hint={'x':0,'y':paperHintY},size_hint=(1,.15))
            bg.bgColor = (167,176,178,.8)
            startBtn = Button(text="start",font_size='20dp',pos_hint={'x':.75,'y':paperHintY+.025},size_hint=(.2,.1))
            startBtn.ttype = ttype
            bg.bind(pos=renderBG)
            startBtn.bind(on_press=self.onMenuStartBtnPressed)
            self.add_widget(bg)
            self.add_widget(Label(text=ttype,font_size='20dp',pos_hint={'x':-.3,'y':paperHintY},size_hint=(1,.15)))
            self.add_widget(startBtn)
    def renderSelectPaperMode(self,ttype,ptype=None):
        self.clear_widgets()
        self.add_widget(self.titleLabel)
        gridBox = GridLayout(cols=1,spacing=1,size_hint_y=None)
        gridBox.bind(minimum_height=gridBox.setter('height'))
        scrollBox = ScrollView(pos_hint={'x':.15,'y':0.3},size_hint=(.7,.4))
        scrollBoxBG = Label(pos_hint={'x':.15,'y':0.3},size_hint=(.7,.4))
        scrollBoxBG.bgColor = (127,127,127,.3)
        scrollBoxBG.bind(pos=lambda a,b:renderBG(a,b,[20]))
        p = Papers[ttype]
        if ptype: p=p[ptype]
        for t in p:
            btn = Button(text=t,font_size="20dp",size_hint=(.7,None),height=self.height*.2)
            btn.ttype = ttype
            btn.ptype = ptype if ptype else t
            btn.paper = t if ptype else None
            btn.bind(on_press=self.onSelectionStartBtnPressed)
            gridBox.add_widget(btn)
        scrollBox.add_widget(gridBox)
        self.add_widget(scrollBox)
        self.add_widget(scrollBoxBG)
    def onMenuStartBtnPressed(self,btn):
        self.renderSelectPaperMode(btn.ttype)
    def onSelectionStartBtnPressed(self,btn):
        if not btn.paper:return self.renderSelectPaperMode(btn.ttype,btn.ptype)
        if self.questionScreen:screenManager.remove_widget(self.questionScreen)
        del self.questionScreen
        self.questionScreen = questionScreen(name='questionScreen',ttype=btn.ttype,ptype=btn.ptype,paper=btn.paper) 
        screenManager.add_widget(self.questionScreen)
        screenManager.switch_to(screen=self.questionScreen,direction='left')
        self.renderMenu()

class questionScreen(Screen):
    def __init__(self, **kwargs):
        self.ttype = kwargs['ttype']
        self.ptype = kwargs["ptype"]
        self.paper = kwargs["paper"]
        del kwargs["ttype"],kwargs['ptype'],kwargs["paper"]
        super(questionScreen,self).__init__(**kwargs)
        self.titleLabel = Label(text=self.ttype+' '+self.ptype+' '+self.paper,font_size='25dp',pos_hint={'x':.0,'y':.9},size_hint=(1,.1))
        self.exitBtn = Button(text="<<Exit",font_size='20dp',pos_hint={'x':.05,'y':.9},size_hint=(.1,.08),background_normal='',background_down='',background_color=(1,1,1,1))
        self.exitBtn.bind(on_press=self.returnMenu)
        self.add_widget(self.titleLabel)
        self.add_widget(self.exitBtn)
        if self.ttype == "Writing": self.renderWritingUploadScreen()
        else: self.renderReadingScreen()
    def renderReadingScreen(self):
        self.textBox = TextInput(text=Papers[self.ttype][self.ptype][self.paper]['text'],font_size='20dp',pos_hint={'x':.1,'y':.45},size_hint=(.8,.45))
        self.previousBtn = Button(text="<=Previous",font_size='20dp',pos_hint={'x':.15,'y':.05},size_hint=(.18,.08),disabled=True)
        self.nextBtn = Button(text="Next=>",font_size='20dp',pos_hint={'x':.67,'y':.05},size_hint=(.18,.08),disabled=True)
        self.previousBtn.bind(on_press=self.previousQuestion)
        self.nextBtn.bind(on_press=self.nextQuestion)
        self.add_widget(self.textBox)
        self.add_widget(self.previousBtn)
        self.add_widget(self.nextBtn)
        self.questionsElem = []
        for question in Papers[self.ttype][self.ptype][self.paper]['questions']:
            elems = []
            questionLabel = Label(text=question['question'],font_size='18dp',pos_hint={'x':.02,'y':-.12},halign="left",valign="middle",padding=(70,70))
            questionLabel.bind(size=questionLabel.setter('text_size'))
            elems.append(questionLabel)
            answerTextBox = None
            if question['type']=="short":
                answerTextBox = TextInput(hint_text="Short Answer",pos_hint={'x':.1,'y':.28},size_hint=(.4,.05),multiline=False)
            elif question['type']=="long":
                answerTextBox = TextInput(hint_text="Long Answer",pos_hint={'x':.1,'y':.2},size_hint=(.7,.13))
            elif question['type']=="MC":
                ansY = .32
                for ans in question['choice']:
                    ansY -= .05
                    box = BoxLayout(pos_hint={'x':-.37,'y':ansY})
                    ansBox = CheckBox(size_hint=(.1,.1),group=self.paper+'Q'+str(Papers[self.ttype][self.ptype][self.paper]['questions'].index(question)+1))
                    ansBox.ansNum = ans[0] #A/B/C/D
                    ansBox.bind(active=self.ansCheckBoxSelected)
                    box.add_widget(ansBox)
                    ansLabel = Label(text=ans,pos_hint={'x':.16,'y':-(.5-ansY-.05)},font_size='17dp',halign="left",valign="center")
                    ansLabel.bind(size=ansLabel.setter('text_size'))
                    elems.append(ansLabel)
                    elems.append(box)
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
        self.answered[self.currentQuestion-1] = value
    def ansCheckBoxSelected(self,checkbox,selected):
        self.nextBtn.disabled = not selected
        self.answered[self.currentQuestion-1] = checkbox.ansNum if selected else False
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
            self.calcReadingResult()
    def calcReadingResult(self):
        score = 0
        pscore = 0
        advises = []
        for i in range(len(self.answered)):
            ans = self.answered[i].lower()
            question = Papers[self.ttype][self.ptype][self.paper]['questions'][i]
            pscore += int(question['score'])
            addScore = 0
            if question['type'] == "short" or question['type'] == "MC":
                addScore = int(question['score']) if ans == question['answer'] else 0
            elif question['type'] == "long":
                reqKeypoint = question['keypoint']
                for word in word_tokenize(ans):
                    if word in reqKeypoint: #keypoint found
                        addScore += 1
            if addScore == 0: advises.append(question['advise'])
            score += addScore
        if score / pscore > 0.6: grade = "A"
        elif score / pscore > 0.5: grade = "B"
        elif score / pscore > 0.4: grade = "C"
        else: grade = "D"
        self.showResult(grade,advises)
    def showResult(self,grade,showText):
        self.clear_widgets()
        bg = Label(size_hint=(1,1))
        bg.bind(size=self.renderScoreBG)
        confirmBtn = Button(text="confirm",font_size='19dp',pos_hint={'x':.4,'y':.15},size_hint=(.2,.1))
        confirmBtn.bind(on_press=self.returnMenu)
        gridBox = GridLayout(cols=1,spacing=1,size_hint_y=None)
        gridBox.bind(minimum_height=gridBox.setter('height'))
        scrollBox = ScrollView(pos_hint={'x':.15,'y':0.3},size_hint=(.7,.4))
        scrollBoxBG = Label(pos_hint={'x':.15,'y':0.3},size_hint=(.7,.4))
        scrollBoxBG.bgColor = (127,127,127,.3)
        scrollBoxBG.bind(pos=lambda a,b:renderBG(a,b,[20]))
        for i in range(len(showText)):
            text = ""
            count = 0
            words = showText[i].split(' ')
            for w in words:
                added = count + len(w)
                count = added if added <=20 else 0
                text += w + ('\n' if added >20 and w != words[-1] else ' ')
            textLabel = Label(text=str(i)+'. '+text,font_size='15dp',size_hint=(.5,None),height=self.height*.1)
            gridBox.add_widget(textLabel)
        scrollBox.add_widget(gridBox)
        self.add_widget(bg)
        self.add_widget(self.titleLabel)
        self.add_widget(Label(text=('Final Grade: '+str(grade) if grade else "Final Result"),font_size='25dp',pos_hint={'x':0,'y':.3}))
        self.add_widget(Label(text=('Advices:' if self.ttype != "Writing" else "Mistakes:"),font_size="17sp",pos_hint={'x':0,'y':0.25}))
        self.add_widget(scrollBox)
        self.add_widget(scrollBoxBG)
        self.add_widget(confirmBtn)
    def renderWritingUploadScreen(self):
        openManagerBtn = Button(text="Select your writing.txt file",pos_hint={'x':.15,'y':.5},size_hint=(.7,.05))
        confirmBtn = Button(text="^Submit^",font_size='19dp',pos_hint={'x':.4,'y':.15},size_hint=(.2,.1))
        def selectPath(path):
            self.filePath = "C:"+path
            openManagerBtn.text = "Selected "+path.split('\\')[-1]
            if not confirmBtn.parent: self.add_widget(confirmBtn)
            self.fileManager.exit_manager()
        self.fileManager = MDFileManager(exit_manager=lambda *a:self.fileManager.close(),select_path=selectPath,ext=['.txt'])
        openManagerBtn.bind(on_press=lambda a:self.fileManager.show('/'))
        confirmBtn.bind(on_press=lambda a:self.calcWritingResult())
        self.add_widget(openManagerBtn)
    def calcWritingResult(self):
        self.clear_widgets()
        self.add_widget(Label(text="Calculating Writing Result...",font_size="25dp"))
        mistakes = []
        def getMistakes():
            with open(self.filePath,'r',encoding='utf-8') as f:
                writing = f.read()
                matches = grammarChecker.check(writing)
                for m in matches:
                    wordNo = str(len(writing[:m.errorLength+m.offset].split(' ')))
                    mistakes.append(m.ruleIssueType+': The '+wordNo+['th','st','nd','rd',*['th']*7][int(wordNo[-1])]+" word '"+writing[m.offset:m.errorLength+m.offset]+"' should be '"+ m.replacements[0]+"'")
                f.close()
            print(mistakes)
            self.showResult(None,mistakes)
        getMistakes()
    def renderScoreBG(self,label,value):
        label.canvas.before.clear()
        with label.canvas.before:
            Color(42/255,196/255,240/255,.8)
            Rectangle(pos=label.pos,size=label.size)
            Color(1,1,1,1)
            RoundedRectangle(pos=[label.pos[0]+self.width*.075,label.pos[1]+self.height*.075],size=[label.size[0]*.85,label.size[1]*.85],radius=[30])
    
    def returnMenu(self,btn):
        screenManager.switch_to(menuS,direction="right")

menuS = menuScreen(name='menuScreen')
class androidApp(MDApp):
    def build(self):
        screenManager.add_widget(menuS)
        return screenManager

if __name__ == '__main__':
    androidApp().run()