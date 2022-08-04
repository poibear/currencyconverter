import tkinter as tk
from currencyconvert import convertCurrency

class CurrencyConversion(tk.Frame):

    bgprocess = convertCurrency(gui=True)

    def __init__(self):
        self.master = self._draw()
        self.bgprocess = convertCurrency(gui=True)
        
    def convInEntryBox(self, finalStringVar, currentCurrency, currentBalance, finalCurrency):
        current = currentCurrency.get()
        toconvert = finalCurrency.get()
        balance = currentBalance.get()
        info = self.bgprocess.getCurrency(current, balance, toconvert)
        finalStringVar.set(info[2])
        return info[2] #not necessary but recommended to info what we're changing

    def _draw(self):
        print('using default config...')
        # base format
        mainframe = tk.Tk()
        mainframe.title('currency converter')
        mainframe.geometry('960x540')
        
        maincontent = tk.Frame(mainframe)

        fromframe = tk.Frame(maincontent, background="#99b1ff")
        toframe = tk.Frame(maincontent, background="#acff99")

        # row/column config
        for rc in range(1):
            fromframe.grid_columnconfigure(rc, weight = 1)
            toframe.grid_columnconfigure(rc, weight = 1)
        
        toframe.grid_rowconfigure((0, 1), weight = 1)
        
        currencylist = self.bgprocess.currenciesToList()

        # elements
        currentbalancetext = tk.StringVar(fromframe) # ORIGINAL CURRENCY TEXT
        currentbalance = tk.Entry(fromframe, textvariable=currentbalancetext)
        
        tocurrencytext = tk.StringVar(toframe)
        tocurrencybalance = tk.Entry(toframe, textvariable=tocurrencytext, state=tk.DISABLED)
        
        currentcurrency = tk.StringVar(fromframe)
        currentcurrency.set(currencylist[currencylist.index('USD')]) #must add this function separate from var assignment to use .get function
        currentcurrencydropdown = tk.OptionMenu(fromframe, currentcurrency, *currencylist)
        
        finalcurrency = tk.StringVar(toframe)
        finalcurrency.set(currencylist[currencylist.index('USD')])
        finalcurrencydropdown = tk.OptionMenu(toframe, finalcurrency, *currencylist)
        
        def conv():
            current = currentcurrency.get()
            toconvert = tocurrencytext.get()
            balance = currentbalancetext.get()
            info = self.bgprocess.getCurrency(current, balance, toconvert)
            finalcurrency.set(info[2])
            return info[2] #not necessary but recommended to info what we're changing
        
        convertbutton = tk.Button(toframe, text="convert", command=self.convInEntryBox(finalcurrency, ))
        
        # init elements
        
        currentbalance.grid(row=0, column=0, sticky="nsew")
        currentcurrencydropdown.grid(row=0, column=1, sticky="nsew")
        
        tocurrencybalance.grid(row=0, column=0, sticky="nsew")
        finalcurrencydropdown.grid(row=0, column=1, sticky="nsew")
        
        convertbutton.grid(row=1, columnspan=2, sticky="nsew")
        
        # init frames
        maincontent.pack(fill="both", expand=True)
        
        fromframe.pack(side="top", fill="both", expand=True)
        toframe.pack(side="bottom", fill="both", expand=True)
        
        print('done!')
        return mainframe
    
    def run(self):
        def completeKill():
            self.master.quit()
            self.master.destroy()
            print('destroyed root window')
        try:
            self.master.wm_protocol('WM_DELETE_WINDOW', completeKill)
            self.master.mainloop()
        except AttributeError:
            print('you haven\'t set a valid master tk frame for the class yet!\neither leave the parameters be or initialize your own with its custom setup!')

obj1 = CurrencyConversion()
obj1.run()
