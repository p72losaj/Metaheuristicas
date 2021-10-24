import random


def mutacionMultiplesGenes(hijo):
    
    #Genereamos un número aletorio de genes a mutar 
    n_genes=random.randint(1,len(hijo))
       
    for i in range(n_genes):
        
        gen_n=random.randint(0,len(hijo)-1) #Se genera la posición aletoria del cromosoma la cual se muta
        hijo[gen_n]=(hijo[gen_n]+1)%2  
        
    return hijo
    
def mutacion(hijos,mProb):
    mutados=[]
    
    for nHijo in hijos:
        
        if random.randint(1,100)<=(mProb*100): #Comprobamos si se llega a mutar ese cromosoma ó no
            mutados.append([mutacionMultiplesGenes(nHijo[0]),0]) #Realizamos una mutación multiple para codificación binaria      
        else:
             mutados.append(nHijo)
                
    return mutados        
        
def cruceOnePoint(padre1,padre2):
   
 
    cruce=[]
    #Generamos aleatoriamente el punto a partir del cual se realiza el cruce de dos padres,
    x=random.randint(0,len(padre1)-2)
    #Realizamos el cruce valores de ambos padres desde la posicion x de cada  hasta el final,
    cruce.append(padre1[0:x+1]+padre2[x+1:len(padre2)])
    cruce.append(padre2[0:x+1]+padre1[x+1:len(padre1)])
    return cruce


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
            padres.append(candidatos[k-1])
            
        return padres    

def evaluarSolucion(solucion, precios, pesos, pesoMax):
    precio = 0
    peso = 0
    for i in range(len(solucion)):
        precio += precios[i]*solucion[i]
        peso += pesos[i]*solucion[i]

    if peso > pesoMax:
        return 0
    else:
        return precio

def aplicarOperadoresGeneticos(poblacion, k, cProb, mProb):
    
        #Seleccionar padres mediante torneo tamaño k
        padres=seleccionPorTorneo(poblacion,k)
             
        #Cruzar padres con probabilidad cProb
        
        Cruzados=cruzarPadres(padres,cProb)
        
        #Se muta cada uno de los cromosomas con probabilidad mProb
        
        Mutados=mutacion(Cruzados,mProb)
        
        poblacion.clear()
        poblacion=Mutados
    
        return poblacion #Devolver la nueva poblacion (sin evaluar)

def main():
    elitista = False
    pesos = [ 120, 95,85,76,94,96,105,85,95,300,340,175,260,125,67,88,99,67,200,120,150,170,120,89,255,124,320,220,120,75,45,130,400,310,220,130,98,115,320,145]

    precios = [ 340, 210, 287, 533, 312,450,290,170,320,245,530,800,900,889,374,1050,780,588,245,760,450,145,670,230,1030,970,490,320,150,180,275,550,320,730,560,430,289,945,670,845]
    pesoMax = 1500 #Peso máximo que se puede poner en la mochila
    nSoluciones = 10 #Tamaño de la poblacion
    maxGeneraciones = 3 #Numero de generaciones
    k = 3 #Tamaño torneo selector de padres
    cProb = 0.1 #Probabilidad de cruce
    mProb = 0.1 #Probabilidad de mutacion

    l=len(pesos)
    ##Creamos n soluciones aleatorias que sean válidas
    poblacion = []
    for i in range(nSoluciones):
        objetos = list(range(l))
        solucion = []
        peso = 0
        while peso < pesoMax:
            objeto = objetos[random.randint(0, len(objetos) - 1)]
            peso += pesos[objeto]
            if peso <= pesoMax:
                solucion.append(objeto)
                objetos.remove(objeto)

        s = []
        for i in range(l):
            s.append(0)
        for i in solucion:
            s[i] = 1
        poblacion.append([s,evaluarSolucion(s,precios,pesos,pesoMax)])
        
    
    it=1
    print("Poblacion"+"",it,"\n---------------")
    print(poblacion)
    #Guradamos la solucion de elite de la generacion inicial en caso de utilizarse elitismo
    if elitista:
        poblacion.sort(reverse=true,key=lambda poblacion:poblacion[1])
        eliteSolucion=poblacion[0]
        
    while it < maxGeneraciones:
        nSoluciones = aplicarOperadoresGeneticos(poblacion,k,cProb,mProb)
        #Modelo generacional
        poblacion = []
        for solucion in nSoluciones:
            poblacion.append([solucion[0],evaluarSolucion(solucion[0],precios,pesos,pesoMax)])
            
        #Comprobamos si se utiliza elitismo
        if elitista:
            #Ordenamos la poblacion de forma descendente con respecto a su valor de fitness
            poblacion.sort(reverse=true,key=lambda poblacion:poblacion[1])
                #Comprobamos si la solucion elite de la generación anterior es mejor que
                #la peor solucion de la  nueva generacion, y la conservamos en caso de ser asi 
            if poblacion[len(poblacion)-1][1] < eliteSolucion[1]:
                poblacion.pop()
                poblacion.append(eliteSolucion)
            #Guardamos la solucion elite de la nueva generación
            poblacion.sort(reverse=true,key=lambda poblacion:poblacion[1])  
            eliteSolucion=poblacion[0]

        it+=1
        print("Poblacion"+"",it,"\n---------------")
        print(poblacion)
        

if __name__ == "__main__":
    main()
