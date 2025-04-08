from scipy.optimize import curve_fit
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import sympy as sp

# Definisco la funzione per calcolare i punti di flesso
def calcolo_flessi(popt):
    '''
    Questa funzione calcola i punti di flesso della funzione
    definita da un polinomio di terzo grado.

    Parametri:
    - popt: i parametri del polinomio di terzo grado
    (a, b, c, d) ottenuti dal fit.

    Restituisce:
    - flesso: il punto di flesso della funzione
    '''
    a, b, c, d = popt
    # Definisci la variabile e la funzione
    x = sp.Symbol('x')
    f = a * x**3 + b * x**2 + c * x + d

    # Calcola la derivata seconda
    f2 = sp.diff(f, x, 2)

    # Trova i punti in cui la derivata seconda è zero
    punti_flesso = sp.solve(f2, x)

    # Controlla il cambio di concavità
    flessi_veri = []
    for p in punti_flesso:
        sinistra = f2.subs(x, p - 0.1)
        destra = f2.subs(x, p + 0.1)
        if sinistra * destra < 0:
            flessi_veri.append(p)
    return flessi_veri[0]


# Definisco la funzione per formattare l'asse y
def _format_func(value, tick_number):
    return r'$10^{%d}$' % value


# Definisco la funzione per plottare
def Plateaux_plot(x, y, popt=None, function=None, flesso=None, bool_fit=True, bool_flesso=True, 
                  plot_settings = {'title': None,
                                   'xlabel': None,
                                   'ylabel': None, 
                                   'xlim': None}):
    '''
    Questa funzione serve per fare il plot dei dati sperimentali

    Parametri:
    - tensione: lista di valori di tensione
    - count_rate: lista di valori di conteggi / tempo di acquisizione
    - popt: i parametri del polinomio di terzo grado
    - function: la funzione da plottare
    - flesso: il punto di flesso della funzione
    - plot_settings: dizionario con le impostazioni del plot
    (title, xlabel, ylabel, xlim)

    Restituisce:
    - None
    '''
    fig, ax = plt.subplots(figsize=(12, 8))
    x_for_plot = np.linspace(min(x), max(x), 100)   # i valori "continui" di tensione per plottare la funzione
    ax.scatter(x, y, marker='o', color='black', facecolor='none', label='punti sperimentali')   # dati sperimentali
    if bool_fit:
        ax.plot(x_for_plot, function(x_for_plot, *popt), color='blue', label='Fit con $ax^3 + bx^2 + cx +d$', alpha=0.5) # fit
    if bool_flesso:
        ax.scatter(flesso, function(flesso, *popt), color='red', marker='x', label='Punto di flesso')   # punto di flesso
    ax.set(**plot_settings)    # titolo e label
    plt.gca().yaxis.set_major_formatter(FuncFormatter(_format_func))   # formato asse y
    ax.grid(linestyle='--', alpha=0.5)  # griglia
    ax.legend(loc='lower right')    # legenda
    plt.show()  