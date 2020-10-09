import sys
import os
import platform

from jpk_support import Jpk_support, AutoScroll, ScrolledText, JpkRequest
from tkinter import filedialog, messagebox

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    py3 = False
    import ttk
except ImportError:
    py3 = True
    import tkinter.ttk as ttk


def vp_start_gui():
    """
    Starting point when module is the main routine.
    """
    global val, w, root
    root = tk.Tk()
    top = MainWindow(root)
    Jpk_support.init(root, top)
    root.mainloop()


w = None


def create_MainWindow(rt, *args, **kwargs):
    '''Starting point when module is imported by another module.
       Correct form of call: 'create_MainWindow(root, *args, **kwargs)' .'''
    global w, w_win, root
    # rt = root
    root = rt
    w = tk.Toplevel(root)
    top = MainWindow(w)
    Jpk_support.init(w, top, *args, **kwargs)
    return (w, top)


def destroy_MainWindow():
    global w
    w.destroy()
    w = None


class MainWindow:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.', background=_bgcolor)
        self.style.configure('.', foreground=_fgcolor)
        self.style.map('.', background=
        [('selected', _compcolor), ('active', _ana2color)])

        top.geometry("638x723+759+98")
        top.minsize(120, 1)
        top.maxsize(3844, 1061)
        top.resizable(0, 0)
        top.title("JPKv7 Sender")
        top.iconbitmap('assets/ico.ico')
        top.configure(background="#d9d9d9")

        self.Labelframe1 = tk.LabelFrame(top)
        self.Labelframe1.place(relx=0.016, rely=0.014, relheight=0.159
                               , relwidth=0.962)
        self.Labelframe1.configure(relief='groove')
        self.Labelframe1.configure(foreground="black")
        self.Labelframe1.configure(text='''Krok 1:''')
        self.Labelframe1.configure(background="#d9d9d9")

        self.Button1 = tk.Button(self.Labelframe1, command=self.load_jpk_file)
        self.Button1.place(relx=0.782, rely=0.174, height=34, width=117
                           , bordermode='ignore')
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Wybierz JPK''')

        self.Button2 = tk.Button(self.Labelframe1, command=self.generate_initial_upload)
        self.Button2.place(relx=0.782, rely=0.609, height=34, width=117
                           , bordermode='ignore')
        self.Button2.configure(activebackground="#ececec")
        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(state='disabled')
        self.Button2.configure(background="#d9d9d9")
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(foreground="#000000")
        self.Button2.configure(highlightbackground="#d9d9d9")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(text='''Generuj''')

        self.Label1 = tk.Label(self.Labelframe1)
        self.Label1.place(relx=0.016, rely=0.174, height=21, width=78
                          , bordermode='ignore')
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(text='''Wybrany plik:''')

        self.Label2 = tk.Label(self.Labelframe1)
        self.Label2.place(relx=0.016, rely=0.348, height=21, width=400
                          , bordermode='ignore')
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(text='''Brak pliku''')

        self.Labelframe2 = tk.LabelFrame(top)
        self.Labelframe2.place(relx=0.016, rely=0.194, relheight=0.119
                               , relwidth=0.956)
        self.Labelframe2.configure(relief='groove')
        self.Labelframe2.configure(foreground="black")
        self.Labelframe2.configure(text='''Krok 2:''')
        self.Labelframe2.configure(background="#d9d9d9")

        self.Label3 = tk.Label(self.Labelframe2)
        self.Label3.place(relx=0.016, rely=0.233, height=61, width=594
                          , bordermode='ignore')
        self.Label3.configure(background="#d9d9d9")
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(text='''Podpisz wygenerowany plik podpisem kwalifikowanym lub profilem zaufanym.''')

        self.Labelframe3 = tk.LabelFrame(top)
        self.Labelframe3.place(relx=0.016, rely=0.318, relheight=0.145
                               , relwidth=0.956)
        self.Labelframe3.configure(relief='groove')
        self.Labelframe3.configure(foreground="black")
        self.Labelframe3.configure(text='''Krok 3:''')
        self.Labelframe3.configure(background="#d9d9d9")

        self.Button3 = tk.Button(self.Labelframe3, command=self.load_signed_file)
        self.Button3.place(relx=0.721, rely=0.19, height=34, width=153
                           , bordermode='ignore')
        self.Button3.configure(activebackground="#ececec")
        self.Button3.configure(activeforeground="#000000")
        self.Button3.configure(background="#d9d9d9")
        self.Button3.configure(disabledforeground="#a3a3a3")
        self.Button3.configure(foreground="#000000")
        self.Button3.configure(highlightbackground="#d9d9d9")
        self.Button3.configure(highlightcolor="black")
        self.Button3.configure(pady="0")
        self.Button3.configure(text='''Wybierz podpisany plik''')

        self.Button3_1 = tk.Button(self.Labelframe3, command=self.send_jpk)
        self.Button3_1.place(relx=0.721, rely=0.571, height=34, width=153
                             , bordermode='ignore')
        self.Button3_1.configure(activebackground="#ececec")
        self.Button3_1.configure(activeforeground="#000000")
        self.Button3_1.configure(background="#d9d9d9")
        self.Button3_1.configure(state='disabled')
        self.Button3_1.configure(disabledforeground="#a3a3a3")
        self.Button3_1.configure(foreground="#000000")
        self.Button3_1.configure(highlightbackground="#d9d9d9")
        self.Button3_1.configure(highlightcolor="black")
        self.Button3_1.configure(pady="0")
        self.Button3_1.configure(text='''Wyślij do MF''')

        self.Label4 = tk.Label(self.Labelframe3)
        self.Label4.place(relx=0.016, rely=0.19, height=31, width=84
                          , bordermode='ignore')
        self.Label4.configure(background="#d9d9d9")
        self.Label4.configure(disabledforeground="#a3a3a3")
        self.Label4.configure(foreground="#000000")
        self.Label4.configure(text='''Wybrany plik:''')

        self.Label5 = tk.Label(self.Labelframe3)
        self.Label5.place(relx=0.016, rely=0.476, height=21, width=400
                          , bordermode='ignore')
        self.Label5.configure(background="#d9d9d9")
        self.Label5.configure(disabledforeground="#a3a3a3")
        self.Label5.configure(foreground="#000000")
        self.Label5.configure(text="Brak pliku")

        self.Button3_3 = tk.Button(self.Labelframe3)
        self.Button3_3.place(relx=0.216, rely=3.857, height=101, width=253
                             , bordermode='ignore')
        self.Button3_3.configure(activebackground="#ececec")
        self.Button3_3.configure(activeforeground="#000000")
        self.Button3_3.configure(background="#d9d9d9")
        self.Button3_3.configure(disabledforeground="#a3a3a3")
        self.Button3_3.configure(foreground="#000000")
        self.Button3_3.configure(highlightbackground="#d9d9d9")
        self.Button3_3.configure(highlightcolor="black")
        self.Button3_3.configure(pady="0")
        self.Button3_3.configure(text='''Wybierz podpisany plik''')

        self.Labelframe4 = tk.LabelFrame(top)
        self.Labelframe4.place(relx=0.016, rely=0.47, relheight=0.214
                               , relwidth=0.956)
        self.Labelframe4.configure(relief='groove')
        self.Labelframe4.configure(foreground="black")
        self.Labelframe4.configure(text='''Krok 4:''')
        self.Labelframe4.configure(background="#d9d9d9")

        self.Listbox1 = tk.Listbox(self.Labelframe4)
        self.Listbox1.place(relx=0.016, rely=0.129, relheight=0.568
                            , relwidth=0.564, bordermode='ignore')
        self.Listbox1.configure(background="white")
        self.Listbox1.configure(disabledforeground="#a3a3a3")
        self.Listbox1.configure(font="TkFixedFont")
        self.Listbox1.configure(foreground="#000000")
        self.load_initial_data()

        self.Button4 = tk.Button(self.Labelframe4, command=self.get_status_jpk)
        self.Button4.place(relx=0.721, rely=0.135, height=34, width=157
                           , bordermode='ignore')
        self.Button4.configure(activebackground="#ececec")
        self.Button4.configure(activeforeground="#000000")
        self.Button4.configure(background="#d9d9d9")
        self.Button4.configure(disabledforeground="#a3a3a3")
        self.Button4.configure(foreground="#000000")
        self.Button4.configure(highlightbackground="#d9d9d9")
        self.Button4.configure(highlightcolor="black")
        self.Button4.configure(pady="0")
        self.Button4.configure(text='''Sprawdz''')

        self.Button4_4 = tk.Button(self.Labelframe4)
        self.Button4_4.place(relx=0.721, rely=0.484, height=34, width=157
                             , bordermode='ignore')
        self.Button4_4.configure(activebackground="#ececec")
        self.Button4_4.configure(activeforeground="#000000")
        self.Button4_4.configure(background="#d9d9d9")
        self.Button4_4.configure(disabledforeground="#a3a3a3")
        self.Button4_4.configure(foreground="#000000")
        self.Button4_4.configure(highlightbackground="#d9d9d9")
        self.Button4_4.configure(highlightcolor="black")
        self.Button4_4.configure(pady="0")
        self.Button4_4.configure(text='''Pobierz UPO''')

        self.Button5 = tk.Button(self.Labelframe4, command=self.removeListBox)
        self.Button5.place(relx=0.59, rely=0.129, height=24, width=38
                           , bordermode='ignore')
        self.Button5.configure(activebackground="#ececec")
        self.Button5.configure(activeforeground="#000000")
        self.Button5.configure(background="#d9d9d9")
        self.Button5.configure(disabledforeground="#a3a3a3")
        self.Button5.configure(foreground="#000000")
        self.Button5.configure(highlightbackground="#d9d9d9")
        self.Button5.configure(highlightcolor="black")
        self.Button5.configure(pady="0")
        self.Button5.configure(text='''Usuń''')

        self.Button6 = tk.Button(self.Labelframe4, command=self.add_item_ListBox)
        self.Button6.place(relx=0.508, rely=0.774, height=24, width=42
                           , bordermode='ignore')
        self.Button6.configure(activebackground="#ececec")
        self.Button6.configure(activeforeground="#000000")
        self.Button6.configure(background="#d9d9d9")
        self.Button6.configure(disabledforeground="#a3a3a3")
        self.Button6.configure(foreground="#000000")
        self.Button6.configure(highlightbackground="#d9d9d9")
        self.Button6.configure(highlightcolor="black")
        self.Button6.configure(pady="0")
        self.Button6.configure(text='''Dodaj''')

        self.Entry = tk.Entry(self.Labelframe4)
        self.Entry.place(relx=0.033, rely=0.774, height=20, relwidth=0.466
                         , bordermode='ignore')
        self.Entry.configure(background="white")
        self.Entry.configure(disabledforeground="#a3a3a3")
        self.Entry.configure(font="TkFixedFont")
        self.Entry.configure(foreground="#000000")
        self.Entry.configure(insertbackground="black")

        self.Scrolledtext = ScrolledText(top)
        self.Scrolledtext.place(relx=0.016, rely=0.705, relheight=0.284
                                , relwidth=0.964)
        self.Scrolledtext.configure(background="white")
        self.Scrolledtext.configure(font="TkTextFont")
        self.Scrolledtext.configure(foreground="black")
        self.Scrolledtext.configure(highlightbackground="#d9d9d9")
        self.Scrolledtext.configure(highlightcolor="black")
        self.Scrolledtext.configure(insertbackground="black")
        self.Scrolledtext.configure(insertborderwidth="3")
        self.Scrolledtext.configure(selectbackground="blue")
        self.Scrolledtext.configure(selectforeground="white")
        self.Scrolledtext.configure(wrap="none")

        self.jpk_file = None
        self.signed_file = None

    def load_initial_data(self):
        try:
            [self.appendListBox(line.strip()) for line in open("status.txt", 'r')]
        except FileNotFoundError:
            open("status.txt", "x")

    def save_data(self):
        with open('status.txt', 'w') as file:
            file.write('\n'.join(item for item in self.Listbox1.get(0, tk.END)))

    def appendScrollText(self, text):
        self.Scrolledtext.insert('1.0', text + '\n')

    def appendListBox(self, item):
        self.Listbox1.insert(0, item)
        self.save_data()

    def removeListBox(self):
        try:
            self.Listbox1.delete(self.Listbox1.index(self.Listbox1.curselection()))
            self.save_data()
        except:
            self.appendScrollText('Nie wybrano numeru')

    def load_jpk_file(self):
        file = filedialog.askopenfile(initialdir=os.getcwd())
        if file:
            self.Button2.config(state='normal')
            self.jpk_file = file
            self.Label2.configure(text=self.jpk_file.name)
            self.appendScrollText(f'Otwarto: \n{file.name}\n')

    def load_signed_file(self):
        file = filedialog.askopenfile(initialdir=os.getcwd())
        if file:
            self.Button3_1.config(state='normal')
            self.signed_file = file.name
            self.Label5.configure(text=self.signed_file)
            self.appendScrollText(f'Otwarto: \n{self.signed_file}\n')

    def add_item_ListBox(self):
        to_append = self.Entry.get()
        if len(to_append) != 32:
            self.appendScrollText("Niewłąściwy numer.")
        else:
            self.appendListBox(to_append)

    def get_status_jpk(self):
        try:
            response = JpkRequest.get_status(self.Listbox1.get(self.Listbox1.curselection()))
            if response['Code'] != 200:
                messagebox.showerror(response['Description'], '\n'.join([response['Description'], response['Details']]))
                self.appendScrollText('\n'.join([response['Description'], response['Details']]))
            else:
                self.appendScrollText('Weryfikacja poprawan, UPO gotowy do pobrania.')
        except tk.TclError:
            self.appendScrollText("Wybierz numer do sprawdzenia!")

    def generate_initial_upload(self):
        if self.jpk_file is None:
            self.appendScrollText("Wybierz plik JPK do wygenerowania. ")
        else:
            try:
                to_sign = JpkRequest.create_init_upload(self.jpk_file.name)
                self.appendScrollText(f"Utworzono plik do podpisania {to_sign}. \nPodpisz go!\n")
            except Exception as e:
                self.appendScrollText(e)

    def send_jpk(self):
        try:
            response = JpkRequest.send_jpk(self.signed_file)
            if response.status_code != 200:
                resp_json = response.json()
                self.appendScrollText(f'Błąd! \n{resp_json["Message"]} \nKod błędu: {resp_json["Code"]}\n')
            else:
                self.appendListBox(response.reference)
                self.appendScrollText(f"Pomyślnie wysłano jpk.\nNumer referencyjny: {response.reference}\n")
        except Exception as e:
            print(e)
            self.appendScrollText(f"Błąd! \nSprawdz podpisany plik!\n")


def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''

    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)

    return wrapped


def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1 * int(event.delta / 120), 'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1 * int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')


def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1 * int(event.delta / 120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1 * int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')


if __name__ == '__main__':
    vp_start_gui()
