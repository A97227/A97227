#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
import matplotlib.pyplot as plt
def lerDataset(fnome):
    f=open(fnome, encoding="utf-8")
    data=json.load(f)
    bd=[]
    i=0
    for f in data:
        filme=[]
        filme.append("f"+str(i))
        for key in f:
            filme.append(f[key])
        i=i+1
        bd.append(filme)
    return bd


def extrairlistas(l):
    res=""
    sep="#"
    for i in range (len(l)-1):
        res=res+str(l[i])+sep
    res=res+str(l[-1])
    return res

def guardarBD(bd,fnome):
    filme=open(fnome,"w", encoding="utf-8")
    sep="::"
    for f in bd:
        res=(str(f[0])+sep+str(f[1])+sep+str(f[2])+sep)
        if len(f[3])>1:
            res=res+extrairlistas(f[3])+sep
        elif len(f[3])==1:
            res=res+f[3][0]+sep
        else:
            res=res+"None"+sep
        if len(f[4])>1:
            res=res+extrairlistas(f[4])
        elif len(f[4])==1:
            res=res+f[4][0]
        else:
            res=res+"None"
            
        res=res+"\n"
        filme.write(res)
    filme.close()        
    


def extrairAG(s):
    return s.split("#")

def carregarBD(fnome,encoding='utf-8'):
    f=open(fnome)   
    bd=[]
    for filme in f:
        res=[]
        filmenovo=filme.strip("\n")
        linha=filmenovo.split("::") 
        
        res.append(linha[0])
        res.append(linha[1])
        res.append(linha[2])
       
        if "#" in linha[3]:
            res.append(extrairAG(linha[3]))
        elif "None"==linha[3]:
            res.append([])
        else:
            res.append([linha[3]])
        if "#" in linha[4]:
            res.append(extrairAG(linha[4]))
        elif "None"==linha[4]:
            res.append([])
        else:
            res.append([linha[4]])
        bd.append(res)
    return bd
        
bd=carregarBD("teste.txt") 
#print(bd)    
def inserirFilme(BD,t,a,at,ge):
        existe=False
        for filme in BD:
            if t==filme[2]:
                existe=True
        if existe==False:
            id=int(BD[-1][0][1:])+1
            id="f"+str(id)
            BD.append([id,t,a,at,ge])
            
        if existe==True:
            res=False
        else:
            res=BD
        return res

def verBD(bd):
    lista=[]
    lista.append("id  | Título                |Ano           ")
    for f in bd:
        if len(f)<5:
            print(f)
        lista.append(str(f[0])+" | "+str(f[1])+" | "+str(f[2]))
    return lista

#print(verBD(bd))  
    
def consultarBD(bd,i):
    res=[]
    res.append("id  | Título                |Ano           ")
    for f in bd:
        temp=""
        if f[0]==i or (i in f[1]) :
            temp=str(f[0])+" | "+str(f[1])+" | "+str(f[2])+" | "
            for a in f[-2]:
                temp=temp+str(a)+" | "
            for g in f[-1]:
                temp=temp + str(g)
            if len(f[-1])>1:
                res.append(temp[:-1])
            else:
                res.append(temp)
    
    return res
#print(consultarBD(bd, "f3"))


def distribfilmesge(bd,p):
    i=0
    esp=[]
    for filme in bd:
        for g in filme[-1]:
            if p in g:
                i=i+1
    esp.append(i)
    return esp
#print(distribfilmesge(bd, "Comedy")  
def distribfilmesano(bd,p):
    esp=[]
    i=0
    for filme in bd:
        if int(p) == int(filme[2]):
            i=i+1
    esp.append(i)
    return esp

#print(distribfilmesano(bd, 2000))

def distribfilmesat(bd):
    res=[]
    rest=[]
    dic={}
    for filme in bd:
        for a in filme[-2]:
            if a in dic.keys():
                dic[a]=dic[a]+1
            else:
                dic[a]=1    
        
           
           
    dic['and']=0
    dic['(voice)']=0
    valores=sorted(dic.items(),key=lambda x:x[1],reverse=True)
    novodic=dict(valores)
    
    for k in novodic:
        rest.append(k)
    res=rest[0:10]
    return res
#print(distribfilmesat(bd))

    
def listartitulo(bd):
    res=[]
    for filme in bd:
        res.append(filme[1])
    res.sort()
    return res

def listargenero(bd,p):
    res=[]
    for filme in bd:
        for g in filme[-1]:
            if p in g:
                res.append(filme[1])
    res.sort()
    return res
    
def listarator(bd,p):
    res=[]
    for filme in bd:
        for a in filme[-2]:
            if p in a:
                res.append(filme[1])
    res.sort()
    return res

def listarano(bd,ano):
    res=[]
    for filme in bd:
        if int(ano)==int(filme[2]):
            res.append(filme[1])
    res.sort()
    return res
#print(listarano(bd, 2000))
def numfilme(bd):
    a=len(bd)
    l=[]
    l.append(a)
    return l


#print(listarator(BD, "Hudson"))

def distribanointervalos(bd,i1,i2):
    d={}
    intervalo=[]
    for i in range(int(i1),int(i2)+1,1):
        intervalo.append(i)
    for filme in bd:
        for j in intervalo:
            if int(filme[2])==j:
                if j in d.keys():
                    d[j]=d[j]+1
                else:
                    d[j]=1
    return d


def plotDistribPorAno(bd,i1,i2):
   
    left=[]
    height=[]
    tick_label=[]
    a=distribanointervalos(bd,i1,i2)
    i=1
    for elem in a:
        tick_label.append(elem)
        height.append(a[elem])
        left.append(i)
        i=i+1
    plt.bar(left, height, tick_label = tick_label,
        width = 0.8, color = ['red'])
    
    plt.xlabel('Anos')
    plt.ylabel('Número de filmes')
    plt.title("Distribuição de filmes por ano")
    plt.show()
    
print(plotDistribPorAno(bd, 2000, 2001))    
    
def distribGEN(bd):
   rest=[]
   dic2={}
   dic={}
   for filme in bd:
       for a in filme[-1]:
           if a in dic.keys():
               dic[a]=dic[a]+1
           else:
               dic[a]=1    
      
          
     
   valores=sorted(dic.items(),key=lambda x:x[1],reverse=True)
   novodic=dict(valores)
    
   # novodic
   for k in novodic:
       
       rest.append(k)
       rest.append(novodic[k])
       
           
           
   res=rest[0:10]
   dic2={res[0]:res[1], res[2]:res[3], res[4]:res[5], res[6]:res[7], res[8]:res[9]}
   return dic2
  

   
print(distribGEN(bd))

def plotDistribPorGEN(bd):
   
    left=[]
    y=[]
    tick_label=[]
    res=distribGEN(bd)
    l=1
   
   
    for elem in res:
        
        tick_label.append(elem)
        y.append(res[elem])
        left.append(l)
        l=l+1
        
    plt.bar(left, y, tick_label = tick_label,
        width = 0.8, color = ['red'])
    
    plt.xlabel('Generos')
    plt.ylabel('Número de filmes')
    plt.title("Distribuição de filmes por genero ")
    plt.show()
print(plotDistribPorGEN(bd))




def distribator(bd):
    rest=[]
    dic2={}
    dic={}
    for filme in bd:
        for a in filme[-2]:
            if a in dic.keys():
                dic[a]=dic[a]+1
            else:
                dic[a]=1    
       
           
    dic['the']=0  
    valores=sorted(dic.items(),key=lambda x:x[1],reverse=True)
    novodic=dict(valores)
     
    # novodic
    for k in novodic:
        
        rest.append(k)
        rest.append(novodic[k])
        
            
            
    res=rest[0:10]
    dic2={res[0]:res[1], res[2]:res[3], res[4]:res[5], res[6]:res[7], res[8]:res[9]}
    return dic2
print(distribator(bd))

def plotDistribPorAtor(bd):
   
    left=[]
    height=[]
    tick_label=[]
    a=distribator(bd)
    i=1
    for chave in a:
        tick_label.append(chave)
        height.append(a[chave])
        left.append(i)
        i=i+1
    plt.bar(left, height, tick_label = tick_label,
        width = 0.35, color = ['red'])
    plt.rcParams['figure.figsize'] = (11,2)
    plt.xlabel('ator')
    plt.ylabel('Número de filmes')
    plt.title("Distribuição de filmes por ator ")
    plt.show()
print(plotDistribPorAtor(bd))
