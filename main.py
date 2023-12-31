""" 
Se pretende codificar todas las posibilidades de combinaciones para el juego del alquimista, 
teniendo en cuenta que los diferentes componentes dan lugar a diferentes resultados. 

Pero lo que no debemos conocer es los componentes, pero sí el resultado.
Para ello la codificación se basará en descomposición de números primos (por color y 
signo de las moleculas, el tamaño no importa):

Azul + : 2
Azul - : 3
Rojo + : 5
Rojo - : 7
Verde + : 11
Verde - : 13


Por lo que cada componente molecular será la multiplicación de 3 de estos elementos, y la unión de dos el producto de estos.
En el caso de que en su descomposición haya un elemento al cuadrado nos dará la solución, si no lo hay la composición obtenida
será aguachirri.
"""
from classes import atomo, molecula

from combinations import calculate_maps
import json

import matplotlib.pyplot as plt
import matplotlib as mplt
import numpy as np

from tqdm.auto import tqdm
import time

import dask
from dask.diagnostics import ProgressBar

# from multiprocessing import Process
# import multiprocessing as mp


def create_combinations_file(filename):
    # definiendo átomos:

    atomos = {'a+': atomo('azul', '+'), 'a-': atomo('azul', '-'),
            'v+': atomo('verde', '+'), 'v-': atomo('verde', '-'),
            'r+': atomo('rojo', '+'), 'r-': atomo('rojo', '-'),
            'b': atomo('blanco'),
            'A+': atomo('Azul', '+'), 'A-': atomo('Azul', '-'),
            'V+': atomo('Verde', '+'), 'V-': atomo('Verde', '-'),
            'R+': atomo('Rojo', '+'), 'R-': atomo('Rojo', '-')}

    # print(atomos['r-'])

    moleculas = {'3+': molecula(atomos['A+'], atomos['R+'], atomos['V+']),
                    '3-': molecula(atomos['A-'], atomos['R-'], atomos['V-']),
                    'r+': molecula(atomos['a-'], atomos['r+'], atomos['V-']),
                    'r-': molecula(atomos['a+'], atomos['r-'], atomos['V+']),
                    'a+': molecula(atomos['a+'], atomos['R-'], atomos['v-']),
                    'a-': molecula(atomos['a-'], atomos['R+'], atomos['v+']),
                    'v+': molecula(atomos['A-'], atomos['r-'], atomos['v+']),
                    'v-': molecula(atomos['A+'], atomos['r+'], atomos['v-']),
                    }

    # calculamos las combinaciones posibles
    sols = calculate_maps(moleculas)

    # To json
    to_file = json.dumps(sols, indent=4)

    # Writing to combinations.json
    with open(filename, "w") as outfile:
        outfile.write(to_file)


def read_combinations_file(filename):
    f = open(filename)
    s = json.load(f)
    f.close()
    return s

def plot_colored_grid(title, data, text='', color_text='w', colors=['white', 'green'], bounds=[0, 0.5, 1], 
                      grid=True, labels=False, frame=True, save=True):
    """Plot 2d matrix with grid with well-defined colors for specific boundary values.

    :param data: 2d matrix
    :param colors: colors
    :param bounds: bounds between which the respective color will be plotted
    :param grid: whether grid should be plotted
    :param labels: whether labels should be plotted
    :param frame: whether frame should be plotted
    """
    path = 'solutions/'

    # create discrete colormap
    cmap = mplt.colors.ListedColormap(colors)
    norm = mplt.colors.BoundaryNorm(bounds, cmap.N)

    # enable or disable frame
    plt.figure(frameon=frame)

    # show grid
    if grid:
        plt.grid(axis='both', color='k', linewidth=1) 
        plt.xticks(np.arange(0.5, data.shape[0], 1))  # correct grid sizes
        plt.yticks(np.arange(0.5, data.shape[1], 1))

    # disable labels
    if not labels:
        plt.tick_params(bottom=False, top=False, left=False, right=False, labelbottom=False, labelleft=False) 

    # plot data matrix
    plt.imshow(data, cmap=cmap, norm=norm)

    # Loop over data dimensions and create text annotations.
    for i in range(data.shape[0]):
        for j in range(i,data.shape[1]):
            if i==j: # print diagonal
                c = 'k'
                plt.text(j, i, i+1, ha="center", va="center", color=c)
            else:
                c = color_text
                plt.text(j, i, text[i][j], ha="center", va="center", color=c)

    # title
    plt.title(title)

    if save:
        plt.savefig(path + title + '.png', dpi=160)
    else: 
        plt.show()
    plt.close()

@dask.delayed
def final_plots(sol:dict, id:str):

    # id = args[1]
    # sol = args[0]

    path = 'solutions/'

    valores = np.array([np.array(x) for x in sol['valores']])
    signos = np.array([np.array(x) for x in sol['signos']])
    
    moleculas = sol['solucion']
    

    with open(path+id +'.txt', "w") as outfile:
        outfile.writelines(' '.join(moleculas))

    # upper triangular matrix to avoid sym matrix (waste)
    zeros = np.zeros_like(valores)
    tri_val = np.triu(valores, k=1)
    tri_sign = np.triu(signos, k=1)

    # diagonal with elements id
    empty = np.array(['' for _ in range(zeros.size)]).reshape(zeros.shape)

    # resumen
    plot_colored_grid(id+'_resumen', tri_val, text=tri_sign, colors=['black','white','blue', 'red', 'green'], bounds=[-3,-1,1,4,8,14])

    # rojo
    plot_colored_grid(id+'_rojo', tri_val, text=empty, colors=['white', 'red', 'white'], bounds=[-3,4,8,14])
    # azul
    plot_colored_grid(id+'_azul', tri_val, text=empty, colors=['white','blue', 'white'], bounds=[-3,1,4,14])
    # verde
    plot_colored_grid(id+'_verde', tri_val, text=empty, colors=['white', 'green'], bounds=[-3,8,14])
    
    # positivo
    plot_colored_grid(id+'_positivos', zeros, text=tri_sign == '+', color_text='k', colors=['white'], bounds=[-1,1])
    # negativo
    plot_colored_grid(id+'_negativos', zeros, text=tri_sign == '-', color_text='k', colors=['white'], bounds=[-1,1])
    # neutro
    plot_colored_grid(id+'_neutros', zeros, text=tri_sign == '', color_text='k', colors=['white'], bounds=[-1,1])

# @dask.delayed
def test():
    a = 2
    for _ in range(10):
        a += a


if __name__=='__main__':

    filename = "combinations.json"

    # create_combinations_file(filename)
    start = time.time()
    print('reading...')
    sols = read_combinations_file(filename)
    fin = time.time()
    print(f'...file read! in {(fin-start)} secs')

    # ID de las combinaciones
    IDs = list(sols.keys())

    with open('soluciones.txt', 'w') as f:
        soluciones = ['\n' + str(ii) + ' ' + str(sols[ii]['solucion']) for ii in IDs]
        f.writelines(soluciones)

    #----------------- Single core ------------------------
    # for id in tqdm(IDs): # por cada combinacion
    #    final_plots(sols[id], id)
    #------------------------------------------------------

    #----------------------- dask -------------------------
    start = time.time()
    print('Creating tasks...')
    tasks = []
    for id in tqdm(IDs):
        tasks.append(final_plots(sols[id],id))
    fin = time.time()
    print(f'Tasks loaded in {(fin-start)}secs')

    print('')
    print('Procesing...')
    with ProgressBar():
        dask.compute(tasks, scheduler='processes', num_workers=14)
    #--------------------------------------------------------

    #--------------------  Pool -----------------------------
    # pool = mp.Pool(processes=4)
    # inputs = [(sols[id], id) for id in IDs]
    # pool.map(final_plots, inputs)
    #--------------------------------------------------------

    #------------------------ Process------------------------
    # for id in tqdm(IDs): # por cada combinacion
    #     p = Process(target=final_plots, args=(sols[id],id))
    #     p.start()
    #     p.join()
    #---------------------------------------------------------