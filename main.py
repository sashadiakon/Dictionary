from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import (Color, Ellipse, Rectangle, Line, Translate, Scale)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.config import Config
from kivy.uix.label import Label
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager , Screen
from kivy.properties import ListProperty
from kivy.config import Config
from aiogoogletrans import Translator
import asyncio
import json
import random
translator = Translator()
loop = asyncio.get_event_loop()
# loop.run_until_complete(translator.translate("Good", src = "ru"))

wp = 5
height = 630
width = 800

Config.set("graphics", "width", width)
Config.set("graphics", "height", height)
Config.set("graphics", "resizble", 0)

class WhiteBack(Widget):
    def __init__(self, **kwargs):
        super(WhiteBack, self).__init__(**kwargs)
        with self.canvas:
            Color(.7,.7,.7,1)
            Rectangle(pos = (0, 0), size = (1000, 1000))
class StartScreen(Screen, Widget):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        bl = BoxLayout(orientation = "vertical", padding = 140, spacing = 50 )
        btn_trans = Button(text = "Translate and add new",\
font_size = 24,background_color = (.6, .6, .8, 1), on_press = self.trans)
        btn_train = Button(text = "Train words",\
font_size = 24, background_color = (.6, .6, .8, 1), on_press = self.train)
        bl.add_widget(btn_trans)
        bl.add_widget(btn_train)
        self.add_widget(WhiteBack())
        self.add_widget(bl)
    def trans(self, instance):
        global sm
        sm.current = "translate"
    def train(self, instance):
        global sm
        sm.current = "train"
class TranslateScreen(Screen, Widget):
    def __init__(self, **kwargs):
        super(TranslateScreen, self).__init__(**kwargs)
        fl = FloatLayout(size = (800, 630))
        btn = Button(text = "Translate \n by yourself",\
font_size = 16, on_press = self.yourself,\
pos_hint = {"x":.79 , "y": .84}, size_hint = (.2, .15))
        self.input = TextInput(text = "", font_size = 32, \
size_hint = (.8, .4), pos_hint = {"x": .1, "y": .35})
        btn2 = Button(text = "Translate", font_size = 12,\
on_press = self.translate, size_hint = (.6, .15),\
pos_hint = {"x": .2, "y": .1})
        btn_back = Button(text = "Back", font_size = 24,\
on_press = self.back,\
size_hint=(.15, .15), pos_hint={"x": 0, "y": .85})
        fl.add_widget(btn)
        fl.add_widget(self.input)
        fl.add_widget(btn2)
        fl.add_widget(btn_back)
        self.add_widget(WhiteBack())
        self.add_widget(fl)

    def yourself(self, instance):
        global sm
        sm.current = "your"
    def translate(self, instance):
        global translator, loop
        tr = loop.run_until_complete(translator.translate(self.input.text, src="en", dest = "ru"))
        print(tr.origin)
        print(self.input.text)
        old_words = json.load(open("words.json"))
        old_words[tr.origin.strip()] = [tr.text]
        with open("words.json", "w") as file:
            file.write(json.dumps(old_words))
    def back(self, instance):
        global sm
        sm.current = "start"

class ChooseTrainScreen (Screen, Widget):
    def __init__(self, **kwargs):
        super(ChooseTrainScreen, self).__init__(**kwargs)
        bl = BoxLayout(orientation = "vertical", padding = 150, spacing = 50)
        btn_learn = Button(text = "Learn new", font_size = 36, \
on_press = self.go_learn)
        btn_repeat = Button(text = "Repeat old", font_size = 36, \
on_press = self.go_repeat)
        bl.add_widget(btn_learn)
        bl.add_widget(btn_repeat)
        self.add_widget(WhiteBack())
        self.add_widget(bl)
    def go_learn(self, instance):
        global sm
        sm.current = "test"
    def go_repeat(self, instance):
        global sm
        sm.current = "repeat"


class TestScreen(Screen, Widget):
    def __init__(self, **kwargs):
        super(TestScreen, self).__init__(**kwargs)
        self.fl = FloatLayout()
        bl = BoxLayout(size_hint = (1, .1), pos_hint = {"x": 0, "y": .875}, padding = 10, spacing = 7)


        self.gener = False

        self.number_input = TextInput(font_size = 24)
        btn_generate = Button(text = "Generate", font_size = 24,\
on_press = self.generate)
        btn_verify = Button(text = "Complete", font_size = 24, background_color = (1, .2, .2, 1),
on_press = self.verify)
        btn_learn =  Button(text = "Learning", font_size = 24, background_color = (.8, 1, 0, 1), \
on_press = self.learn)
        bl.add_widget(self.number_input)
        bl.add_widget(btn_generate)
        bl.add_widget(btn_verify)
        bl.add_widget(btn_learn)
        self.fl.add_widget(bl)
        self.add_widget(WhiteBack())
        self.add_widget(self.fl)
    def generate(self, instance):
        self.gener = True
        self.grid = GridLayout(size_hint = (1, .875), cols = 3, spacing = [0, 20])
        n = int(self.number_input.text)
        words = json.load(open("words.json"))
        if n > 15 :
            n = 15
        if n > len(words):
            n = len(words)

        rand = random.sample(range(len(words)), n)
        print(words)
        self.answers = []
        self.list_inp = []
        self.lbls = []
        for i in rand:
            tr = list(words.values())[i][0]
            self.answers.append(list(words.keys())[i])
            print(tr)
            input = TextInput(font_size = 32)
            self.list_inp.append(input)
            self.grid.add_widget(Label(text = tr.title() + " -", font_size = 36))
            self.grid.add_widget(input)
            lbl = Label(text = list(words.keys())[i], font_size = 32, color = (.4, 1, .3, 1), opacity = 0)
            self.lbls.append(lbl)
            self.grid.add_widget(lbl)
        print(self.answers)
        print(self.list_inp)
        self.fl.add_widget(self.grid)
    def verify(self, instance):
        print(2)
        if self.gener:
            print(len(self.answers), len(self.list_inp))
            for i in range(0, len(self.answers)):
                print(self.answers[i], self.list_inp[i].text)
                if self.answers[i] == self.list_inp[i].text:
                    self.list_inp[i].background_color = (.4, 1, .3, 1)
                else:
                    self.list_inp[i].background_color = (1, .2, .2, 1)
            for b in self.lbls:
                b.opacity = 1
        else:
            pass
    def learn(self, instance):
        global sm
        sm.current = "learn"

class RepeatScreen(Screen, Widget):
    def __init__(self, **kwargs):
        super(RepeatScreen, self).__init__(**kwargs)
        self.fl = FloatLayout()
        bl = BoxLayout(size_hint=(1, .1), pos_hint={"x": 0, "y": .875}, padding=10, spacing=7)

        self.gener = False

        self.number_input = TextInput(font_size=24)
        btn_generate = Button(text="Generate", font_size=24, \
                              on_press=self.generate)
        btn_verify = Button(text="Complete", font_size=24, background_color=(1, .2, .2, 1),
                            on_press=self.verify)
        btn_learn = Button(text="Learning", font_size=24, background_color=(.8, 1, 0, 1), \
                           on_press=self.learn)
        bl.add_widget(self.number_input)
        bl.add_widget(btn_generate)
        bl.add_widget(btn_verify)
        bl.add_widget(btn_learn)
        self.fl.add_widget(bl)
        self.add_widget(WhiteBack())
        self.add_widget(self.fl)

    def generate(self, instance):
        self.gener = True
        self.grid = GridLayout(size_hint=(1, .875), cols=3, spacing=[0, 20])
        n = int(self.number_input.text)
        words = json.load(open("words.json"))
        if n > 15:
            n = 15
        if n > len(words):
            n = len(words)

        rand = random.sample(range(len(words)), n)
        print(words)
        self.answers = []
        self.list_inp = []
        self.lbls = []
        for i in rand:
            tr = list(words.values())[i][0]
            self.answers.append(list(words.keys())[i])
            print(tr)
            input = TextInput(font_size=32)
            self.list_inp.append(input)
            self.grid.add_widget(Label(text=tr.title() + " -", font_size=36))
            self.grid.add_widget(input)
            lbl = Label(text=list(words.keys())[i], font_size=32, color=(.4, 1, .3, 1), opacity=0)
            self.lbls.append(lbl)
            self.grid.add_widget(lbl)
        print(self.answers)
        print(self.list_inp)
        self.fl.add_widget(self.grid)

    def verify(self, instance):
        print(2)
        if self.gener:
            print(len(self.answers), len(self.list_inp))
            for i in range(0, len(self.answers)):
                print(self.answers[i], self.list_inp[i].text)
                if self.answers[i] == self.list_inp[i].text:
                    self.list_inp[i].background_color = (.4, 1, .3, 1)
                else:
                    self.list_inp[i].background_color = (1, .2, .2, 1)
            for b in self.lbls:
                b.opacity = 1
        else:
            pass

    def learn(self, instance):
        global sm
        sm.current = "learn"

class LearnScreen(Screen, Widget):
    def __init__(self, **kwargs):
        super(LearnScreen, self).__init__(**kwargs)
        global wp
        fl = FloatLayout()
        bl = BoxLayout(pos_hint = {"x": 0,"y": 0}, size_hint = (1, 0.15), padding = 10)
        btn_first = Button(text = "First", font_size = 24, on_press = self.first)
        btn_next = Button(text = "Next", font_size = 24, on_press = self.next)
        btn_test = Button(text = "Dictation", font_size = 24, on_press = self.test)
        bl.add_widget(btn_first)
        bl.add_widget(btn_next)
        bl.add_widget(btn_test)
        words = json.load(open("words.json"))

        self.n = 1
        self.n_max = int(len(list(words.keys())) / wp)
        if isinstance(self.n_max, int):
            self.n_max +=1
        self.grid = GridLayout(cols = 2, pos_hint = {"x": 0,"y": 0.15}, size_hint = (1,0.85))
        words1 = list(words.keys())[0: wp]
        for i in words1:
            self.grid.add_widget(Label(text = i))
            self.grid.add_widget(Label(text = words[i][0]))
        fl.add_widget(bl)
        fl.add_widget(self.grid)
        self.add_widget(fl)
    def test(self, instance):
        global sm
        sm.current = "test"
    def first(self, instance):
        self.n = 1
        self.grid.clear_widgets()
        words = json.load(open("words.json"))
        words1 = list(words.keys())[0: wp]
        for i in words1:
            self.grid.add_widget(Label(text=i))
            self.grid.add_widget(Label(text=words[i][0]))

    def next(self, instance):
        if self.n < self.n_max:
            self.grid.clear_widgets()
            words = json.load(open("words.json"))
            self.n += 1
            wordsn = list(words.keys())[wp * (self.n - 1): wp * self.n]
            for i in wordsn:
                self.grid.add_widget(Label(text=i))
                self.grid.add_widget(Label(text=words[i][0]))
class YourselfScreen(Screen, Widget):
    def __init__(self, **kwargs):
        super(YourselfScreen, self).__init__(**kwargs)
        fl = FloatLayout()
        btn_back = Button(text = "Back", font_size = 24, \
on_press = self.back, \
size_hint = (.15, .15), pos_hint={"x": 0, "y": .85})

        lbl_or = Label(text = "Origin", font_size = 32, \
size_hint = (.2, .2), pos_hint = {"x": .4, "y": .7})
        self.input_or = TextInput(font_size = 32, \
size_hint = (.8, .15), pos_hint = {"x": .1, "y": .6})

        lbl_tr = Label(text="Translation", font_size = 32, \
size_hint = (.2, .1), pos_hint = {"x": .4, "y": .45})
        self.input_tr = TextInput(font_size = 32, \
size_hint = (.8, .15), pos_hint = {"x": .1, "y": .3})

        btn_save = Button(text = "Save",\
font_size = 24, on_press = self.save, \
size_hint = (.5, .15), pos_hint = {"x": .25, "y": .1})
        fl.add_widget(btn_back)
        fl.add_widget(lbl_or)
        fl.add_widget(self.input_or)
        fl.add_widget(lbl_tr)
        fl.add_widget(self.input_tr)
        fl.add_widget(btn_save)
        self.add_widget(WhiteBack())
        self.add_widget(fl)
    def save(self, instance):
        global sm
        origin = self.input_or.text.strip()
        translation = self.input_tr.text.strip()
        old_words = json.load(open("words.json"))
        old_words[origin] = [translation]
        with open("words.json", "w") as file:
            file.write(json.dumps(old_words))
        sm.current = "start"
    def back(self, instance):
        global sm
        sm.current = "start"

sm = ScreenManager()
sm.add_widget(StartScreen(name = "start"))
sm.add_widget(TranslateScreen(name = "translate"))
sm.add_widget(ChooseTrainScreen(name = "train"))
sm.add_widget(YourselfScreen(name = "your"))
sm.add_widget(RepeatScreen(name = "repeat"))
sm.add_widget(TestScreen(name = "test"))
sm.add_widget(LearnScreen(name = "learn"))
sm.current = "start"

class My_App(App):
    def build(self):
        return sm
My_App().run()