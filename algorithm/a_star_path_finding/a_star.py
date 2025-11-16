import heapq

# 定义启发式函数（曼哈顿距离）
def heuristic(a, b):
    # a 和 b 都是 (row, col) 格式的坐标
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# 定义网格（0 代表可通过，1 代表障碍物）
# 4x5 的网格
GRID = [
    [0, 0, 0, 0, 1],
    [0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0]
]

# 网格尺寸
GRID_HEIGHT = len(GRID)
GRID_WIDTH = len(GRID[0])

# 起点和终点
START = (0, 0) # 左上角
END = (3, 4)   # 右下角

# 实现 A* 搜索函数A* 算法的核心在于维护三个值：
# g 值：从起点到当前节点的实际代价。
# h 值：从当前节点到终点的预估代价（启发式）。
# f 值：总代价，即 $f(n) = g(n) + h(n)$。

def a_star_search(grid, start, end):
    # 优先队列：(f_score, g_score, current_node)
    # 优先队列中存储的 g_score 是为了解决 tie-breaking（当 f_score 相同时）
    # 但在这个简单例子中，我们只用 f_score 来排序
    priority_queue = [(0, start)] # (f_score, node)

    # g_score 记录从起点到当前节点的实际代价
    # 使用字典来存储，键为节点坐标，值为 g_score
    g_score = {start: 0}

    # came_from 记录路径，键为当前节点，值为其前一个节点
    came_from = {}

    while priority_queue:
        # 取出 f_score 最小的节点
        current_f, current_node = heapq.heappop(priority_queue)
        
        # 检查是否到达终点
        if current_node == end:
            return reconstruct_path(came_from, end)

        # 检查所有邻居 (上, 下, 左, 右)
        r, c = current_node
        # 邻居的相对坐标
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)] 

        for dr, dc in neighbors:
            neighbor_node = (r + dr, c + dc)
            
            # 检查邻居是否在网格内
            if not (0 <= neighbor_node[0] < GRID_HEIGHT and 0 <= neighbor_node[1] < GRID_WIDTH):
                continue

            # 检查邻居是否是障碍物 (1)
            if grid[neighbor_node[0]][neighbor_node[1]] == 1:
                continue

            # 从当前节点移动到邻居节点的代价 (这里简化为 1)
            cost = 1
            
            # 尝试计算从起点经过当前节点到达邻居节点的 g_score
            tentative_g_score = g_score.get(current_node, float('inf')) + cost
            
            # 如果新路径的 g_score 更优 (更小)
            if tentative_g_score < g_score.get(neighbor_node, float('inf')):
                # 更新路径信息
                came_from[neighbor_node] = current_node
                g_score[neighbor_node] = tentative_g_score
                
                # 计算 f_score = g_score + h_score
                h_score = heuristic(neighbor_node, end)
                f_score = tentative_g_score + h_score
                
                # 将邻居节点加入优先队列
                heapq.heappush(priority_queue, (f_score, neighbor_node))

    # 如果队列为空，但未找到路径
    return None

def reconstruct_path(came_from, current):
    """从 came_from 字典中重建路径"""
    p = []
    while current in came_from:
        p.append(current)
        current = came_from[current]
    p.append(current) # 添加起点
    return p[::-1] # 反转，使其从起点到终点

# --- 运行示例 ---
path = a_star_search(GRID, START, END)

if path:
    print(f"✅ 找到路径！总步数: {len(path) - 1}")
    print("路径坐标:")
    print(path)
    
    # 打印可视化路径
    path_grid = [row[:] for row in GRID] # 复制网格
    for r, c in path:
        if (r, c) != START and (r, c) != END:
            path_grid[r][c] = '*' # 路径标记
            
    print("\n🗺️ 路径可视化 (S:起点, E:终点, 1:障碍物, *:路径):")
    for r in range(GRID_HEIGHT):
        row_str = ""
        for c in range(GRID_WIDTH):
            if (r, c) == START:
                row_str += " S "
            elif (r, c) == END:
                row_str += " E "
            elif path_grid[r][c] == 1:
                row_str += " 1 "
            elif path_grid[r][c] == '*':
                row_str += " * "
            else:
                row_str += " . " # 可通过的空地
        print(row_str)
else:
    print("❌ 未找到路径。")

# 核心概念总结
# 优先队列 (heapq)：存储待探索的节点，始终取出 f 值最小 的节点。
# g 值 (g_score)：从起点到当前节点的实际移动代价。
# h 值 (heuristic)：从当前节点到终点的预估移动代价。
# f 值：总预估代价 ($g + h$)，用于优先队列排序。
# came_from：用于记录父节点，以便找到路径后可以回溯重建。