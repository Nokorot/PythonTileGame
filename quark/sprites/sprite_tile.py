
from random import randint
from sprite_sheet import qSpriteSheetHandeler
from quark.tile_grid import qLevelDataObject, qTile, qTileLevelFileReader
from quark.maths import qVec2

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

qTileLevelFileReader.levelDataObjects['SpriteSheets'] = SpriteSheetData
