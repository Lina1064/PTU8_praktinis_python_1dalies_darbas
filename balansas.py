from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pickle
from tkinter import messagebox


langas = Tk()
langas.title('Biudžetas')
langas.geometry("740x740")
langas.iconbitmap(r'payment.ico')

frame1 = Frame(langas)
frame1.pack(side=RIGHT, fill=X)
frame2 = Frame(langas)
frame2.pack(side=LEFT, fill=Y)

pasirinkta = {var: StringVar() for var in ["pasirinkta_paj", "pasirinkta_isl"]}

def naujas_pajamu_irasas():
    global skaitliukas
    # tree_p.insert(parent='', index='end', iid=skaitliukas, text="", values=(e_paj_sum.get(), e_siuntejas.get(), e_info.get()))
    try:
        pajamu_suma = float(e_paj_sum.get())
    except ValueError:
        status['text'] = "Klaida! Pajamos turi būti skaičius"
    else:
        if pajamu_suma <0:
            status['text'] = "Pajamos turi būti teigiamas skaičius"
        else:
            siuntejas = e_siuntejas.get()
            info =e_info.get()
            if pajamu_suma and siuntejas and info:
                tree_p.insert('', tk.END, values=(pajamu_suma, siuntejas, info))
                skaitliukas +=1
                status['text'] = f'Pridėtas naujas pajamų įrasas: Pajamos: {pajamu_suma}, siuntejas: {siuntejas}, info: {info}'
                e_paj_sum.delete(0,END)
                e_siuntejas.delete(0, END)
                e_info.delete(0, END)
                b_paj_keisti['state'] = DISABLED
                b_paj_trinti['state'] = DISABLED
                pasirinkta["pasirinkta_paj"].set(-1)
                balansas()
                l_balansas_status['text'] = f'{sas_likutis:.2f}'
            else: 
                status['text'] = "Įvesta ne visa informacija, prašom suvesti"

def pazymetas_pajamu_irasas(ivykis):
    for i in tree_i.selection():
        tree_i.selection_remove(i)
    tree_p=ivykis.widget   
    e_paj_sum.delete(0,END)
    e_siuntejas.delete(0, END)
    e_info.delete(0, END)
    e_isl_suma.delete(0,END)
    e_atsis_budas.delete(0, END)
    e_preke.delete(0, END)
    try:
        selected = tree_p.focus()
        e_paj_sum.insert(0, tree_p.item(selected).get('values')[0])
        e_siuntejas.insert(0, tree_p.item(selected).get('values')[1])
        e_info.insert(0, tree_p.item(selected).get('values')[2])
    except IndexError:
        pass
    else:
        pasirinkta["pasirinkta_paj"].set(selected)
        b_paj_keisti['state'] = NORMAL
        b_paj_trinti['state'] = NORMAL

def keisti_pajamu_irasa():
    selected = tree_p.focus()
    tree_p.item(selected, text='', values=(e_paj_sum.get(), e_siuntejas.get(), e_info.get()))
    e_paj_sum.delete(0,END)
    e_siuntejas.delete(0, END)
    e_info.delete(0, END)
    b_paj_keisti['state'] = DISABLED
    b_paj_trinti['state'] = DISABLED
    pasirinkta["pasirinkta_paj"].set(-1)
    status['text'] = f'Pajamų įrašas sėkmingai paredaguotas'
    balansas()
    l_balansas_status['text'] = f'{sas_likutis:.2f}'
  
def trinti_pajamu_irasa():
    selected = pasirinkta["pasirinkta_paj"].get()
    senas_irasas = tree_p.item(selected)['values']
    tree_p.delete(selected)
    e_paj_sum.delete(0,END) 
    e_siuntejas.delete(0, END)
    e_info.delete(0, END)
    b_paj_keisti['state'] = DISABLED
    b_paj_trinti['state'] = DISABLED
    pasirinkta["pasirinkta_paj"].set(-1)
    status['text'] = f'Įrašas: {senas_irasas} sėkmingai pašalintas'
    balansas()
    l_balansas_status['text'] = f'{sas_likutis:.2f}'

def trinti_visas_pajamas():
    for paj_lentele in tree_p.get_children():
        tree_p.delete(paj_lentele)
    b_paj_keisti['state'] = DISABLED
    b_paj_trinti['state'] = DISABLED
    e_paj_sum.delete(0,END)
    e_siuntejas.delete(0, END)
    e_info.delete(0, END)
    pasirinkta["pasirinkta_paj"].set(-1)
    status['text'] = f'Visi pajamų įrašai išvalyti'
    balansas()
    l_balansas_status['text'] = f'{sas_likutis:.2f}'

def issaugoti_pajamas():
    pkl_pavadinimas = filedialog.asksaveasfilename(defaultextension='.pkl')
    if pkl_pavadinimas:
        with open(pkl_pavadinimas, 'wb') as pkl:
            irasai = []
            for sk in tree_p.get_children():
                irasai.append(tree_p.item(sk)['values'])
            pickle.dump(irasai, pkl)
        status['text'] = f'Pajamų įrašas išsaugotas {pkl_pavadinimas}'

def pajamu_itidarymas():
        pkl_pavadinimas = filedialog.askopenfilename(defaultextension='.pkl')
        if pkl_pavadinimas:
            with open(pkl_pavadinimas, 'rb') as pkl:
                pajamu_irasai =pickle.load(pkl)
                for paj_irasas in pajamu_irasai:
                    tree_p.insert('', 'end', values=paj_irasas)
                status['text'] = f'Pajamų įrašas atidarytas iš {pkl_pavadinimas}'

def atidaryti_pajamu_irasa():
    ar_yra = tree_p.get_children()
    if ar_yra == ():
        pajamu_itidarymas()
        balansas()
        l_balansas_status['text'] = f'{sas_likutis:.2f}'
    else:
        zinute = messagebox.askyesno("Biudžetas", "Pajamų lentelėje jau yra įrašytų duomenų\nJuos ištrinti priesš įkeliant?")
        if zinute == 1:
            trinti_visas_pajamas()
            pajamu_itidarymas()
            balansas()
            l_balansas_status['text'] = f'{sas_likutis:.2f}'
        else:
            pajamu_itidarymas()
            balansas()
            l_balansas_status['text'] = f'{sas_likutis:.2f}'
             
# Islaidu funkcijos
def naujas_islaidu_irasas():
    global islaidu_skait
    try:
        islaidu_suma = float(e_isl_suma.get())
    except ValueError:
        status['text'] = "Klaida! Išlaidos turi būti skaičius"
    else:
        if islaidu_suma < 0:
            status['text'] = "Įveskite išlaistų sumą, '-' rašyti nereikia"
        else:
            atsiskaitymo_budas = e_atsis_budas.get()
            preke =e_preke.get()
            if islaidu_suma and atsiskaitymo_budas and preke:
                tree_i.insert('', tk.END, values=(islaidu_suma, atsiskaitymo_budas, preke))
                islaidu_skait +=1
                status['text'] = f'Pridėtas naujas išlaidų įrasas: Išlaidos: {islaidu_suma}, atsiskaityta: {atsiskaitymo_budas}, įsigyta prekė/paslauga: {preke}'
                e_isl_suma.delete(0,END)
                e_atsis_budas.delete(0, END)
                e_preke.delete(0, END)
                b_isl_keisti['state'] = DISABLED
                b_isl_trinti['state'] = DISABLED
                pasirinkta["pasirinkta_isl"].set(-1)
                balansas()
                l_balansas_status['text'] = f'{sas_likutis:.2f}'
            else: 
                status['text'] = "Įvesta ne visa informacija, prašom suvesti"

def pazymetas_islaidu_irasas(ivykis):
    for i in tree_p.selection():
        tree_p.selection_remove(i)
    tree_i=ivykis.widget   
    e_isl_suma.delete(0,END)
    e_atsis_budas.delete(0, END)
    e_preke.delete(0, END)
    e_paj_sum.delete(0,END)
    e_siuntejas.delete(0, END)
    e_info.delete(0, END)
    try:
        selected_isl = tree_i.focus()
        e_isl_suma.insert(0, tree_i.item(selected_isl).get('values')[0])
        e_atsis_budas.insert(0, tree_i.item(selected_isl).get('values')[1])
        e_preke.insert(0, tree_i.item(selected_isl).get('values')[2])
    except IndexError:
        pass
    else:
        pasirinkta["pasirinkta_isl"].set(selected_isl)
        b_isl_keisti['state'] = NORMAL
        b_isl_trinti['state'] = NORMAL

def keisti_islaidu_irasa():
    selected_isl = tree_i.focus()
    tree_i.item(selected_isl, text='', values=(e_isl_suma.get(), e_atsis_budas.get(), e_preke.get()))
    e_isl_suma.delete(0,END)
    e_atsis_budas.delete(0, END)
    e_preke.delete(0, END)
    b_isl_keisti['state'] = DISABLED
    b_isl_trinti['state'] = DISABLED
    pasirinkta["pasirinkta_isl"].set(-1)
    status['text'] = f'Išlaidų įrašas sėkmingai paredaguotas'
    balansas()
    l_balansas_status['text'] = f'{sas_likutis:.2f}'
    
def trinti_islaidu_irasa():
    selected_isl = pasirinkta["pasirinkta_isl"].get()
    senas_isl_irasas = tree_i.item(selected_isl)['values']
    tree_i.delete(selected_isl)
    e_isl_suma.delete(0,END)
    e_atsis_budas.delete(0, END)
    e_preke.delete(0, END)
    b_isl_keisti['state'] = DISABLED
    b_isl_trinti['state'] = DISABLED
    pasirinkta["pasirinkta_isl"].set(-1)
    status['text'] = f'Išlaidų įrašas: {senas_isl_irasas} sėkmingai pašalintas'
    balansas()
    l_balansas_status['text'] = f'{sas_likutis:.2f}'

def trinti_visas_islaidas():
    for isl_lentele in tree_i.get_children():
        tree_i.delete(isl_lentele)
    b_isl_keisti['state'] = DISABLED
    b_isl_trinti['state'] = DISABLED
    e_isl_suma.delete(0,END)
    e_atsis_budas.delete(0, END)
    e_preke.delete(0, END)
    pasirinkta["pasirinkta_isl"].set(-1)
    status['text'] = f'Visi išlaidų įrašai išvalyti'
    balansas()
    l_balansas_status['text'] = f'{sas_likutis:.2f}'

def issaugoti_islaidas():
    pkl_pavadinimas_islaidu = filedialog.asksaveasfilename(defaultextension='.pkl')
    if pkl_pavadinimas_islaidu:
        with open(pkl_pavadinimas_islaidu, 'wb') as pkl:
            irasai = []
            for sk in tree_i.get_children():
                irasai.append(tree_i.item(sk)['values'])
            pickle.dump(irasai, pkl)
        status['text'] = f'Pajamų įrašas išsaugotas {pkl_pavadinimas_islaidu}'

def islaidu_atidarymas():
    pkl_pavadinimas_islaidu = filedialog.askopenfilename(defaultextension='.pkl')
    if pkl_pavadinimas_islaidu:
        with open(pkl_pavadinimas_islaidu, 'rb') as pkl:
            islaidu_irasai =pickle.load(pkl)
            for isl_irasas in islaidu_irasai:
                tree_i.insert('', 'end', values=isl_irasas)
        status['text'] = f'Pajamų įrašas atidarytas iš {pkl_pavadinimas_islaidu}'

def atidaryti_islaidu_irasa():
    ar_yra_isl = tree_i.get_children()
    if ar_yra_isl == ():
        islaidu_atidarymas()
        balansas()
        l_balansas_status['text'] = f'{sas_likutis:.2f}'
    else:
        zinute_isl = messagebox.askyesno("Biudžetas", "I6laidų lentelėje jau yra įrašytų duomenų\nJuos ištrinti priesš įkeliant?")
        if zinute_isl == 1:
            trinti_visas_islaidas()
            islaidu_atidarymas()
            balansas()
            l_balansas_status['text'] = f'{sas_likutis:.2f}'
        else:
            islaidu_atidarymas()
            balansas()
            l_balansas_status['text'] = f'{sas_likutis:.2f}'

def balansas():
    pajamu_sarasas = []
    islaidu_sarasas = []
    pajamos = 0
    islaidos = 0
    for irasai in tree_p.get_children():
        pajamu_sarasas.append(tree_p.item(irasai)['values'][0])  
    for p in range(0, len(pajamu_sarasas)):
        pajamu_sarasas[p] = float(pajamu_sarasas[p])
    pajamos = sum(pajamu_sarasas)   
    for iras in tree_i.get_children():
        islaidu_sarasas.append(tree_i.item(iras)['values'][0])
    for i in range(0, len(islaidu_sarasas)):
        islaidu_sarasas[i] = float(islaidu_sarasas[i])
    islaidos = sum(islaidu_sarasas)
    global sas_likutis
    sas_likutis = pajamos-islaidos
    if sas_likutis < 20:
        l_balansas_status.config(bg="#660000", fg="white", font="Helvetika 13")
    elif sas_likutis < 200:
        l_balansas_status.config(bg="#e60000", fg="white", font="Helvetika 13")
    elif sas_likutis < 500:
        l_balansas_status.config(bg="#ff751a", fg="black", font="Helvetika 13")
    else:
        l_balansas_status.config(bg="White", fg="black", font="Helvetika 13")


# Meniu ir submeniu
m_pagrindinis = Menu(langas)
langas.config(menu=m_pagrindinis)
m_meniu = Menu(m_pagrindinis, tearoff=0)
m_pagrindinis.add_cascade(label="Meniu", menu=m_meniu)
m_meniu.add_command(label="Trinti pajamų įrašus", command=trinti_visas_pajamas)
m_meniu.add_command(label="Išsaugoti pajamų įrašus", command=issaugoti_pajamas)
m_meniu.add_command(label="Atidaryti pajamu įrašus", command=atidaryti_pajamu_irasa)
m_meniu.add_separator()
m_meniu.add_command(label="Trinti išlaidų įrašus", command=trinti_visas_islaidas)
m_meniu.add_command(label="Išsaugoti išlaidų įrašus", command=issaugoti_islaidas)
m_meniu.add_command(label="Atidaryti išlaidų įrašus", command=atidaryti_islaidu_irasa)
m_meniu.add_separator()
m_meniu.add_command(label="Išeiti", command=langas.destroy)

# Pajamu "medis"
stilius = ttk.Style()
stilius.theme_use("default")

stilius.configure("Treeview",
    background="white",
    foreground="black",
    rowheight=25,
    fieldbackground="white"
    )
stilius.map('Treeview',
    background=[('selected', 'blue')])

tree_p = ttk.Treeview(frame1)
tree_p['columns'] = ("suma", "siuntejas", "papildoma_info")
tree_p.column("#0", width=0, stretch=NO)
tree_p.column("suma", width=150, anchor=CENTER)
tree_p.column("siuntejas", width=200, anchor=CENTER)
tree_p.column("papildoma_info", width=200, anchor=CENTER)

tree_p.heading("#0", text="Label")
tree_p.heading("suma", text='Pajamu suma')
tree_p.heading("siuntejas", text='Siuntėjas')
tree_p.heading("papildoma_info", text='Papildoma informacija')
tree_p.grid(row=0, column=0, sticky=NE)

tree_p.tag_configure('oodrow', background="white")
tree_p.tag_configure('evenrow', background="lightblue")
tree_p.bind('<<TreeviewSelect>>', pazymetas_pajamu_irasas)

paj_lentele = []
global skaitliukas 
skaitliukas = 0
for irasui in paj_lentele:
    if skaitliukas %2 == 0:
        tree_p.insert(parent='', index='end', iid=skaitliukas, text="", values=(irasui[0], irasui[1], irasui[2]), tags=('evenrow'))
    else:
        tree_p.insert(parent='', index='end', iid=skaitliukas, text="", values=(irasui[0], irasui[1], irasui[2]), tags=('oodrow'))
    skaitliukas += 1
 
scrollbar_p = ttk.Scrollbar(frame1, orient=tk.VERTICAL, command=tree_p.yview)
tree_p.configure(yscroll=scrollbar_p.set)
scrollbar_p.grid(row=0, column=1, sticky="ns")

# Išlaidų medis
tree_i = ttk.Treeview(frame1)
tree_i['columns'] = ("islaidos", "atsiskaitymas", "preke")
tree_i.column("#0", width=0, stretch=NO)
tree_i.column("islaidos", width=150, anchor=CENTER)
tree_i.column("atsiskaitymas", width=200, anchor=CENTER)
tree_i.column("preke", width=200, anchor=CENTER)

tree_i.heading("#0", text="Label")
tree_i.heading("islaidos", text='Išlaidų suma')
tree_i.heading("atsiskaitymas", text='Atsiskaitymo budas')
tree_i.heading("preke", text='Įsigyta prekė/paslauga')
tree_i.grid(row=5, column=0, sticky=NE)

tree_i.tag_configure('oodrow', background="white")
tree_i.tag_configure('evenrow', background="lightblue")
tree_i.bind('<<TreeviewSelect>>', pazymetas_islaidu_irasas)

islaidu_lentele = []
global islaidu_skait
islaidu_skait = 0
for irasui in paj_lentele:
    if islaidu_skait %2 ==0:
        tree_i.insert(parent='', index='end', iid=skaitliukas, text="", values=(irasui[0], irasui[1], irasui[2]), tags=('evenrow',))
    else:
        tree_i.insert(parent='', index='end', iid=skaitliukas, text="", values=(irasui[0], irasui[1], irasui[2]), tags=('oodrow',))
    islaidu_skait += 1

scrollbar_i = ttk.Scrollbar(frame1, orient=tk.VERTICAL, command=tree_i.yview)
tree_i.configure(yscroll=scrollbar_i.set)
scrollbar_i.grid(row=5, column=1, sticky="ns")

l_pajamu_sum = Label(frame2, text="Pajamu suma", border=5)
l_siuntejas = Label(frame2, text="Siuntėjas", border=5)
l_info = Label(frame2, text='Info', border=5)

e_paj_sum = Entry(frame2)
e_siuntejas = Entry(frame2)
e_info = Entry(frame2)

b_pajam_ived = Button(frame2, width=12, border=3, text='Įrašyti pajamas', command=naujas_pajamu_irasas)
b_paj_keisti = Button(frame2, width=12, border=3, text='Redaguoti įrašą', state = DISABLED, command=keisti_pajamu_irasa)
b_paj_trinti = Button(frame2, width=12, border=3, text='Trinti įrašą', state = DISABLED, command=trinti_pajamu_irasa)

l_tuscias1 = Label(frame2, text="", border=5)
l_tuscias1.config(height=1)
l_tuscias2 = Label(frame2, text="", border=5)
l_tuscias2.config(height=9)
l_tuscias4 = Label(frame1, text="", border=5)
l_tuscias5 = Label(frame1, text="", border=5)
l_tuscias6 = Label(frame1, text="", border=5)
l_tuscias6.config(height=3)

e_isl_suma = Entry(frame2)
e_atsis_budas = Entry(frame2)
e_preke = Entry(frame2)

l_isl_suma = Label(frame2, text='Išlaidų suma', border=5)
l_atsis_budas = Label(frame2, text='Atsiskaitymo būdas', border=5)
l_preke = Label(frame2, text='Įsigyta prekė/paslauga', border=5)

b_islaid_ived = Button(frame2, width=12,border=3, text='Įrašyti išlaidas', command=naujas_islaidu_irasas)
b_isl_keisti = Button(frame2, width=12, border=3, text='Redaguoti įrašą', state = DISABLED, command=keisti_islaidu_irasa)
b_isl_trinti = Button(frame2, width=12, border=3, text='Trinti įrašą', state = DISABLED, command=trinti_islaidu_irasa)
 
l_balansas = Label(frame1, text="Sąskaitos balansas")
l_balansas_status = Label(frame1, text=" ", width=20)

l_balansas.grid(row=2, column=0)
l_balansas_status.grid(row=3, column=0)
l_tuscias1.grid(row=0, column=0)
l_pajamu_sum.grid(row=1, column=0)
e_paj_sum.grid(row=2, column=0)
l_siuntejas.grid(row=3, column=0)
e_siuntejas.grid(row=4, column=0)
l_info.grid(row=5, column=0)
e_info.grid(row=6, column=0)
b_pajam_ived.grid(row=7, column=0)
b_paj_keisti.grid(row=8, column=0)
b_paj_trinti.grid(row=9, column=0)
l_tuscias2.grid(row=10, column=0)
l_isl_suma.grid(row=11, column=0)
e_isl_suma.grid(row=12, column=0)
l_atsis_budas.grid(row=13, column=0)
e_atsis_budas.grid(row=14, column=0)
l_preke.grid(row=15, column=0)
e_preke.grid(row=16, column=0)
b_islaid_ived.grid(row=17, column=0)
b_isl_keisti.grid(row=18, column=0)
b_isl_trinti.grid(row=19, column=0)
l_tuscias4.grid(row=1, column=2)
l_tuscias5.grid(row=4, column=0)
l_tuscias6.grid(row=6, column=1)

status = Label(frame1, text= "Laukiam veiksmų", relief=SUNKEN, width=78, border=1, justify=CENTER)
status.config(bg="white", font="Helvetika 9")
status.grid(row=7, column=0)

langas.mainloop()