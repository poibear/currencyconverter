import tkinter as tk
from tkinter import ttk
from currencyconvert import convertCurrency


class CurrencyConversion:
    """A class that converts currency using the Tkinter module."""

    bgprocess = convertCurrency(gui=True)

    def __init__(self):
        self.bgprocess = convertCurrency(gui=True)
        self.master = self._draw()

    def _draw(self):
        mainframe = tk.Tk()
        mainframe.title("currency converter")
        mainframe.geometry("960x540")

        maincontent = tk.Frame(mainframe)

        fromframe = tk.Frame(maincontent, background="#99b1ff")
        toframe = tk.Frame(maincontent, background="#acff99")

        # row/column config
        for r_c in range(1):
            fromframe.grid_columnconfigure(r_c, weight=1)
            toframe.grid_columnconfigure(r_c, weight=1)

        fromframe.grid_rowconfigure((0), weight=1)  # by default no weight
        toframe.grid_rowconfigure((0, 1), weight=1)

        currencylist = self.bgprocess.currenciesToList()

        # design
        mainfocusfont = ("Poppins", 25)
        mainselectionfont = ("Poppins", 20)
        dropdownlistfont = ("Poppins", 14)

        # elements
        currentbalancetext = tk.StringVar(fromframe)  # ORIGINAL CURRENCY TEXT
        currentbalancetext.set("Current Currency")
        currentbalance = tk.Entry(
            fromframe, textvariable=currentbalancetext, font=mainfocusfont
        )

        tocurrencytext = tk.StringVar(toframe)
        tocurrencytext.set("Converted Currency")
        tocurrencybalance = tk.Entry(
            toframe, textvariable=tocurrencytext, font=mainfocusfont, state=tk.DISABLED
        )

        currentcurrency = tk.StringVar(fromframe)
        currentcurrency.set(
            currencylist[currencylist.index("USD")]
        )  # must add this function separate from var assignment to use .get function
        # currentcurrencydropdown = tk.OptionMenu(fromframe, currentcurrency, *currencylist)
        currentcurrencydropdown = ttk.Combobox(
            fromframe,
            width=4,
            textvariable=currentcurrency,
            values=currencylist,
            state="readonly",
        )  # combobox for scrollbar
        currentcurrencydropdown.config(font=mainselectionfont)

        finalcurrency = tk.StringVar(toframe)
        finalcurrency.set(currencylist[currencylist.index("USD")])
        # finalcurrencydropdown = tk.OptionMenu(toframe, finalcurrency, *currencylist)
        finalcurrencydropdown = ttk.Combobox(
            toframe,
            width=4,
            textvariable=finalcurrency,
            values=currencylist,
            state="readonly",
        )
        finalcurrencydropdown.config(font=mainselectionfont)

        fromframe.option_add("*TCombobox*Listbox.font", dropdownlistfont)
        toframe.option_add("*TCombobox*Listbox.font", dropdownlistfont)

        def convinentrybox() -> int | None:
            """Converts the given currency and its worth into a desired currency with its converted worth. Puts the converted currency's worth into the uneditable entry box."""
            current = currentcurrency.get()
            toconvert = finalcurrency.get()
            balance = currentbalancetext.get()
            try:
                info = self.bgprocess.getCurrency(current, balance, toconvert)
                tocurrencytext.set(info[2])
                return info[2]  # not necessary but recommended to notify what we're changing, returns balance of final converted currency
            except ValueError:
                currentbalancetext.set("ENTER A VALID NUMBER")
                tocurrencytext.set("Converted Currency")
                convbtntext.set("convert")
                return None

        def clearinput(
            event=None,
        ):  # event parameter required when binding, does nothing otherwise
            """Empties the current string of the StringVar currentbalancetext"""
            currentbalancetext.set("")

        convbtntext = tk.StringVar(toframe)
        convbtntext.set("convert")
        convertbutton = tk.Button(
            toframe,
            textvariable=convbtntext,
            font=mainselectionfont,
            command=convinentrybox,
        )

        # init elements

        currentbalance.grid(row=0, column=0, sticky="nsew")
        currentbalance.bind("<Button-1>", clearinput)  # left click mouse button

        currentcurrencydropdown.grid(row=0, column=1, sticky="nsew")

        tocurrencybalance.grid(row=0, column=0, sticky="nsew")
        finalcurrencydropdown.grid(row=0, column=1, sticky="nsew")

        convertbutton.grid(row=1, columnspan=2, sticky="nsew")

        mainframe.tk.call(
            "source", "C:\\Users\\JoshL\\Python\\projects\\assets\\azurettk\\azure.tcl"
        )  # import theme
        mainframe.tk.call("set_theme", "light")

        # init frames
        maincontent.pack(fill="both", expand=True)

        fromframe.pack(side="top", fill="both", expand=True)
        toframe.pack(side="bottom", fill="both", expand=True)

        print("done!")
        return mainframe

    def convinentrybox(
        self,
        final_string_var: tk.StringVar,
        current_currency: tk.StringVar,
        current_balance: tk.StringVar,
        final_currency: tk.StringVar,
    ) -> int:
        current = current_currency.get()
        toconvert = final_currency.get()
        balance = current_balance.get()
        info = self.bgprocess.getCurrency(current, balance, toconvert)
        final_string_var.set(info[2])
        return info[2]  # not necessary but recommended to info what we're changing

    def run(self):
        def completekill():
            self.master.quit()
            self.master.destroy()
            print("destroyed root window")

        try:
            self.master.wm_protocol("WM_DELETE_WINDOW", completekill)
            self.master.mainloop()
        except AttributeError:
            print(
                "you haven't set a valid master tk frame for the class yet!\neither leave the parameters be or initialize your own with its custom setup!"
            )


obj1 = CurrencyConversion()
obj1.run()
