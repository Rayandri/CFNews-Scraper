# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 12:42:57 2020

@author: Rayan
"""
# var_temp correspond a variable temporaire 
# verif correspond a une variable qui sert de verification


from selenium import webdriver
from time import *

import os
from tkinter import *
from tkinter.font import *
from datetime import*
import time #pour ne pas mélanger avec datetime
import sys #qui viens de système

try:
    from fonction_recurante import* # dans le pythonpath ou dans le dossier envoyer
except:
    sys.path.append("C:\\aa rayan\\NSI\\fonction") 
    from fonction_recurante import *
    print('importé via sys')

# fonction 
#%% 

 
espace(2)
def temps(nb_jour,temps_pour_fichier,i):
    '''
    cette fonction calcule temps restant
    en se basent de la moyenne du temps pour telecharger un fichier (le temps de navigation)
    elle affiche aussi on est combien de %

    Parameters
    ----------
    nb_jour : int
        DESCRIPTION.
    temps_pour_fichier : list
        DESCRIPTION.
    i : int
        DESCRIPTION.

    Returns
    -------
    None.
    >>> temps(10,[2,2,2],2)
    <BLANKLINE>
    il reste environ 0 heure et 0 minutes soit 14 secondes  
     on est a 20.0 %
    <BLANKLINE>

    '''
    temps_tt=0
    for j in temps_pour_fichier: #pour enregistrer le temps total du lancement du code
        temps_tt+=j
    estimation=int( ( (temps_tt//len(temps_pour_fichier) )*nb_jour) -temps_tt)# on calcul le temps pour tous telcharger depuis le debut - le temps passer 
    if estimation<0: #des fois ça arrive en dessous de 0 vers la fin
        print('bientôt finis')
    else:
        estimation_m=estimation//60
        estimation_h=estimation_m//60
        estimation_m=estimation_m%60
        espace(1)
        print(f"il reste environ {estimation_h} heure et {estimation_m} minutes soit {estimation} secondes  ")
    
    pourcent = round((i*100)/ nb_jour,2)
    print(f' on est à {pourcent} %')
    espace(1)



def liste_de_date(date_deb,date_fin):
    '''
    cette fonction créé une liste de date 
    
    Parameters
    ----------
    annee_de_deb : TYPE
        DESCRIPTION.
    mois_de_deb : TYPE
        DESCRIPTION.
    nb_de_ans : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    >>> liste_de_date('01/01/2019','09/01/2019')
    ['01/01/2019', '02/01/2019', '03/01/2019', '04/01/2019', '05/01/2019', '06/01/2019', '07/01/2019', '08/01/2019', '09/01/2019']
    '''
    d,m,a=recupe_date(date_deb)
    date_l=[] #liste vide pour enregistrer nos date dedans 
    verif2=False
    date=datetime(a,m,d)
    while not verif2 :
        var_temp1 = str( date.strftime('%d/%m/%Y')) #on formate la date
        date_l.append(var_temp1)
        if var_temp1==date_fin:
            verif2 = True
        date+= timedelta(1)
    return(date_l)

def connexion(mdp_txt,stop):
    '''

    Parameters
    ----------
    mdp_txt : str
        mot de passe .
    stop : bool
        variable qui gere l'arret du programme .

    Returns: 
        stop
        driver: le webdriver (Chrome)
        
    -------
    None.
    >>> connexion('faux mdp',False)
    Email ou mot de passe incorrect
    'test past'
    '''
    #connexion au compte
    driver = webdriver.Chrome() #on utlise le webdriver de Chrome
    driver.set_window_size(1050, 720) # simple 720p classic 
    driver.get("https://secure.cfnews.net/cfn/login/?redir=/Referentiel/Operations")
    mail = driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/div/form/input[3]') #les xpath sont copiable avec l'inspecteur 
    mail.send_keys('PUT YOUR MAIL HERE')
    mdp = driver.find_element_by_xpath('//*[@id="user-password"]') 
    mdp.send_keys(mdp_txt)
    driver.find_element_by_xpath('//*[@id="submit"]').click()#connexion
    sleep(2)#le temps que la page se charge
    try:
        driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/div/div[1]/strong')
        print('Email ou mot de passe incorrect')
        driver.quit()
        if mdp_txt=='faux mdp':  return('test past') # pour un test
        else: return(True, driver)# stop=True
    except:
         print('connexion au compte réussi ')
         return(False, driver)# stop=False 
           
     
def telechargement(date_l,intervalle,test,nb_jour , driver):
    '''
    

    Parameters
    ----------
    date_l : TYPE
        DESCRIPTION.
    intervalle : TYPE
        DESCRIPTION.
    test : TYPE
        DESCRIPTION.
    nb_jour : TYPE
        DESCRIPTION.
    driver : TYPE
        DESCRIPTION.

    Returns
    -------
    None.
    ce n'est pas testable a l'aide d'un doctest a cause du driver 
    '''
    
    for i in range(0,len(date_l),intervalle): #on avence de 2 en 2 car je veut telecharger a un intervalle de 2 jours
        heure_de_debut=float(time.time()) #correspond au temps ecoulé en seconde depuis 1970 (je crois)
        deb=date_l[i]
        try:#pour le dernier jour fichier
            fin=date_l[i+intervalle-1]
        except:
            fin=date_l[i]
        driver.get("https://www.cfnews.net/Referentiel/Operations")
        date_deb = driver.find_element_by_xpath('//*[@id="depuis"]')
        date_deb.send_keys(deb)
        date_fin = driver.find_element_by_xpath('//*[@id="jusquau"]')
        date_fin.send_keys(fin)
        driver.find_element_by_xpath('//*[@id="rechercher2"]').submit()
        try:
            assert test==False
            driver.find_element_by_xpath('//*[@id="search-sort"]/a').click()#on DL 
            #mais pour les week-end ou jours férié il n'y a rien a DL donc on mets un try
        except:
            print(f" Rien entre {deb} et {fin} ")
        #cette partis sert a calculer le temps 
        heure_de_fin=float(time.time())#pour mesurer le temps de telechargement de un fichier
        temps_pour_fichier.append(heure_de_fin-heure_de_debut)
        if i==2:
            espace(1)
            print('calcul du temps restant ')
        elif i!=0 and i%4==0:
            temps(nb_jour, temps_pour_fichier , i)
            
    
    
    

def fermer():
    '''
    cette fonction recupere les valeurs des input et ferme la fenetre
    on ne peut pas return donc on mets des liste 
    qui ne se detruissent pas avec les fonctions 
    '''
    saisie.append(value_mdp.get())
    saisie.append(value_date_deb.get())
    saisie.append(value_date_fin.get())
    saisie.append(value_intervalle.get())
    fenetre.destroy()
    
def doctest_active():  
    saisie[1]='doctest'
    print("c'est un doctest")
    fenetre.destroy()
    
def annuler():
    '''
    cette fonction annule le programme
    
    edit je decouvre que sys.exit(0) existe 
    '''
    print('stop')
    saisie.append('stop')
    fenetre.destroy()
def bu_test():
    saisie.append(value_mdp.get())
    saisie.append('test')
    fenetre2= Toplevel(fenetre)
    fenetre2['bg']= 'black'
    fenetre2.geometry('200x100')
    bu_normal=  Button(fenetre2,text='Normal',font=police, bg='white',fg='red',borderwidth=5,width=8,relief='groove',command=fenetre.destroy).place(x=10, y=25)
    bu_doctest= Button(fenetre2,text='Doctest',font=police, bg='white',fg='red',borderwidth=5,width=8,relief='groove',command=doctest_active).place(x=110, y=25) 
    
    
#%% 
'''
code principal
'''
espace(1)
print('debut du programme')
'''
constante et variable
'''
verif3= False
saisie=[]
stop=False
test=False
doctest_v=False
#%%         tkinter 

while not verif3:   
    fenetre = Tk()
    fenetre.title('Downloader')
    fenetre.iconbitmap('download.ico')
    fenetre['bg']='black'
    fenetre.geometry("500x300")
    
    police= Font( size=11)#la police
    
    value_mdp = StringVar() 
    value_mdp.set("Taper le mot de passe ici")
    
    value_date_deb = StringVar() 
    value_date_deb.set("Date de debut (dd,mm,aaaa avec les 0) ")
    
    value_date_fin = StringVar() 
    value_date_fin.set("Date de fin ( dd/mm/aaaa avec les 0)")
    
    value_intervalle = StringVar() 
    value_intervalle.set("Intervalle de téléchargement par défaut 2 jours ")
    
    entree_mdp = Entry(fenetre,font=police,textvariable=value_mdp, width=50,selectborderwidth=2,borderwidth=3,show='*',fg='maroon',bg='bisque',relief='raised').place(x=30, y=30)
    entree_date_deb = Entry(fenetre,font=police,textvariable=value_date_deb, width=50 ,selectborderwidth=2,borderwidth=3,relief='raised').place(x=30, y=80)
    entree_date_fin = Entry(fenetre,font=police,textvariable=value_date_fin,width=50,selectborderwidth=2,borderwidth=3,relief='raised').place(x=30, y=130)
    entree_inter = Entry(fenetre,font=police,textvariable=value_intervalle,width=50,selectborderwidth=2,borderwidth=3,relief='raised').place(x=30, y=180)
    button_confi= Button(fenetre,text='Confirmer',font=police, bg='white',fg='red',borderwidth=5,width=8,relief='groove',command=fermer).place(x=30, y=240)
    button_stop= Button(fenetre,text='Annuler ',font=police, bg='white',fg='red',borderwidth=5,width=8,relief='groove',command=annuler).place(x=195,y=240)
    
    button_test= Button(fenetre,text='Test',width=8,font=police, bg='white',fg='red',borderwidth=5,relief='groove',command=bu_test).place(x=350, y=240)
    
    fenetre.mainloop()
    if 'stop' in saisie:
        sys.exit(0) # stop le programme
    if 'doctest' in saisie:
        doctest_v=True
        stop=True
        break
    if 'test' in saisie:
        test=True 
        mdp_txt=saisie[0]
        date_deb='01/01/2019'
        date_fin='10/01/2019'
        intervalle=2
        break #on sort pour ne pas faire le try qui ne marchera pas 
        
    try:
        mdp_txt,date_deb, date_fin =str(saisie[0]) ,str(saisie[1]),str(saisie[2])
        if saisie[3]=="intervalle de telechargement par default 2":
            intervalle=2
        else:
            intervalle=int(saisie[3])
            
        verif3=True
    except:
         print('Taper vos date en chiffre ( Mars seras egale a 3)')




#%% connexion au compte
         
if stop==False:  
    date_l=liste_de_date(date_deb, date_fin)# on appel notre fonction qui va nous generer une liste de date 
    stop, driver =connexion(mdp_txt, stop)

    espace(1)
    temps_pour_fichier=[] #liste qui contiendra le temps de chaque fichier
    nb_jour=len(date_l)
    
    
#%% boucle de telechargement 
if stop==False:  
    telechargement(date_l, intervalle, test, nb_jour, driver)
    print('on est a 100 %')
    print("La fenêtre va s'auto détruire dans 5 secondes ")
    sleep(5)
    driver.quit()
    print("fermer l'invite de commande quand c'est bon ")
    os.system('pause')#pour ne pas fermer la console direct ( pour le fichier en .exe )
    
#%%
    
if __name__ == '__main__' and doctest_v==True:
    import doctest
    aa= False
    aa= True
    doctest.testmod(verbose=aa)
