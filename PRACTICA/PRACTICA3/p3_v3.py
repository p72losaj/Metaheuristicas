import random
import itertools
import sys
import time


class Grafo:

   
    
    def __init__(self,tipoEvento=None,relaciones=None,nNodos=None,nRegistros=None): #Pasamos parámetros por defecto para simular la sobrecarga del constructor de la clase
    
        if(tipoEvento==None and relaciones==None and nNodos==None and nRegistros==None):
            self.tipoEvento=[0,0,0,0,0]  #Almacena el número de eventos de cada tipo que tiene cada objeto de Grafo. Es  decir un vector con valor [2,1,0,1,3] , quiere decir que nuestro grafo 
                            #tiene 2 eventos/nodos de tipo A , 1 de tipo B , 0 de tipo C , 1 de tipo D y 3 de tipo E.
            
            self.relaciones=[]          #Almacena las relaciones de los nodos de eventos de cada objeto de Grafo
            self.nNodos=0               #Almacena el número de nodos de cada objeto de Grafo
            self.nRegistros=0           #Almacena el número de registros de la base de datos que son validos para el objeto Grafo
            
            
        
        else:
            
            self.relaciones=relaciones  #Almacena las relaciones de los nodos de eventos de cada objeto de Grafo 
            self.tipoEvento=tipoEvento  #Almacena el número de eventos de cada tipo que tiene cada objeto de Grafo. Es  decir un vector con valor [2,1,0,1,3] , quiere decir que nuestro grafo 
                            #tiene 2 eventos/nodos de tipo A , 1 de tipo B , 0 de tipo C , 1 de tipo D y 3 de tipo E.
            self.nNodos=nNodos      #Almacena el número de nodos de cada objeto de Grafo
            self.nRegistros=nRegistros      #Almacena el número de registros de la base de datos que son validos para el objeto Grafo
                
    def getRelaciones(self):
        return self.relaciones
        
        
    def setRelaciones(self,vector):
        
        
        self.relaciones=vector
         
    
    def addNodo(self,evento):
        self.nNodos=self.nNodos+1    
        self.tipoEvento[evento-1]=self.tipoEvento[evento-1]+1  
        self.relaciones.append(evento+(self.tipoEvento[evento-1]/100))  #Almacenamos los eventos/nodos añadidos para luego crear las relaciones
        
    def getFitness(self):
    
        if self.nNodos < 4 or self.nNodos > 16:
            return 0
        
        else:
        
            aux=0
        
            for i in self.relaciones:
                aux=aux+i[1][1]-i[1][0]
                
            aux=aux/len(self.relaciones)   #Calculamos el valor medio del rango de tiempos de las relaciones del objeto Grafo
            
            aux=25-aux
            aux=aux/25                      #Normalizamos el valor medio del rango de tiempos a 25 
                                            #ya que es la máxima diferencia posible entre el rango máximo y mínimo de una relacion del grafo
                                            #según se ha establecido en la función de crearRelaciones
            
        
            fitness=(self.nRegistros/1000)*0.9+(self.nNodos/16)*0.05+aux*0.05      #Dividimos el número de nodos del grafo entre 16 ya que es el número máximo de nodos 
                                                                                   #que hay en los registros de la base de datos 
            
            return fitness
        
    def calcularSubconjuntos(self,registro):
        
        permutaciones=[]
        for x in range(len(self.tipoEvento)):
            if self.tipoEvento[x]>0:
                aux=list(itertools.permutations(registro[x+1],self.tipoEvento[x]))   #Obtenemos las permutaciones de un registro de la base de datos para un el objeto Grafo
                permutaciones.append(aux)
        
        listaSubconjuntos=[]
        Hash={}
        tipoNodoAnt=-1

        for i in range(len(permutaciones)): 
        
            permutacionesEventoI=list(permutaciones[i])
            sizeSubconjuntos=len(listaSubconjuntos)
            
            if sizeSubconjuntos > 0 and i!=0:    #Comprobamos si ya hemos añadido los primeras elementos a la lista de subconjuntos del tipo de evento primero  
            
                    if (len(permutacionesEventoI)) > 1: #Comprobamos si el actual tipo de evento tiene más de una permutación, de no ser asi no hace falta añadir mas hash a la lista 
                    
                        for x in range(len(permutacionesEventoI)-1):  #En caso de haber mas de una permutación para el un tipo de evento duplicamos los valores actuales de la lista de subconjunto N-1 veces
                        
                            for q in range(sizeSubconjuntos):
                            
                                listaSubconjuntos.append(listaSubconjuntos[q].copy())
                                
            tipoNodo=tipoNodoAnt+1           
            while self.tipoEvento[tipoNodo]==0: #Para encontar el siguiente tipo de evento que contenga nodos en nuestro grafo, y por tanto permutaciones para nuestro determinado registro 
                tipoNodo=tipoNodo+1
            tipoNodoAnt=tipoNodo
            
            
            ant=0
            sig=0
            
            for j in range(len(permutacionesEventoI)): #Recorremos cada una de las permutaciones para un miso tipo de evento , es decir, tipoEvento-->3 
                                                       # por ejemplo si tenemos 2 nodos en nuestro grafo para el tipo de evento 3:(3,4) (4,3) (5,3) (3,5) (4,5) (5,4)
                                                       
            
                    
                valoresNodosMismoTipo=list(permutacionesEventoI[j])
                a=1
                
                if i > 0:
                    #Para cada una de las permutaciones de un tipo evento calculamos las posiciones de la lista de subconjuntos que ha de acceder para añadir sus valores para los N nodos de ese tipo de evento
                    sig=len(listaSubconjuntos)/len(permutacionesEventoI)  
                    sig=int(sig)
                    sig=sig+ant
                    
                    
                
            
                for valorNodo in valoresNodosMismoTipo:
                
                    nodoIndex=tipoNodo+1+(a/100)  #Calculamos el valor de la clave de cada nodo del Hash
                    Hash[nodoIndex]=valorNodo     #Añadimos esa clave y ese valor al Hash o diccionario
                
                    if i > 0:       
                                   
                        for n in range(ant,sig):
                             
                            listaSubconjuntos[n][nodoIndex]=valorNodo
                            
                        
                        
                    a=a+1
                    
                ant=sig
                
                if i==0: #En caso de tratarse de las  permutaciones del primer tipo evento con uno o mas nodos en  nuestro Grafo, añadimos tantos Hash o diccionarios a lista de subconjuntos como permutaciones existan para ese determinado tipo de evento 
                
                    Hash_copia=Hash.copy();
                    listaSubconjuntos.append(Hash_copia)
                    Hash.clear();
                    
        return listaSubconjuntos     
        
        
    def crearRelaciones(self):
    
        aux=[]
        if self.nNodos>=4 and self.nNodos<=16:
            while len(self.relaciones)> 1: 
                
                
                disponiblesNodoN=self.relaciones.copy() #Copiamos los nodos disponibles hasta el momento 
                
                nodoNSelecionado=random.randint(0,len(self.relaciones)-1) #Selecionamos aleatoriamente un nodo de los introducidos en el grafo
               
                nRelacionesNodoN=random.randint(1,len(self.relaciones)-1) #Selecionamos el número de relaciones de ese nodo con el resto , es decir , si el nodoSelecionado se relaciona con uno, dos o con N-1 nodos.
               
                disponiblesNodoN.pop(nodoNSelecionado) #Eliminamos el nodo selecionado,para que no se pueda dar la relacion de un nodo consigo mismo
               
                
                for i in range(1,nRelacionesNodoN+1): 
                
                    
                    
                    nodoRelacionado=random.randint(0,len(disponiblesNodoN)-1) #Selecionamos aleatoriamente que nodo se va a relacionar con el selecionado con el selecionado anteriormente
                  
                    
                    rangoMin=random.randint(-10,0) #Generamos aleatoriamente un valor de tiempo mínimo 
                    rangoMax=random.randint(1,15)#Generamos aleatoriamente un valor de tiempo máximo
                    
                    copia=self.relaciones.copy() #Hacemos una copia del vector de relaciones para que no haya problemas luego con las refrencias al almcenarse en el vector aux
                    
                    
                    aux.append([[copia[nodoNSelecionado],disponiblesNodoN[nodoRelacionado]],[rangoMin,rangoMax]])
                    
                    disponiblesNodoN.pop(nodoRelacionado) #Eliminamos el nodo con el que se ha relacionado anteriormente, para que no se relacione dos veces con un mismo nodo.
                
                self.relaciones.pop(nodoNSelecionado) #Una vez establecidas las relaciones del nodo X se elimina, para evitar generar relaciones repetidas. 
                    
                     
            self.relaciones.clear()
            self.relaciones=aux
        
        else:
            self.relaciones=[]
        
    def evaluarGrafo(self,Registros):
    
        self.nRegistros=0
          
        registroAnterior={}
        subconjuntoValido=False
        
        if self.nNodos >= 4 and self.nNodos<=16:
    
            for registroI in Registros:
                
                if len(registroAnterior)> 0 and registroI==registroAnterior: #Comprobamos si el registro actual es igual que el anterior 
                    
                   
                    if  subconjuntoValido==True:    #Si hemos encontrado un subconjunto valido para el registro anterior,tambien lo vamos a encontrar para el registro actual ya que ambos son identicos.
                        
                        self.nRegistros=self.nRegistros+1
                
                
                else: 
                    subconjuntoValido=False
                    if registroI['Nnodos'] >= self.nNodos: #Comprobamos que el registroI de la base de datos tenga al menos el mismo número de nodos que nuestro objeto Grafo
                        evaluarRelaciones=True
                        for i in range(len(self.tipoEvento)):
                            if self.tipoEvento[i] > 0:
                                if i+1 not in registroI.keys(): #Comprobamos si un tipoEvento de nuestro grafo no esta en el registroI, es decir, si nuestro grafo tiene dos nods de tipo 1 y en el registroI no hay nodos de tipo 1.Ese registro no es valido 
                                    evaluarRelaciones=False
                                    break
                                elif self.tipoEvento[i] > len(registroI[i+1]): #En caso de existir el tipo de evento en nuestro registroI, comprobamos si el número de nodos de ese tipo de evento en el registroI es menor  que  el número  de nodos de ese tipo de evento en nuestro grafo.
                                    evaluarRelaciones=False
                                    break
                     

                        if evaluarRelaciones==True:
                            copia=registroI.copy()
                            
                            
                            
                            
                            listaSubconjuntos=self.calcularSubconjuntos(copia)
                             
                            
                                 
                            for posibleSubconjunto in listaSubconjuntos: #Recorremos cada uno de los subconjuntos para un determinado RegistroI y se comprueba si es valido para el Grafo
                                if subconjuntoValido==True:     #En cuanto se encuentra un subconjunto valido, no es necesario comprobar el resto de subconjuntos
                                    break
                            
                                for relacionI in self.relaciones: #Comprobamos cada una de las relaciones de nuestro grafo para el subconjuntoI
                                
                                   
                                    nodo1=relacionI[0][0]
                                    nodo2=relacionI[0][1]
                                    rangoMin=relacionI[1][0]
                                    rangoMax=relacionI[1][1]
                                    valorResta=posibleSubconjunto[nodo2]-posibleSubconjunto[nodo1]
                                
                                    #print(relacionI)
                                    #print("Valor Resta: ",valorResta)
                                    #print("Rango Minimo: ",rangoMin)
                                    #print("Rango Maximo: ",rangoMax)
                                
                                
                                
                                    if valorResta>= rangoMin and valorResta<= rangoMax:
                                        subconjuntoValido=True
                                    else:                       #Si ese subconjunto se encuentra una relacion no valida , no es necesario comprobar el resto de relaciones para ese subconjunto
                                        subconjuntoValido=False
                                        break
                                    
                            if subconjuntoValido==True: #Una vez recorridos los subconjuntos, si se ha encontrado un subconjunto valido para el registroI.Se aumenta el número de registros del grafo.
                                
                                self.nRegistros=self.nRegistros+1
                                    
                        
                        
                registroAnterior=registroI        #Almacenamos el registro anterior
                            
                        
        
                         
                            
                   
            
                
            
           
def cargarFichero(fichero):

    lista1 = []
    Hash={}
    

    # Leemos el fichero de entrada en formato lectura

    with open(fichero) as fichero:
        lineas = fichero.readlines()
        for linea in lineas:
            aux=linea.strip("\n") #Eliminamos el \n de la linea
            aux=aux.split(":") #Dividimos la linea en una lista en la que el simbolo de ":" indica el final del contenido de cada posicion de la lista
            for i in aux: #Iteramos sobre cada elemento de la lista
                Key, value=i.split(" ") #Dividimos los elementos de la lista anterior por espacios y obtenemos asi la clave y los valores de cada uno de los eventos del fichero
                if Key=="A":
                    Key=1
                    
                if Key=="B":
                    Key=2 
                    
                if Key=="C":
                    Key=3
                    
                if Key=="D":
                    Key=4
                    
                if Key=="E":
                    Key=5

                    
                value=int(value)
                if Key not in Hash.keys():    #Si el evento todavia no se ha añadido al Hash, se añade con su valor de tiempo
                    Hash[Key]=[value]
                    
                else:   #Si el evento ya existe en el Hash , se añade un nuevo tiempo a un mismo tipo de evento.Por tanto poseemos varios eventos de un mismo tipo
                    ant=list(Hash.get(Key))
                    ant.append(int(value))
                    Hash[Key]=ant
            Hash['Nnodos']=len(aux)       
            Prueba=Hash.copy()
            
            lista1.append(Prueba)
            
            Hash.clear()
            
    
    # Cerramos el fichero de texto
    
    fichero.close()
    return lista1 

def crearPoblacion(registros,nIndividuos,maxNnodos):

    poblacion=[]
    
    

    for x in range(nIndividuos):
              
        Nnodos=random.randint(4,maxNnodos) #El número de nodos de cada grafo
        G=Grafo( )
       
        
        for i in range(Nnodos):
        
            nodoTipo=random.randint(1,5)
            G.addNodo(nodoTipo)
        
        G.crearRelaciones()
        G.evaluarGrafo(registros)
        poblacion.append([G,G.getFitness()])
        
        
    
    return poblacion


def seleccionPorTorneo(poblacion,k):
    
        #Seleccion de los padres de una población mediante torneos de k participantes.
    
        padres=[]
        
     #Generamos tantos hijos como padres hay actualmente en la población,
        for i in range(len(poblacion)):
            #selecionamos aleatoriamente k  padres para el torneo,
            candidatos=random.sample(poblacion,k)
            #Ordenamos los candidatos por valor de fitness ascendente,
            candidatos.sort(key=lambda candidatos:candidatos[1])
            #Escogemos el mejor candidato del torneo,
            G=Grafo(candidatos[k-1][0].tipoEvento,candidatos[k-1][0].relaciones,candidatos[k-1][0].nNodos,candidatos[k-1][0].nRegistros)  
            #Generamos nuevos objetos de grafo para evitar problemas al seleccionar mas de una vez un mismo grafo.
            #Al modificarlo en el proceso de cruce y mutación, como los grafos son punteros de objetos cada vez que se modifique ese objeto, se modificaran N instancias de nuestro vector padres.
            padres.append([G,G.getFitness()])
        
        
        for i in poblacion: #Destruimos los objetos
            del i[0]
            

        
        return padres  
        
        

        
        
        
        
        
def cruzarPadres(padres,cProb):
       
   
        i=0
        cruzados=[]
        while i<len(padres):
            if i+1 < len(padres): #Comprobamos que si el número de soluciones es impar, que el ultimo cromosoma no se cruzará con ninguno otro 
                if random.randint(1,100) <= (cProb*100):
                    cruce=cruceOnePoint(padres[i][0],padres[i+1][0])
                    cruzados.append([cruce[0],0])
                    cruzados.append([cruce[1],0])
                
                else:
                    cruzados.append(padres[i])
                    cruzados.append(padres[i+1])  
            
            else: #Al ser impar el número de soluciones, se guarda el último cromosoma tal cual
                cruzados.append(padres[i])
            
            i=i+2  
            
            
        
        return cruzados

def cruceOnePoint(padre1,padre2):

    
 
    cruce=[]
    aux1=[0,0,0,0,0]
    aux2=[0,0,0,0,0]
    
    

    
    #Generamos aleatoriamente el punto a partir del cual se realiza el cruce de dos padres,
    x=random.randint(0,len(padre1.tipoEvento)-2)
    #Realizamos el cruce valores de ambos padres desde la posicion x de cada  hasta el final,
    aux1=padre1.tipoEvento[0:x+1]+padre2.tipoEvento[x+1:len(padre2.tipoEvento)]
    aux2=padre2.tipoEvento[0:x+1]+padre1.tipoEvento[x+1:len(padre1.tipoEvento)]
        
        
                        
    
    padre1.nNodos=sum(aux1)
    padre1.tipoEvento=aux1
    padre1.nRegistros=0
    padre1.relaciones=[]
       
    p3=[]
    
    for i in range(len(padre1.tipoEvento)):
        if padre1.tipoEvento[i] > 0:
            for j in range(padre1.tipoEvento[i]):
                a=i+1
                b=(j+1)/100
                p3.append(a+b)
                
                
    padre1.setRelaciones(p3)
    padre1.crearRelaciones()
    
    
    
    
    padre2.nNodos=sum(aux2)
    padre2.tipoEvento=aux2
    padre2.nRegistros=0
    padre2.relaciones=[]
    
    
    
    p4=[]
    
    for i in range(len(padre2.tipoEvento)):
        if padre2.tipoEvento[i] > 0:
            for j in range(padre2.tipoEvento[i]):
                a=i+1
                b=(j+1)/100
                p4.append(a+b)
                
               
                
                
    padre2.setRelaciones(p4)                      
    padre2.crearRelaciones()
    
    
        
        
    cruce.append(padre1)
    cruce.append(padre2)
    return cruce
    
    
def mutacion(hijos,mProb):
    mutados=[]
    
    for nHijo in hijos:
    
       
        
        if random.randint(1,100)<=(mProb*100): #Comprobamos si se llega a mutar ese cromosoma ó no
            aux=[]
            
            
            for relacionI in nHijo[0].getRelaciones():
                rangoMin=int(relacionI[1][0]/2)
                rangoMax=int(relacionI[1][1]/2)
                aux.append([[relacionI[0][0],relacionI[0][1]],[rangoMin,rangoMax]])
            
            nHijo[0].setRelaciones(aux)
            
            
            
                
            mutados.append([nHijo[0],0]) #Realizamos una mutación multiple para codificación binaria      
        else:
             mutados.append(nHijo)
                
    return mutados        
        


def aplicarOperadoresGeneticos(poblacion, k, cProb, mProb):
    
        #Seleccionar padres mediante torneo tamaño k
        padres=seleccionPorTorneo(poblacion,k)
        
        #Cruzar padres con probabilidad cProb
        
        cruzados=cruzarPadres(padres,cProb)
     
        
        #Se muta cada uno de los cromosomas con probabilidad mProb
        
        Mutados=mutacion(cruzados,mProb)
        
        poblacion.clear()
        poblacion=Mutados
        
        
    
        return poblacion

    
        

def main(argv):

    inicio = time.time()
    
    time.sleep(1)

   
    if len(argv) < 8:
        print("Error,faltan argumentos de entrada")
        print("Formato: <Nombre_del_script> <Nombre_del_fichero_entrada> <Número_de_Individuos> <Número_de_generaciones><Número máximo de nodos><valor del torneo>")
        print("<probabilidad de cruce><probabilidad de mutación>")
        exit(-1)
        
    poblacion=[]    
        
    fichero=argv[1]
    nIndividuos=int(argv[2])
    maxGeneraciones=int(argv[3])
    maxNnodos=int(argv[4])
    if maxNnodos > 16:
       maxNnodos=16
       
    elif maxNnodos < 4:
        maxNnodos=4
       
    k =int(argv[5]) #Tamaño torneo selector de padres
    cProb = float(argv[6]) #Probabilidad de cruce
    mProb = float(argv[7]) #Probabilidad de mutacion  
    
    
    Registros=cargarFichero(fichero)
    poblacion=crearPoblacion(Registros,nIndividuos,maxNnodos)
      
    it=1
    eliteSoluciones=[]
    poblacion.sort(reverse=True,key=lambda poblacion:poblacion[1])
    for i in range(5):
        G=Grafo(poblacion[i][0].tipoEvento,poblacion[i][0].relaciones,poblacion[i][0].nNodos,poblacion[i][0].nRegistros)
        eliteSoluciones.append([G,G.getFitness()])
        
    

    while it < maxGeneraciones:
    
        nSoluciones = aplicarOperadoresGeneticos(poblacion,k,cProb,mProb)
        
        poblacion=[]
        
        for solucion in nSoluciones:
            
            solucion[0].evaluarGrafo(Registros)
            poblacion.append([solucion[0],solucion[0].getFitness()])
            
        
            
        
        
            
            
        #Ordenamos la poblacion de forma descendente con respecto a su valor de fitness
        poblacion.sort(reverse=True,key=lambda poblacion:poblacion[1])
        #Actualizamos los valores de las soluciones de elite
        #Concatenamos los valores de las mejores soluciones de la generación actual y de las soluciones elite de la generación anterior 
        aux=eliteSoluciones.copy()+poblacion[:5].copy()
        #Ordenamos dichos elementos de forma descendente con respecto a su valor de fitness 
        aux.sort(reverse=True,key=lambda aux:aux[1])
        #Vaciamos el vector de soluciones de elite
        eliteSoluciones.clear()
        #Actualizamos el vector de soluciones elite con las 5 mejores soluciones de todas las generaciones hasta el momento.
        for i in range(5):
            G=Grafo(aux[i][0].tipoEvento,aux[i][0].relaciones,aux[i][0].nNodos,aux[i][0].nRegistros)
            eliteSoluciones.append([G,G.getFitness()])
        it=it+1
        
    
    for i in  eliteSoluciones:
        print("Valor de fitness: ",i[1])
        print("Número de registros que cumple: ",i[0].nRegistros)
        print("Número de nodos: ",i[0].nNodos)
        print("Diversidad de tipos de eventos: ",i[0].tipoEvento)
        print("Relaciones: ",i[0].getRelaciones())
        print("\n")
    
    
    fin = time.time()
    
    print("Timepo de ejecucion: ",fin-inicio)
    
    
    
    
    
        


if __name__ == "__main__":
    main(sys.argv)
