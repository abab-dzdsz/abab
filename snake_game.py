import turtle
import time
import random
import tkinter as tk

# 游戏常量定义
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# 颜色定义
BG_COLOR = "#2C3E50"  # 深蓝色背景
GRID_COLOR = "#34495E"  # 网格线颜色
BORDER_COLOR = "#E74C3C"  # 边界颜色
SNAKE_HEAD = "#2ECC71"  # 蛇头颜色（绿色）
SNAKE_BODY = "#58D68D"  # 蛇身颜色（浅绿）
FOOD_COLOR = "#E74C3C"  # 食物颜色（红色）
SCORE_COLOR = "#F1C40F"  # 分数颜色
STATUS_COLOR = "#3498DB"  # 状态提示颜色
FAIL_COLOR = "#E74C3C"  # 失败原因颜色

# 方向常量
UP = (0, 1)
DOWN = (0, -1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    """蛇类，负责管理蛇的移动、生长和绘制"""
    
    def __init__(self, screen):
        """初始化蛇的位置和状态"""
        self.screen = screen
        self.head_color = "#FFFFFF"  # 初始白色
        self.body_color = "#CCCCCC"  # 蛇身稍浅
        self.reset()
        self.create_turtles()
    
    def reset(self):
        """重置蛇的状态，用于游戏重新开始"""
        self.body = [
            (GRID_WIDTH // 2, GRID_HEIGHT // 2),
            (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2),
            (GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2)
        ]
        self.direction = RIGHT
        self.next_direction = RIGHT
    
    def create_turtles(self):
        """创建蛇的绘制对象"""
        # 蛇头
        self.head_turtle = turtle.Turtle()
        self.head_turtle.speed(0)
        self.head_turtle.shape("square")
        self.head_turtle.color(self.head_color)
        self.head_turtle.penup()
        self.head_turtle.shapesize(0.9, 0.9)  # 稍微大一点
        
        # 蛇身
        self.body_turtles = []
        for _ in range(len(self.body) - 1):
            t = turtle.Turtle()
            t.speed(0)
            t.shape("square")
            t.color(self.body_color)
            t.penup()
            t.shapesize(0.8, 0.8)  # 蛇身稍微小一点
            self.body_turtles.append(t)
    
    def update_color(self, head_color, body_color):
        """更新蛇的颜色"""
        self.head_color = head_color
        self.body_color = body_color
        self.head_turtle.color(head_color)
        for t in self.body_turtles:
            t.color(body_color)
    
    def update_direction(self, new_direction):
        """更新蛇的移动方向，防止180度转向"""
        if (new_direction[0] != -self.direction[0] or 
            new_direction[1] != -self.direction[1]):
            self.next_direction = new_direction
    
    def move(self):
        """移动蛇，更新位置（不穿墙）"""
        self.direction = self.next_direction
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.body.insert(0, new_head)
        self.body.pop()
    
    def check_wall_collision(self):
        """检查蛇头是否撞墙（提前检查下一个位置）"""
        head_x, head_y = self.body[0]
        next_head_x = head_x + self.direction[0]
        next_head_y = head_y + self.direction[1]
        return (next_head_x < 0 or next_head_x >= GRID_WIDTH or 
                next_head_y < 0 or next_head_y >= GRID_HEIGHT)
    
    def grow(self):
        """蛇吃到食物后增长一节"""
        tail_x, tail_y = self.body[-1]
        self.body.append((tail_x, tail_y))
        
        # 添加新的身体海龟（使用当前颜色）
        t = turtle.Turtle()
        t.speed(0)
        t.shape("square")
        t.color(self.body_color)
        t.penup()
        t.shapesize(0.8, 0.8)
        self.body_turtles.append(t)
    
    def draw(self):
        """绘制蛇"""
        # 绘制蛇头
        head_x, head_y = self.body[0]
        self.head_turtle.goto(head_x * GRID_SIZE - SCREEN_WIDTH//2 + GRID_SIZE//2,
                              head_y * GRID_SIZE - SCREEN_HEIGHT//2 + GRID_SIZE//2)
        
        # 绘制蛇身
        for i, segment in enumerate(self.body[1:]):
            seg_x, seg_y = segment
            self.body_turtles[i].goto(seg_x * GRID_SIZE - SCREEN_WIDTH//2 + GRID_SIZE//2,
                                     seg_y * GRID_SIZE - SCREEN_HEIGHT//2 + GRID_SIZE//2)
    
    def check_self_collision(self):
        """检查蛇头是否与身体碰撞"""
        head = self.body[0]
        return head in self.body[1:]
    
    def clear(self):
        """清除蛇的所有海龟对象"""
        self.head_turtle.hideturtle()
        for t in self.body_turtles:
            t.hideturtle()


class Food:
    """食物类，负责管理食物的生成和绘制"""
    
    def __init__(self, screen):
        """初始化食物位置"""
        self.screen = screen
        self.position = (0, 0)
        
        # 创建食物海龟
        self.food_turtle = turtle.Turtle()
        self.food_turtle.speed(0)
        self.food_turtle.shape("circle")
        self.food_turtle.color(FOOD_COLOR)
        self.food_turtle.penup()
        self.food_turtle.shapesize(0.8, 0.8)
        
        self.generate_new()
    
    def generate_new(self):
        """生成新的食物位置（随机位置，距离边界至少4格）"""
        margin = 4  # 边界容错
        self.position = (
            random.randint(margin, GRID_WIDTH - 1 - margin),
            random.randint(margin, GRID_HEIGHT - 1 - margin)
        )
    
    def draw(self):
        """绘制食物"""
        food_x, food_y = self.position
        self.food_turtle.goto(food_x * GRID_SIZE - SCREEN_WIDTH//2 + GRID_SIZE//2,
                              food_y * GRID_SIZE - SCREEN_HEIGHT//2 + GRID_SIZE//2)
    
    def clear(self):
        """清除食物海龟"""
        self.food_turtle.hideturtle()


class Game:
    """游戏主类，负责游戏循环、事件处理和状态管理"""
    
    def __init__(self):
        """初始化游戏环境"""
        # 创建屏幕
        self.screen = turtle.Screen()
        self.screen.title("贪吃蛇游戏 🐍")
        self.screen.setup(width=SCREEN_WIDTH + 100, height=SCREEN_HEIGHT + 180)  # 增加高度显示按键说明
        self.screen.bgcolor(BG_COLOR)
        self.screen.tracer(0)
        
        # 绘制边界和网格
        self.draw_border()
        self.draw_grid()
        
        # 创建游戏对象
        self.snake = Snake(self.screen)
        self.food = Food(self.screen)
        
        # 游戏状态
        self.score = 0
        self.game_over = False
        self.paused = False
        self.waiting_for_start = True  # 等待用户开始游戏
        
        # 速度控制
        self.base_speed = 0.080  # 初始速度（原来的0.6倍，更慢）
        self.speed_multiplier = 1.0  # 速度倍数
        self.max_speed_multiplier = 2.5  # 最大速度倍数
        self.last_speed_increase = 0  # 上次加速时的分数
        
        # 彩虹变色控制
        self.rainbow_colors = [
            "#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#9400D3"
        ]
        self.rainbow_index = 0
        self.rainbow_mode = False  # 是否处于彩虹模式
        
        # 创建分数显示
        self.score_pen = turtle.Turtle()
        self.score_pen.speed(0)
        self.score_pen.color(SCORE_COLOR)
        self.score_pen.penup()
        self.score_pen.hideturtle()
        self.score_pen.goto(0, SCREEN_HEIGHT//2 + 30)
        self.update_score_display()
        
        # 创建状态显示
        self.status_pen = turtle.Turtle()
        self.status_pen.speed(0)
        self.status_pen.color(STATUS_COLOR)
        self.status_pen.penup()
        self.status_pen.hideturtle()
        self.status_pen.goto(0, SCREEN_HEIGHT//2 + 60)
        
        # 创建失败原因显示
        self.fail_reason_pen = turtle.Turtle()
        self.fail_reason_pen.speed(0)
        self.fail_reason_pen.color(FAIL_COLOR)
        self.fail_reason_pen.penup()
        self.fail_reason_pen.hideturtle()
        self.fail_reason_pen.goto(0, SCREEN_HEIGHT//2 - 50)
        
        # 创建按钮
        self.create_buttons()
        
        # 绑定键盘事件（多次调用 listen 确保有效）
        self.screen.listen()
        self.screen.onkeypress(self.go_up, "Up")
        self.screen.onkeypress(self.go_down, "Down")
        self.screen.onkeypress(self.go_left, "Left")
        self.screen.onkeypress(self.go_right, "Right")
        self.screen.onkeypress(self.start_game, "Return")  # Enter键开始
        self.screen.onkeypress(self.start_game, "space")   # 空格键也可开始
        # P键暂停（支持大小写和数字键1作为备用）
        self.screen.onkeypress(self.toggle_pause, "p")
        self.screen.onkeypress(self.toggle_pause, "P")
        self.screen.onkeypress(self.toggle_pause, "1")  # 数字键1作为备用
        # R键重新开始（支持大小写和数字键2作为备用）
        self.screen.onkeypress(self.reset_game, "r")
        self.screen.onkeypress(self.reset_game, "R")
        self.screen.onkeypress(self.reset_game, "2")  # 数字键2作为备用
        self.screen.listen()  # 再次调用确保事件绑定生效
        
        # 显示按键说明（左下角）
        self.draw_key_hints()
        
        # 显示开始提示
        self.show_start_message()
    
    def draw_border(self):
        """绘制游戏边界"""
        border = turtle.Turtle()
        border.speed(0)
        border.color(BORDER_COLOR)
        border.pensize(3)
        border.penup()
        border.goto(-SCREEN_WIDTH//2 - 2, -SCREEN_HEIGHT//2 - 2)
        border.pendown()
        
        for _ in range(4):
            border.forward(SCREEN_WIDTH + 4)
            border.left(90)
        
        border.hideturtle()
    
    def create_buttons(self):
        """创建鼠标点击按钮（使用tkinter原生按钮）"""
        # 获取turtle的底层canvas和root
        canvas = self.screen.getcanvas()
        root = canvas.winfo_toplevel()
        
        button_x = SCREEN_WIDTH // 2 + 60  # 按钮位置更靠右
        
        # 开始游戏按钮
        self.start_button = tk.Button(root, text="开始游戏", bg="#2ECC71", fg="white", 
                                      font=("微软雅黑", 12, "bold"), width=10,
                                      command=lambda: self.handle_button_click(self.start_game))
        canvas.create_window(button_x, 80, window=self.start_button)
        
        # 暂停/继续按钮
        self.pause_button = tk.Button(root, text="暂停", bg="#F39C12", fg="white", 
                                      font=("微软雅黑", 12, "bold"), width=10,
                                      command=lambda: self.handle_button_click(self.toggle_pause))
        canvas.create_window(button_x, 20, window=self.pause_button)
        
        # 重新开始按钮
        self.reset_button = tk.Button(root, text="重新开始", bg="#E74C3C", fg="white", 
                                      font=("微软雅黑", 12, "bold"), width=10,
                                      command=lambda: self.handle_button_click(self.reset_game))
        canvas.create_window(button_x, -40, window=self.reset_button)
        
        # 按钮点击冷却时间（防蠢机制）
        self.last_button_click = 0
        self.button_cooldown = 300  # 300毫秒冷却
    
    def create_button(self, x, y, text, color, callback):
        """旧的按钮创建方法（已弃用）"""
        pass
    
    def handle_button_click(self, callback):
        """处理按钮点击，添加冷却机制"""
        current_time = time.time() * 1000  # 毫秒
        if current_time - self.last_button_click >= self.button_cooldown:
            self.last_button_click = current_time
            callback()
    
    def draw_key_hints(self):
        """在左下角绘制按键说明"""
        hint = turtle.Turtle()
        hint.speed(0)
        hint.color("#BDC3C7")  # 浅灰色
        hint.penup()
        hint.hideturtle()
        hint.goto(-SCREEN_WIDTH//2 + 10, -SCREEN_HEIGHT//2 - 35)
        
        hint_text = "按键: ↑↓←→移动 | P/1暂停 | R/2重开 | Enter/空格开始"
        hint.write(hint_text, align="left", font=("微软雅黑", 10, "normal"))
    
    def draw_grid(self):
        """绘制游戏网格"""
        grid = turtle.Turtle()
        grid.speed(0)
        grid.color(GRID_COLOR)
        grid.pensize(1)
        grid.penup()
        
        # 绘制垂直线
        for x in range(-SCREEN_WIDTH//2, SCREEN_WIDTH//2 + 1, GRID_SIZE):
            grid.goto(x, -SCREEN_HEIGHT//2)
            grid.pendown()
            grid.goto(x, SCREEN_HEIGHT//2)
            grid.penup()
        
        # 绘制水平线
        for y in range(-SCREEN_HEIGHT//2, SCREEN_HEIGHT//2 + 1, GRID_SIZE):
            grid.goto(-SCREEN_WIDTH//2, y)
            grid.pendown()
            grid.goto(SCREEN_WIDTH//2, y)
            grid.penup()
        
        grid.hideturtle()
    
    def start_game(self):
        """开始游戏（无倒计时，立即开始）"""
        if self.waiting_for_start:
            self.waiting_for_start = False
    
    def go_up(self):
        """处理向上移动"""
        self.snake.update_direction(UP)
    
    def go_down(self):
        """处理向下移动"""
        self.snake.update_direction(DOWN)
    
    def go_left(self):
        """处理向左移动"""
        self.snake.update_direction(LEFT)
    
    def go_right(self):
        """处理向右移动"""
        self.snake.update_direction(RIGHT)
    
    def toggle_pause(self):
        """切换暂停状态（P键）"""
        if not self.game_over and not self.waiting_for_start:
            self.paused = not self.paused
    
    def update_score_display(self):
        """更新分数显示"""
        self.score_pen.clear()
        self.score_pen.write(f"🎯 分数: {self.score}", align="center", font=("微软雅黑", 22, "bold"))
    
    def show_start_message(self):
        """显示开始提示"""
        self.status_pen.clear()
        self.status_pen.color(STATUS_COLOR)
        self.status_pen.write("按 Enter 或 空格键 开始游戏", align="center", font=("微软雅黑", 18, "normal"))
    
    def show_fail_reason(self, reason):
        """显示失败原因"""
        self.fail_reason_pen.clear()
        self.fail_reason_pen.write(reason, align="center", font=("微软雅黑", 16, "bold"))
    
    def show_status(self, message):
        """显示游戏状态信息"""
        self.status_pen.clear()
        self.status_pen.color(STATUS_COLOR)
        self.status_pen.write(message, align="center", font=("微软雅黑", 16, "normal"))
    
    def check_collisions(self):
        """检查各种碰撞情况"""
        head = self.snake.body[0]
        
        # 检查蛇头与食物碰撞
        if head == self.food.position:
            self.score += 10
            self.snake.grow()
            self.update_score_display()
            
            # 检查是否达到加速条件（每个颜色分段加0.1倍，上限到300分彩虹模式）
            color_thresholds = [20, 50, 90, 140, 200, 300]  # 颜色分段阈值
            if self.score <= 300:
                # 计算当前处于哪个颜色分段
                current_segment = 0
                for threshold in color_thresholds:
                    if self.score >= threshold:
                        current_segment += 1
                if current_segment > self.last_speed_increase:
                    self.speed_multiplier = min(self.speed_multiplier + 0.1, self.max_speed_multiplier)
                    self.last_speed_increase = current_segment
            
            # 检查蛇变色条件（隐藏玩法）
            self.update_snake_color()
            
            # 生成新食物，确保不在蛇身上
            while self.food.position in self.snake.body:
                self.food.generate_new()
        
        # 检查蛇头与自身碰撞（头尾相触）
        if self.snake.check_self_collision():
            self.game_over = True
            self.show_fail_reason("头尾相触 - 游戏失败！")
    
    def update_snake_color(self):
        """根据分数更新蛇的颜色（隐藏玩法）"""
        # 颜色定义：白(初始) -> 绿(20) -> 蓝(50) -> 紫(90) -> 金(140) -> 红(200) -> 彩虹(300)
        colors = {
            0: ("#FFFFFF", "#CCCCCC"),      # 白色
            20: ("#2ECC71", "#58D68D"),     # 绿色
            50: ("#3498DB", "#5DADE2"),     # 蓝色
            90: ("#9B59B6", "#BB8FCE"),     # 紫色
            140: ("#F1C40F", "#F4D03F"),    # 金色
            200: ("#E74C3C", "#EC7063")     # 红色
        }
        
        # 检查是否进入彩虹模式（300分及以上）
        if self.score >= 300:
            self.rainbow_mode = True
        else:
            self.rainbow_mode = False
            # 找到当前分数对应的颜色
            current_color = colors[0]  # 默认白色
            for threshold in sorted(colors.keys()):
                if self.score >= threshold:
                    current_color = colors[threshold]
            
            self.snake.update_color(current_color[0], current_color[1])
    
    def update_rainbow_color(self):
        """更新彩虹颜色"""
        if self.rainbow_mode and not self.game_over:
            # 获取当前彩虹颜色
            head_color = self.rainbow_colors[self.rainbow_index]
            # 身体颜色稍暗
            body_color = self.rainbow_colors[(self.rainbow_index + 1) % len(self.rainbow_colors)]
            self.snake.update_color(head_color, body_color)
            
            # 周期性变化颜色
            if not self.paused:
                self.rainbow_index = (self.rainbow_index + 1) % len(self.rainbow_colors)
    
    def update(self):
        """更新游戏状态"""
        if not self.game_over and not self.paused and not self.waiting_for_start:
            # 移动前检查是否会撞墙
            if self.snake.check_wall_collision():
                self.game_over = True
                self.show_fail_reason("头部碰墙 - 游戏失败！")
            else:
                self.snake.move()
                self.check_collisions()
        
        # 更新彩虹颜色
        self.update_rainbow_color()
    
    def draw(self):
        """绘制游戏画面"""
        # 清空状态显示
        if not self.waiting_for_start:
            self.status_pen.clear()
        
        # 绘制蛇和食物
        self.snake.draw()
        self.food.draw()
        
        # 绘制状态提示
        if self.paused and not self.game_over:
            self.show_status("⏸️ 游戏暂停 - 按 P 键继续")
        if self.game_over:
            self.show_status("💀 游戏结束！按 R 键重新开始")
        
        # 更新显示
        self.screen.update()
    
    def reset_game(self):
        """重置游戏状态"""
        # 清除失败原因显示
        self.fail_reason_pen.clear()
        
        # 清除旧对象
        self.snake.clear()
        self.food.clear()
        
        # 创建新对象
        self.snake = Snake(self.screen)
        self.food = Food(self.screen)
        
        # 重置状态
        self.score = 0
        self.game_over = False
        self.paused = False
        self.waiting_for_start = True  # 重新等待用户开始
        
        # 重置速度
        self.speed_multiplier = 1.0
        self.last_speed_increase = 0
        
        # 重置彩虹模式
        self.rainbow_index = 0
        self.rainbow_mode = False
        
        self.update_score_display()
        self.show_start_message()
    
    def run(self):
        """游戏主循环"""
        while True:
            # 关键：每次循环都需要调用 listen() 确保窗口接收键盘事件
            self.screen.listen()
            self.update()
            self.draw()
            # 减小基础延迟，让转向更灵敏
            time.sleep(self.base_speed / self.speed_multiplier)


if __name__ == "__main__":
    game = Game()
    game.run()
