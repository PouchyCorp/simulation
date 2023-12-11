import pygame as p
import random
import cProfile as profile

p.font.init()
font = p.font.SysFont('Comic Sans MS', 9)

HEIGHT = 500
WIDTH = HEIGHT
WIN = p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption("Pouchy's Lore")
height_width = 50
cell_width = HEIGHT / height_width
last = p.time.get_ticks()
bugHp = 1000
fruitHp = 2

class CELL():
    def __init__(self, x, y):
        self.state = 0
        self.x = x
        self.y = y
        self.neighborCount = 0
        self.appartenance = []
        self.master = 0
        self.seedCountdown = -1
        self.colo = (0, 0)
        self.size = 0
        self.hp = 0
        pass

    def checkCell(self, dir, state, bypass = False):
        if dir == "UP" and self.y > 0 and (ca[self.x][self.y - 1].state in state or bypass):
            return True
        elif dir == "DOWN" and self.y < height_width - 1 and (ca[self.x][self.y + 1].state in state or bypass):
            return True
        elif dir == "RIGHT" and self.x < height_width - 1 and (ca[self.x + 1][self.y].state in state or bypass):
            return True
        elif dir == "LEFT" and self.x > 0 and (ca[self.x - 1][self.y].state in state or bypass):
            return True
        elif dir == "UP LEFT" and self.y > 0 and self.x > 0 and (ca[self.x - 1][self.y - 1].state in state or bypass):
            return True
        elif dir == "UP RIGHT" and self.x < height_width - 1 and self.y > 0 and (ca[self.x + 1][self.y - 1].state in state or bypass):
            return True
        elif dir == "DOWN LEFT" and self.y < height_width - 1 and self.x > 0 and (ca[self.x - 1][self.y + 1].state in state or bypass):
            return True
        elif dir == "DOWN RIGHT" and self.y < height_width - 1 and self.x < height_width - 1 and (ca[self.x + 1][self.y + 1].state in state or bypass):
            return True
        return False

    def checkNeighbor(self, state):
        self.neighborCount = 0
        self.neighbors = []
        if self.checkCell('UP', [state]):
            self.neighborCount += 1
            self.neighbors.append(ca[self.x][self.y - 1])
        if self.checkCell('DOWN', [state]):
            self.neighborCount += 1
            self.neighbors.append(ca[self.x][self.y + 1])
        if self.checkCell('LEFT', [state]):
            self.neighborCount += 1
            self.neighbors.append(ca[self.x - 1][self.y])
        if self.checkCell('RIGHT', [state]):
            self.neighborCount += 1
            self.neighbors.append(ca[self.x + 1][self.y])
        if self.checkCell('UP LEFT', [state]):
            self.neighborCount += 1
            self.neighbors.append(ca[self.x - 1][self.y - 1])
        if self.checkCell('UP RIGHT', [state]):
            self.neighborCount += 1
            self.neighbors.append(ca[self.x + 1][self.y - 1])
        if self.checkCell('DOWN LEFT', [state]):
            self.neighborCount += 1
            self.neighbors.append(ca[self.x - 1][self.y + 1])
        if self.checkCell('DOWN RIGHT', [state]):
            self.neighborCount += 1
            self.neighbors.append(ca[self.x + 1][self.y + 1])

        return self.neighborCount

    def moveCell(self, dir, destState = [0], bypass = False):
        dest = 0
        if self.checkCell(dir, destState) or bypass:
            if dir == "UP" and hasattr(ca[self.x][self.y - 1], 'futureState') is False:
                dest = ca[self.x][self.y - 1]
            elif dir == "DOWN" and hasattr(ca[self.x][self.y + 1], 'futureState') is False:
                dest = ca[self.x][self.y + 1]
            elif dir == "RIGHT" and hasattr(ca[self.x + 1][self.y], 'futureState') is False:
                dest = ca[self.x + 1][self.y]
            elif dir == "LEFT" and hasattr(ca[self.x - 1][self.y], 'futureState') is False:
                dest = ca[self.x - 1][self.y]
            elif dir == "UP LEFT" and hasattr(ca[self.x - 1][self.y - 1], 'futureState') is False:
                dest = ca[self.x - 1][self.y - 1]
            elif dir == "UP RIGHT" and hasattr(ca[self.x + 1][self.y - 1],'futureState') is False:
                dest = ca[self.x + 1][self.y - 1]
            elif dir == "DOWN LEFT" and hasattr(ca[self.x - 1][self.y + 1],'futureState') is False:
                dest = ca[self.x - 1][self.y + 1]
            elif dir == "DOWN RIGHT" and hasattr(ca[self.x + 1][self.y + 1],'futureState') is False:
                dest = ca[self.x + 1][self.y + 1]
            if dest != 0:
                dest.futureState = self.state
                dest.size = self.size
                dest.hp = self.hp
                self.hp = 0
                self.size = 0
                self.futureState = dest.state

    def cellCount(self, searched_state):
        count = 0
        for line in ca:
            for cell in line:
                if cell.state == searched_state:
                    count += 1
        return count

    def ruleSand(self):
        downLeft = self.checkCell('DOWN LEFT', [0])
        downRight = self.checkCell('DOWN RIGHT', [0])
        if self.state != 0 and self.checkCell('DOWN', [0]) == False:
            if downLeft and downRight:
                if random.randint(1, 2) == 1:
                    self.moveCell('DOWN LEFT')
                else:
                    self.moveCell('DOWN RIGHT')
            elif downLeft:
                self.moveCell('DOWN LEFT')
            elif downRight:
                self.moveCell('DOWN RIGHT')

    def ruleWater(self):
        right = self.checkCell('RIGHT', [0])
        left = self.checkCell('LEFT', [0])
        if self.checkCell('DOWN', [0]):
            self.moveCell('DOWN')
        if self.checkCell('DOWN', [0]) == False:
            if right and left:
                if random.randint(1, 2) == 1:
                    self.moveCell('LEFT')
                else:
                    self.moveCell('RIGHT')
            elif left:
                self.moveCell('LEFT')
            elif right:
                self.moveCell('RIGHT')


    def rulePlant(self):
        if self.state == 2 and self.y > 0 and ca[self.x][self.y - 1].state == 0 and self.checkCell('DOWN', [1]) == True:
            ca[self.x][self.y - 1].futureState = 3
            ca[self.x][self.y - 1].master = self
            self.appartenance.append(ca[self.x][self.y - 1])

        if self.state == 2 and self.seedCountdown != -1:
            self.seedCountdown -= 1
            if self.seedCountdown < 0:
                self.futureState = 0

        if self.state == 3 and self.checkCell('DOWN', [2]):
            self.neighborCount += 1

        if self.state == 3 and (self.master.state != 2 or self.neighborCount == 0):
            if random.randint(0,100) == 0:
                self.futureState = 0
            pass
        
        if random.randint(0,10) == 1:
            if self.state == 3 and hasattr(self.master, 'appartenance') and len(self.master.appartenance) <= self.master.size:
                randDir = random.randint(0, 4)
                if randDir in [0,1,2] and self.checkCell('UP', [0]) and self.checkCell('UP LEFT', [0]) and self.checkCell('UP RIGHT', [0]):
                    ca[self.x][self.y - 1].futureState = 3
                    ca[self.x][self.y - 1].master = self.master
                    self.master.appartenance.append(self)
                elif randDir == 3 and self.checkCell('RIGHT', [0]) and self.checkCell('UP RIGHT', [0]) and self.checkCell('DOWN RIGHT', [0]):
                    ca[self.x + 1][self.y].futureState = 3
                    ca[self.x + 1][self.y].master = self.master
                    self.master.appartenance.append(self)
                elif randDir == 4 and (self.checkCell('LEFT', [0])) and self.checkCell('UP LEFT', [0]) and self.checkCell('DOWN LEFT', [0]):
                    ca[self.x - 1][self.y].futureState = 3
                    ca[self.x - 1][self.y].master = self.master
                    self.master.appartenance.append(self)


        rand = random.randint(10, 20)
        if self.state == 3 and self.master.size <= len(self.master.appartenance) < self.master.size + 2:
            if self.checkCell('UP', [0]) and self.checkNeighbor(3) < 3:
                self.master.appartenance.append(ca[self.x][self.y - 1])
                ca[self.x][self.y - 1].futureState = 5
                ca[self.x][self.y - 1].master = self.master
                ca[self.x][self.y - 1].hp = fruitHp

        if self.state == 5 and self.hp < 0:
            self.futureState = 2
            self.size = rand
            plant_count = -1
            for cell in self.master.appartenance:
                if cell.state == 5:
                    plant_count += 1
            if plant_count == 0:
                self.master.seedCountdown = 100

    def ruleBug(self):
        rand = random.randint(1, 4)
        self.hp -= 1
        cell.checkNeighbor(5)

        if self.hp > 0:
            if rand == 1 and self.checkCell('UP', [0]):
                self.moveCell('UP')
            elif rand == 2 and self.checkCell('DOWN', [0]):
                self.moveCell('DOWN')
            elif rand == 3 and self.checkCell('LEFT', [0]):
                self.moveCell('LEFT')
            elif rand == 4 and self.checkCell('RIGHT', [0]):
                self.moveCell('RIGHT')

            if self.neighborCount > 0:
                if self.checkCell('UP', [0]):
                    if hasattr(ca[self.x][self.y - 1], 'futureState') == False:
                        ca[self.x][self.y - 1].futureState = 4
                        ca[self.x][self.y - 1].hp = bugHp
                        self.neighbors[0].hp -= 1
                        # print(self.neighbors[0].hp)
        else:
            self.futureState = 0

    def ruleBomb(self):
        if self.checkCell('DOWN', [1]):
            for x in range(self.x - 5, self.x + 5):
                for y in range(self.y - 5, self.y + 5):
                    for line in ca:
                        for cell in line:
                            if cell.x == x and cell.y == y:
                                cell.futureState = 0

    def color(self):
        if self.state == 3 and self.colo[1] != 3:
            col = {'#009900': 3, '#007f00': 3, '#00b200': 3, '#006600': 3}
            self.colo = random.choice(list(col.items()))
        if self.state == 1 and self.colo[1] != 1:
            col = {'#FFBF00': 1, '#FDDA0D': 1, '#FFC000': 1, '#F4BB44': 1}
            self.colo = random.choice(list(col.items()))

    def gravity(self):
        if self.checkCell('DOWN', [0, 7], True):
            self.moveCell('DOWN', [0, 7])

    def update(self):
        if hasattr(self, 'futureState'):
            self.state = self.futureState
            del self.futureState
        else:
            pass


def copy_properties(src, dest):
    for attr in vars(src).keys():
        setattr(dest, attr, getattr(src, attr))


ca = [[CELL(n, i) for i in range(height_width)] for n in range(height_width)]

run = True
clock = p.time.Clock()
while run:
    clock.tick(60)
    now = p.time.get_ticks()
    click = p.mouse.get_pressed()
    roundedPosX = round(p.mouse.get_pos()[0] / cell_width)
    roundedPosY = round(p.mouse.get_pos()[1] / cell_width)

    for event in p.event.get():
        if event.type == p.QUIT:
            run = False
            break
        if event.type == p.KEYDOWN:
            if event.key == p.K_KP2:
                for line in ca:
                    for cell in line:
                        if cell.x == roundedPosX and cell.y == roundedPosY:
                            cell.state = 2
                            cell.size = random.randint(10, 20)
            elif event.key == p.K_KP4:
                for line in ca:
                    for cell in line:
                        if cell.x == roundedPosX and cell.y == roundedPosY:
                            cell.state = 4
                            cell.hp = bugHp
            elif event.key == p.K_KP6:
                for line in ca:
                    for cell in line:
                        if cell.x == roundedPosX and cell.y == roundedPosY:
                            cell.state = 6
            elif event.key == p.K_KP7:
                for line in ca:
                    for cell in line:
                        if cell.x == roundedPosX and cell.y == roundedPosY:
                            cell.state = 7


    if click[0]:
        for line in ca:
            for cell in line:
                if cell.x == roundedPosX and cell.y == roundedPosY:
                    if cell.checkCell('RIGHT', [0]):
                        ca[cell.x + 1][cell.y].futureState = 1
                    if cell.checkCell('DOWN RIGHT', [0]):
                        ca[cell.x + 1][cell.y + 1].futureState = 1
                    if cell.checkCell('DOWN', [0]):
                        ca[cell.x][cell.y + 1].futureState = 1
                    cell.futureState = 1
    if click[2]:
        for line in ca:
            for cell in line:
                if cell.x == roundedPosX and cell.y == roundedPosY:
                    ca[cell.x + 1][cell.y].futureState = 0
                    ca[cell.x + 1][cell.y + 1].futureState = 0
                    ca[cell.x][cell.y + 1].futureState = 0

    for line in ca:
        for cell in line:
            if cell.state != 0:
                if cell.state in [1, 2, 6]:
                    cell.gravity()
                if cell.state == 1 or cell.state == 2:
                    cell.checkNeighbor(1)
                if cell.state == 1:
                    cell.ruleSand()
                if cell.state == 3:
                    cell.checkNeighbor(3)
                if cell.state == 2 or cell.state == 3 or cell.state == 5:
                    cell.rulePlant()
                if cell.state == 4:
                    cell.ruleBug()
                if cell.state == 6:
                    cell.ruleBomb()
                if cell.state == 7:
                    cell.ruleWater()
            

    for line in ca:
        for cell in line:
            cell.update()
            if cell.state == 1:
                cell.color()
            if cell.state == 3:
                cell.color()

    WIN.fill('#457b9d')

    for line in ca:
        for cell in line:
            if cell.state == 1:
                rect = p.Rect(cell.x * cell_width, cell.y * cell_width, cell_width, cell_width)
                p.draw.rect(WIN, cell.colo[0], rect)
            elif cell.state == 2:
                rect = p.Rect(cell.x * cell_width, cell.y * cell_width, cell_width, cell_width)
                p.draw.rect(WIN, '#5B653B', rect)
            elif cell.state == 3:
                rect = p.Rect(cell.x * cell_width, cell.y * cell_width, cell_width, cell_width)
                p.draw.rect(WIN, cell.colo[0], rect)
            elif cell.state == 4:
                rect = p.Rect(cell.x * cell_width, cell.y * cell_width, cell_width, cell_width)
                p.draw.rect(WIN, 'grey', rect)
            elif cell.state == 5:
                rect = p.Rect(cell.x * cell_width, cell.y * cell_width, cell_width, cell_width)
                p.draw.rect(WIN, 'red', rect)
            elif cell.state == 6:
                rect = p.Rect(cell.x * cell_width, cell.y * cell_width, cell_width, cell_width)
                p.draw.rect(WIN, 'black', rect)
            elif cell.state == 7:
                rect = p.Rect(cell.x * cell_width, cell.y * cell_width, cell_width, cell_width)
                p.draw.rect(WIN, 'blue', rect)
            #stat = font.render(str(cell.size),False,(0,0,0))
            #WIN.blit(stat,(cell.x*cell_width,cell.y*cell_width))

    x = 0
    pos = font.render(str(roundedPosX) + ' ' + str(roundedPosY), False, (100, 100, 100))
    WIN.blit(pos, (20, 20))
    # for i in range(height_width):
    # text = font.render(str(i),False,(100,100,100))
    # WIN.blit(text,(0+x,0))
    # WIN.blit(text,(0,0+x))
    # p.draw.line(WIN,(10,10,10),(0+x,0),(0+x,WIDTH))
    # p.draw.line(WIN,(10,10,10),(0,0+x),(WIDTH,0+x))
    # x+=cell_width
    # del x
    p.display.update()