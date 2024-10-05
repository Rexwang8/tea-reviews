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
def WordPartToStrength(wordPart, isAttribute):
    wordsStr1 = ["slightly", "slight", "hint", "hint of","mild", "light", "watery"]
    wordsStr2 = ["mild", "thin"]
    wordsStr3 = ["moderate", "medium-thin"]
    wordsStr4 = ["pronounced", "medium"]
    wordsStr5 = ["strong", "medium-thick"]
    wordsStr6 = ["intense", "thick"]
    wordsStr123 = wordsStr1 + wordsStr2 + wordsStr3
    wordsStr456 = wordsStr4 + wordsStr5 + wordsStr6
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
        if wordPart in wordsStr123:
            return -1
        elif wordPart in wordsStr456:
            return -2
        else:
            # if number, return num
            if wordPart.isdigit():
                return int(wordPart)
            print(f"Unknown flavor word part: {wordPart}")
            return -9
    
def PartToMap(part):
    # Split the part into the word and the strength
    isAttribute = False
    parts = part.split(" ")
    # remove empty parts
    parts = list(filter(None, parts))
    # remove parts with only spaces
    parts = list(filter(lambda x: x.strip() != "", parts))
    if len(parts) > 2:
        parts[1] = " ".join(parts[1:])
    elif len(parts) < 2:
        temp = parts[0]
        parts[0] = "slight"
        parts.append(temp)
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
    params = ReviewParts[1]
    waterVessel = ReviewParts[2]
    times = ReviewParts[3]
    notes = ReviewParts[4]
    SteepNotes = ReviewParts[6]
    attrNotes = ReviewParts[5]
    remark = ReviewParts[7]
    if format == "long":
        times = ReviewParts[7]
        notes = ReviewParts[8]
        attrNotes = ReviewParts[9]
        SteepNotes = ReviewParts[13]
        remark = ReviewParts[14]

    print(datetimeVendorTitleType + "\n")
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
    for part in notesParts:
        strength, flavor = PartToMap(part)
        if strength > 0:
            attributeNotes[flavor] = strength
        else:
            flavorNotes[flavor] = strength
    attr = attrNotes.replace("Attributes: ", "")
    attrParts = attr.split(", ")
    for part in attrParts:
        strength, flavor = PartToMap(part)
        if strength > 0:
            attributeNotes[flavor] = strength
        else:
            flavorNotes[flavor] = strength
    results["flavorNotes"] = flavorNotes
    results["attributeNotes"] = attributeNotes
    
    # Steeping Notes
    steepNotes = SteepNotes.replace("Steeping Notes:", "")
    results["steepNotes"] = steepNotes
    
    # Remark
    remark = remark.replace("Remark: ", "")
    results["remark"] = remark
    
    return results
    
    
reviewString = '''
09/23/2024 LP 2016 Old Tree Yiwu Sheng
Params: 12.7
Water, Vessel: 99c 90tds zerowater mix, bamboo charcoal, 130mL NZWH ShuiPing
Time: 15, 20, 25, 40, 60, 105, 180, 600, (end)
Notes: pronounced rock sugar, camphor, citrus, lemon, powdery, wood, resin, herbal
Attributes: pronounced sweetness, medium viscosity, moderate bitterness, pronounced storage, mild aftertaste
Steeping Notes: 25 weak
Remark: mild, sweet, woody, citrus
'''.strip()
reviewJson = ""
try:
    reviewJson = parseReview(reviewString, "long")
except:
    reviewJson = parseReview(reviewString, "short")
reviewJson['CostPerGram'] = 0.25 # Cost per gram of tea
reviewJson['StaminaScore'] = 5 # How long the tea lasts relative to others of the same type
reviewJson['IntensityScore'] = 5 # How strong the tea is relative to others of all types
reviewJson['OccasionalityScore'] = 6 # How often you would drink this tea / How special it is
reviewJson['OverallScore'] = 7.75 # Overall score, Aim for 5 as average
reviewJson['Rebuy'] = True # Would you consider buying this tea again once you run out?
reviewJson['Attempts'] = 3 # How many times you've tried this tea so far
reviewJson['RawReview'] = reviewString
reviewJson['emojis'] = [
    "lemon.png",
    "candy.png",
    "evergreen_tree.png",
]
        
'''
example
{'date': '09/17/2024', 'vendorShort': 'W2T', 'vendorLong': 'White2Tea', 'title': 'Qilan', 'year': '2024', 'type': 'Yancha', 'params': '7', 'waterVessel': '100mL Gaiwan', 'waterVesselVolume': '100', 'steepCount': 2, 'flavorNotes': {'grass': -1, 'berry': -1}, 'attributeNotes': {'roast': 2, 'sweet': 1}}
'''
print(reviewJson)

MakeFilePath(FolderJson)
WriteJson(f"{FolderJson}/RecentReview.json", reviewJson)
folderPath = f"{FolderJson}/{reviewJson['vendorLong'].replace(' ', '_')}"
MakeFilePath(folderPath)
jsonPath = f"{folderPath}/{reviewJson['title'].replace(' ', '_')}"
MakeFilePath(jsonPath)
jsonPath = f"{jsonPath}/{reviewJson['year']}_{reviewJson['date'].replace('/','_')}_Attempt_{reviewJson['Attempts']}.json"
WriteJson(jsonPath, reviewJson)

print(f"Success: \n\nSaved to {jsonPath}")