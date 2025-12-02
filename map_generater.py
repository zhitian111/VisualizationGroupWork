"""
校园建筑有权无向图生成器
使用 geopy 计算建筑物之间的精确距离，构建图结构并导出CSV文件
"""

from geopy.distance import geodesic
import csv


# 定义所有建筑物节点
# 每个节点包含: name(名称), position(经度, 纬度), picture(预留图片字段)
buildings = [
    # 振声苑所有楼栋
    {"name": "振声苑e", "position": (120.6870, 36.3627), "picture": ""},
    {"name": "振声苑s", "position": (120.6864, 36.3622), "picture": ""},
    {"name": "振声苑n", "position": (120.6864, 36.3632), "picture": ""},
    {"name": "振声苑w", "position": (120.6860, 36.3627), "picture": ""},
    
    # 华岗苑所有楼栋
    {"name": "华岗苑e", "position": (120.6870, 36.3645), "picture": ""},
    {"name": "华岗苑w", "position": (120.6859, 36.3645), "picture": ""},
    {"name": "华岗苑n", "position": (120.6863, 36.3650), "picture": ""},
    {"name": "华岗苑s", "position": (120.6863, 36.3641), "picture": ""},
    
    # 第周苑所有楼栋
    {"name": "第周苑a", "position": (120.6883, 36.3627), "picture": ""},
    {"name": "第周苑b", "position": (120.6894, 36.3631), "picture": ""},
    {"name": "第周苑c", "position": (120.6911, 36.3632), "picture": ""},
    {"name": "第周苑d", "position": (120.6926, 36.3625), "picture": ""},
    {"name": "第周苑e", "position": (120.6910, 36.3621), "picture": ""},
    {"name": "第周苑f", "position": (120.6895, 36.3622), "picture": ""},
    
    # 淦昌苑所有楼栋
    {"name": "淦昌苑a", "position": (120.6882, 36.3645), "picture": ""},
    {"name": "淦昌苑b", "position": (120.6894, 36.3649), "picture": ""},
    {"name": "淦昌苑c", "position": (120.6909, 36.3651), "picture": ""},
    {"name": "淦昌苑d", "position": (120.6926, 36.3644), "picture": ""},
    {"name": "淦昌苑e", "position": (120.6912, 36.3640), "picture": ""},
    {"name": "淦昌苑f", "position": (120.6896, 36.3641), "picture": ""},
    
    # 其他建筑
    {"name": "会文南", "position": (120.6917, 36.3655), "picture": ""},
    {"name": "会文北", "position": (120.6917, 36.3669), "picture": ""},
    {"name": "s2宿舍", "position": (120.6914, 36.3593), "picture": ""},
    {"name": "曦园", "position": (120.6924, 36.3597), "picture": ""},
    {"name": "晨园", "position": (120.6868, 36.3738), "picture": ""},
    {"name": "体育馆", "position": (120.6855, 36.3590), "picture": ""},
    {"name": "博物馆", "position": (120.6875, 36.3610), "picture": ""},
    {"name": "图书馆", "position": (120.6890, 36.3663), "picture": ""},
    {"name": "红操场", "position": (120.6910, 36.3603), "picture": ""},
    {"name": "蓝操场", "position": (120.6857, 36.3614), "picture": ""},
    {"name": "双创", "position": (120.6912, 36.3558), "picture": ""},
    {"name": "专家公寓2号楼", "position": (120.6927, 36.3581), "picture": ""},
]


def calculate_distance(pos1, pos2):
    """
    使用 geopy 计算两点之间的距离（米）
    
    参数:
        pos1: 第一个点的坐标 (经度, 纬度)
        pos2: 第二个点的坐标 (经度, 纬度)
    
    返回:
        两点之间的距离（米）
    """
    # geopy 需要 (纬度, 经度) 格式
    point1 = (pos1[1], pos1[0])
    point2 = (pos2[1], pos2[0])
    return geodesic(point1, point2).meters


def build_graph(buildings):
    """
    构建有权无向图
    
    参数:
        buildings: 建筑物列表
    
    返回:
        nodes: 节点列表
        edges: 边列表，每条边包含 (node1, node2, weight)
        distance_matrix: 距离矩阵（二维字典）
    """
    nodes = buildings
    edges = []
    distance_matrix = {}
    
    n = len(buildings)
    
    # 初始化距离矩阵
    for building in buildings:
        distance_matrix[building["name"]] = {}
    
    # 计算所有建筑物之间的距离（无向图，只需计算一半）
    for i in range(n):
        for j in range(i, n):
            name1 = buildings[i]["name"]
            name2 = buildings[j]["name"]
            pos1 = buildings[i]["position"]
            pos2 = buildings[j]["position"]
            
            if i == j:
                distance = 0.0
            else:
                distance = calculate_distance(pos1, pos2)
                # 添加边（无向图）
                edges.append((name1, name2, distance))
            
            # 填充距离矩阵（对称）
            distance_matrix[name1][name2] = distance
            distance_matrix[name2][name1] = distance
    
    return nodes, edges, distance_matrix


def export_buildings_csv(buildings, filename="buildings.csv"):
    """
    导出建筑物坐标到CSV文件
    
    参数:
        buildings: 建筑物列表
        filename: 输出文件名
    """
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        # 写入表头
        writer.writerow(["建筑物名称", "经度", "纬度", "图片"])
        
        # 写入数据
        for building in buildings:
            writer.writerow([
                building["name"],
                building["position"][0],
                building["position"][1],
                building["picture"]
            ])
    
    print(f"建筑物坐标已导出到: {filename}")


def export_distances_csv(buildings, distance_matrix, filename="distances.csv"):
    """
    导出建筑物之间距离矩阵到CSV文件
    
    参数:
        buildings: 建筑物列表
        distance_matrix: 距离矩阵
        filename: 输出文件名
    """
    building_names = [b["name"] for b in buildings]
    
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        
        # 写入表头（第一列为空，后面是所有建筑物名称）
        header = [""] + building_names
        writer.writerow(header)
        
        # 写入每行数据
        for name1 in building_names:
            row = [name1]
            for name2 in building_names:
                # 距离保留2位小数
                distance = round(distance_matrix[name1][name2], 2)
                row.append(distance)
            writer.writerow(row)
    
    print(f"距离矩阵已导出到: {filename}")


def print_graph_info(nodes, edges):
    """
    打印图的基本信息
    """
    print("=" * 50)
    print("校园建筑有权无向图信息")
    print("=" * 50)
    print(f"节点数量: {len(nodes)}")
    print(f"边数量: {len(edges)}")
    print()
    
    print("节点列表:")
    for i, node in enumerate(nodes, 1):
        print(f"  {i}. {node['name']} - 坐标: {node['position']}")
    print()
    
    # 打印一些示例边（距离最近的10条边）
    sorted_edges = sorted(edges, key=lambda x: x[2])
    print("距离最近的10条边:")
    for i, (n1, n2, dist) in enumerate(sorted_edges[:10], 1):
        print(f"  {i}. {n1} <-> {n2}: {dist:.2f} 米")
    print()
    
    # 打印距离最远的10条边
    print("距离最远的10条边:")
    for i, (n1, n2, dist) in enumerate(sorted_edges[-10:], 1):
        print(f"  {i}. {n1} <-> {n2}: {dist:.2f} 米")


def main():
    """
    主函数
    """
    print("开始构建校园建筑有权无向图...")
    print()
    
    # 构建图
    nodes, edges, distance_matrix = build_graph(buildings)
    
    # 打印图信息
    print_graph_info(nodes, edges)
    
    # 导出CSV文件
    export_buildings_csv(buildings, "buildings.csv")
    export_distances_csv(buildings, distance_matrix, "distances.csv")
    
    print()
    print("=" * 50)
    print("图构建完成！")
    print("=" * 50)
    
    return nodes, edges, distance_matrix


if __name__ == "__main__":
    nodes, edges, distance_matrix = main()
