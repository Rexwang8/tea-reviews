from helpers import *
# Word to Strength Mapping
# 1 - Slightly
# 2 - Mild
# 3 - Moderate
# 4 - Pronounced
# 5 - Strong
# 6 - Intense

# Word to Flavor Mapping
# -1 - Slightly
# -2 - Pronounced

# Convert the word part to a strength value
# Positive values are for attributes, negative values are for flavors
# Attributes are (0-6), flavors are (0- -2)
wordsStrNone = ["None", "none", "n/a", "nil", "null", "zero", "0"]
wordsStr1 = ["slightly", "slight", "hint", "hint of", "light", "watery"]
wordsStr2 = ["mild", "thin", "short"]
wordsStr3 = ["moderate", "medium-thin", "medium-short"]
wordsStr4 = ["pronounced", "medium"]
wordsStr5 = ["strong", "medium-thick", "medium-long"]
wordsStr6 = ["intense", "thick", "long"]
wordsStr123 = wordsStr1 + wordsStr2 + wordsStr3
wordsStr456 = wordsStr4 + wordsStr5 + wordsStr6

def WordPartToStrength(wordPart, isAttribute):
    if wordPart in wordsStrNone:
        return 0
    
    if isAttribute:
        if wordPart in wordsStr1:
            return 1
        elif wordPart in wordsStr2:
            return 2
        elif wordPart in wordsStr3:
            return 3
        elif wordPart in wordsStr4:
            return 4
        elif wordPart in wordsStr5:
            return 5
        elif wordPart in wordsStr6:
            return 6
        else:
            # if number, return num
            if wordPart.isdigit():
                return int(wordPart)
            RichPrintError(f"Unknown attribute word part: {wordPart}")
            return -8
    else:
        if wordPart.isdigit():
            return int(wordPart)
        if wordPart in wordsStr123:
            return -1
        elif wordPart in wordsStr456:
            return -2
        else:
            if len(wordPart) > 0:
                RichPrintWarning(f"Unknown flavor word part: {wordPart}, assuming slight")
                return -1
            else:
                RichPrintError(f"Empty flavor word part, Error")
                EarlyExit()
                return -9
    
def PartToMap(part):
    # Split the part into the word and the strength
    isAttribute = False
    parts = part.split(" ")
    # remove empty parts
    parts = list(filter(None, parts))
    # remove parts with only spaces
    parts = list(filter(lambda x: x.strip() != "", parts))
    # if there is more than one part, combine the rest into the flavor
    if len(parts) > 2:
        parts[1] = " ".join(parts[1:])
        
    # if there is only one part, assume slight
    elif len(parts) < 2:
        temp = parts[0]
        parts[0] = "slight"
        parts.append(temp)
    # if there is two parts but first isn't a number of "slight", assume two part flavor
    elif not parts[0].isdigit() and (parts[0].lower() not in wordsStr123 and parts[0].lower() not in wordsStr456):
        temp = ' '.join(parts)
        parts[0] = "slight"
        parts[1] = temp
        parts = parts[:2]
        
    strength = parts[0].lower()
    flavor = parts[1].lower()
    flavor = NoteAliasesMap(flavor)
    # Handled differently from flavor notes
    attributes = ["storage", "sweetness", "viscosity", "bitter", "roast", "astringency", "aftertaste"]
    if flavor in attributes:
        isAttribute = True
    strengthValue = WordPartToStrength(strength, isAttribute)
    
    return (strengthValue, flavor)
    
def NoteAliasesMap(note):
    if note == "juicy" or note == "juiciness" or note == "tart":
        return "juicy"
    if note == "floral" or note == "flowers":
        return "floral"
    if note == "fruity" or note == "fruit":
        return "fruit"
    if note == "spice":
        return "spicy"
    if note == "woody" or note == "wood":
        return "wood"
    if note == "smoke" or note == "smoky":
        return "smoke"
    if note == "mineral" or note == "minerals":
        return "mineral"
    if note == "vegetal" or note == "vegetal":
        return "vegetable"
    if note == "grassy" or note == "grassiness":
        return "grass"
    if note == "thick":
        return "viscosity"
    if note == "bitterness" or note == "bite":
        return "bitter"
    if note == "papery":
        return "paper"
    if note == "warm" or note == "warming":
        return "heating"
    else:
        return note
    
def parseReview(reviewString, format):
    results = {}
    # Seperate into lines
    ReviewParts = reviewString.split("\n")
    datetimeVendorTitleType = ReviewParts[0]
    
    # Sort parts based on starting word
    # Params: 
    params, waterVessel, times, notes, attrNotes, SteepNotes, remark = "", "", "", "", "", "", ""
    GraphScores = ""
    for part in ReviewParts:
        if part.startswith("Params:"):
            params = part
        elif part.startswith("Water, Vessel:"):
            waterVessel = part
        elif part.startswith("Time:"):
            times = part
        elif part.startswith("Notes:"):
            notes = part
        elif part.startswith("Attributes:"):
            attrNotes = part
        elif part.startswith("Steeping Notes:"):
            SteepNotes = part
        elif part.startswith("Remark:"):
            remark = part
        elif part.startswith("GraphScores:"):
            GraphScores = part
            
    # Parts Detected:
    RichPrintInfo(f"Parts Detected?: \n\nParams: {params not in ['']}\nWater, Vessel: {waterVessel not in ['']}\nTime: {times not in ['']}\nNotes: {notes not in ['']}\nAttributes: {attrNotes not in ['']}\nSteeping Notes: {SteepNotes not in ['']}\nRemark: {remark not in ['']}\nGraphScores: {GraphScores not in ['']}")
    RichPrintSeparator()
    RichPrintInfo(datetimeVendorTitleType)
    RichPrintSeparator()
    parts = datetimeVendorTitleType.split(" ")
    # Date
    date = parts[0]
    parts = parts[1:]
    # vendor
    vendor = parts[0]
    parts = parts[1:]
    # title
    title = " ".join(parts[:-1])
    parts = parts[-1:]
    year = title.split(" ")[0]
    title = title[len(year):].strip()
    # type
    teaType = parts[0]
    results["date"] = date
    results["vendorShort"] = vendor
    results["vendorLong"] = vendorShortToLong(vendor)
    results["title"] = title
    results["year"] = year
    results["type"] = typeToTypeMap(teaType)

    params = params.replace("Params: ", "")
    results["params"] = params

    waterVessel = waterVessel.replace("Water, Vessel: ", "")
    waterVesselParts = waterVessel.split(", ")
    waterVessel = waterVesselParts[-1]
    waterVesselVolume = waterVessel.split(" ")[0].replace("mL", "")
    results["waterVessel"] = waterVessel
    results["waterVesselVolume"] = waterVesselVolume

    # Count number of steeps, occurances of numbers
    timesString = times.replace("Time: ", "").replace(", (end)", "")
    timesParts = timesString.split(", ")
    steepCount = len(timesParts)
    results["steepCount"] = steepCount
    notes = notes.replace("Notes: ", "")
    notesParts = notes.split(", ")
    flavorNotes = {}
    attributeNotes = {}
    RichPrintInfo(f"Flavor Notes:")
    for part in notesParts:
        
        strength, flavor = PartToMap(part)
        if strength > 0:
            attributeNotes[flavor] = strength
        elif strength < 0:
            flavorNotes[flavor] = strength
        else:
            RichPrintWarning(f"Ignoring Note: {part} due to 0 strength")
        RichPrintInfo(f"Flavor Part: {part} -> Flavor: {flavor} Strength: {strength}")
            
    attr = attrNotes.replace("Attributes: ", "")
    attrParts = attr.split(", ")
    RichPrintSeparator()
    RichPrintInfo(f"Attribute Notes:")
    for part in attrParts:
        strength, flavor = PartToMap(part)
        if strength > 0:
            attributeNotes[flavor] = strength
        else:
            flavorNotes[flavor] = strength
        RichPrintInfo(f"Attribute Part: {part} -> Flavor: {flavor} Strength: {strength}")
    results["flavorNotes"] = flavorNotes
    results["attributeNotes"] = attributeNotes
    RichPrintSeparator()
    
    # Steeping Notes
    steepNotes = SteepNotes.replace("Steeping Notes:", "")
    results["steepNotes"] = steepNotes
    
    # Remark
    remark = remark.replace("Remark: ", "")
    results["remark"] = remark
    
    # Graph Scores
    #GraphScores: Stamina: 5, Intensity: 5, Occasionality: 5, Rebuy: True, Attempts: 3, Overall: 5, Cost: 0.10, Emojis: [one.png|two.png|three.png]
    if GraphScores not in ['']:
        RichPrintInfo(f"Parsing Graph Scores...")
        GraphScores = GraphScores.replace("GraphScores: ", "")
        GraphScoresParts = GraphScores.split(", ")
        for part in GraphScoresParts:
            key, value = part.split(": ")
            #print(f"Key: {key} Value: {value}")
            if key == "Rebuy":
                results[key] = value.lower() == "true"
                RichPrintInfo(f"Added Rebuy: {results[key]}")
            elif key == "Cost":
                results["CostPerGram"] = float(value)
                RichPrintInfo(f"Added Cost: {results['CostPerGram']}")
            elif key == "Emojis":
                results["emojis"] = value.replace("[", "").replace("]", "").split("|")
                RichPrintInfo(f"Added Emojis: {results['emojis']}")
            elif key == "Attempts":
                results[key] = int(value)
                RichPrintInfo(f"Added {key}: {results[key]}")
            else:
                results[key] = float(value)
                RichPrintInfo(f"Added {key} Score: {results[key]}")
    
    
    return results
    
    
reviewString = '''
10/15/2024 LP 2006 Maocha Raw
Params: 9
Water, Vessel: 90tds zerowater mix, bamboo charcoal, 99C, 130mL NZWH ShuiPing
---
Dry: petrichor
Steamed: petrichor, parsnip, beets
Wet: petrichor, parsnip, beets, carrots
Time: 10, 15, 20, 30, 45, 75, 120, 180, 360, (end)
Notes: pronounced petrichor, dust, dirt, mineral, earth, parsnip, spicy, heating, silky
Attributes: intense storage, mild sweetness, medium viscosity, medium aftertaste
Qi? N
---
Archetype: Wet Aged Sheng | Petrichor, Dust, Parsnip
GraphScores: StaminaScore: 9, IntensityScore: 5, OccasionalityScore: 6, Rebuy: False, Attempts: 1, OverallScore: 6, Cost: 0.20, Emojis: [dust.png|parsnip.png|stone.png]
Steeping Notes:
Remark: very dark, almost purple mark,  carrot-y
'''.strip()
reviewJson = ""
try:
    reviewJson = parseReview(reviewString, "long")
except:
    reviewJson = parseReview(reviewString, "short")
    
# New review bonus info
reviewJson['RawReview'] = reviewString
'''
reviewJson['CostPerGram'] = 0.09 # Cost per gram of tea
reviewJson['StaminaScore'] = 7 # How long the tea lasts relative to others of the same type
reviewJson['IntensityScore'] = 3 # How strong the tea is relative to others of all types
reviewJson['OccasionalityScore'] = 3 # How often you would drink this tea / How special it is
reviewJson['OverallScore'] = 4.5 # Overall score, Aim for 5 as average
reviewJson['Rebuy'] = True # Would you consider buying this tea again once you run out?
reviewJson['Attempts'] = 1 # How many times you've tried this tea so far

reviewJson['emojis'] = [
    "fallen_leaf.png",
    "hay.png",
    "beer.png",
]
'''

RichPrintInfo(f"Scores: \n\nCostPerGram: {reviewJson['CostPerGram']}\nStaminaScore: {reviewJson['StaminaScore']}\nIntensityScore: {reviewJson['IntensityScore']}\nOccasionalityScore: {reviewJson['OccasionalityScore']}\nOverallScore: {reviewJson['OverallScore']}\nRebuy: {reviewJson['Rebuy']}\nAttempts: {reviewJson['Attempts']}\nemojis: {reviewJson['emojis']}")
RichPrintSeparator()
RichPrintInfo(f"Raw Review: \n\n{reviewJson['RawReview']}")
RichPrintSeparator()
'''
example
{'date': '09/17/2024', 'vendorShort': 'W2T', 'vendorLong': 'White2Tea', 'title': 'Qilan', 'year': '2024', 'type': 'Yancha', 'params': '7', 'waterVessel': '100mL Gaiwan', 'waterVesselVolume': '100', 'steepCount': 2, 'flavorNotes': {'grass': -1, 'berry': -1}, 'attributeNotes': {'roast': 2, 'sweet': 1}}
'''

MakeFilePath(FolderJson)
WriteJson(f"{FolderJson}/RecentReview.json", reviewJson)
folderPath = f"{FolderJson}/{reviewJson['vendorLong'].replace(' ', '_')}"
MakeFilePath(folderPath)
jsonPath = f"{folderPath}/{reviewJson['year']}_{reviewJson['title'].replace(' ', '_')}"
MakeFilePath(jsonPath)
jsonPath = f"{jsonPath}/{reviewJson['year']}_{reviewJson['date'].replace('/','_')}_Attempt_{reviewJson['Attempts']}.json"
WriteJson(jsonPath, reviewJson)

if os.path.exists(jsonPath):
    RichPrintSuccess(f"Success: \n\nSaved to {jsonPath}")
else:
    RichPrintError(f"Error: \n\nFailed to save to {jsonPath}")