import math
import time
import random
import numpy as np
import pandas as pd
import concurrent.futures
from model import PlacementProcedure, generateInputs
from model import generateInputs, BRKGA
from plot import plot_3D

import matplotlib.pyplot as plt

inputs = {
    'p': [188, 188, 188, 188, 188, 188, 188, 188, 188, 188, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 260, 260, 260, 260, 260, 260, 260, 260, 260, 260, 260, 260, 260, 260, 145, 145, 145, 145, 145],
    'q': [28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 80, 80, 80, 80, 80 ],
    'r': [58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96],
    'L': [610, 610, 610, 610],
    'W': [244, 244, 244, 244],
    'H': [259, 259, 259, 259]
}

inputs = {'v':list(zip(inputs['p'], inputs['q'], inputs['r'])), 'V':list(zip(inputs['L'], inputs['W'], inputs['H']))}
print('number of boxes:',len(inputs['v']))

start_time = time.time()

inputs = generateInputs(75, 20, (600, 250, 250))

model = BRKGA(inputs, num_generations = 100, num_individuals=70, num_elites = 10, num_mutants = 7, eliteCProb = 0.7)
model.fit(patient = 15,verbose = True)
print('used bins:',model.used_bins)
print('time:',time.time() - start_time)

inputs['solution'] = model.solution
decoder = PlacementProcedure(inputs, model.solution)
print('fitness:',decoder.evaluate())

def plot_history(history, tick = 2):
    for target in ['mean', 'min']:
        plt.plot(history[target], label = target)
    plt.title('Fitness during evolution')
    plt.ylabel('fitness')
    plt.xlabel('generation')
    plt.xticks(np.arange(0, len(history['min']), tick))
    plt.legend()
    # h-line for integer
    for i in np.arange(math.ceil(min(history['min'])), int(max(history['mean']))+1):
        plt.axhline(y = i, color = 'g', linestyle = '-') 
    plt.show()

plot_history(model.history)

V = (610, 244, 259)
def draw(decoder):
    for i in range(decoder.num_opend_bins):
        container = plot_3D(V=V)
        for box in decoder.Bins[i].load_items:
            container.add_box(box[0], box[1], mode = 'EMS')
        print('Container',i, ':')
        container.findOverlapping()
        container.show()
        
draw(decoder)

