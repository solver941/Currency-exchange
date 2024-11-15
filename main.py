#!/usr/bin/env python3

from os.path import basename, splitext
import tkinter as tk
import datetime
import requests
# from tkinter import ttk
from os.path import exists
from tkinter import ttk

class MyEntry(tk.Entry):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        if "textvariable" not in kw:
            self.variable = tk.StringVar()
            self.config(textvariable=self.variable)
        else:
            self.variable = kw["textvariable"]

    @property
    def value(self):
        return self.variable.get()

    @value.setter
    def value(self, new: str):
        self.variable.set(new)



class Application(tk.Tk):
    name = basename(splitext(basename(__file__.capitalize()))[0])
    name = "Foo"


    def __init__(self):
        super().__init__(className=self.name)
        self.varAuto = tk.BooleanVar()
        self.ChboxAuto = tk.Checkbutton(self, text="Automaticky stahovat kurzovní lístek", variable=self.varAuto, command=self.chboxAutoClick)
        self.ChboxAuto.pack()
        self.btnDownload = tk.Button(self, text="Stáhnout kurzovní lístek")
        self.btnDownload.pack()

        self.lblTransaction = tk.LabelFrame(self, text="Transakce")
        self.lblTransaction.pack()
        self.varTransaction = tk.IntVar()
        #self.rbtnPUrchase = tk.Radiobutton(self.lblTransaction, text="Prodej")
        #self.rbtnPUrchase.pack()
        self.rbtnSale = tk.Radiobutton(
            self.lblTransaction,
            text="Prodej",
            variable=self.varTransaction,
            value="sale",
        )
        self.rbtnSale.pack()

        self.cboxCountry = ttk.Combobox(self, values=[])
        self.cboxCountry.pack(anchor="w", padx=5, pady=5)
        self.cboxCountry.bind("<<ComboboxSelected>>", self.on_select)

        self.lblCourse = tk.LabelFrame(self, text="kurz")
        self.lblCourse.pack(anchor="w", padx=5, pady=5)

        self.entryAmount = MyEntry(self.lblCourse)
        self.entryAmount.pack()

        self.entryRate = MyEntry(self.lblCourse, state="readonl")
        self.entryRate.pack()



        self.title(self.name)
        self.bind("<Escape>", self.quit)
        self.lbl = tk.Label(self, text="Hello World")
        self.lbl.pack()
        self.btn = tk.Button(self, text="Quit", command=self.quit)
        self.btn.pack()

    def chboxAutoClick(self):
        if self.varAuto == True:
            self.btnDownload.config(state="disabled")

        else:
            self.btnDownload.config(state=tk.DISABLED)

    def download(self):
        filename = "currency_exchange_rate.txt"
        URL = "https://www.cnb.cz/en/financial_markets/foreign_exchange_market/exchange_rate_fixing/daily.txt"
        try:
            response = requests.get(URL)
            data = response.text
            with open("kurzovni_listek.txt", "r") as f:
                f.write(data)
            return

        except requests.exceptions.ConnectionError as e:
            print(f"Error: {e}")
            if not exists("kurzovni_listek.txt"):
                with open("kurzovni_listek.txt", "r") as f:
                    data = f.read()
            else:
                print("Error: Failed to download data. ")
                exit(500)

        self.ticket = {}
        for line in data.splitlines()[2:]:
            country, currency, amount, code, rate = line.split("|")
            self.ticket[country] = {
                "currency": currency,
                "amount": amount,
                "code": code,
                "rate": rate,
            }
            self.cboxCountry.config(values=list(self.ticket.keys()))



    def on_select(self, event=None):
        country = self.cboxCountry.get()
        self.lblCourse.config(text="")
        self.amount = int(self.ticket[country]["code"])

        self.entryAmount.config(text=self.ticket[country]["code"])

        if self.varTransaction.get() == "purchase":
            self.rate = float(self.ticket[country]["rate"] ) * 0.96
        else:
            self.rate = float(self.ticket[country]["rate"]) * 1.04

        self.entryAmount.value = str(self.amount)
        self.entryRate.value = str(self.rate)

    def transactionClick(self, *args):
        self.on_select()


    def quit(self, event=None):
        super().destroy()


app = Application()
app.mainloop()
