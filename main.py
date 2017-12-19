from tkinter import *
import subprocess
import serial

try:
    ports = subprocess.check_output(['python', '-m', 'serial.tools.list_ports']).split('\n')
except:
    ports = ["/dev/ttyUSB0", "/dev/ttyUSB1"]  # TODO: REMOVE ME: stub to debug without any ports

ard_ports = [i for i in range(16)]  # TODO: implement possibility to skip busy portrs

top = Tk()

ports_list = Listbox(top)
for i in range(len(ports)):
    ports_list.insert(i + 1, ports[i])

cols_edit = Entry(top)
cols_edit.delete(0, END)
cols_edit.insert(0, "4")
rows_edit = Entry(top)
rows_edit.delete(0, END)
rows_edit.insert(0, "3")

ser = None


def checkbox_changed(port, var):
    def f():
        if var.get() == 1:
            # ser.write(str(port) + "+\n") #TODO: uncomment me
            print("checked " + str(port))
        else:
            # ser.write(str(port) + "-\n") #TODO: uncomment me
            print("unchecked " + str(port))
            # ser.flush() #TODO: uncomment me

    return f


def connect():
    rows_count = int(rows_edit.get())
    cols_count = int(cols_edit.get())
    com_port = ports_list.get(ACTIVE)
    print("connect rows:" + str(rows_count) + " cols:" + str(cols_count) + " port:" + com_port)
    # ser = serial.Serial(com_port) #TODO: uncomment me
    # print("connected to :" + ser.name)

    ind = 0
    start_row = 4  # TODO: fix placing
    for i in range(rows_count):
        for j in range(cols_count):
            port = ard_ports[ind]
            var = IntVar()
            chb = Checkbutton(top, text=str(port), variable=var, command=checkbox_changed(port, var))
            chb.grid(row=start_row + i, column=j)
            ind += 1


connect_button = Button(top, text="connect", width=10, command=connect)

Label(top, text="Port: ").grid(row=0)
ports_list.grid(row=0, column=1)
Label(top, text="Rows: ").grid(row=1)
Label(top, text="Columns: ").grid(row=2)
rows_edit.grid(row=1, column=1)
cols_edit.grid(row=2, column=1)
connect_button.grid(row=3)


def on_closing():
    # ser.close() #TODO: uncomment me
    top.destroy()


top.protocol("WM_DELETE_WINDOW", on_closing)
top.mainloop()
