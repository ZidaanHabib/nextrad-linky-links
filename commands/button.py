from interfaces.command_interface import ICommand


class Button:

    def __init__(self, command: ICommand):
        self.command = command

    def press(self, *args):
        self.command.execute(*args)
