import json

def correr(ruta_parametros):
    with open(ruta_parametros, 'r') as file:
        param = json.load(file)
        
    alpha = param['alpha']
    beta = param['beta']
    k_h = param['k_h']
    d_r = param['d_r']
    d_w = param['d_w']