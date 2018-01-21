import tkinter as tk
import subprocess
import serial


class Connection:
    def __init__(self, parent):
        self.parent = parent
        parent_frame = self.parent.get_frame()
        self.size_frame = tk.Frame(parent_frame)
        self.size_frame.grid(row=0)
        self.model_frame = tk.Frame(parent_frame)
        self.model_frame.grid(row=1)
        self.connect_frame = tk.Frame(parent_frame)
        self.connect_frame.grid(row=2)

        self.ports_listbox = tk.Listbox(self.connect_frame)
        self.cols_edit = tk.Entry(self.size_frame)
        self.rows_edit = tk.Entry(self.size_frame)

        self.model = []

    def draw(self):

        self.cols_edit.delete(0, tk.END)
        self.cols_edit.insert(0, "4")
        self.rows_edit.delete(0, tk.END)
        self.rows_edit.insert(0, "3")
        tk.Label(self.size_frame, text="Rows: ").grid(row=0)
        self.rows_edit.grid(row=0, column=1)
        tk.Label(self.size_frame, text="Columns: ").grid(row=1)
        self.cols_edit.grid(row=1, column=1)
        change_size_button = tk.Button(self.size_frame, text="change size", width=10, command=self.change_size())
        change_size_button.grid(row=2)

        self.change_size()()

        available_serials = get_available_serials()
        for i in range(len(available_serials)):
            self.ports_listbox.insert(i + 1, available_serials[i])

        tk.Label(self.connect_frame, text="Port: ").grid(row=0)
        self.ports_listbox.grid(row=0, column=1)
        connect_button = tk.Button(self.connect_frame, text="connect", width=10, command=self.connect())
        connect_button.grid(row=1)

    def change_size(self):
        def f():
            for child in self.model_frame.winfo_children():
                child.destroy()
            tk.Label(self.model_frame, text="Leave selected checkboxes \nwhere you have leds: ").grid(row=1)

            rows_count = int(self.rows_edit.get())
            cols_count = int(self.cols_edit.get())
            self.model = []
            start_row = 2
            for i in range(rows_count):
                self.model.append([1] * cols_count)
                for j in range(cols_count):
                    port = i * cols_count + j
                    var = tk.IntVar(value=1)
                    chb = tk.Checkbutton(self.model_frame, text=str(port), variable=var,
                                         command=self.checkbox_changed(i, j, var))
                    chb.grid(row=start_row + i, column=j + 1)

        return f

    def connect(self):
        def f():
            com_port = self.ports_listbox.get(tk.ACTIVE)
            ser = serial.Serial(com_port)
            print("connected to :" + ser.name)

            self.parent.on_connect(ser, self.model)
            self.size_frame.destroy()
            self.model_frame.destroy()
            self.connect_frame.destroy()

        return f

    def checkbox_changed(self, i, j, var):
        def f():
            self.model[i][j] = var.get()

        return f


def get_available_serials():
    ports_string = subprocess.check_output(['python', '-m', 'serial.tools.list_ports']).decode("utf-8").strip()
    print("FOUND: " + ports_string)
    if len(ports_string) == 0:  # TODO: REMOVE ME: stub to debug without any ports
        print("stubs used as no ports found")
        return ["/dev/ttyUSB0", "/dev/ttyUSB1"]
    return ports_string.split('\n')
