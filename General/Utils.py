
'''
Método para dar formato de dinero a una cantidad
@author Luis GP
@param {List} lista del carrito
@return {String} formato 1,000.00
'''
def number_format(numero):
    return "$ {:,.2f}".format(numero)