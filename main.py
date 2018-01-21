import tkinter as tk

import connection_frame
import awesome_example

class Main:
    def __init__(self):
        self.serial = None
        self.top = tk.Tk()
        self.checks = []
        self.last_check_ind = 0

    def start(self):
        connection_frame.Connection(self).draw()
        self.top.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.top.mainloop()

    def on_closing(self):
        if self.serial is not None:
            self.serial.close()
        self.top.destroy()

    def get_frame(self):
        return self.top

    def on_connect(self, ser, model):
        self.serial = ser
        ind = 0
        start_row = 1
        for i in range(len(model)):
            for j in range(len(model[0])):
                if model[i][j] == 1:
                    var = tk.IntVar()
                    chb = tk.Checkbutton(self.top, text=str(ind), variable=var,
                                         command=checkbox_changed(ind, var, self.serial))
                    chb.grid(row=start_row + i, column=j)
                    ind += 1
                    self.checks.append((chb, var))
        self.last_check_ind = ind - 1
        awesome_button = tk.Button(self.top, text="make awesome", width=10, command=self.algo_run)
        awesome_button.grid(row=start_row + len(model), column=len(model[0]))

    def select(self, i):
        self.serial.write(("+" + str(i)).encode("utf-8"))
        self.serial.flush()
        self.checks[i][0].select()

    def deselect(self, i):
        self.serial.write(("-" + str(i)).encode("utf-8"))
        self.serial.flush()
        self.checks[i][0].deselect()

    def state(self, i):
        return self.checks[i][1].get()

    def toggle(self, i):
        if self.state(i) == 1:
            self.deselect(i)
        else:
            self.select(i)

    def algo_run(self):
        awesome_example.Awesome(self).do()





def checkbox_changed(port, var, ser):
    def f():
        to_send = "-"
        if var.get() == 1:
            to_send = "+"
            print("checked " + str(port))
        else:
            to_send = "-"
            print("unchecked " + str(port))
        to_send += str(port) + "\n"
        ser.write(to_send.encode("utf-8"))
        ser.flush()

    return f


def main():
    Main().start()


main()
