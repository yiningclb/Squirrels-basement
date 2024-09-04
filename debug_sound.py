#Border collision
if bird_y > HEIGHT - BIRD_HEIGHT or bird_y < 0:
    game_over = True
    if hit_sound:
        print("Playing sound for border collision")  
        hit_sound.play()
                    
# Collision with pipes
if bird_x + BIRD_WIDTH > pipe_x and bird_x < pipe_x + PIPE_WIDTH:
    if bird_y < HEIGHT // 2 - pipe_gap // 2 + pipe_y or bird_y + BIRD_HEIGHT > HEIGHT // 2 + pipe_gap // 2 + pipe_y:
        game_over = True
        if hit_sound:
            print("Playing sound for pipe collision")  
            hit_sound.play()  