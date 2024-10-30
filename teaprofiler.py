# Draw a taste/aroma wheel from scratch, and superimpose two polygons, one for taste and one for aroma


from enum import Enum
import math
import random
import matplotlib.pyplot as plt
import colorsys
import PIL
from PIL import Image, ImageDraw
import io

import numpy as np
from helpers import *


# given HSV, and opacity, vary the H to get a new color
def getNewColor(color, colorChange, value=1):
    hue = color[0]
    hue = (hue + colorChange) % 255
    return (hue, color[1], value)

# Return a list of hexcode colors of length n, and opacity list
def getColorMap(n, opacities, offset=0, increment=10):
    colors = []
    startingColor = (10+offset, 60, 1)
    c = startingColor
    for i in range(n):
        opacity = opacities[i]
        greyscale = False
        if opacity == -1:
            opacity = 25
            greyscale = True
            
        color = getNewColor(c, increment, opacity)
        c = color
        
        if greyscale:
            color = (color[0], 0, color[2])
        
        # Convert to hsv to rgb
        colorRGB = colorsys.hsv_to_rgb(color[0]/255, color[1]/100, color[2]/100)
        #rgb to hex
        color = plt.cm.colors.rgb2hex(colorRGB)
        colors.append(color)
    return colors

def dummy_numbers1(length):
    # random integers between 50-100 in increments of 5
    randNum = []
    for i in range(length):
        randomNumber = random.randint(50, 100)
        randNum.append(randomNumber)
    return randNum
def dummy_numbers2(length):
    # either 10, 70, 100
    randNum = []
    for i in range(length):
        randomNumber = random.choice([-1, -1, 40, 100])
        randNum.append(randomNumber)
    return randNum
def rating_to_color(ratings):
    nums = []
    for r in ratings:
        if r == 0:
            nums.append(-1)
        elif r == 1:
            nums.append(35)
        elif r == 2:
            nums.append(100)
        elif r == 3:
            nums.append(80)
    return nums

# Data structure representing the 3-tier flavor wheel for both aroma and taste
class labelData:
    label = {
    "High Notes": (15, {
        "Grass": (-1, 4, {
                "Bamboo": (-1, 1),
                "Fresh Grass": (-1, 1),
                "Hay": (-1, 1),
                "Straw": (-1, 1),
                }),
            "Vegetable": (-1, 4, {
                "Squash": (-1, 1),
                "Corn": (-1, 1),
                "Parsnip": (-1, 1),
                "Spinach": (-1, 1),
                }),
            "Herbal": (-1, 2, {
                "Mint": (-1, 1),
                "Lavender": (-1, 1),
                }),
            "Floral": (-1, 5, {
                "Rose": (-1, 1),
                "Honeysuckle": (-1, 1),
                "Orchid": (-1, 1),
                "Chrysanthemum": (-1, 1),
                "Osmanthus": (-1, 1),
                }),
        }),
    "Mid Notes": (35, {
        "Milky": (-1, 4, {
                "Cream": (-1, 1),
                "Cocoa": (-1, 1),
                "Milk Chocolate": (-1, 1),
                "Dark Chocolate": (-1, 1),
                }),
            "Nutty": (-1, 3, {
                 "Sunflower": (-1, 1),
                 "Peanut": (-1, 1),
                 "Betel Nut": (-1, 1),
                }),
            "Sweet": (-1, 6, {
                 "Brown Sugar": (-1, 1),
                 "Rock Sugar": (-1, 1),
                 "Honey": (-1, 1), 
                 "Caramel": (-1, 1),
                 "Vanilla": (-1, 1),
                 "Malt": (-1, 1),            
                }),
            "Spicy": (-1, 3, {
                "Ginger": (-1, 1),
                "Clove": (-1, 1),
                "Cinnamon": (-1, 1),
                }),
            "Berry": (-1, 2, {
                "Strawberry": (-1, 1),
                "Raspberry": (-1, 1),
                }),
            "Fruit": (-1, 3, {
                "Apple": (-1, 1),
                "Melon": (-1, 1),
                "Pear": (-1, 1),
                }),
            "Citrus": (-1, 3, {
                "Grapefruit": (-1, 1),
                "Orange": (-1, 1),
                "Lemon": (-1, 1),
                }),
            "Vinefruit": (-1, 3, {
                "Grape": (-1, 1),
                "Muscat": (-1, 1),
                "Raisin": (-1, 1),
                }),
            "Stonefruit": (-1, 4, {
                "Peach": (-1, 1),
                "Apricot": (-1, 1),
                "Plum": (-1, 1),
                "Cherry": (-1, 1),
                }),
            "Tropical": (-1, 4, {
                "Pineapple": (-1, 1),
                "Mango": (-1, 1),
                "Banana": (-1, 1),
                "Coconut": (-1, 1),
                }),
            "Marine": (-1, 3, {
                "Seaweed": (-1, 1),
                "Ocean": (-1, 1),
                "Fish": (-1, 1),
                }),
        }),
    "Low Notes": (17, {
        "Mineral": (-1, 2, {
                "Metallic": (-1, 1),
                "Petrichor": (-1, 1),
                }),
            "Earth": (-1, 4, {
                "Dirt": (-1, 1),
                "Dust": (-1, 1),
                "Old Books": (-1, 1),
                "Mushroom": (-1, 1),
                }),
            "Forest": (-1, 4, {
                "Fresh Leaves": (-1, 1),
                "Autumn Leaves": (-1, 1),
                "Moss": (-1, 1),
                "Sticks": (-1, 1),
                }),
            "Wood": (-1, 5, {
                "Pine": (-1, 1),
                "Cedar": (-1, 1),
                "Mahogany": (-1, 1),
                "Resin": (-1, 1),
                "Incense": (-1, 1),
                }),
            "Fire": (-1, 6, {
                "Ash": (-1, 1),
                 "Charcoal": (-1, 1),
                 "Pine Smoke": (-1, 1),
                 "Pipe Smoke": (-1, 1),
                 "Barbeque": (-1, 1),
                 "Tobacco": (-1, 1),
                }),
                
            "Animal": (-1, 2, {
                "Leather": (-1, 1),
                "Musk": (-1, 1),
                }),
        }),
    "Misc Notes": (8, {
            "Flavored": (-1, 3, {
                "Chenpi": (-1, 1),
                "Mi Xiang": (-1, 1),
                "Jasmine": (-1, 1),
                }),
            "Chemical": (-1, 6, {
                "Soap": (-1, 1),
                "Petrol": (-1, 1),
                "Alcohol": (-1, 1),
                "Camphor": (-1, 1),
                "Sharpness": (-1, 1),
                "Medicinal": (-1, 1),
                }),
            "Off-Tastes": (-1, 2, {
                "Wet Pile": (-1, 1),
                "Paper": (-1, 1),
                }),
            }),
    "Attributes": (12, {
        "Bitterness": (-1, 3, {
            "Mild": (-1, 1),
            "Pronounced": (-1, 1),
            "Strong": (-1, 1),
            }),
        "Sweetness": (-1, 3, {
            "Mild": (-1, 1),
            "Pronounced": (-1, 1),
            "Strong": (-1, 1),
            }),
        "Mouth": (-1, 6, {
            "Coating": (-1, 1),
            "Numbing": (-1, 1),
            "Minty": (-1, 1),
            "Juicy": (-1, 1),
            "Silky": (-1, 1),
            "Electric": (-1, 1),
            }),
        "Body": (-1, 2, {
            "Cooling": (-1, 1),
            "Heating": (-1, 1),
            }),
        "Other": (-1, 3, {
            "Sour": (-1, 1),
            "Salty": (-1, 1),
            "Umami": (-1, 1),
            }),
        }),
    "Texture": (8, {
        "Viscosity": (-1, 3, {
            "Light": (-1, 1),
            "Medium": (-1, 1),
            "Heavy": (-1, 1),
            }),
        "Astringency": (-1, 3, {
            "Light": (-1, 1),
            "Medium": (-1, 1),
            "Heavy": (-1, 1),
            }),
        "Aftertaste": (-1, 3, {
            "Short": (-1, 1),
            "Intermediate": (-1, 1),
            "Long": (-1, 1),
            }),
        "Other": (-1, 2, {
            "Powdery": (-1, 1),
            "Drying": (-1, 1),
            }),
        }),
    "Processing": (5, {
        "Storage": (-1, 3, {
            "Light": (-1, 1),
            "Medium": (-1, 1),
            "Heavy": (-1, 1),
            }),
        "Roasting": (-1, 3, {
            "Light": (-1, 1),
            "Medium": (-1, 1),
            "Heavy": (-1, 1),
            }),
        }),
    }
    def __init__(self):
        pass
    
    def getNumT1(self):
        return len(self.label)
    def getNumT2(self):
        lbs = self.getT2Labels()
        return len(lbs)
    def getNumChildrenT2(self, t1):
        num = 0
        for k1 in self.label.keys():
            v1 = self.label[k1]
            if k1 == t1:
                num += len(v1[1].keys())
        return num
    
    def getNumChildrenT3(self, t1):
        num = 0
        for k1 in self.label.keys():
            v1 = self.label[k1]
            if k1 == t1:
                for k2 in v1[1].keys():
                    v2 = v1[1][k2]
                    num += len(v2[2].keys())
        return num
    
    def getNumT3(self):
        lbs = self.getT3Labels()
        return len(lbs)
    def getPctT1(self, name):
        return self.label[name][0]
    
    def populatePercentsT2(self):
        for k in self.label.keys():
            keyPctTotal = self.getPctT1(k)
            numChildren = len(self.label[k][1])
            if numChildren == 0:
                continue
            totalWeights = 0
            for k2 in self.label[k][1].keys():
                v2 = self.label[k][1][k2]
                totalWeights += v2[1]
            increments = keyPctTotal / totalWeights
            for k2 in self.label[k][1].keys():
                prevV2 = self.label[k][1][k2]
                weight = prevV2[1]
                newV2 = (weight * increments, prevV2[1], prevV2[2])
                self.label[k][1][k2] = newV2
    def populatePercentsT3(self):
        self.populatePercentsT2()
        for k1 in self.label.keys():
            for k2 in self.label[k1][1].keys():
                v2 = self.label[k1][1][k2]
                keyPctTotal = v2[0]
                totalWeights = 0
                for k3 in v2[2].keys():
                    v3 = v2[2][k3]
                    totalWeights += v3[1]
                if totalWeights == 0:
                    continue
                increments = keyPctTotal / totalWeights
                for k3 in v2[2].keys():
                    prevV3 = v2[2][k3]
                    weight = prevV3[1]
                    newV3 = (weight * increments, prevV3[1])
                    v2[2][k3] = newV3
    
    def getT1Labels(self):
        labels = []
        for k in self.label.keys():
            labels.append(k)
        return labels
    def getT1Sizes(self):
        return [self.label[k][0] for k in self.label.keys()]
    def getT2Sizes(self):
        self.populatePercentsT2()
        sizes = []
        for k1 in self.label.keys():
            for k2 in self.label[k1][1].keys():
                v2 = self.label[k1][1][k2]
                sizes.append(v2[0])
        # round to 2 decimal places
        sizes = [round(s, 2) for s in sizes]
        return sizes
    
    def getT2Labels(self):
        labels = []
        for k1 in self.label.keys():
            for k2 in self.label[k1][1].keys():
                labels.append(k2)
        return labels
    def getT3Labels(self):
        labels = []
        for k1 in self.label.keys():
            for k2 in self.label[k1][1].keys():
                for k3 in self.label[k1][1][k2][2].keys():
                    labels.append(k3)
        return labels
    
    
    def getT3Sizes(self):
        self.populatePercentsT3()
        sizes = []
        for k1 in self.label.keys():
            v1 = self.label[k1]
            for k2 in v1[1].keys():
                v2 = v1[1][k2]
                for k3 in v2[2].keys():
                    v3 = v2[2][k3]
                    sizes.append(v3[0])
                    
        # round to 2 decimal places
        sizes = [round(s, 2) for s in sizes]
        return sizes
    
class Rating:
    allRatingsT3 = []
    allRatingsT2 = []
    allRatingsT1 = []
    def __init__(self):
        pass
    def AddT1(self, rating):
        #flatten the list
        self.allRatingsT1.append(rating)
    def AddT2(self, rating):
        self.allRatingsT2.append(rating)
    def AddT3(self, rating):
        self.allRatingsT3.append(rating)
    def AddMixedT2T3(self, rating):
        t2 = rating[0]
        t3 = rating[1]
        if t2 == [-1]:
            if sum(t3) > 3:
                t2 = [2]
            elif sum(t3) > 2:
                t2 = [1]
            else:
                t2 = [0]
        self.AddT2(t2)
        self.AddT3(t3)
    def Flatten(self):
        self.allRatingsT1 = [item for sublist in self.allRatingsT1 for item in sublist]
        self.allRatingsT2 = [item for sublist in self.allRatingsT2 for item in sublist]
        self.allRatingsT3 = [item for sublist in self.allRatingsT3 for item in sublist]
    def GetT1(self):
        return self.allRatingsT1
    def GetT2(self):
        return self.allRatingsT2
    def GetT3(self):
        return self.allRatingsT3
    
def defineRatings():
    ld = labelData()
    rating = Rating()
    t1_rating = [1,1,1, #['High Notes', 'Mid Notes', 'Low Notes',
                 1,3,3,3] # 'Misc Notes', 'Attributes', 'Texture', 'Processing']

    # High Notes
    rating.AddMixedT2T3([[-1], [0, 0, 0, 0]]) #Grass - 'Bamboo', 'Fresh Grass', 'Hay','Straw',
    rating.AddMixedT2T3([[-1], [0, 0, 0, 0]]) #Vegetable - 'Squash', 'Corn', 'Parsnip', 'Spinach',
    rating.AddMixedT2T3([[-1], [0, 0]]) #Herbal - 'Mint', 'Lavender',
    rating.AddMixedT2T3([[-1], [0, 0, 0, 0, 0]]) #Floral - 'Rose', 'Honeysuckle', 'Orchid', 'Chrysanthemum', 'Osmanthus',

    # Mid Notes
    rating.AddMixedT2T3([[-1], [0, 0, 0, 0]]) #Milky - 'Cream', 'Cocoa', 'Milk Chocolate', 'Dark Chocolate',
    rating.AddMixedT2T3([[-1], [0,0, 0]]) #Nutty - 'Sunflower', 'Peanut', 'Betel Nut',
    rating.AddMixedT2T3([[-1], [0,0,0,0,0,0]]) #Sweet - 'Brown Sugar', 'Rock Sugar', 'Honey', 'Caramel', 'Vanilla', 'Malt',
    rating.AddMixedT2T3([[-1], [0,0,0]]) #Spicy - 'Ginger', 'Clove', 'Cinnamon',
    rating.AddMixedT2T3([[-1], [0,0]]) #Berry - 'Strawberry', 'Raspberry',
    rating.AddMixedT2T3([[-1], [0,0, 0]]) #Fruit - 'Apple', 'Melon', 'Pear',
    rating.AddMixedT2T3([[-1], [0,0,0]]) #Citrus - 'Grapefruit', 'Orange', 'Lemon',
    rating.AddMixedT2T3([[-1], [0,0,0]]) #Vine - 'Grape', 'Muscat', 'Raisin',
    rating.AddMixedT2T3([[-1], [0,0,0,0]]) #Stonefruit - 'Peach', 'Apricot', 'Plum', 'Cherry',
    rating.AddMixedT2T3([[-1], [0,0,0,0]]) #Tropical - 'Pineapple', 'Mango', 'Banana', 'Coconut',
    rating.AddMixedT2T3([[-1], [0,0,0]]) #Marine - 'Seaweed', 'Ocean', 'Fish',

    # Low Notes
    rating.AddMixedT2T3([[-1], [0,0]]) #Mineral -  'Metallic', 'Petrichor',
    rating.AddMixedT2T3([[-1], [0,0,0,0]]) #Earth - 'Dirt', 'Dust', 'Old Books', 'Mushroom',
    rating.AddMixedT2T3([[-1], [0,0,0,0]]) #Forest - 'Fresh Leaves', 'Autumn Leaves', 'Moss', 'Sticks',
    rating.AddMixedT2T3([[-1], [0,0,0,0, 0]]) #Wood - 'Pine', 'Mahogony, Resin', 'Cedar', 'Incense',
    rating.AddMixedT2T3([[-1], [0,0,0,0,0,0]]) #Fire - 'Ash', 'Charcoal', 'Pine Smoke', 'Pipe Smoke', 'Barbeque', 'Tobacco',
    rating.AddMixedT2T3([[-1], [0,0]]) #Animal - 'Leather', 'Musk',
    rating.AddMixedT2T3([[-1], [0,0,0]]) #Flavored - 'Chenpi', 'Mi Xiang', 'Jasmine'
    rating.AddMixedT2T3([[-1], [0,0,0,0,0,0]]) #Chemical - 'Soap', 'Petrol', 'Camphor', 'Alcohol', 'Sharpness', 'Medicinal',
    rating.AddMixedT2T3([[-1], [0,0]]) #Off-Tastes - 'Wet Pile', 'Paper',

    rating.AddMixedT2T3([[-1], [0,0,0]]) #Bitterness - 'Mild', 'Pronounced', 'Heavy',
    rating.AddMixedT2T3([[-1], [0,0,0]]) #Sweetness - 'Mild', 'Pronounced', 'Heavy',
    rating.AddMixedT2T3([[-1], [0,0]]) #Body - 'Cooling', 'Heating',
    rating.AddMixedT2T3([[-1], [0,0,0, 0, 0, 0]]) #Mouth - 'Coating', 'Numbing', 'Minty', 'Juicy', 'Silky', 'Electric',
    rating.AddMixedT2T3([[-1], [0,0,0]]) #Other - 'Sour', 'Salty', 'Umami',

    rating.AddMixedT2T3([[-1], [0,0,0]]) #Viscosity - 'Light', 'Medium', 'Heavy',
    rating.AddMixedT2T3([[-1], [0,0,0]]) #Astringency - 'Light', 'Medium', 'Heavy',
    rating.AddMixedT2T3([[-1], [0,0, 0]]) #Aftertaste - 'Short', 'Intermediate', 'Long',
    rating.AddMixedT2T3([[-1], [0,0]]) #Other - 'Powdery', 'Drying',

    rating.AddMixedT2T3([[-1], [0,0,0]]) #Storage - 'Light', 'Medium', 'Heavy',
    rating.AddMixedT2T3([[-1], [0,0,0]]) #Roasting - 'Light', 'Medium', 'Heavy',


    rating.AddT1(t1_rating)
    rating.Flatten()
 
    if len(rating.GetT3()) != ld.getNumT3():
        RichPrintError("Error: Rating and LabelData T3 sizes do not match")
        RichPrintError(f"The number of T3 ratings is {len(rating.GetT3())} and the number of T3 labels is {ld.getNumT3()}")
        EarlyExit()
    return ld, rating

def TryGetFromDict(d, key):
    try:
        return d[key]
    except:
        return None
def ParseAttribute(pairData, attribute, Tags=["Light", "Medium", "Heavy"], OccuranceOnPie=0):
    returnVal = None
    idx = 0
    if  attribute != None and attribute != 0:
        if attribute < 3:
            # Set 2nd T3 'mild' to 1
            idx = [i for i, n in enumerate(pairData) if n[0] == Tags[0]][OccuranceOnPie]
            returnVal = (Tags[0], attribute)
        elif attribute < 5:
            attribute = attribute - 2
            idx = [i for i, n in enumerate(pairData) if n[0] == Tags[1]][OccuranceOnPie]
            returnVal = (Tags[1], attribute)
        else:
            attribute = attribute - 4
            idx = [i for i, n in enumerate(pairData) if n[0] == Tags[2]][OccuranceOnPie]
            returnVal = (Tags[2], attribute)
    return idx, returnVal

def drawPie(ld: labelData, rating:Rating, review: dict):
    # Make list of pairs of item name and scores
    flavorNotes = review["flavorNotes"]
    attributeNotes = review["attributeNotes"]
    pairedDataT3 = []
    pairedDataT2 = []
    pairedDataT1 = []
    for i in range(len(ld.getT3Sizes())): # 3rd tier
        pairedDataT3.append((ld.getT3Labels()[i], rating.GetT3()[i]))
    for i in range(len(ld.getT2Sizes())): # 2nd tier
        pairedDataT2.append((ld.getT2Labels()[i], rating.GetT2()[i]))
    for i in range(len(ld.getT1Sizes())): # 1st tier
        pairedDataT1.append((ld.getT1Labels()[i], rating.GetT1()[i]))
    
    
    for k, v in flavorNotes.items():
        RichPrintInfo(f"Processing {k} with value {v}")
        key = k.title().strip()
        value = abs(v)
        matched = False
        # T1
        for i in range(len(pairedDataT1)):
            if pairedDataT1[i][0] == key:
                oldKey = pairedDataT1[i][0]
                newValue = value
                pairedDataT1[i] = (oldKey, newValue)
                matched = True
                RichPrintInfo(f"Matched {key} to {value} in T1")
        # T2
        if not matched:
            for i in range(len(pairedDataT2)):
                if pairedDataT2[i][0] == key:
                    oldKey = pairedDataT2[i][0]
                    newValue = value
                    pairedDataT2[i] = (oldKey, newValue)
                    matched = True
                    RichPrintInfo(f"Matched {key} to {value} in T2")
        # T3
        if not matched:
            for i in range(len(pairedDataT3)):
                if pairedDataT3[i][0] == key:
                    oldKey = pairedDataT3[i][0]
                    newValue = value
                    pairedDataT3[i] = (oldKey, newValue)
                    matched = True
                    RichPrintInfo(f"Matched {key} to {value} in T3")
        
        # If not matched, print out the key
        if not matched:
            RichPrintError(f"Key {key} not found in any of the lists")
    
    # Handles Attributes seperately
    # 1, 2 is mild, 3, 4 is pronounced, 5, 6 is heavy
    idx, val = ParseAttribute(pairedDataT3, TryGetFromDict(attributeNotes, "bitter"), ["Mild", "Pronounced", "Strong"], 0)
    if idx != None and val != None:
        pairedDataT3[idx] = val
        idx2 = [i for i, n in enumerate(pairedDataT2) if n[0] == "Bitterness"][0]
        pairedDataT2[idx2] = (pairedDataT2[idx2][0], 1)
        RichPrintInfo(f"Matched bitterness to {val}")
    idx, val = ParseAttribute(pairedDataT3, TryGetFromDict(attributeNotes, "sweetness"), ["Mild", "Pronounced", "Strong"], 1)
    if idx != None and val != None:
        pairedDataT3[idx] = val
        idx2 = [i for i, n in enumerate(pairedDataT2) if n[0] == "Sweetness"][0]
        pairedDataT2[idx2] = (pairedDataT2[idx2][0], 1)
        RichPrintInfo(f"Matched sweetness to {val}")
    idx, val = ParseAttribute(pairedDataT3, TryGetFromDict(attributeNotes, "viscosity"), ["Light", "Medium", "Heavy"], 0)
    if idx != None and val != None:
        pairedDataT3[idx] = val
        idx2 = [i for i, n in enumerate(pairedDataT2) if n[0] == "Viscosity"][0]
        pairedDataT2[idx2] = (pairedDataT2[idx2][0], 1)
        RichPrintInfo(f"Matched viscosity to {val}")
    idx, val = ParseAttribute(pairedDataT3, TryGetFromDict(attributeNotes, "astringency"), ["Light", "Medium", "Heavy"], 1)
    if idx != None and val != None:
        pairedDataT3[idx] = val
        idx2 = [i for i, n in enumerate(pairedDataT2) if n[0] == "Astringency"][0]
        pairedDataT2[idx2] = (pairedDataT2[idx2][0], 1)
        RichPrintInfo(f"Matched astringency to {val}")
    idx, val = ParseAttribute(pairedDataT3, TryGetFromDict(attributeNotes, "aftertaste"), ["Short", "Long"], 0)
    if idx != None and val != None:
        pairedDataT3[idx] = val
        idx2 = [i for i, n in enumerate(pairedDataT2) if n[0] == "Aftertaste"][0]
        pairedDataT2[idx2] = (pairedDataT2[idx2][0], 1)
        RichPrintInfo(f"Matched aftertaste to {val}")
    idx, val = ParseAttribute(pairedDataT3, TryGetFromDict(attributeNotes, "storage"), ["Light", "Medium", "Heavy"], 2)
    if idx != None and val != None:
        pairedDataT3[idx] = val
        idx2 = [i for i, n in enumerate(pairedDataT2) if n[0] == "Storage"][0]
        pairedDataT2[idx2] = (pairedDataT2[idx2][0], 1)
        RichPrintInfo(f"Matched storage to {val}")
    idx, val = ParseAttribute(pairedDataT3, TryGetFromDict(attributeNotes, "roast"), ["Light", "Medium", "Heavy"], 3)
    if idx != None and val != None:
        pairedDataT3[idx] = val
        idx2 = [i for i, n in enumerate(pairedDataT2) if n[0] == "Roasting"][0]
        pairedDataT2[idx2] = (pairedDataT2[idx2][0], 1)
        RichPrintInfo(f"Matched roast to {val}")
    
    
        
    ratingT3Values = [x[1] for x in pairedDataT3]
    ratingT2Values = [x[1] for x in pairedDataT2]
    ratingT1Values = [x[1] for x in pairedDataT1]
        
    colorMap3 = getColorMap(ld.getNumT3(), rating_to_color(ratingT3Values), 100, 25)
    colorMap2 = getColorMap(ld.getNumT2(), rating_to_color(ratingT2Values), 0, 10)
    colorMap1 = getColorMap(ld.getNumT1(), rating_to_color(ratingT1Values), 0, 10)

    explode_t1 = (0, 0.1, 0.1, 0.1)
    explode_t2 = ld.getNumChildrenT2("Taste") * [0] + ld.getNumChildrenT2("Attributes") * [0.1] + ld.getNumChildrenT2("Texture") * [0.1] + ld.getNumChildrenT2("Processing") * [0.1]
    explode_t3 = ld.getNumChildrenT3("Taste") * [0] + ld.getNumChildrenT3("Attributes") * [0.1] + ld.getNumChildrenT3("Texture") * [0.1] + ld.getNumChildrenT3("Processing") * [0.1]

    # Create a figure
    fig, ax = plt.subplots(figsize=(24,24))

    # Draw the Sunburst chart as a pie chart with two different color schemes for aroma and taste
    wedge3, labels3 = ax.pie(ld.getT3Sizes(), labels=ld.getT3Labels(), colors=colorMap3, radius=1.5, startangle=90, counterclock=False, wedgeprops=dict(width=0.5, edgecolor='w'), labeldistance=0.85)

    wedge2, labels2 = ax.pie(ld.getT2Sizes(), labels=ld.getT2Labels(), colors=colorMap2, radius=1, startangle=90, counterclock=False, wedgeprops=dict(width=0.4, edgecolor='w'), labeldistance=0.8)
    wedge1, labels1 = ax.pie(ld.getT1Sizes(), labels=ld.getT1Labels(), colors=colorMap1, radius=0.6, startangle=90, counterclock=False, wedgeprops=dict(width=0.3, edgecolor='w'), labeldistance=0.73)



    fontSize = 12
    for w, l in (zip(wedge1, labels1)):
        l.set_horizontalalignment('center')
        l.set_fontsize(fontSize)
        # change angle of text
        angle =  math.ceil(((w.theta2 + w.theta1) / 2) % 360)
        if angle > 90 and angle < 270:
            angle += 180
        l.set_rotation(angle)

    for w, l in (zip(wedge2, labels2)):
        l.set_horizontalalignment('center')
        l.set_fontsize(fontSize)
        # change angle of text
        angle =  math.ceil(((w.theta2 + w.theta1) / 2) % 360)
        if angle > 90 and angle < 270:
            angle += 180
        l.set_rotation(angle)
    for w, l in (zip(wedge3, labels3)):
        l.set_horizontalalignment('center')
        l.set_fontsize(fontSize)
        # change angle of text
        angle =  math.ceil(((w.theta2 + w.theta1) / 2) % 360)
        if angle > 90 and angle < 270:
            angle += 180
        l.set_rotation(angle)
    RichPrintSuccess("Finished drawing pie")
    return fig

# Convert to PIL image
def fig2img(fig):
    """Convert a Matplotlib figure to a PIL Image and return it"""
    
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = PIL.Image.open(buf)
    return img






def repositionPie(fullImg, img):
    # Resize such that the original pie is 600x600 with 50 pad and on the top left side of the image, the full image is 1000x1000
    img = img.resize((2100, 2100), PIL.Image.ANTIALIAS)
    
    fullImg.paste(img, (225, 550))
    return fullImg



        
    
    

def drawTextOnReview(fullImg, review):
    #draw lines, horizontal at 650 and vertical at 50
    draw = ImageDraw.Draw(fullImg)
    draw.line((0, 600, 2550, 600), fill=128)
    draw.line((0, 2600, 2550, 2600), fill=128)
    draw.line((950, 0, 950, 600), fill=128)

    #draw text
    # Title (Placeholder)
    fontSizeNormal = 60
    fontSizeLarge = 85
    fontSizeSmall = 40
    font = PIL.ImageFont.truetype("arial", fontSizeNormal)
    fontLarge = PIL.ImageFont.truetype("arial", fontSizeLarge)
    fontSmall = PIL.ImageFont.truetype("arial", fontSizeSmall)
    #Top right block
    draw.text((1000, 100), f"Tea Profiler {Version}", fill="black", font=fontLarge)
    draw.text((1000, 200), "Rex Wang, Python", fill="black", font=fontSmall)
    # Notes
    #draw.text((1100, 300), f"Notes: Placeholder", fill="black", font=font)
    steepNotes = review["steepNotes"]
    if steepNotes.strip() == "":
        steepNotes = "None"
    draw.text((1000, 275), f"Steeping Notes: {steepNotes}", fill="black", font=font)
    remark = review["remark"]
    RichPrintInfo(f"{remark}")
    # break into multiple lines if necessary
    if len(remark) > 50:
        #break at word
        remarkWords = remark.split(" ")
        remarkLine1 = ""
        remarkLine2 = ""
        
        breakpointSplit = 50
        breakPointWord = 0
        buff = ""
        for i, word in enumerate(remarkWords):
            if len(buff) + len(word) < breakpointSplit:
                buff += word + " "
            else:
                breakPointWord = i
                break
        del buff
        
        for i, word in enumerate(remarkWords):
            if i < breakPointWord:
                remarkLine1 += word + " "
            else:
                remarkLine2 += word + " "
        remark = remarkLine1 + "\n" + remarkLine2
    draw.text((1000, 350), f"{remark}", fill="black", font=font)

    # Get numbers and variables
    year = getKeyFromDict(review, "year")
    teaTitle = getKeyFromDict(review, "title")
    teaType = getKeyFromDict(review, "type")
    teaType = teaType.title()
    teaTypeEnum = TeaTypeToEnum(teaType)
    vendor = getKeyFromDict(review, "vendorLong")
    teaCost = getKeyFromDict(review, "CostPerGram")
    teaCost = ParseToFloat(teaCost)
    vesselVolume = getKeyFromDict(review, "waterVesselVolume")
    vesselVolume = ParseToInt(vesselVolume)
    steeps = getKeyFromDict(review, "steepCount")
    gramsTeaUsed = getKeyFromDict(review, "params")
    gramsTeaUsed = ParseToFloat(gramsTeaUsed)
    date = getKeyFromDict(review, "date")
    attempts = getKeyFromDict(review, "Attempts")
    waterVessel = getKeyFromDict(review, "waterVessel")
    rebuy = getKeyFromDict(review, "Rebuy")
    emojis = getKeyFromDict(review, "emojis")

    # Tea Title
    draw.text((100, 100), f"{year} {teaTitle}", fill="black", font=fontLarge)
    draw.text((100, 200), f"{vendor} {teaType}", fill="black", font=font)
    # Tea year, type, vendor
    
    # tea cost
    PricePerSession = round( teaCost * gramsTeaUsed, 2)
    VolumePerSession = round(vesselVolume * steeps, 2)
    PricePerLiter = round(PricePerSession / VolumePerSession * 1000, 2)
    draw.text((100, 450), f"${teaCost}/g | ${PricePerLiter}/L | ${PricePerSession:0.2f}/Session", fill="black", font=fontSmall)
    # Current Date
    draw.text((100, 275), f"Date Tried: {date}", fill="black", font=font)
    # Number of attempts
    draw.text((100, 350), f"Attempts: {attempts}", fill="black", font=font)
    # Water Vessel, params
    draw.text((100, 500), f"{waterVessel} | {gramsTeaUsed}g | {steeps} steeps", fill="black", font=fontSmall)

    # Bottom Right block
    # Tea bars for stamina, total score, and checkbox for rebuy?
    draw.text((2000, 2500), f"Rebuy?: ", fill="black", font=font)
    emojiPath = f"{FolderEmojis}/white_check_mark.png"
    if not rebuy:
        emojiPath = f"{FolderEmojis}/x.png"
    try:
        emojiImg = PIL.Image.open(emojiPath)
        emojiImg = emojiImg.resize((100, 100), PIL.Image.ANTIALIAS)
        fullImg.paste(emojiImg, (2250, 2475), emojiImg)
    except:
        RichPrintError(f"Could not find emoji {emojiPath}")
        EarlyExit()
    
    # Emoji Summary
    draw.text((100, 2300), f"Emojis: ", fill="black", font=font)
    for i, emoji in enumerate(emojis):
        # Draw image from Emojis folder
        emojiPath = f"{FolderEmojis}/{emoji}"
        try:
            emojiImg = PIL.Image.open(emojiPath)
            if emojiImg.size[0] > 160:
                emojiImg = emojiImg.resize((160, 160), PIL.Image.ANTIALIAS)
            elif emojiImg.size[0] < 160:
                emojiImg = emojiImg.resize((160, 160), PIL.Image.ANTIALIAS)
            fullImg.paste(emojiImg, (160 + 160 * i, 2400), emojiImg)
        except:
            RichPrintError(f"Could not find emoji {emojiPath}")
            EarlyExit()
            
    # Draw central emoji
    score = getKeyFromDict(review, "OverallScore")
    score = ParseToFloat(score)
    if score >= 9.5:
        emoji = f"exploding_head.png"
    elif score > 9:
        emoji = f"heart_eyes.png"
    elif score > 8:
        emoji = f"pray.png"
    elif score > 7:
        emoji = f"yum.png"
    elif score > 6:
        emoji = f"don1.png"
    elif score > 4:
        emoji = f"tea.png"
    else:
        emoji = f"egghead.png"
        
    emojiPath = f"{FolderEmojis}/{emoji}"
    try:
        emojiImg = PIL.Image.open(emojiPath)
        emojiImg = emojiImg.resize((240, 240), PIL.Image.ANTIALIAS)
        x = int((A4PaperSizeWidthPx/2) - 100)
        y = int((A4PaperSizeHeightPx/2) - 165)
        fullImg.paste(emojiImg, (x, y), emojiImg)
    except:
        RichPrintError(f"Could not find emoji {emojiPath}")
        EarlyExit()
    
        
        
    
    # Draw a bookmark style block of color based on type of tea on the top left
    color = TeaTypeEnumToColor(teaTypeEnum)
    draw.rectangle([0, 25, 50, 150], fill=color)
    return fullImg


def drawBarChart(review):
    # Fixing random state for reproducibility
    np.random.seed(19680801)

    # Example data
    categories = ('Stamina', 'Intensity', 'Occasionality',  'Overall')
    stamina = review["StaminaScore"]
    intensity = review["IntensityScore"]
    occasionality = review["OccasionalityScore"]
    overall = review["OverallScore"]
    category_scores = [stamina, intensity, occasionality, overall]
    category_colors = ['r', 'g', 'b', 'y']
    y_pos = np.arange(len(categories))
    error = np.random.rand(len(categories))

    fig, ax = plt.subplots(figsize=(10, 2))

    hbars = ax.barh(y_pos, category_scores, xerr=error, align='center', color=category_colors)
    ax.set_yticks(y_pos, labels=categories)
    ax.invert_yaxis()  # labels read top-to-bottom
   # ax.set_title('Scores by category')
    # set limit of x
    ax.set_xlim(right=12)
    # Remove x ticks
    ax.set_xticks([0, 2, 4, 6, 8, 10])
    
    # Label bar chart
    # Label with specially formatted floats
    #ax.bar_label(hbars, fmt='%.2f')
    labels = ["Stamina", "Intensity", "Occasionality", "Overall"]
    word = ""
    if stamina >= 9:
        word = "Amazing"
    elif stamina >= 7:
        word = "Great"
    elif stamina >= 6:
        word = "Good"
    elif stamina >= 4:
        word = "Average"
    elif stamina >= 2:
        word = "Poor"
    else:
        word = "Terrible"
    labels[0] = f"Stamina: {stamina} ({word})"
    if intensity >= 9:
        word = "Intense"
    elif intensity >= 7:
        word = "Strong"
    elif intensity >= 6:
        word = "Medium"
    elif intensity >= 4:
        word = "Mild"
    elif intensity >= 2:
        word = "Weak"
    else:
        word = "Watery"
    labels[1] = f"Intensity: {intensity} ({word})"
    if occasionality >= 9:
        word = "Special"
    elif occasionality >= 7:
        word = "Unique"
    elif occasionality >= 6:
        word = "Occasional"
    elif occasionality >= 5:
        word = "Bi-Weekly"
    elif occasionality >= 3:
        word = "Weekly"
    else:
        word = "Daily"
    labels[2] = f"Occasionality: {occasionality} ({word})"
    if overall >= 9:
        word = "Incredible"
    elif overall >= 7:
        word = "Delicious"
    elif overall >= 6:
        word = "Great"
    elif overall >= 4:
        word = "Average"
    elif overall >= 2:
        word = "Poor"
    else:
        word = "Terrible"
    labels[3] = f"Overall: {overall} ({word})"
    ax.bar_label(hbars, labels=labels, padding=8)
    return fig

def getRecentReview():
    # Gets the review from the FolderJson/RecentReview.json
    path = f"{FolderJson}/RecentReview.json"
    data = ReadJson(path)
    return data
def getReviewFromPathRelative(path):
    path = path.replace("\\", "/")
    data = ReadJson(path)
    return data

# Test
#review = {'date': '09/17/2024', 'vendorShort': 'W2T', 'vendorLong': 'White2Tea', 'title': 'Qilan', 'year': '2024', 'type': 'Yancha', 'params': '7', 'waterVessel': '100mL Gaiwan', 'waterVesselVolume': '100', 'steepCount': 9, 'flavorNotes': {'grass': -1, 'berry': -1, 'sunflower': -1, 'mineral': -1}, 'attributeNotes': {'viscosity': 4, 'roast': 3, 'sweet': 2}, 'CostPerGram': 0.15, 'StaminaScore': 7, 'IntensityScore': 6, 'OccasionalityScore': 5, 'OverallScore': 8, 'Rebuy': True, 'Attempts': 1}
rpath = r'data\json\White2Tea\Qilan\2024_09_17_2024_Attempt_1.json'
#review = getReviewFromPathRelative(rpath)
review = getRecentReview()

ld, rating = defineRatings()
img = fig2img(drawPie(ld, rating, review))
fullImg = PIL.Image.new('RGB', (A4PaperSizeWidthPx, A4PaperSizeHeightPx), (255, 255, 255))
fullImg = repositionPie(fullImg, img)
fullImg = drawTextOnReview(fullImg, review)
imgbars = fig2img(drawBarChart(review=review))
# resize bars
imgbars = imgbars.resize((A4PaperSizeWidthPx, 550), PIL.Image.ANTIALIAS)
# Paste the img
fullImg.paste(imgbars, (-15, A4PaperSizeWidthPx+100))

RichPrintInfo(f"This is a tea of type... {review['type']}")
RichPrintInfo(f"Size of total image is: {fullImg.size} pixels, size of the chart is: {imgbars.size} pixels")

# Display the chart
if openGraphOnCreation:
    # Open with OS default image viewer
    fullImg.show()

# Save the image
graphPath = f"{FolderGraphs}/{review['vendorLong'].replace(' ', '_')}"
MakeFilePath(graphPath)
graphPath = f"{graphPath}/{review['year']}_{review['title'].replace(' ', '_')}"
MakeFilePath(graphPath)
graphPath = f"{graphPath}/{review['year']}_{review['date'].replace('/','_')}_Attempt_{review['Attempts']}.png"
fullImg.save(graphPath)
fullImg.save(f"{FolderGraphs}/LatestGraph.png")

RichPrintSuccess(f"Success: \n\nSaved image to {graphPath}")