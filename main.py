import tkinter as tk
import connection_frame


class Main:
    def __init__(self):
        self.serial = None
        self.top = tk.Tk()

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


def checkbox_changed(port, var, ser):
    def f():
        to_send = str(port)
        if var.get() == 1:
            to_send += "+"
            print("checked " + str(port))
        else:
            to_send += "-"
            print("unchecked " + str(port))
        to_send += "\n"
        ser.write(to_send.encode("utf-8"))
        ser.flush()

    return f


def main():
    Main().start()


main()
