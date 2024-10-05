# Stores constants, settings and helpers for the rest of the project
from enum import Enum
import json
import os


A4PaperSizeWidthPx = 2550
A4PaperSizeHeightPx = 3300
Version = "v3.2.1"

FolderData = "./data"
FolderJson = "./data/json"
FolderGraphs = "./data/graphs"
FolderEmojis = "./data/emojis"
FolderStatic = "./data/static"


class VendorsEnum(Enum):
    LiquidProust = 1
    YunnanSourcing = 2
    White2Tea = 3
    BitterleafTeas = 4
    CrimsonLotusTea = 5
    TeasWeLike = 6
    TaiYangTeas = 7
    Unknown = 8
    
def VendorToEnum(vendor):
    return VendorsEnum[vendor]
def VendorEnumToString(vendor):
    if vendor == VendorsEnum.LiquidProust:
        return "Liquid Proust"
    elif vendor == VendorsEnum.YunnanSourcing:
        return "Yunnan Sourcing"
    elif vendor == VendorsEnum.White2Tea:
        return "White2Tea"
    elif vendor == VendorsEnum.BitterleafTeas:
        return "Bitterleaf Teas"
    elif vendor == VendorsEnum.CrimsonLotusTea:
        return "Crimson Lotus Tea"
    elif vendor == VendorsEnum.TeasWeLike:
        return "TeasWeLike"
    elif vendor == VendorsEnum.TaiYangTeas:
        return "TaiYangTeas"
    else:
        return "Unknown Vendor"

class TeaTypeEnum(Enum):
    Black = 1
    Green = 2
    Yancha = 3
    White = 4
    Sheng = 5
    Shou = 6
    Dancong = 7
    Anxi = 8
    GreenOolong = 9
    RoastedOolong = 10
    Fuzhuan = 11
    LiuBao = 12
    Herbal = 13
    JapaneseGreen = 14
    JapaneseBlack = 15
    JapaneseOther = 16
    Matcha = 17
    SanJian = 18
    HeiZhuan = 19
    QingZhuan = 20
    HuaZhuan = 21
    YiJuan = 22
    
def TeaTypeToEnum(teaType):
    teaType = teaType.strip().title()
    try:
        return TeaTypeEnum[teaType]
    except:
        print(f"Unknown tea type {teaType}")
        return TeaTypeEnum.Black

def TeaTypeEnumToColor(teaType):
    darkOrange = (180, 100, 0)
    black = (75, 50, 50)
    VeryBlack = (0, 0, 0)
    Green = (50, 175, 50)
    if teaType == TeaTypeEnum.Black:
        return black
    elif teaType == TeaTypeEnum.Green:
        return (50, 150, 50)
    elif teaType == TeaTypeEnum.Yancha:
        return darkOrange
    elif teaType == TeaTypeEnum.White:
        return (200, 200, 200)
    elif teaType == TeaTypeEnum.Sheng:
        return Green
    elif teaType == TeaTypeEnum.Shou:
        return VeryBlack
    elif teaType == TeaTypeEnum.Dancong:
        return (200, 50, 200)
    elif teaType == TeaTypeEnum.Anxi or teaType == TeaTypeEnum.GreenOolong:
        return (200, 200, 50)
    elif teaType == TeaTypeEnum.RoastedOolong:
        return (200, 50, 50)
    elif teaType == TeaTypeEnum.Fuzhuan:
        return (50, 200, 200)
    elif teaType == TeaTypeEnum.LiuBao:
        return (200, 50, 200)
    elif teaType == TeaTypeEnum.Herbal:
        return (50, 200, 50)
    elif teaType == TeaTypeEnum.JapaneseGreen:
        return (50, 200, 200)
    elif teaType == TeaTypeEnum.JapaneseBlack:
        return (200, 50, 50)
    elif teaType == TeaTypeEnum.JapaneseOther:
        return (50, 50, 200)
    elif teaType == TeaTypeEnum.Matcha:
        return (50, 255, 50)
    elif teaType == TeaTypeEnum.SanJian:
        return (50, 50, 255)
    elif teaType == TeaTypeEnum.HeiZhuan:
        return (255, 50, 50)
    elif teaType == TeaTypeEnum.QingZhuan:
        return (50, 255, 50)
    elif teaType == TeaTypeEnum.HuaZhuan:
        return (50, 50, 255)
    elif teaType == TeaTypeEnum.YiJuan:
        return (255, 50, 50)
    else:
        print(f"Unknown tea type {teaType}")
        return (0, 0, 0)
    
def vendorShortToLong(vendorShort):
    if vendorShort == "LP":
        return "Liquid Proust"
    elif vendorShort == "YS":
        return "Yunnan Sourcing"
    elif vendorShort == "W2T":
        return "White2Tea"
    elif vendorShort == "BLT":
        return "Bitterleaf Teas"
    elif vendorShort == "CLT":
        return "Crimson Lotus Tea"
    elif vendorShort == "TWL":
        return "TeasWeLike"
    elif vendorShort == "TYT":
        return "TaiYangTeas"
    else:
        return "Unknown Vendor"
def typeToTypeMap(teaType):
    if teaType == "Raw":
        return "Sheng"
    elif teaType == "Ripe":
        return "Shou"
    else:
        return teaType
    
# Operations with errors
def getKeyFromDict(dict, key):
    try:
        return dict[key]
    except:
        print(f"Key {key} not found in dict, Please check manually")
        return None
def ParseToFloat(value):
    try:
        return float(value)
    except:
        print(f"Could not parse {value} to float")
def ParseToInt(value):
    try:
        return int(value)
    except:
        print(f"Could not parse {value} to int")
    
    
# Os Operations
def MakeFilePath(path):
    # Make sure the folder exists
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Made {path} folder")
    else:
        print(f"{path} folder already exists")
        
def WriteFile(path, content):
    with open(path, "w") as file:
        file.write(content)
    print(f"Written {path} to file")
    
def ReadFile(path):
    with open(path, "r") as file:
        print(f"Read {path} from file")
        return file.read()

def ListFiles(path):
    return os.listdir(path)

def WriteJson(path, data):
    with open(path, "w") as file:
        json.dump(data, file)
    print(f"Written {path} to file")

def ReadJson(path):
    with open(path, "r") as file:
        print(f"Read {path} from file")
        return json.load(file)
    