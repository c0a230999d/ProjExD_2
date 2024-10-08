import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
pg.K_UP: (0, -5),
pg.K_DOWN: (0, +5),
pg.K_LEFT: (-5, 0),
pg.K_RIGHT: (+5, 0),
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとん、または、爆弾のRect
    戻り値：真理値タプル（横判定結果、縦判定結果）
    画面内ならTrue、画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    font = pg.font.Font(None, 80)
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  #空のSurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))  #ふちを透過
    bb_rct = bb_img.get_rect()  #爆弾Rectの抽出
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, -5

    overlay = pg.Surface((WIDTH, HEIGHT))  #背景
    overlay.set_alpha(200)  #背景の透明度
    overlay.fill((0, 0, 0))  #背景を黒で埋める

    kk2_img = pg.image.load("fig/8.png")  #GameOver後のこうかとん一号
    kk2_rct = kk2_img.get_rect()
    kk2_rct.center = 350, HEIGHT//2

    kk2_2_img = pg.image.load("fig/8.png")  #GameOver後のこうかとん二号
    kk2_2_rct = kk2_2_img.get_rect()
    kk2_2_rct.center = 750, HEIGHT//2
    

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0])


        if tmr > 1000:
            screen.blit(overlay, (0, 0))
            c_txt = font.render("Clear The Game!!", True, (255, 255, 255))  #GameOverの表示
            txt2_rct = c_txt.get_rect(center = (WIDTH//2, HEIGHT//2))
            screen.blit(c_txt, txt2_rct)
        
            pg.display.update()
            time.sleep(5)  #5秒待つ
            return

        if kk_rct.colliderect(bb_rct):  
            #こうかとんと爆弾が重なっていたら
            screen.blit(overlay, (0, 0))

            go_txt = font.render("GameOver", True, (255, 255, 255))  #GameOverの表示
            txt_rct = go_txt.get_rect(center = (WIDTH//2, HEIGHT//2))
            screen.blit(go_txt, txt_rct)
            
            screen.blit(kk2_img, kk2_rct)

            screen.blit(kk2_2_img, kk2_2_rct)

            pg.display.update()
            time.sleep(5)  #5秒待つ
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]  #横座標、縦座標
        #if key_lst[pg.K_UP]:
            #sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
            #sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
            #sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
            #sum_mv[0] += 5
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
