import matplotlib.pyplot as plt
import json

# 1. Đọc dữ liệu từ file JSON
with open("output_data.json") as f:
    data = json.load(f)

# 2. Tạo hình ảnh cực kỳ đơn giản
plt.figure(figsize=(10, 5))

# Vẽ các điểm node cơ bản
for i, node in enumerate(data.get("euler_pmos", [])):
    plt.plot(i, 1, 'bo', markersize=15)  # PMOS màu xanh
    plt.text(i, 1.1, node, ha='center')

for i, node in enumerate(data.get("euler_nmos", [])):
    plt.plot(i, 0, 'ro', markersize=15)  # NMOS màu đỏ
    plt.text(i, -0.1, node, ha='center')

# Vẽ đường kết nối đơn giản
for u, v in data["edges_pmos"]:
    if u in data.get("euler_pmos", []) and v in data.get("euler_pmos", []):
        u_idx = data["euler_pmos"].index(u)
        v_idx = data["euler_pmos"].index(v)
        plt.plot([u_idx, v_idx], [1, 1], 'b-')

for u, v in data["edges_nmos"]:
    if u in data.get("euler_nmos", []) and v in data.get("euler_nmos", []):
        u_idx = data["euler_nmos"].index(u)
        v_idx = data["euler_nmos"].index(v)
        plt.plot([u_idx, v_idx], [0, 0], 'r-')

plt.title("Simple Stick Diagram")
plt.axis('off')

# 3. Lưu file ảnh và thông báo rõ ràng
output_file = "simple_diagram.png"
plt.savefig(output_file)
print(f"✅ ĐÃ LƯU THÀNH CÔNG file ảnh tại: {output_file}")
print(f"📌 Hãy mở file bằng cách:")
print(f"1. Trên Ubuntu: xdg-open {output_file}")
print(f"2. Hoặc copy file về máy tính của bạn")