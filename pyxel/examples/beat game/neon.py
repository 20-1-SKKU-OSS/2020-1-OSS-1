"""https://github.com/Ssnnaaiill/NEON을 바탕으로 만들었습니다."""

import os, random, pyxel

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120

class App:
    def reset(self):
        self.r, self.r2 = random.uniform(1, 5), random.uniform(20, 25)
        self.x, self.y = random.uniform(self.r2, SCREEN_WIDTH - self.r2), random.uniform(self.r2, SCREEN_HEIGHT - self.r2)
        self.color = random.randrange(8, 13, 2)

    def levelup(self):
        self.reset()
        self.FLAG = 3
        self.LEVEL += 1
        self.TIME = self.LEVEL * 200
        self.LIFE += (self.LEVEL * 5)

    def trueReset(self, flag):
        self.reset()
        self.SCORE, self.FLAG, self.LIFE, self.LEVEL = 0, flag, 100, 1
        self.TIME = self.LEVEL * 200
    
    def title_circ(self, x, y):
        for i in range(3): pyxel.circ(x + i * 15, y, 5, (i + 4) * 2)
        pyxel.text(60, 62, "<-", 7)
        pyxel.text(75, 62, "->", 7)
        pyxel.text(90, 62, "sp", 7)
    
    def calc(self):
        if(abs(self.r2 - self.r) < 2): self.SCORE += 20
        elif(abs(self.r2 - self.r) < 5): self.SCORE += 10
        else: self.SCORE += 0
        if self.SCORE >= self.BESTSCORE:
            self.BESTSCORE = self.SCORE
            f = open("bestscore.dat", "w")
            f.write(str(self.BESTSCORE))
            f.close()
    def loselife(self): self.LIFE -= 5

    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, caption="B E A T")

        pyxel.mouse(True)
        if os.path.exists("bestscore.dat"): self.BESTSCORE = int(open("bestscore.dat", "r").readline())
        else: self.BESTSCORE = 0
        self.trueReset(0)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q): pyxel.quit()
        if pyxel.btnp(pyxel.KEY_SPACE):
            if self.FLAG == 0 or self.FLAG == 3: 
                self.FLAG = 1
                pyxel.load("beatgame.pyxres")
                pyxel.playm(0, loop=True)
            if self.FLAG == 2: self.trueReset(1)
        if self.FLAG == 1 and (pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.KEY_SPACE)):
            if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.KEY_SPACE): self.calc()
            else: self.loselife()
            self.reset()
        if self.r >= self.r2:
            self.loselife()
            self.reset()
        if self.LIFE <= 0: self.FLAG = 2
        if self.TIME == 0: self.levelup()

    def draw(self):
        pyxel.cls(0)
        if self.FLAG == 0:
            pyxel.text(64, 45, "N E O N", pyxel.frame_count % 16)
            self.title_circ(63, 64)
            if(pyxel.frame_count % 60 < 30): 
                pyxel.text(34, 80, "press spacebar to start", 5) 
                pyxel.text(24, 90, "control with LEFT RIGHT SPACE", 5)
        elif self.FLAG == 1:
            self.TIME -= 1
            pyxel.circ(self.x, self.y, self.r, self.color)
            pyxel.circb(self.x, self.y, self.r2, self.color)
            pyxel.text(10, 10, "score " + str(self.SCORE), 7)
            pyxel.text(10, 20, "life  " + str(self.LIFE), 7)
            pyxel.text(10, 30, "level  " + str(self.LEVEL), 7)
            pyxel.text(10, 40, "time  " + str(self.TIME), 7)
            pyxel.text(110, 10, "best  " + str(self.BESTSCORE), 7)
            if self.r < self.r2: self.r += 1
            else: self.reset()
        elif self.FLAG == 2:
            pyxel.text(64, 45, "GAME OVER", pyxel.frame_count % 16)
            pyxel.text(61, 55, "score : " + str(self.SCORE), 7)
            if(pyxel.frame_count % 60 < 30):
                if self.SCORE == self.BESTSCORE: pyxel.text(61, 65, "BEST SCORE!", 7)
                pyxel.text(30, 90, "press spacebar to restart", 5)
        else:
            pyxel.text(64, 45, "LEVEL UP!", pyxel.frame_count % 16)
            if(pyxel.frame_count % 60 < 30): pyxel.text(30, 80, "press spacebar to continue", 5)

App()