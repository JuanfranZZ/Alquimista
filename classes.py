import numpy as np
import copy


class referencias():

    def __init__(self):
        self.values = {'azul+': 2, 'azul-': 3,
                        'rojo+': 5, 'rojo-': 7,
                        'verde+': 11, 'verde-': 13,
                        'blanco': 0,
                        'Azul+': 17, 'Azul-': 19,
                        'Rojo+': 23, 'Rojo-': 29,
                        'Verde+': 31, 'Verde-': 37,
                        '____': -2}
        

class atomo():

    ref = referencias().values
    color = ''
    signo = ''
    valor = -2

    def __init__(self, color='', signo=''):
        self.color = color
        self.signo = signo
        if color != '____' and color != '':
            self.valor = self._assign()

    # def set(self, color, signo):
    #     self.color = color
    #     self.signo = signo
    #     self.valor = self._assign()

    def reset(self):
        self.color = ''
        self.valor = ''
        self.signo = ''

    def __repr__(self):
        return list(['color = ' + self.color,'signo = ' + self.signo, 'valor = ' + self._valor])

    def __str__(self):
        if self.color == '' or self.color == '':
            return '____'
        else:
            return list(self.ref.keys())[list(self.ref.values()).index(self.valor)]

    def _assign(self):

        if self.color == '':
            return -1

        i_color = self.color[0]

        if str.capitalize(i_color) == 'A':
            color = i_color + 'zul'
        elif str.capitalize(i_color) == 'R':
            color = i_color + 'ojo'
        elif str.capitalize(i_color) == 'V':
            color = i_color + 'erde'
        elif str.capitalize(i_color) == 'B':
            color = i_color + 'lanco'

        if self.signo == '':
            signo = ''
        else:
            if self.signo == '+' or self.signo[0] == 'p':
                signo = '+'
            elif self.signo == '-' or self.signo[0] == 'n':
                signo = '-'
        
        return self.ref[color + signo]
    
def resize(atom):
    v = copy.deepcopy(atom)
    if v.color[0].isupper():
        color = v.color.lower()
    else:
        if v.color[0] != 'b':
            color = v.color[0].upper() + v.color[1:]
        
    return atomo(color, v.signo)
    
class molecula():

    def __init__(self, atomo1: atomo, atomo2: atomo, atomo3: atomo):
        """ Cada átomo debería ser siempre de un color, debe exigirse mismo orden?"""
        self._atomo1 = atomo1
        self._atomo2 = atomo2
        self._atomo3 = atomo3
        self._valor = self._creacion(atomo1, atomo2, atomo3)
        self._valor_inverso = self._creacion_inversa(atomo1, atomo2, atomo3)

    def _creacion(self, atomo1: atomo, atomo2: atomo, atomo3: atomo):
        
        return atomo1.valor * atomo2.valor * atomo3.valor
    
    def _creacion_inversa(self, atomo1: atomo, atomo2: atomo, atomo3: atomo):
        """ se construye la molécula inversa en cuanto a tamaño, es decir, se cambia la mayúscula/minúscula del color"""

        return resize(atomo1).valor * resize(atomo2).valor * resize(atomo3).valor
    
    
class caldero():

    ref = referencias().values

    def __init__(self):
        pass

    def reaccion(self, molecula1: molecula, molecula2: molecula):

        if molecula1._valor == molecula2._valor:
            return atomo(color='____')
        
        reacc = np.gcd(molecula1._valor, molecula2._valor_inverso)

        try:
            atomo_reaccion_aux = list(self.ref.keys())[list(self.ref.values()).index(reacc)]
            return atomo(color=atomo_reaccion_aux[:-1].lower(), signo=atomo_reaccion_aux[-1])
        
        except ValueError as e:
            return atomo(color='blanco', signo='')