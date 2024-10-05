# tea-reviews
Personal tea review scripts for generating graphs. Excludes actual reviews

Not really intended for public use, but feel free to use it if you want. I'm not responsible for any issues that may arise from using this code.

Feel free to ask me questions about the code or how to use it. I'm happy to help.

Version: 3.2.1


## Usage
1. Clone the repository
2. Install the required packages
3. Place text review in the variable in `reviewparser.py`. Supply additional information if needed.
4. Run `reviewparser.py` to generate the graphs. It will automatically pull the parsed reviews from most recent parsed review.

## Modifications
- `reviewparser.py` is the marshalls and parses text reviews into a json. You can modify or make a new script that does the same thing. Attributes are traits that have 6 levels of intensity. Flavors are traits that have 2 levels of intensity. Intensity is represented on the graph by the brightness of the color. Attributes will instead pick one of three tiles to represent the intensity, with two colors each.
- `teaprofiler.py` is the script that generates the graphs. Categories and positions on the graph are hardcoded, so you may need to modify it to fit your needs.
- `helpers.py` define vendors, tea types, their associated colors, and other helper functions.

## Examples

Current Review Format (Long)

```
09/19/2024 TWL BYH 2015 LSGC Sheng
Params: 10
Water, Vessel: 90tds zerowater mix, bamboo charcoal, 99C, 130mL NZWH ShuiPing
---
Dry: cherry, yesheng hongcha
Steamed: pronounced cherry, pronounced fruit, slight stonefruit
Wet: slight tart, slight cherry, slight stonefruit, slight tobacco
Time: 15, 20, 25, 35, 60, 120, 300, 600, (end)
Notes: slight cherry, pronounced rock sugar, slight wood, slight fruit, slight camphor, slight citrus, slight grapefruit, slight pine, light powdery
Attributes: mild bitterness, moderate sweetness, pronounced aftertaste, moderate storage, medium viscosity, slight heating
Qi? N
---
Archetype: Yang camphor, grapefruit pithy, 
Steeping Notes: steep harder, drop 25s steep
Remark: banger as always, fruity, woody and sweet
```

Current Data generated from review
```
{
    "date": "09/19/2024",
    "vendorShort": "TWL",
    "vendorLong": "Teas We Like",
    "title": "2015 LSGC",
    "year": "BYH",
    "type": "Sheng",
    "params": "10",
    "waterVessel": "130mL NZWH ShuiPing",
    "waterVesselVolume": "130",
    "steepCount": 8,
    "flavorNotes": {
        "cherry": -1,
        "rock sugar": -2,
        "wood": -1,
        "fruit": -1,
        "camphor": -1,
        "citrus": -1,
        "grapefruit": -1,
        "pine": -1,
        "powdery": -1,
        "heating": -1
    },
    "attributeNotes": {
        "bitter": 2,
        "sweetness": 3,
        "aftertaste": 4,
        "storage": 3,
        "viscosity": 4
    },
    "steepNotes": " steep harder, drop 25s steep",
    "remark": "banger as always, fruity, woody and sweet",
    "CostPerGram": 0.63,
    "StaminaScore": 6,
    "IntensityScore": 5,
    "OccasionalityScore": 8.5,
    "OverallScore": 8.5,
    "Rebuy": true,
    "Attempts": 2,
    "RawReview": "09/19/2024 TWL BYH 2015 LSGC Sheng\nParams: 10\nWater, Vessel: 90tds zerowater mix, bamboo charcoal, 99C, 130mL NZWH ShuiPing\n---\nDry: cherry, yesheng hongcha\nSteamed: pronounced cherry, pronounced fruit, slight stonefruit\nWet: slight tart, slight cherry, slight stonefruit, slight tobacco\nTime: 15, 20, 25, 35, 60, 120, 300, 600, (end)\nNotes: slight cherry, pronounced rock sugar, slight wood, slight fruit, slight camphor, slight citrus, slight grapefruit, slight pine, light powdery\nAttributes: mild bitterness, moderate sweetness, pronounced aftertaste, moderate storage, medium viscosity, slight heating\nQi? N\n---\nArchetype: Yang camphor, grapefruit pithy, \nSteeping Notes: steep harder, drop 25s steep\nRemark: banger as always, fruity, woody and sweet",
    "emojis": [
        "cherries.png",
        "christmas_tree.png",
        "don1.png"
    ]
}
```
