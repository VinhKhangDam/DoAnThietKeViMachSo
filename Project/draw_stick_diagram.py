import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Node trong cây NMOS hậu tố
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

# Dựng cây từ biểu thức hậu tố
def build_tree(postfix_tokens):
    stack = []
    for token in postfix_tokens:
        if token in ['+', '*']:
            right = stack.pop()
            left = stack.pop()
            node = Node(token)
            node.left = left
            node.right = right
            stack.append(node)
        else:
            stack.append(Node(token))
    return stack[0] if stack else None

# Đọc file CMOS
def read_cmos_data(filename="cmos_data.txt"):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()

    section = None
    pmos_blocks = []
    nmos_expr = []

    for line in lines:
        line = line.strip()
        if line == "PMOS":
            section = "PMOS"
        elif line == "NMOS":
            section = "NMOS"
        elif line:
            if section == "PMOS":
                parts = line.split()
                if parts[0] == "parallel":
                    pmos_blocks.append(parts[1:])
            elif section == "NMOS":
                parts = line.split()
                if parts[0] == "parallel":
                    nmos_expr = parts[1:]
    return pmos_blocks, nmos_expr

# Vẽ 1 transistor
def draw_transistor(ax, x, y, label, color='black'):
    # Nguồn - Drain
    ax.plot([x-0.5, x+0.5], [y, y], color=color, linewidth=3)
    # Gate
    ax.plot([x, x], [y-1, y+1], color='red', linewidth=2)
    ax.text(x, y+0.3, label, ha='center', color='red', fontsize=9)

# Vẽ các nhánh PMOS
def draw_pmos(ax, pmos_blocks, start_x=2, base_y=10):
    spacing_y = 2
    spacing_x = 2
    transistor_positions = []

    for i, block in enumerate(pmos_blocks):
        y = base_y - i * spacing_y
        x = start_x
        for var in block:
            draw_transistor(ax, x, y, var, color='orange')
            x += spacing_x
        # Nối lên VDD và xuống output sau
        ax.plot([start_x-0.5, start_x-0.5], [y, y+1], color='blue')
        ax.plot([x-1+0.5, x-1+0.5], [y, y-1], color='blue')
        transistor_positions.append(((start_x-0.5, y+1), (x-1+0.5, y-1)))

    return transistor_positions

# Duyệt cây NMOS và vẽ
nm_y_base = 2
nm_spacing_x = 2
nm_spacing_y = 2
nmos_x_tracker = 0

def draw_nmos_tree(ax, node, x, y):
    global nmos_x_tracker

    if not node:
        return []

    if node.value in ['+', '*']:
        if node.value == '+':  # parallel
            left = draw_nmos_tree(ax, node.left, x, y)
            right = draw_nmos_tree(ax, node.right, x, y - nm_spacing_y)
            return left + right
        elif node.value == '*':  # series
            left = draw_nmos_tree(ax, node.left, x, y)
            x = max(p[1][0] for p in left) + nm_spacing_x
            right = draw_nmos_tree(ax, node.right, x, y)
            return left + right
    else:
        draw_transistor(ax, x, y, node.value, color='green')
        # Vẽ nối xuống GND và lên output sau
        ax.plot([x-0.5, x-0.5], [y, y+1], color='blue')
        ax.plot([x+0.5, x+0.5], [y, y-1], color='blue')
        return [((x-0.5, y+1), (x+0.5, y-1))]

# Vẽ stick diagram tổng thể
def draw_stick_diagram():
    fig, ax = plt.subplots(figsize=(14, 10))

    pmos_blocks, nmos_postfix = read_cmos_data()
    nmos_tree = build_tree(nmos_postfix)

    # Vẽ VDD / GND
    ax.plot([0, 30], [11, 11], color='blue', linewidth=2)
    ax.text(30.5, 11, 'VDD')
    ax.plot([0, 30], [1, 1], color='blue', linewidth=2)
    ax.text(30.5, 1, 'GND')

    pmos_conns = draw_pmos(ax, pmos_blocks)
    nmos_conns = draw_nmos_tree(ax, nmos_tree, 2, nm_y_base)

    # Vẽ output Y
    if pmos_conns and nmos_conns:
        px = (pmos_conns[-1][1][0] + pmos_conns[0][0][0]) / 2
        nx = (nmos_conns[-1][1][0] + nmos_conns[0][0][0]) / 2
        cx = max(px, nx) + 1
        cy = 6
        ax.plot([px, cx], [pmos_conns[0][0][1], cy], color='blue')
        ax.plot([nx, cx], [nmos_conns[0][1][1], cy], color='blue')
        ax.text(cx + 0.5, cy, "Y", fontsize=12, color='red')

    ax.set_xlim(0, 35)
    ax.set_ylim(0, 13)
    ax.axis('off')
    plt.title("Stick Diagram - Auto Layout from CMOS Data")
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    draw_stick_diagram()