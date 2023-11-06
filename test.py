import socket


class App:
    def __init__(self):
        self.active_display1 = True
        self.active_display2 = True

    def reboot(self):
        ...

    def off_display1(self):
        self.active_display1 = False

    def on_display1(self):
        self.active_display1 = True

    def off_display2(self):
        self.active_display2 = False

    def on_display2(self):
        self.active_display2 = True

    def clicked(self, click):
        print(f'click: {click}')


application = App()