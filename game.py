import tkinter as tk
import random

# --- Window setup ---
root = tk.Tk()
root.title("Real-Time Dodge Game")
root.geometry("600x400")

canvas = tk.Canvas(root, width=600, height=400, bg="white")
canvas.pack()

# --- Player setup ---
player = canvas.create_rectangle(270, 350, 330, 370, fill="blue")
player_speed = 10

# --- Obstacles & game variables ---
obstacles = []
obstacle_speed = 5
obstacle_interval = 1000  # milliseconds
game_running = True
score = 0
level = 1

score_text = canvas.create_text(50, 20, text=f"Score: {score}", font=("Arial", 14))
level_text = canvas.create_text(550, 20, text=f"Level: {level}", font=("Arial", 14))

# --- Player movement ---
def move_player(event):
    if not game_running:
        return
    x1, y1, x2, y2 = canvas.coords(player)
    if event.keysym == 'Left' and x1 > 0:
        canvas.move(player, -player_speed, 0)
    elif event.keysym == 'Right' and x2 < 600:
        canvas.move(player, player_speed, 0)

root.bind("<Left>", move_player)
root.bind("<Right>", move_player)

# --- Create obstacle ---
def create_obstacle():
    if not game_running:
        return
    x = random.randint(20, 580)
    size = random.choice([20, 30, 40])
    color = random.choice(["red", "green", "orange"])
    obstacle = canvas.create_rectangle(x, 0, x+size, size, fill=color)
    obstacles.append(obstacle)
    root.after(obstacle_interval, create_obstacle)

# --- Move obstacles ---
def move_obstacles():
    global game_running, score, level, obstacle_speed
    if not game_running:
        return
    for obstacle in obstacles[:]:
        canvas.move(obstacle, 0, obstacle_speed)
        ox1, oy1, ox2, oy2 = canvas.coords(obstacle)
        px1, py1, px2, py2 = canvas.coords(player)
        # Collision detection
        if ox2 > px1 and ox1 < px2 and oy2 > py1 and oy1 < py2:
            game_over()
            return
        # Remove obstacle if out of screen
        if oy1 > 400:
            canvas.delete(obstacle)
            obstacles.remove(obstacle)
            score += 10
            canvas.itemconfig(score_text, text=f"Score: {score}")
            if score % 100 == 0:
                level += 1
                obstacle_speed += 1
                canvas.itemconfig(level_text, text=f"Level: {level}")
    root.after(30, move_obstacles)

# --- Game over ---
def game_over():
    global game_running
    game_running = False
    canvas.create_text(300, 200, text="Game Over!", font=("Arial", 30), fill="black")
    restart_button = tk.Button(root, text="Restart", command=restart_game)
    canvas.create_window(300, 250, window=restart_button)

# --- Restart game ---
def restart_game():
    global game_running, obstacles, score, level, obstacle_speed, player
    game_running = True
    score = 0
    level = 1
    obstacle_speed = 5
    canvas.delete("all")
    # Reset player and texts
    player = canvas.create_rectangle(270, 350, 330, 370, fill="blue")
    global score_text, level_text
    score_text = canvas.create_text(50, 20, text=f"Score: {score}", font=("Arial", 14))
    level_text = canvas.create_text(550, 20, text=f"Level: {level}", font=("Arial", 14))
    obstacles = []
    create_obstacle()
    move_obstacles()
    root.bind("<Left>", move_player)
    root.bind("<Right>", move_player)

# --- Start game ---
create_obstacle()
move_obstacles()
root.mainloop()
