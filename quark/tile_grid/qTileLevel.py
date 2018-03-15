
import sys,os
import copy

import json
import numpy as np
from qMaths import qVec2
from quark import qGameObject

class qTile(qGameObject):
    cord = qVec2(0,0)
    tileSize = qVec2(48, 48)

class qTileLayer(qGameObject):
    tiles = []
    width, height = 0,0
    layerDepth = None

    def __init__(self, parent):#, width, heigt, tiles):
        qGameObject.__init__(self, parent)
        pass#self.width, self.height, self.tiles = width, height, tiles

    def add(self, instent, cords, **kwargs):
        qGameObject.add(self, instent, cords=cords, **kwargs)

class qTileLevel(qGameObject):
    size = qVec2(0,0)

    def __init__(self, tileSize, size):
        self.tileLayers = {}
        self.tileSize = tileSize
        self.size = qVec2(size) * tileSize

    def add(self, child, depth=0, **kwargs):
        if isinstance(child, qTileLayer):
            if self.tileLayers.__contains__(depth) \
                and self.tileLayers[depth] != None:
                self.tileLayers[depth].removeMe()
            self.tileLayers[depth] = child
            child.layerDepth = depth
        qGameObject.add(self, child, depth, **kwargs)

class qLevelDataObject():
    symbols = []
    def __init__(self, levelReader, data):
        self.levelReader = levelReader
        self.symbols = {
            int: data['symbols'],
            list: data['symbols']
        }[type(data['symbols'])]

    def getSymbolData(self, symbol):
        return None

# *** Begin Sprite Data ***
from qSprite import qSpriteSheetHandeler
class SpriteSheetData(qLevelDataObject):
    sheetHandeler = qSpriteSheetHandeler()

    def __init__(self, reader, data):
        qLevelDataObject.__init__(self, reader, data)
        filename, XY = data['file'], data['XY']
        self.sheet = self.sheetHandeler.loadGridSpriteSheet(filename, *XY)
        self.sheetCords = {k:(v[0] + v[1]*XY[0]) for (k,v) in zip(data['symbols'], data['values'])}
        self.tiles = {}

        self.symbols = {k:(v[0] + v[1]*XY[0]) for (k,v) in zip(data['symbols'], data['values'])}

    def getSymbolData(self, symbol):
        if self.tiles.__contains__(symbol):
            return self.tiles[symbol]
        tile = qSimpleSpriteTile(self.sheet[self.sheetCords[symbol]])
        self.tiles[symbol] = tile
        return tile

from random import randint
class qSimpleSpriteTile(qTile):
    sprite = None
    def __init__(self, sprite):
        self.sprite = sprite
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))

    def pos(self):
        return qVec2(self.cords) * self.tileSize

    def getPos(self):
        if self.parent == None:
            return self.pos()
        return self.pos() + self.parent.getPos();

    def Render(self, screen):
        pos = self.getPos()
        #screen.rect(self.color, (pos[0], pos[1], self.sprite.width, self.sprite.height))
        if self.sprite:
            self.sprite.render(screen, self.getPos())
# *** End Sprite Data ***

class qTileLevelFileReader():
    levelDataObjects = {
        'SpriteSheets': SpriteSheetData
    }
    symbols = {}

    def __init__(self):
        self.symbols = copy.copy(self.symbols)
        self.levelDataObjects = copy.copy(self.levelDataObjects)

    def getSymbolData(self, symbol):
        if symbol == '00':
            return None
        return self.symbols[symbol].getSymbolData(symbol)

    def initLevelDataObj(self, dataObj, data):
        ldo = self.levelDataObjects[dataObj](self, data)
        for s in ldo.symbols:
            self.symbols[s] = ldo

    def readFile(self, levelFile):
        data = json.load(open(levelFile))
        level = qTileLevel(qVec2(48, 48), data['size'])
        for dataObj in self.levelDataObjects.keys():
            if data.__contains__(dataObj):
                objData = data[dataObj]
                if type(data[dataObj]) == list:
                    for x in objData:
                        self.initLevelDataObj(dataObj, x)
                else:
                    self.initLevelDataObj(dataObj, objData)

        for lKey in filter(lambda x: x.startswith('#Layer'), data.keys()):
            layerIndex = int(lKey[len('#Layer'):])
            tlayer = qTileLayer(level)
            for (j, row) in enumerate(data[lKey]):
                for (i, s) in enumerate(row.split(' ')):
                    tileInstant = self.getSymbolData(str(s))
                    if tileInstant: tlayer.add(tileInstant, (i, j))
            level.add(tlayer, layerIndex)
        return level
