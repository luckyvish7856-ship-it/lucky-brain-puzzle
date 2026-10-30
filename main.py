
__version__ = "1.0.0"

import random
from kivy.app import App
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.metrics import dp

Window.clearcolor = (0.04, 0.06, 0.12, 1)

THEMES = {
    "Blue": (0.08, 0.16, 0.32, 1),
    "Green": (0.05, 0.25, 0.16, 1),
    "Purple": (0.20, 0.08, 0.30, 1),
    "Red": (0.30, 0.07, 0.08, 1),
    "Gold": (0.30, 0.22, 0.04, 1),
}

class BrainPuzzle(App):
    def build(self):
        self.store = JsonStore("player.json")
        if not self.store.exists("data"):
            self.store.put("data", score=0, coins=0, level=1,
                           theme="Blue", best=0, last_reward="")

        self.data = self.store.get("data")
        self.score = self.data["score"]
        self.coins = self.data["coins"]
        self.level = self.data["level"]
        self.theme = self.data["theme"]
        self.best = self.data["best"]

        self.root = BoxLayout(orientation="vertical",
                              padding=dp(14), spacing=dp(10))
        self.root.add_widget(Label(
            text="[b]LUCKY BRAIN PUZZLE PRO[/b]",
            markup=True, font_size="25sp", size_hint_y=None,
            height=dp(65)))

        self.info = Label(font_size="17sp", size_hint_y=None,
                          height=dp(35))
        self.root.add_widget(self.info)

        self.question = Label(text="दिमागी खेल में आपका स्वागत है!",
                              font_size="23sp", halign="center")
        self.root.add_widget(self.question)

        self.answer = TextInput(
            hint_text="अपना जवाब लिखें",
            multiline=False, input_filter="int",
            font_size="22sp", size_hint_y=None, height=dp(55),
            halign="center")
        self.root.add_widget(self.answer)

        self.check_btn = self.make_button("जवाब चेक करें", self.check)
        self.root.add_widget(self.check_btn)

        self.message = Label(text="", font_size="18sp")
        self.root.add_widget(self.message)

        self.root.add_widget(self.make_button("नया सवाल", self.new_question))
        self.root.add_widget(self.make_button("दुकान / Themes", self.shop))
        self.root.add_widget(self.make_button("Daily Reward", self.reward))
        self.root.add_widget(self.make_button("Player Profile", self.profile))

        self.new_question()
        self.update_info()
        return self.root

    def make_button(self, text, callback):
        b = Button(text=text, font_size="18sp",
                   size_hint_y=None, height=dp(52),
                   background_normal="", background_color=(0.12, 0.42, 0.78, 1))
        b.bind(on_release=callback)
        return b

    def save(self):
        self.store.put("data", score=self.score, coins=self.coins,
                       level=self.level, theme=self.theme,
                       best=self.best, last_reward=self.data["last_reward"])

    def update_info(self):
        self.root.background_color = THEMES[self.theme]
        self.info.text = (
            f"⭐ Score: {self.score}    🪙 Coins: {self.coins}    "
            f"Level: {self.level}"
        )

    def new_question(self, *args):
        self.a = random.randint(2, 12 + self.level)
        self.b = random.randint(2, 12 + self.level)
        self.op = random.choice(["+", "-", "×"])
        if self.op == "+":
            self.correct = self.a + self.b
        elif self.op == "-":
            self.correct = self.a - self.b
        else:
            self.correct = self.a * self.b
        self.question.text = f"{self.a} {self.op} {self.b} = ?"
        self.answer.text = ""
        self.message.text = ""

    def check(self, *args):
        if not self.answer.text.strip():
            self.message.text = "पहले जवाब लिखो!"
            return
        try:
            value = int(self.answer.text)
        except ValueError:
            self.message.text = "सही नंबर लिखो!"
            return

        if value == self.correct:
            self.score += 10
            self.coins += 5
            self.best = max(self.best, self.score)
            if self.score >= self.level * 50:
                self.level += 1
                self.message.text = "सही जवाब! नया Level खुल गया! 🎉"
            else:
                self.message.text = "बिल्कुल सही! +10 Score, +5 Coins"
            self.save()
            self.update_info()
            self.new_question()
        else:
            self.message.text = "फिर कोशिश करो! जवाब गलत है।"

    def shop(self, *args):
        box = BoxLayout(orientation="vertical", padding=dp(10),
                        spacing=dp(7))
        pop = Popup(title="Theme Shop", content=box,
                    size_hint=(0.9, 0.8))
        for name in THEMES:
            if name == self.theme:
                label = " (चालू)"
            elif name == "Blue":
                label = " (Free)"
            else:
                label = " (20 Coins)"
            btn = Button(text=name + label, size_hint_y=None,
                         height=dp(48))
            btn.bind(on_release=lambda b, n=name: self.buy_theme(n, pop))
            box.add_widget(btn)
        box.add_widget(Button(text="बंद करें", size_hint_y=None,
                              height=dp(45), on_release=pop.dismiss))
        pop.open()

    def buy_theme(self, name, pop):
        if name != "Blue" and name != self.theme:
            if self.coins < 20:
                self.message.text = "इस Theme के लिए 20 Coins चाहिए।"
                return
            self.coins -= 20
        self.theme = name
        self.save()
        self.update_info()
        pop.dismiss()
        self.message.text = name + " Theme चुनी गई!"

    def reward(self, *args):
        from datetime import date
        today = str(date.today())
        if self.data["last_reward"] == today:
            self.message.text = "आज का Reward पहले ही मिल चुका है!"
            return
        self.coins += 20
        self.data["last_reward"] = today
        self.save()
        self.update_info()
        self.message.text = "Daily Reward: +20 Coins! 🎁"

    def profile(self, *args):
        text = (f"Player: Lucky\nScore: {self.score}\n"
                f"Best Score: {self.best}\nLevel: {self.level}\n"
                f"Coins: {self.coins}\nTheme: {self.theme}")
        Popup(title="Player Profile",
              content=Label(text=text, font_size="20sp"),
              size_hint=(0.85, 0.55)).open()

if __name__ == "__main__":
    BrainPuzzle().run()
