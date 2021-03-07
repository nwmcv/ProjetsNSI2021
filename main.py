import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askokcancel,showinfo
import os
import sqlite3

def connexion_bd(bd_path):
    """
    Fonction: connexion_bd
    : parametre : bd_path #Chemin d'accès vers la base de données
    """
    connexion = None
    try:
        connexion = sqlite3.connect(bd_path)
    except sqlite3.Error as e:
        return e
    return connexion

def execute_sql(connexion,sql):
    cur = connexion.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    return rows

def maxi_in_row(rows,num):
    maxi=0
    for row in rows:
        if len(str(row[num]))>maxi:
            maxi = len(str(row[num]))
    return maxi

def separateur(largeur_colonnes):
    sep = '+'
    for num in largeur_colonnes[:-1]:
        sep += '-'*num + '+'
    return sep + '\n'


def affichage(rows):
    nb_colones = len(rows[0])
    largeur_colonnes = [3]
    largeur_colonnes += [largeur_colonnes.append(maxi_in_row(rows,i)) for i in range(nb_colones)]
    sepa = separateur(largeur_colonnes)
    finale = sepa 
    for i in range(len(rows)):
        for k in range(len(rows[i])):
            finale += '| ' + str(i) + ' |' + str(rows[i][k]) + ' '*(largeur_colonnes[k+1]-len(str(rows[i][k]))) + '|\n'
            finale += sepa
    return finale

def charger_req_dico():
    req = {}
    liste_req=os.listdir(dir_req)
    liste_req.remove('alire.md')
    for fichier in liste_req:
        requete=open(dir_req+fichier)
        txt=requete.read()
        requete.close()
        list_q_req = txt.split('\n')
        numq=list_q_req[0][0]
        req[numq] = (list_q_req[0],list_q_req[1])
    return req

def Afficher_rep():
    numq = choix_req.get()[0]
    req_a_executer = dico_req[numq][1]
    conn = connexion_bd(dir_db+nom_db)
    res = execute_sql(conn,req_a_executer)
    text.delete('1.0',tk.END)
    text.insert(1.0,affichage(res))

def test_req(sql):
    connect = connexion_bd(dir_db+nom_db)   
    try:
        execute_sql(connect,sql)
    except (TypeError,NameError,sqlite3.Error) as e:
        return (False,e)
    return (True,"")

def modifications():
    def ajouter():
        if not saisie_q.get():
            askokcancel(title = "erreur question",
                        message = "Veuillez saisir une question",
                        parent = add_q,
                        icon = "error")
        elif not saisie_req.get():
            askokcancel(title = "erreur requète",
                        message = "Veuillez saisir une requète",
                        parent = add_q,
                        icon = "error")
        else:
            test = test_req(saisie_req.get())
            if not test[0]:
                askokcancel(title = "erreur requète",
                            message = "Votre requète contient une erreur :\n\n"+str(test[1]),
                            parent = add_q,
                            icon = "error")
            else:
                maxnum = int(max(dico_req.keys()))+1
                fichier = open(dir_req+"req"+str(maxnum)+".sql","x")
                fichier.write(str(maxnum)+") "+str(saisie_q.get())+"\n"+str(saisie_req.get()))
                fichier.close()
                showinfo (title = "Succès",
                          message = "requète ajoutée avec succès !",
                          parent = add_q)




    modifications = tk.Tk()
    modifications.title("Modifications")
    modifications.geometry('720x480')
    modifications.minsize(480,360)


    add_q = tk.LabelFrame(modifications,
                          text = "ajouter une question",
                          height = 100,
                          labelanchor = "nw")
    txt_q = tk.Label(add_q, 
                     text = 'écrivez si dessous la question :',
                     height = 1,
                     fg = "Black")

    saisie_q = tk.Entry(add_q,
                        bg = "white",
                        borderwidth = 3)
    txt_req = tk.Label(add_q, 
                       text = 'écrivez si dessous la requète :',
                       height = 1,
                       fg = "Black")
    saisie_req = tk.Entry(add_q,
                          bg = "white",
                          borderwidth = 3)
    b_ajouter = tk.Button(add_q,
                          text = "Ajouter",
                          command = ajouter,
                          width = 5)
    

    add_q.pack(fill = "x")
    txt_q.pack(side = "top",fill = "x")
    saisie_q.pack(side = "top", fill = "x")
    txt_req.pack(side = "top", fill = "x")
    saisie_req.pack(side = "top", fill = "x")
    b_ajouter.pack(side = "top")
    modifications.mainloop()


dir_req = "requetes/"
dir_db = "DATA/"
nom_db = "imdb.db"


if __name__=="__main__":

    dico_req=charger_req_dico()


#Création de la fenêtre
    root = tk.Tk()
    root.title("Réponses questions SQL")
    root.geometry('720x480')
    root.minsize(480,360)

    menu = tk.LabelFrame(root,
                         text = "choix question",
                         height = 100,
                         labelanchor = "nw")

    cadre_rep = tk.LabelFrame(root,
                              bg = "white")


# Widgets #
    
        # texte
    txt_bienvenu = tk.Label(root, 
                            text = 'Bienvenu !',
                            height = 2,
                            fg = "Black",
                            font = ("Calibri",18))

    texte="votre réponse s'affichera ici"
    text=tk.Text(cadre_rep, wrap = 'none')
    scroll_x=tk.Scrollbar(text.master, orient='horizontal')
    scroll_x.config(command = text.xview)
    text.configure(xscrollcommand = scroll_x.set)
    scroll_x.pack(side = 'bottom', fill = 'x', anchor = 'w')
    scroll_y = tk.Scrollbar(text.master)
    scroll_y.config(command = text.yview)
    text.configure(yscrollcommand = scroll_y.set)
    scroll_y.pack(side = tk.RIGHT, fill = 'y')
    text.insert("1.0", texte)

        #menu déroulant

    choix_req = tk.StringVar()
    questions = [tpl[0] for tpl in dico_req.values()]
    questions = sorted(questions)

    menu_déroulant = ttk.Combobox(menu,
                                  textvariable = choix_req,
                                  values = questions,
                                  width=75)
    menu_déroulant.current(0)

        # boutons
    b_affiche_rep = tk.Button(menu,
                            text = "afficher la réponse",
                            height = 1,
                            command = Afficher_rep)

    b_quit = tk.Button(root, 
                        text = "Quitter",
                        relief = tk.GROOVE,
                        height = 1,
                        width = 5,
                        fg = "Black",
                        bg = "#dadeff",
                        command = root.destroy)

    b_modif = tk.Button(menu, 
                        text = "modifcations",
                        height = 1,
                        command = modifications)
# Affichage

    b_quit.pack(side = "bottom",pady=10)
    txt_bienvenu.pack()
    menu.pack(fill = "x")
    cadre_rep.pack(expand = 1 ,fill = "both")
    b_affiche_rep.pack(side = "right",pady=10,padx=5)
    b_modif.pack(side = "right",pady=10,padx=5)
    menu_déroulant.pack(side = "left",expand = 1)
    text.pack(side = 'left', expand = 1, fill = "both")
    root.mainloop()