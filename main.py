if __name__ == "__main__":
    import os, sys, inspect;
    os.chdir(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))));

    if sys.argv.__contains__('-linux'):
       sys.path.insert(0, os.path.abspath('../site-packages/linux'));
    elif sys.argv.__contains__('-macos'):
       sys.path.insert(0, os.path.abspath('../site-packages/mac os'));

sys.path.insert(0, os.path.abspath('quark'))
sys.path.insert(0, os.path.abspath('quark/tile_grid'))

from quark import qApplication
from qTileLevel import qTileLevelFileReader

from player import Player
from qSprite import qSpriteSheetHandeler

class GameApp(qApplication):
    def OnInit(self):
        levelReader = qTileLevelFileReader()
        level = levelReader.readFile('res/level.json')
        level.pos = (self.screen.size() - level.size + 48) / 2
        print self.screen.size()
        self.add(level)

        ss = qSpriteSheetHandeler().loadGridSpriteSheet("terrain_1.png", 9, 15)
        player = Player(ss[3 * 9])
        self.add(player)

    def Update(self):
        pass

if __name__ == "__main__":
    GameApp().start()
