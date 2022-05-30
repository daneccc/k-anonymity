
import pandas as pd

from pandas.core.frame import DataFrame

names = (
    'Data',
    'Idade',
    'Doenca',
)

dforiginal = pd.read_csv("alunos.csv", sep=";", header=None, names=names, index_col=False, engine='python')
dforiginal = dforiginal.iloc[1: , :]

df = dforiginal.copy(deep=True)


# ####### Classes de equivalência

def equivalence_classes(DataFrame:df):

  list_equivalence_classes_data_idade = []
  for row in range(len(df)):
    data = df.iloc[row, 0]
    idade = df.iloc[row, 1]
    doenca = df.iloc[row, 2]
    if not list_equivalence_classes_data_idade:
      list_equivalence_classes_data_idade.append([[data, idade], [row], [doenca]])
    else:
      aux = 0
      for i in range(len(list_equivalence_classes_data_idade)):
        if(data == list_equivalence_classes_data_idade[i][0][0] and idade == list_equivalence_classes_data_idade[i][0][1]):
          list_equivalence_classes_data_idade[i][1].append(row)
          list_equivalence_classes_data_idade[i][2].append(doenca)
          aux = 1   
      if(aux == 0):
        list_equivalence_classes_data_idade.append([[data, idade], [row], [doenca]])

  return list_equivalence_classes_data_idade

def printa_classes(df: DataFrame):
  classes_equivalentes_l = equivalence_classes(df)
  print('Total de classes: ', len(classes_equivalentes_l))

  for i in range(len(classes_equivalentes_l)):
    print(len(classes_equivalentes_l[i][1]), classes_equivalentes_l[i])

############# Generalização

def generaliza(df: DataFrame, variavel: int, nivel: int):
  df_gen = df
  if(variavel == 1):
    if(nivel == 1):
      df['Idade']
    elif(nivel == 2):
      df['Idade']= df['Idade'].replace(['16','17', '18', '19', '20'],['[15-17]','[15-17]', '[18-20]', '[18-20]', '[18-20]'])
    elif(nivel == 3):
      df['Idade'] = df['Idade'].apply(lambda x: "[16-20]")

  elif(variavel == 2):
      df['Data'] = pd.to_datetime(df.Data, errors = 'coerce')
      if(nivel == 1):
        df['Data'] = df['Data'].dt.strftime('%d-%m-%Y')
      elif(nivel == 2):
        df['Data'] = df['Data'].dt.strftime('%m-%Y')
      elif(nivel == 3):
        df['Data'] = df['Data'].dt.strftime('%Y')
      elif(nivel == 4):
        df['Data'] = df['Data'].dt.strftime('%Y')
        df['Data'] = df['Data'].apply(lambda x: (int(x)//10)*10)
  
  return df_gen

def k_anonimato(list_classes_equivalentes: list, k: int):
  resultado = True
  i = 0
  while resultado == True and i < len(list_classes_equivalentes):
    if(len(list_classes_equivalentes[i][1]) < k):
      resultado = False
    i = i + 1
  
  return resultado

####### Anonimização

k = 2
dfa_k2 = df
dfn_k2 = dfa_k2
nivel = [1, 2, 3, 4]
i = 0
j = 0
para = False

while(para == False):
  lclasses_equivaletes = equivalence_classes(dfa_k2)

  if(k_anonimato(lclasses_equivaletes, k) == False):

    if(i == 0):
        j = 0
    else:
      if(i//2 == (i-1)//2):
        pass
      else:
        j = j + 1
    

    if(i%2 == 0):     
      dfn_k2 = generaliza(dfa_k2, 1, nivel[j])
    else:
      dfn_k2 = generaliza(dfa_k2, 2, nivel[j])

    dfa_k2 = dfn_k2
  
  else:
    para = True
  
  i = i + 1


##################################
# printa_classes(dfn_k2)
# dfa_k2.to_csv('2AnonAlunos.csv')
##################################

k = 4
dfa_k4 = df
dfn_k4 = dfa_k4 
nivel = [1, 2, 3, 4]
i = 0
j = 0
para = False

while(para == False):
  lclasses_equivalentes = equivalence_classes(dfa_k4)

  if(k_anonimato(lclasses_equivalentes, k) == False):
    if(i == 0):
        j = 0
    else:
      if(i//2 == (i-1)//2):
        pass
      else:
        j = j + 1
    
    if(i%2 == 0):     
      dfn_k4 = generaliza(dfa_k4, 1, nivel[j])
    else:
      dfn_k4 = generaliza(dfa_k4, 2, nivel[j])

    dfa_k4 = dfn_k4
  
  else:
    para = True
  
  i = i + 1


##################################
# printa_classes(dfn_k4)
# dfa_k4.to_csv('4AnonAlunos.csv')
##################################

k = 8
dfa_k8 = df
dfn_k8 = dfa_k8
nivel = [1, 2, 3, 4]
i = 0
j = 0
para = False

while(para == False):
  lclasses_equivalentes = equivalence_classes(dfa_k8)

  if(k_anonimato(lclasses_equivalentes, k) == False):
    if(i == 0):
        j = 0
    else:
      if(i//2 == (i-1)//2):
        pass
      else:
        j = j + 1
    
    if(i%2 == 0):     
      df_k8_novo = generaliza(dfa_k8, 1, nivel[j])
    else:
      df_k8_novo = generaliza(dfa_k8, 2, nivel[j])

    dfa_k8 = dfn_k8
  
  else:
    para = True
  
  i = i + 1


#########################
# printa_classes(dfn_k8)
# dfa_k8.to_csv('8AnonAlunos.csv')
#############################

######### L-Diversidade

def cdoencas_df(df: DataFrame):
  doenca = df['Doenca'].tolist()
  doencas_dif_df = []
  for i in doenca:
    if not doencas_dif_df:
      doencas_dif_df.append(i)
    else:
      aux = 0
      for j in doencas_dif_df:
        if(i == j): aux = 1
      if(aux == 0): 
        doencas_dif_df.append(i)
  return doencas_dif_df


def cdoenca_na_classe(df: DataFrame, linhas: list):
  doencas_dif_na_classe = []
  for row in linhas:
    if not doencas_dif_na_classe:
      doencas_dif_na_classe.append(df.iloc[row, 2])
    else:
      aux = 0
      for doenca in doencas_dif_na_classe:
        if(df.iloc[row, 2] == doenca):
          aux = 1
      if(aux == 0):
        doencas_dif_na_classe.append(df.iloc[row, 2])
  return doencas_dif_na_classe




def printa_diversidade(lequivalentes_k8, df):
  for class_equivalence in lequivalentes_k8:
    for row in class_equivalence[1]:
      print(row, class_equivalence[0], df.iloc[row, 2])
    
    print('##################################')


############################
# lequivalentes_k8 = equivalence_classes(dfn_k8)
# printa_diversidade(lequivalentes_k8, dfn_k8)
########################





def pertubacao(lclasses_equivalentes: list, l_diver: int, df: DataFrame):
  doencas_dif_df = cdoencas_df(df)
  for class_equivalence in lclasses_equivalentes:
    #print(class_equivalence[1])
    doencas_dif_na_classe = cdoenca_na_classe(df, class_equivalence[1])
    if(len(doencas_dif_na_classe) < l_diver):
        for j in range(len(doencas_dif_df)):
          for row in class_equivalence[1]:
            
            if not doencas_dif_df[j] in doencas_dif_na_classe:
              if(df.iloc[row, 2] != doencas_dif_df[j]):
                df.loc[row, 'Doenca'] = doencas_dif_df[j]
  return df




def main():

  ans=True
  while ans:
      print ("""
      1. Exibir as classes de equivalencia
      2. 2 Anonimato
      3. 4 Anonimato
      4. 8 Anonimato
      5. lequivalentes_k8
      6. gerar csv
      7. mostrar medidas de utilidade
      """)
      ans = input("Escolha uma opcao: ") 
      if ans=="1": 
        print("\n Exibir as classes de equivalencia") 
        printa_classes(df)

      elif ans=="2":
        print("\n 2 Anonimato") 
        printa_classes(dfn_k2)
        dfa_k2.to_csv('2AnonAlunos.csv')

      elif ans=="3":
        print("\n 4 Anonimato") 
        printa_classes(dfn_k4)
        dfa_k4.to_csv('4AnonAlunos.csv')

      elif ans=="4":
        print("\n 8 Anonimato") 
        printa_classes(dfn_k8)
        dfa_k8.to_csv('8AnonAlunos.csv')

      elif ans=="5":
        print("\n lequivalentes_k8") 
        lequivalentes_k8 = equivalence_classes(dfn_k8)
        printa_diversidade(lequivalentes_k8, dfn_k8)

      elif ans=="6":
          lequivalente_k8 = equivalence_classes(dfn_k8)
          df_l2 = pertubacao(lequivalente_k8, 2, dfn_k8)
          printa_diversidade(lequivalente_k8, dfn_k8)
          lequivalente_k8 = equivalence_classes(dfn_k8)
          df_l3 = pertubacao(lequivalente_k8, 3, dfn_k8)
          printa_diversidade(lequivalente_k8, dfn_k8)
          lequivalente_k8 = equivalence_classes(dfn_k8)
          df_l4 = pertubacao(lequivalente_k8, 4, dfn_k8)
          printa_diversidade(lequivalente_k8, dfn_k8)
          df_l2.to_csv('2lAnonAlunos.csv')
          df_l3.to_csv('3lAnonAlunos.csv')
          df_l4.to_csv('4lAnonAlunos.csv')


      elif ans=="7":
        print("""
            Precisão de anonimização

            Prec(D) = 1 - 300+225/600
            Prec(D) = 1 - 0,875
            Prec(D) = 0,125

            ######## 

            Tamanho médio das Classes de equivalência

            Cavg = (totalRegistro / totalClassesEq) / k 
            k = 2 ->  (300/15)/2 = 10
            k = 4 ->  (300/15)/4 = 5
            k = 8 ->  (300/15)/8 = 2.5
        """)

      elif ans=="8":
        print(dforiginal)



      elif ans !="":
        print("\n Tente de novo") 
  



if __name__ == '__main__':

    main()
