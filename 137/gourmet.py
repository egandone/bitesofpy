#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pairs wines and cheeses by similarity of wine name and cheese name.
"""

from collections import Counter
import operator

CHEESES = [
    "Red Leicester",
    "Tilsit",
    "Caerphilly",
    "Bel Paese",
    "Red Windsor",
    "Stilton",
    "Emmental",
    "Gruyère",
    "Norwegian Jarlsberg",
    "Liptauer",
    "Lancashire",
    "White Stilton",
    "Danish Blue",
    "Double Gloucester",
    "Cheshire",
    "Dorset Blue Vinney",
    "Brie",
    "Roquefort",
    "Pont l'Evêque",
    "Port Salut",
    "Savoyard",
    "Saint-Paulin",
    "Carré de l'Est",
    "Bresse-Bleu",
    "Boursin",
    "Camembert",
    "Gouda",
    "Edam",
    "Caithness",
    "Smoked Austrian",
    "Japanese Sage Derby",
    "Wensleydale",
    "Greek Feta",
    "Gorgonzola",
    "Parmesan",
    "Mozzarella",
    "Pipo Crème",
    "Danish Fynbo",
    "Czech sheep's milk",
    "Venezuelan Beaver Cheese",
    "Cheddar",
    "Ilchester",
    "Limburger",
]

RED_WINES = [
    "Châteauneuf-du-Pape",  # 95% of production is red
    "Syrah",
    "Merlot",
    "Cabernet sauvignon",
    "Malbec",
    "Pinot noir",
    "Zinfandel",
    "Sangiovese",
    "Barbera",
    "Barolo",
    "Rioja",
    "Garnacha",
]

WHITE_WINES = [
    "Chardonnay",
    "Sauvignon blanc",
    "Semillon",
    "Moscato",
    "Pinot grigio",
    "Gewürztraminer",
    "Riesling",
]

SPARKLING_WINES = [
    "Cava",
    "Champagne",
    "Crémant d’Alsace",
    "Moscato d’Asti",
    "Prosecco",
    "Franciacorta",
    "Lambrusco",
]

wines = {
    'red': RED_WINES,
    'white': WHITE_WINES,
    'sparkling': SPARKLING_WINES,
    'all': RED_WINES + WHITE_WINES + SPARKLING_WINES
}

def compute_intersection_count(s1, s2):
    s1_counter = Counter(s1.lower())
    s2_counter = Counter(s2.lower())
    count = 0
    for l1, c1 in s1_counter.most_common():
        count += min(c1, s2_counter[l1])
    return count

def compute_similiarity(s1, s2):
    intersect_count = compute_intersection_count(s1, s2)
    return intersect_count / (1 + (len(s1) - len(s2))**2)

def best_match_per_wine(wine_type="all"):
    """ wine cheese pair with the highest match score
    returns a tuple which contains wine, cheese, score
    """
    if wine_type not in wines:
        raise ValueError('Invalid wine_type')
    
    scores = []
    for wine in wines[wine_type]:
        for cheese in CHEESES:
            scores.append((wine, cheese, compute_similiarity(wine, cheese)))
    best_score = max(scores, key=lambda score: score[2])
    return best_score

def match_wine_5cheeses():
    """  pairs all types of wines with cheeses ; returns a sorted list of tuples,
    where each tuple contains: wine, list of 5 best matching cheeses.
    List of cheeses is sorted by score descending then alphabetically ascending.
    e.g: [
    ('Barbera', ['Cheddar', 'Gruyère', 'Boursin', 'Parmesan', 'Liptauer']),
    ...
    ...
    ('Zinfandel', ['Caithness', 'Bel Paese', 'Ilchester', 'Limburger', 'Lancashire'])
    ]
    """
    wine_scores = []
    for wine in sorted(wines['all']):
        scores = []
        for cheese in CHEESES:
            scores.append((cheese, compute_similiarity(wine, cheese)))
        # Sort the list first by name in case there are matches in the
        # similiarity the order will then be by name (alphbetical)
        scores.sort(key=lambda score: score[0])
        scores.sort(key=lambda score: score[1], reverse=True)
        wine_scores.append((wine, [score[0] for score in scores[:5]]))
    return wine_scores