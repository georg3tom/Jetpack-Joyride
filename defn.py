import time


def cls(y=0, x=0):
    print("\033[%d;%dH" % (y, x))


def bullet_maintainance(bullets, board, rods, snowballs):

    for i in range(3):
        tmp = []
        for bullet in bullets:
            bullet.forward(board)
            for rod in rods:
                if rod.collision(board, bullet) == 1:
                    bullet.clear(board)
            if bullet.isvisible():
                tmp.append(bullet)
        bullets = tmp

    return bullets


def coin_maintainance(coins, board, din):
    for coin in coins:
        coin.coin_col(din)
    for coin in coins:
        coin.screen(board)


def speedb_maintainance(speedbs, board, din, prev_speed):
    for i in speedbs:
        x = i.speed_col(din)
        if x == 1:
            return speedboost(prev_speed, 1), time.time()

    return speedboost(prev_speed), prev_speed


def enemy_maintainance(boss, din, objboard):
    boss.reposition(din.retx(), objboard)


def enemy_kill(boss, din, objboard, bullets):
    for bullet in bullets:
        if boss.collision(bullet) == 1:
            bullet.clear(objboard)
        boss.gameover(objboard, din)


def speedboost(prev_speed, inp=0):
    if inp == 1:
        if time.time() - prev_speed > 8 or prev_speed == -1:
            return 1
        else:
            return 0
    elif time.time() - prev_speed > 6:
        return 0
    else:
        return 1


def snowball_maintainance(snowballs, din, objboard):
    for i in snowballs:
        i.forward(objboard)
        # x,y=i.rowcol()
        ret = din.col(0, 0, objboard)
        if ret == 1:
            i.clear(objboard)
