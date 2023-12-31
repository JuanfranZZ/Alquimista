from classes import caldero
import itertools as iter
import random, tqdm

def calculate_maps(moleculas, _seed=0):

    c = caldero()

    # todas las permutaciones posibles
    rows = list(iter.permutations(list(moleculas.keys())))

    random.seed(_seed)

    ids = random.sample(range(10000, 2*len(rows)), len(rows)) # random id to identify the matrix combination
    sols = dict()

    for n_row, row in enumerate(tqdm.tqdm(rows)): # por cada permutación

        # iniciamos la matriz de combinaciones
        matrix_reacciones = []

        # mapa único
        for i, element_r in enumerate(row): # por cada elemento en fila
            matrix_reacciones.append([])
            for element_c in row: # por cada elemento en columna
                matrix_reacciones[i].append(c.reaccion(moleculas[element_r], moleculas[element_c]))

        sols[ids[n_row]] = {'solucion':row,
                            'resumen':[[y.__str__() for y in x] for x in matrix_reacciones],
                            'colores':[[y.color for y in x] for x in matrix_reacciones],
                            'signos':[[y.signo for y in x] for x in matrix_reacciones],
                            'rojos':[[(1 if y.color == 'rojo' else 0) for y in x] for x in matrix_reacciones],
                            'verdes':[[(1 if y.color == 'verde' else 0) for y in x] for x in matrix_reacciones],
                            'azules':[[(1 if y.color == 'azul' else 0) for y in x] for x in matrix_reacciones],
                            'valores':[[y.valor for y in x] for x in matrix_reacciones]}
                            # 'reacciones':matrix_reacciones,}
        
    return sols