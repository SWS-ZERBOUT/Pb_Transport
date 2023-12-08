import streamlit as st
import numpy as np
from io import StringIO
st.header("Données :")

# Choix de la methode du remplissage des donnees
input_type = st.selectbox("Votre instance", ["Fichier txt", "Remplir manuellement"])

if input_type == "Fichier txt":
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        string_data = stringio.read()
        matrix = np.array([list(map(float, row.split())) for row in  string_data.split('\n')])
        couts = matrix[0:len(matrix)-1,0:len(matrix[0])-1]
        offre = matrix[0:len(matrix)-1,-1]
        demande = matrix[-1,0:len(matrix[0])-1]

        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(' ')

        with col2:
            st.write(couts)

        with col3:
            st.write(' ')
        col1, col2, = st.columns(2)
        with col1:
            st.header("Offre")
            st.write(offre)

        with col2:
            st.header("Demande")
            st.write(demande)


if input_type == "Remplir manuellement":
    num_rows = st.number_input("Donner le nombre de sources:", min_value=1, step=1)
    num_cols = st.number_input("Donner le nombre de destinations:", min_value=1, step=1)

    st.header("Entrer la matrice des couts")
    matrix_str = st.text_area("Entrer les valeurs de la matrice (ligne par ligne,les colonnes separees par des espaces):")
    try:
        couts = np.array([list(map(float, row.split())) for row in matrix_str.split('\n')])           
        if couts.shape == (num_rows, num_cols):
            st.success("La matrice a été chargée avec succès:")
            col1, col2, col3 = st.columns(3)

            with col1:
                st.write(' ')

            with col2:
                st.write(couts)

            with col3:
                st.write(' ')
            
        else:
            st.error(f"Erreur : la forme de la matrice ne correspond pas aux lignes spécifiées ({num_rows}) et colonnes ({num_cols}).")
    except ValueError:
        st.error("Erreur : Veuillez saisir une matrice valide.")

    col1, col2, = st.columns(2)
    with col1:
        st.header("Offre")

        offre_str = st.text_area("Entrer les valeurs du vecteur offre (separees par des espaces):")
        try:
            offre = np.array([list(map(float, row.split())) for row in offre_str.split('\n')])
            if offre.shape == (1 , num_rows):
                st.success("vecteur chargé avec succès:")
                offre = np.transpose(offre)
                offre = offre.flatten()
                st.write(offre)
            else :
                st.error(f"Erreur : la forme du vecteur ne correspond pas aux lignes spécifiées ({num_rows})).")
        except ValueError:
            st.error("Erreur : Veuillez saisir un vecteur valide.")    
    with col2 :   
        st.header("Demande")

        demande_str = st.text_area("Entrer les valeurs du vecteur demande (separees par des espaces):")
        try:
            demande = np.array([list(map(float, row.split())) for row in demande_str.split('\n')])
            if demande.shape == (1 , num_cols):
                st.success("vecteur chargé avec succès:")
                demande = np.transpose(demande)
                demande = demande.flatten()
                st.write(demande)
            else :
                st.error(f"Erreur : la forme du vecteur ne correspond pas aux lignes spécifiées ({num_cols})).")
        except ValueError:
            st.error("Erreur : Veuillez saisir un vecteur valide.")

st.title('Résolution')
# les fonctions de resolution coin nord ouest et moindres couts
def coin_nord_ouest(offre,demande,couts):
    i = 0
    j = 0
    cout = 0
    affectation = np.zeros((len(offre),len(demande)))
    while (i < len(offre)):
        while (j < len(demande)):
            minimum = min(offre[i],demande[j])
            cout = cout + couts[i][j]*minimum
            affectation[i][j] = minimum
            offre [i] = offre [i] - minimum
            demande[j] = demande[j] - minimum
            if (minimum == demande[j] + minimum):
                j = j + 1
            elif (minimum == offre[i] + minimum):
                i = i + 1
        i = i + 1
    st.write("l'affectation est : ")
    st.write(affectation)
    st.write('le cout est : ' ,cout)
    
def moindres_couts(offre,demande,couts,couts_M):
    cout = 0
    affectation = np.zeros((len(offre),len(demande)))
    while True:        
        min_cout = float('inf')
        min_ligne, min_colonne = -1, -1
        for i in range(len(couts)):
            for j in range(len(couts[0])):
                if offre[i] > 0 and demande[j] > 0 and couts_M[i][j] < min_cout:
                    min_cout = couts_M[i][j]
                    min_ligne, min_colonne = i, j
        if min_ligne == -1 or min_colonne == -1:
            break
        minimum = min(offre[min_ligne], demande[min_colonne])
        affectation[min_ligne][min_colonne] = minimum
        cout += couts[min_ligne][min_colonne]*minimum
        offre[min_ligne] -= minimum
        demande[min_colonne] -= minimum
    st.write("l'affectation est : ")
    st.write(affectation)
    st.write('le cout est : ' ,cout)

#choix du probleme
Pb = st.selectbox("Quel type de problème", ["Maximisation", "Minimisation"])

#ajout de ligne ou colonne fictives
sum_offre = offre.sum()
sum_demande = demande.sum()
if sum_offre > sum_demande:
    colonne_fictive = np.zeros(len(demande))
    colonne_fictive = colonne_fictive.reshape(-1, 1)
    demande  = np.append(demande,sum_offre-sum_demande)
    couts = np.hstack([couts, colonne_fictive])
    st.write("Demande",demande.reshape(1,len(demande)))
elif sum_demande > sum_offre:
    ligne_fictive = np.zeros(len(offre))
    ligne_fictive = ligne_fictive.reshape(1,len(demande))
    offre = np.append(offre,sum_demande-sum_offre)
    couts = np.vstack([couts, ligne_fictive])
    st.write("Offre",offre.reshape(1,len(offre)))
st.write("matrice des couts")
if Pb == "Maximisation":
    couts_M = np.amax(couts) - couts
    st.write("Matrice maximisation") 
    st.write(couts_M)
else :
    couts_M = couts
    st.write(couts_M)

# choix de la methode de resolution
methode = st.selectbox("Choose the method", ["Coin Nord Ouest", "Moindres Cout"])

if st.button("Résoudre"):
    if methode == "Coin Nord Ouest":
        coin_nord_ouest(offre, demande, couts)
    elif methode == "Moindres Cout":
        moindres_couts(offre, demande, couts, couts_M)