from tkinter import *
import re


'''
Entry widget que solo deja escribir numeros reales
@author Luis GP
@return {None}
'''
class Number_Entry(Entry):
    def __init__(self, *args, **kwargs):
        
        if 'parent' in kwargs:
            self.parent = kwargs['parent']
        else:
            self.parent = args[0]

        if 'validate' not in kwargs:
            kwargs['validate'] = "key"
        
        if 'validatecommand' not in kwargs:
            kwargs['validatecommand'] = (self.parent.register(self.es_num), "%S", "%d")

        super().__init__(*args, **kwargs)




    '''
    Método para validar que la entrada sean numeros reales positivos o negativos
    @author Luis GP
    @param {String} caracter tecleado
    @param {int} 1 si es inserción o 0 si es eliminación
    @return {Boolean}
    '''
    def es_num(self, txt, code):
        
        if int(code) == 1:

            cadena = f"{self.get()}{txt}"
            if re.match(r'(^\-?([0-9]+|[0-9]+?(\.[0-9]*))$)|(^\-{1}$)', cadena):
                return True
            else:
                return False
                
        else:
        
            return True