import socket


class App:
    def __init__(self):
        self.active_display = True

    def reboot(self):
        ...

    def off_display(self):
        self.active_display = False

    def on_display(self):
        self.active_display = True

    def clicked(self, click):
        print(f'click: {click}')


application = App()