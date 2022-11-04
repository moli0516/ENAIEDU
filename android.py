__version__ = "1.0.0"
import kivy,socket,json,time
from kivymd.app import MDApp
from kivy.clock import Clock
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
from kivymd.toast import toast

Window.clearcolor = (1,1,1,1)
Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
Window.softinput_mode = "below_target"

StudentName = None
Sid = None

Builder.load_string("""
<Label>
    markup: True
    color: 0,0,0,1
""")

Papers = {
    'Reading':{
        'Mock':{
            "Paper1":'1'
        },
        'Assignment':{
            "Paper1":'1'
        },
        'Self practice':{
            "Paper1":'1'
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

class client():
    def __init__(self):
        super().__init__()
        self.serverPort = 1234
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connected = False
    def connect(self,serverIP='123.202.82.205'):
        try:
            if not self.connected: self.socket.connect((serverIP,self.serverPort))
            self.connected = True
            return True
        except:
            showToast("Failed to connect server")
            return False
    def send(self,data):
        try:
            sended = self.socket.send(json.dumps(data).encode('utf-8')+b'\r\nSocketEnd\r\n')
            if not sended:return False
            return self.recv()
        except:
            pass
    def recv(self):
        try:
            data = b""
            while True:
                d = self.socket.recv(2)
                data += d
                if data.endswith(b'\r\nSocketEnd\r\n'):break
            return json.loads(data.decode('utf-8')[:-13])
        except Exception as e:
            print(e)
            return False
    def close(self,*a):
        self.socket.close()


def word_tokenize(string):# Cant import nltk word_tokenize in android qwq
    res = ['']
    chars = [*string]
    for c in chars:
        if c in "~!@#$%^&*()_+{}|:\"<>?`-=[]\;',./" and res[-1] != '': res.extend([c,''])
        elif c == ' ':res.append('') if res[-1] != '' else ''
        else:res[-1] += c
    return res[:-1] if res[-1] == '' else res

def renderBG(elem,value,radius=None):
    elem.canvas.before.clear()
    with elem.canvas.before:
        Color(elem.bgColor[0]/255,elem.bgColor[1]/255,elem.bgColor[2]/255,elem.bgColor[3])
        RoundedRectangle(pos=elem.pos,size=elem.size,radius=radius) if radius else Rectangle(pos=elem.pos,size=elem.size)

def showToast(text,duration=2.5):
    if platform == 'android': toast(text=text,gravity=80,length_long=duration)
    else: toast(text=text,duration=duration)

def disableTextBox(box,value):
    box.text = value

class menuScreen(Screen):
    def __init__(self, **kwargs):
        super(menuScreen,self).__init__(**kwargs)
        self.titleLabel = Label(text='[b]ENAI EDU[/b]',font_size='30dp',pos_hint={'x':.0,'y':.9},size_hint=(1,.1))#,background_color=(1,1,1,1)=
        self.titleLabel.bgColor = (42,196,240,.8)
        self.titleLabel.bind(pos=renderBG)
        self.renderLogin()
    def renderLogin(self):
        self.add_widget(self.titleLabel)
        loginBG = Label(pos_hint={'x':.15,'y':0.3},size_hint=(.7,.4))
        loginBG.bgColor = (127,127,127,.3)
        loginBG.bind(pos=lambda a,b:renderBG(a,b,[20]))
        serverIPLabel = Label(text="Server IP:",pos_hint={'x':-.2,'y':.15})
        serverIPBox = TextInput(text="123.202.82.205",size_hint=(.6,.05),pos_hint={'x':.2,'y':.58},multiline=False)
        sidLabel = Label(text="Students ID:",pos_hint={'x':-.2,'y':.06})
        sidBox = TextInput(hint_text="220000000",size_hint=(.6,.05),pos_hint={'x':.2,'y':.49},multiline=False)
        passwLabel = Label(text="password:",pos_hint={'x':-.2,'y':-.03})
        passwBox = TextInput(size_hint=(.6,.05),pos_hint={'x':.2,'y':.40},multiline=False)
        loginBtn = Button(text="Login",size_hint=(.2,.05),pos_hint={'x':.6,'y':.3})
        def onLoginBtnPressed(btn):
            btn.disabled = True
            Clock.schedule_once(lambda *a:self.login(btn,serverIPBox.text,sidBox.text,passwBox.text),.1)
        loginBtn.bind(on_press=onLoginBtnPressed)
        self.add_widget(loginBG)
        self.add_widget(serverIPLabel)
        self.add_widget(serverIPBox)
        self.add_widget(sidLabel)
        self.add_widget(sidBox)
        self.add_widget(passwLabel)
        self.add_widget(passwBox)
        self.add_widget(loginBtn)
    def login(self,btn,serverIP,sid,passw):
        global StudentName,Sid
        if not sid or not passw:
            btn.disabled = False
            return showToast(text="Missing studentID or password")
        if not socketClient.connect(serverIP):
            btn.disabled = False
            return showToast(text="Incorrect Server IP or server offline")
        data = socketClient.send({'task':'login','sid':sid,'passw':passw})
        if not data or not data['state']:
            btn.disabled = False
            return showToast(text="Incorrect studentID or password")
        showToast('Login successful')
        StudentName = data['name']
        Sid = sid
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
        scrollBox = ScrollView(pos_hint={'x':.15,'y':0.3},size_hint=(.7,.38))
        scrollBoxBG = Label(pos_hint={'x':.15,'y':0.3},size_hint=(.7,.38))
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
        self.titleLabel = Label(text=self.ttype+' '+self.ptype+' '+self.paper,font_size='23dp',pos_hint={'x':.0,'y':.9},size_hint=(1,.1))
        self.exitBtn = Button(text="<<Exit",font_size='20dp',pos_hint={'x':.05,'y':.9},size_hint=(.1,.08),background_normal='',background_down='',background_color=(1,1,1,1))
        self.exitBtn.bind(on_press=self.returnMenu)
        self.add_widget(self.titleLabel)
        self.add_widget(self.exitBtn)
        waitingPaperLabel = Label(text="Getting Paper...",font_size="25dp")
        self.add_widget(waitingPaperLabel)
        if self.ttype == "Writing": self.renderWritingUploadScreen()
        else: 
            def startQuestion(*a):
                data = socketClient.send({'task':'getpaper',"paperType":self.ptype,"paper":Papers[self.ttype][self.ptype][self.paper]})
                if not data:
                    waitingPaperLabel.text = "Error: Cant connect to server"
                else:
                    self.remove_widget(waitingPaperLabel)
                    self.paperText = data['text']
                    self.questions = data['questions']
                    self.renderReadingScreen()
            Clock.schedule_once(startQuestion,.5)
    def renderReadingScreen(self):
        self.textBox = TextInput(text=self.paperText,font_size='20dp',pos_hint={'x':.1,'y':.45},size_hint=(.8,.45))
        self.textBox.do_cursor_movement("cursor_home",True)
        self.textBox.bind(text=lambda a,b:disableTextBox(a,self.paperText))
        self.previousBtn = Button(text="<=Previous",font_size='20dp',pos_hint={'x':.15,'y':.05},size_hint=(.18,.08),disabled=True)
        self.nextBtn = Button(text="Next=>",font_size='20dp',pos_hint={'x':.67,'y':.05},size_hint=(.18,.08),disabled=True)
        self.previousBtn.bind(on_press=self.previousQuestion)
        self.nextBtn.bind(on_press=self.nextQuestion)
        self.add_widget(self.textBox)
        self.add_widget(self.previousBtn)
        self.add_widget(self.nextBtn)
        self.questionsElem = []
        for question in self.questions:
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
                    ansBox = CheckBox(size_hint=(.1,.1),group=self.paper+'Q'+str(self.questions.index(question)+1))
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
            question = self.questions[i]
            pscore += int(question['score'])
            addScore = 0
            if question['type'] == "short" or question['type'] == "MC":
                addScore = int(question['score']) if ans == question['answer'] else 0
            elif question['type'] == "long":
                reqKeypoint = question['keypoint']
                print(word_tokenize(ans),ans)
                for word in word_tokenize(ans):
                    if word in reqKeypoint: #keypoint found
                        addScore += 1
            if addScore == 0: advises.append(question['advise'])
            score += addScore
        if score / pscore > 0.6: grade = "A"
        elif score / pscore > 0.5: grade = "B"
        elif score / pscore > 0.4: grade = "C"
        else: grade = "D"
        self.sendReport(grade,score,pscore)
        self.showResult(grade,advises)
    def resultPageResizeText(self,text):
        t = ""
        count = 0
        words = text.split(' ')
        for w in words:
            added = count + len(w)
            count = added if added <=20 else 0
            t += ('\n'+w+' ' if added >20 and w != words[-1] else w+' ')
        return t
    def showResult(self,grade,showText,writing=None,correction=None):
        self.clear_widgets()
        bg = Label(size_hint=(1,1))
        bg.bind(size=self.renderScoreBG)
        confirmBtn = Button(text="confirm",font_size='19dp',pos_hint={'x':.4,'y':.15},size_hint=(.2,.05))
        confirmBtn.bind(on_press=self.returnMenu)
        gridBox = GridLayout(cols=1,spacing=2,size_hint_y=None)
        gridBox.bind(minimum_height=gridBox.setter('height'))
        scrollBoxSize = (.7,.28) if self.ttype == "Writing" else (.7,.4)
        scrollBoxPos = {'x':.15,'y':0.2} if self.ttype == "Writing" else {'x':.15,'y':0.3}
        scrollBox = ScrollView(pos_hint=scrollBoxPos,size_hint=scrollBoxSize)
        scrollBoxBG = Label(pos_hint=scrollBoxPos,size_hint=scrollBoxSize)
        scrollBoxBG.bgColor = (127,127,127,.3)
        scrollBoxBG.bind(pos=lambda a,b:renderBG(a,b,[20]))
        
        for i in range(len(showText)):
            text = self.resultPageResizeText(showText[i])
            textLabel = Label(text=str(i+1)+'. '+text,font_size='15dp',size_hint=(.5,None))
            if platform == 'android': textLabel.height=self.height*.1
            gridBox.add_widget(textLabel)
        scrollBox.add_widget(gridBox)
        self.add_widget(bg)
        self.add_widget(self.titleLabel)
        self.add_widget(Label(text=('Final Grade: '+str(grade) if grade else "Final Result"),font_size='25dp',pos_hint={'x':0,'y':.35}))
        self.add_widget(scrollBox)
        self.add_widget(scrollBoxBG)
        self.add_widget(confirmBtn)
        if correction:
            writingBox = TextInput(text=writing,font_size='16dp',pos_hint={'x':.15,'y':.55},size_hint=scrollBoxSize)
            writingBox.bind(text=lambda a,b:disableTextBox(a,writing))
            self.add_widget(writingBox)
            writingBox.do_cursor_movement("cursor_home",True)
            gridBox = GridLayout(cols=1,spacing=2,size_hint_y=None)
            gridBox.bind(minimum_height=gridBox.setter('height'))
            scrollBox1 = ScrollView(pos_hint=scrollBoxPos,size_hint=scrollBoxSize)
            text = self.resultPageResizeText(correction)
            if platform == 'android':
                text = text.split('\n\n')
                for t in text:
                    correctionLabel = Label(text=t,font_size='15dp',size_hint=(.5,None),valign="top")
                    correctionLabel.height = len(t.split('\n'))*(self.height*(.1/4))
                    gridBox.add_widget(correctionLabel)
            else:
                correctionLabel = Label(text=text,font_size='15dp',size_hint=(.5,None),valign="top")
                correctionLabel.height = len(text.split('\n'))*18
                gridBox.add_widget(correctionLabel)
            scrollBox1.add_widget(gridBox)
            mistakesBtn = Button(text="Mistakes",font_size='17dp',pos_hint={'x':.25,'y':.5},size_hint=(.19,.05),disabled_color=(0,0,0,1))
            mistakesBtn.disabled = True
            correctionBtn = Button(text="Suggestion",font_size='17dp',pos_hint={'x':.57,'y':.5},size_hint=(.19,.05),disabled_color=(0,0,0,1))
            def changeBtnState(btn,btn1):
                btn.disabled = True
                btn1.disabled = False
            mistakesBtn.bind(on_press=lambda a:changeBtnState(a,correctionBtn))
            correctionBtn.bind(on_press=lambda a:changeBtnState(a,mistakesBtn))
            pages = [scrollBox,scrollBox1]
            def changePage(btn,page):
                self.remove_widget(pages[page])
                self.remove_widget(pages[int(not page)])
                self.add_widget(pages[page])
            mistakesBtn.bind(on_press=lambda a:changePage(a,0))
            correctionBtn.bind(on_press=lambda a:changePage(a,1))
            self.add_widget(mistakesBtn)
            self.add_widget(correctionBtn)
        else:
            self.add_widget(Label(text=('Advices:' if self.ttype != "Writing" else "Mistakes:"),font_size="17dp",pos_hint={'x':0,'y':0.25}))
    def renderWritingUploadScreen(self):
        writingBox = TextInput(hint_text="Paste your writing here",font_size='16dp',pos_hint={'x':.1,'y':.45},size_hint=(.8,.45))
        confirmBtn = Button(text="^Submit^",font_size='19dp',pos_hint={'x':.4,'y':.15},size_hint=(.2,.1))
        confirmBtn.disabled = True
        def onBoxInput(box,value):
            confirmBtn.disabled = not value
        writingBox.bind(text=onBoxInput)
        confirmBtn.bind(on_press=lambda a:self.calcWritingResult(writingBox.text))
        self.add_widget(writingBox)
        self.add_widget(confirmBtn)
    def calcWritingResult(self,writing):
        self.clear_widgets()
        self.add_widget(self.titleLabel)
        self.add_widget(Label(text="Calculating Writing Result...",font_size="25dp"))
        def sendWriting(*a):
            data = socketClient.send({"task":"calcwriting","writing":writing})
            if not data:return
            print(data['mistakes'])
            print(data['correction'])
            self.showResult(None,data['mistakes'],writing,data['correction'])
        Clock.schedule_once(sendWriting,1)
    def sendReport(self,grade,score,pscore):
        socketClient.send({'task':'sendreport',"sid":Sid,"name":StudentName,"grade":grade,"score":str(score)+'/'+str(pscore)})
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

socketClient = client()

if __name__ == '__main__':
    Window.bind(on_request_close=socketClient.close)
    androidApp().run()