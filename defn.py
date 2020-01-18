
def cls(y=0, x=0):
    print("\033[%d;%dH" % (y, x))

def bullet_maintainance(bullets,board,rods):
    for i in range(3):
        tmp = []
        for bullet in bullets:
            bullet.forward(board)
            for rod in rods:
                if  rod.col(board,bullet) == 1:
                    bullet.clear(board)
            if bullet.isvisible() == True:
                tmp.append(bullet)
        bullets = tmp

    return bullets

def coin_maintainance(coins,board,din):
    for coin in coins:
        coin.coin_col(din)
    for coin in coins:
        coin.screen(board)
