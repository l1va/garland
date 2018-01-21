
class Awesome:
    def __init__(self, main):
        self.main = main

    def do(self):
        self.awesome_on(0)

    def awesome_on(self, i):
        self.main.select(i)
        if i == self.main.last_check_ind:
            self.main.top.after(2000, self.awesome_off, self.main.last_check_ind)
        else:
            self.main.top.after(2000, self.awesome_on, i + 1)

    def awesome_off(self, i):
        self.main.deselect(i)
        if i > 0:
            self.main.top.after(2000, self.awesome_off, i - 1)