#!/usr/bin/env python
# coding: utf-8

# In[3]:
def janelaerro(mensagem):
    errolayout=[[sg.Text(mensagem)],[sg.Button("Ok")]]
    janelaErro=sg.Window("Janela de Erro", errolayout)
    erro1,erro2=janelaErro.read(close=True)   

import PySimpleGUI as sg
import FuncPROJ as fg
sg.theme('LightBrown11')

bd=[]
menu_list_column= [
        [sg.Button("Ver BD")],
        [sg.Button("Consultar BD")],
        [sg.Button("Inserir Novo Filme")],
        [sg.Button("Listar Filmes")],
        [sg.Button("Dados estatísticos")],
        [sg.Button("Gráficos")]]
         
entradas=[]


data_viewer_column = [[sg.Listbox(values=entradas, size=(45, 10), key="_entradas", horizontal_scroll=True)]]

interfacePrincipal= [[sg.Button("Carregar BD"),sg.Button("Guardar BD"),sg.Button("Sair")],
         [sg.Column(data_viewer_column),
          sg.VSeperator(),
          sg.Column(menu_list_column)]]

tipos=[("TXT (*.txt)","*.txt")]
       
window = sg.Window("A minha cinemateca",font="Helvetica 24", default_element_size=(20,1)).layout(interfacePrincipal) 
stop = False
while not stop:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        stop = True

    elif event=="Sair":
        layoutSair=[[sg.Text("Quer guardar antes de sair?")],
                    [sg.Button("Sim"), sg.Button("Não")]]
        janelaSair= sg.Window("Sair", layoutSair)
        escolha1, valor1= janelaSair.read(close=True)
        if escolha1=="Sim":
            pass
        elif escolha1=="Não":
            stop=True
            
    elif event=="Carregar BD":
        layoutcarrega=[ [sg.Text("Ficheiro:"), sg.Input(key='-FICHEIRO-'), sg.FileBrowse(file_types=tipos)],
                        [sg.Button("Carregar")]]
        janelacarrega=sg.Window("Carregar BD", layoutcarrega)
        x, y=janelacarrega.read(close=True)
        res=[]
        window['_entradas'].update(values=res)
        if x==sg.WIN_CLOSED:
            janelacarrega.close()

        if y['-FICHEIRO-'] is not None:
            bd=fg.carregarBD(y['-FICHEIRO-'])
        else:
            janelaerro("Não existe um ficheiro com o nome inserido")
        
        

    elif event=="Guardar BD":
        layoutguarda=[[sg.Text("Nome do ficheiro:"), sg.InputText(key="-Nome-")],[sg.Button("Guardar")]]
        janelaguarda=sg.Window("Guardar BD", layoutguarda)
        z,w=janelaguarda.read(close=True)
        res=[]
        window['_entradas'].update(values=res)
        if w["-Nome-"] is not None:
            fg.guardarBD(bd,w["-Nome-"]+".txt")
        else:
            janelaerro("Insira o nome com que pretende guardar o ficheiro.")
        
        
    
    elif event=="Ver BD":
        res=[]
        window['_entradas'].update(values=res)
        if bd==[]:
            janelaerro("Carregue uma Base de dados.")
        else:
            res=fg.verBD(bd)
            window['_entradas'].update(values=res)       
        
    elif event=="Consultar BD":
        if bd==[]:
            janelaerro("Carregue uma Base de dados.")
        else:
            layoutConsultar=[[sg.Text("Insira ID na forma 'fNumero':"), sg.InputText(key='-ID-')],
                             [sg.Text("Inserir título:"), sg.InputText(key='-TITU-')],
                             [sg.Button("Inserir")]]
            res=[]
            window['_entradas'].update(values=res)
            janelaConsultar=sg.Window("Consultar Filme", layoutConsultar)
            es, val= janelaConsultar.read(close=True)
            
            if es=="Inserir":
                if len(val['-ID-']) !=0:
                    res.append(fg.consultarBD(bd, val['-ID-']))
                    window['_entradas'].update(values=res)
                    
                else:
                    titu=val['-TITU-'][0]
                    titu=titu.capitalize()+val['-TITU-'][1:]
                    res=fg.consultarBD(bd,titu )
                    window['_entradas'].update(values=res)
                    
                if len(res)==1:
                    janelaerro("Filme não foi encontrado! Tente escrever o título em inglês.")
        
    elif event=="Inserir Novo Filme":
        res=[]
        window['_entradas'].update(values=res)
        if bd==[]:
            janelaerro("Carregue uma Base de dados.")
        else:
            layoutInserir=[[sg.Text("Título: "), sg.InputText(key='-TIT-')],
                           [sg.Text("Ano: "), sg.InputText(key='-ANO-')],
                           [sg.Text("Elenco (Separe os atores por vírgula): "), sg.InputText(key='-ELE-')],
                           [sg.Text("Género: "), sg.InputText(key='-GEN-')],
                           [sg.Button("Inserir"), sg.Button("Cancelar")]]
            janelaInserir= sg.Window("Inserir Novo Filme", layoutInserir)
            escolha2, valor2=janelaInserir.read(close=True)
            
            if escolha2=="Inserir":
                ele=[]
                ele=(valor2['-ELE-']).split(",")
                gen=[]
                gen=(valor2['-GEN-']).split(";")
                temp=bd
                temp=fg.inserirFilme(temp, valor2['-TIT-'], int(valor2['-ANO-']), ele, gen)
                if temp==False:
                    res=["O filme já existe",""]
                    window['_entradas'].update(values=res)
                else:
                    bd=temp
                    
            elif escolha2=="Cancelar":
                janelaInserir.close()
    
    elif event=="Listar Filmes":
        if bd==[]:
            janelaerro("Carregue uma Base de dados.")
        else:
            layoutListar=[[sg.Button("por título")],
                          [sg.Button("por género")],
                          [sg.Button("por ator")],
                          [sg.Button("por ano")],
                          [sg.Button("Cancelar")]]
            janelaListar=sg.Window("Listar Filmes", font="Helvetica 24", default_element_size=(20,1)).layout(interfacePrincipal)
            escolha3, valor3=janelaListar.read(close=True)
            if escolha3=="Cancelar":
                janelaListar.close()
                
            elif escolha3=="por ator":
                layoutlistator=[[sg.Text("Ator:"), sg.InputText(key='-ATOR-'), sg.Button("Inserir")]]
                janelalistator=sg.Window("Listar por ator", layoutlistator)
                ator1, ator2=janelalistator.read(close=True)
                if ator1=="Inserir":
                    res=[]
                    window['_entradas'].update(values=res)
                    res=fg.listarator(bd,ator2['-ATOR-'].capitalize())
                    window['_entradas'].update(values=res)
                    if len(res)==0:
                        janelaerro("Nome de ator inválido")
            elif escolha3=="por género":
                layoutlistagen=[[sg.Text("Género (em inglês):"), sg.InputText(key='-GEN-'), sg.Button("Inserir")]]
                janelalistagen=sg.Window("Listar por género", layoutlistagen)
                gen1, gen2=janelalistagen.read(close=True)
                if gen1=="Inserir":
                    res=[]
                    window['_entradas'].update(values=res)
                    res=fg.listargenero(bd,gen2['-GEN-'].capitalize())
                    window['_entradas'].update(values=res)
                    if len(res)==0:
                        janelaerro("Género inválido! Tente escrever em inglês.")
            
            elif escolha3=="por ano":
                layoutlistano=[[sg.Text("Ano:"), sg.InputText(key='-ANO-'), sg.Button("Inserir")]]
                janelalistano=sg.Window("Listar por ano", layoutlistano)
                an1, an2=janelalistano.read(close=True)
                if an1=="Inserir":
                    res=[]
                    window['_entradas'].update(values=res)
                    if int(an2['-ANO-'])>=2000 and int(an2['-ANO-'])<=2018:
                        res=fg.listarano(bd,int(an2['-ANO-']))
                        window['_entradas'].update(values=res)
                    
                    else:
                       janelaerro("Insira um ano entre 2000-2018")
            
            elif escolha3=="por título":
                res=[]
                window['_entradas'].update(values=res)
                res=fg.listartitulo(bd)
                window['_entradas'].update(values=res)
            
        
    elif event=="Dados estatísticos":
        if bd==[]:
            janelaerro("Carregue uma Base de dados.")
        else:
            layoutEstatistica=[[sg.Button("Número de Filmes")],
                               [sg.Button("Distribuição por Género")],
                               [sg.Button("Distribuição por Ator")],
                               [sg.Button("Distribuição por Ano")]]
            
            janelaEstatistica=sg.Window("Dados estatísticos", layoutEstatistica)
            escolha4, valor4=janelaEstatistica.read(close=True)
            
            if escolha4=="Número de Filmes": 
                res=[]
                window['_entradas'].update(values=res)
                res=fg.numfilme(bd)
                window['_entradas'].update(values=res)
                
            
            elif escolha4==("Distribuição por Ator"):
                res=[]
                window['_entradas'].update(values=res)
                res.append("Top 10 de atores: ")
                print(fg.distribfilmesat(bd))
                for a in fg.distribfilmesat(bd):
                    res.append(a)
                window['_entradas'].update(values=res)
            
            elif escolha4==("Distribuição por Género"): 
                layoutgen2=[[sg.Text("Género:"), sg.InputText(key='-GEN-'), sg.Button("Inserir")]]
                janelalayoutgen2=sg.Window("Distribuição por género", layoutgen2)
                genero1,genero2=janelalayoutgen2.read(close=True)
                if genero1=="Inserir":
                    res=[]
                    window['_entradas'].update(values=res)
                    res.append("Número de filmes do género "+str(genero2['-GEN-'])+": "+str(fg.distribfilmesge(bd, genero2['-GEN-'])[0]))
                    window['_entradas'].update(values=res)
                    if len(res)==0:
                        janelaerro("Género inválido! Tente escrever em inglês.")
                
            elif escolha4==("Distribuição por Ano"): #nao da
                layoutan2=[[sg.Text("Ano:"), sg.InputText(key='-ANO-'), sg.Button("Inserir")]]
                janelalayoutan2=sg.Window("Distribuição por ano", layoutan2)
                ano1,ano2=janelalayoutan2.read(close=True)
                if ano1=="Inserir":
                    res=[]
                    window['_entradas'].update(values=res)
                    res.append("Número de filmes do ano de "+str(ano2['-ANO-'])+": "+str(fg.distribfilmesano(bd, ano2['-ANO-'])[0]))
                    window['_entradas'].update(values=res)
                    if len(res)==0:
                       janelaerro("Insira um ano entre 2000-2018")
                       
    elif event=="Gráficos":
        if bd==[]:
            janelaerro("Carregue uma Base de dados.")
        else:
            layoutGraficos=[[sg.Button("Distribuição por Ano")],
                                  [sg.Button("Distribuição por Género")],
                                  [sg.Button("Distribuição por Ator")]]
                
            janelaGraficos=sg.Window("Gráficos", layoutGraficos)
            grafico1, grafico2=janelaGraficos.read(close=True)
            if grafico1=="Distribuição por Ano":
                layoutgraf1=[[sg.Text("Insira o intervalo de distribuição")],
                             [sg.Text("Ano 1: "), sg.InputText(key='-ANO1-'), sg.Text("Ano 2: "), sg.InputText(key='-ANO2-'),sg.Button("Inserir")]]
                janelagraf1=sg.Window("Distribuição por Ano", layoutgraf1)
                grafano1, grafano2=janelagraf1.read(close=True)
                if grafano1=="Inserir":
                    fg.plotDistribPorAno(bd,grafano2['-ANO1-'],grafano2['-ANO2-'])
                    
                    
            if grafico1=="Distribuição por Género":
                res=[]
                window['_entradas'].update(values=res)
                res=fg.plotDistribPorGEN(bd)
                window['_entradas'].update(values=res)
              
                
                     
            if grafico1=="Distribuição por Ator":
                  res=[]
                  window['_entradas'].update(values=res)
                  res=fg.plotDistribPorAtor(bd)
                  window['_entradas'].update(values=res)
                


        
window.close()


# In[ ]:




