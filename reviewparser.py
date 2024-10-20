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
wordsStr1 = ["slightly", "slight", "hint", "hint of", "light", "watery"]
wordsStr2 = ["mild", "thin", "short"]
wordsStr3 = ["moderate", "medium-thin", "medium-short"]
wordsStr4 = ["pronounced", "medium"]
wordsStr5 = ["strong", "medium-thick", "medium-long"]
wordsStr6 = ["intense", "thick", "long"]
wordsStr123 = wordsStr1 + wordsStr2 + wordsStr3
wordsStr456 = wordsStr4 + wordsStr5 + wordsStr6

def WordPartToStrength(wordPart, isAttribute):
    
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
            print(f"Unknown attribute word part: {wordPart}")
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
                print(f"Unknown flavor word part: {wordPart}, assuming slight")
                return -1
            else:
                print(f"Empty flavor word part, Error")
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
    if note == "spice" or note == "spicy":
        return "spice"
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
    print(f"Parts Detected?: \n\nParams: {params not in ['']}\nWater, Vessel: {waterVessel not in ['']}\nTime: {times not in ['']}\nNotes: {notes not in ['']}\nAttributes: {attrNotes not in ['']}\nSteeping Notes: {SteepNotes not in ['']}\nRemark: {remark not in ['']}\nGraphScores: {GraphScores not in ['']}")
    print(f"\n----------------------")
    #params = ReviewParts[1]
    #waterVessel = ReviewParts[2]
    #times = ReviewParts[3]
    #notes = ReviewParts[4]
    #SteepNotes = ReviewParts[6]
    #attrNotes = ReviewParts[5]
    #remark = ReviewParts[7]
    #if format == "long":
    #    times = ReviewParts[7]
    #    notes = ReviewParts[8]
    #    attrNotes = ReviewParts[9]
    #    SteepNotes = ReviewParts[13]
    #    remark = ReviewParts[14]

    print(datetimeVendorTitleType + "\n----------------------")
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
    print(f"\nFlavor Notes:")
    for part in notesParts:
        
        strength, flavor = PartToMap(part)
        if strength > 0:
            attributeNotes[flavor] = strength
        else:
            flavorNotes[flavor] = strength
        print(f"Flavor Part: {part} -> Flavor: {flavor} Strength: {strength}")
            
    attr = attrNotes.replace("Attributes: ", "")
    attrParts = attr.split(", ")
    print(f"\nAttribute Notes:")
    for part in attrParts:
        strength, flavor = PartToMap(part)
        if strength > 0:
            attributeNotes[flavor] = strength
        else:
            flavorNotes[flavor] = strength
        print(f"Attribute Part: {part} -> Flavor: {flavor} Strength: {strength}")
    results["flavorNotes"] = flavorNotes
    results["attributeNotes"] = attributeNotes
    print(f"\n----------------------")
    
    # Steeping Notes
    steepNotes = SteepNotes.replace("Steeping Notes:", "")
    results["steepNotes"] = steepNotes
    
    # Remark
    remark = remark.replace("Remark: ", "")
    results["remark"] = remark
    
    # Graph Scores
    #GraphScores: Stamina: 5, Intensity: 5, Occasionality: 5, Rebuy: True, Attempts: 3, Overall: 5, Cost: 0.10, Emojis: [one.png|two.png|three.png]
    if GraphScores not in ['']:
        GraphScores = GraphScores.replace("GraphScores: ", "")
        GraphScoresParts = GraphScores.split(", ")
        for part in GraphScoresParts:
            key, value = part.split(": ")
            if key == "Rebuy":
                results[key] = value.lower() == "true"
            elif key == "Cost":
                results["CostPerGram"] = float(value)
            elif key == "Emojis":
                results["emojis"] = value.split("|")
            else:
                results[key + "Score"] = float(value)
    
    
    return results
    
    
reviewString = '''
10/05/2024 TH 2014 Bingdao raw
Params: 8.2
Water, Vessel: 99c 90tds zerowater mix, bamboo charcoal, 175mL Pumpkin
Time: 20, 30, 45, 90, 150, 300, 600, (end)
Notes: pronounced wood, resin, pronounced mahogany, pine smoke, grape, vinefruit, chrysanthemum, floral, herbal, umami, coating, mouth, powdery, heating, body
Attributes: moderate storage, powdery, medium viscosity, mild astringency, medium-short aftertaste, mild sweetness
Steeping Notes: experimental sesh - western sheng
Remark: similar to gongfu, very hardwood and resin profile, good stuff
'''.strip()
reviewJson = ""
try:
    reviewJson = parseReview(reviewString, "long")
except:
    reviewJson = parseReview(reviewString, "short")
    
# New review bonus info
reviewJson['CostPerGram'] = 0.23 # Cost per gram of tea
reviewJson['StaminaScore'] = 8 # How long the tea lasts relative to others of the same type
reviewJson['IntensityScore'] = 6 # How strong the tea is relative to others of all types
reviewJson['OccasionalityScore'] = 5 # How often you would drink this tea / How special it is
reviewJson['OverallScore'] = 8 # Overall score, Aim for 5 as average
reviewJson['Rebuy'] = True # Would you consider buying this tea again once you run out?
reviewJson['Attempts'] = 2 # How many times you've tried this tea so far
reviewJson['RawReview'] = reviewString
reviewJson['emojis'] = [
    "evergreen_tree.png",
    "dust.png",
    "christmas_tree.png",
]


print(f"Scores: \n\nCostPerGram: {reviewJson['CostPerGram']}\nStaminaScore: {reviewJson['StaminaScore']}\nIntensityScore: {reviewJson['IntensityScore']}\nOccasionalityScore: {reviewJson['OccasionalityScore']}\nOverallScore: {reviewJson['OverallScore']}\nRebuy: {reviewJson['Rebuy']}\nAttempts: {reviewJson['Attempts']}\nemojis: {reviewJson['emojis']}")
print(f"\n----------------------")
print(f"Raw Review: \n\n{reviewJson['RawReview']}")
print(f"\n----------------------")
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
    print(f"Success: \n\nSaved to {jsonPath}")
else:
    print(f"Error: \n\nFailed to save to {jsonPath}")