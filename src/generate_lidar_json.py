import json # JSONデータの読み書きに使うライブラリ
import numpy as np # 数値計算、特に配列操作に使うライブラリ
import os # ファイルやディレクトリの操作に使うライブラリ

# 関数: 現実的なLiDARデータを生成する
# num_frames: 生成するフレーム数（今回は300フレーム）
# interval_ms: 1フレームごとの時間間隔（今回は100ミリ秒）
def generate_realistic_lidar_data(num_frames=300, interval_ms=100):
    msgs = [] # 生成したメッセージを格納するリスト
    base_timestamp_sec = 1672531200 # 基準となるタイムスタンプの秒
    base_timestamp_nanosec = 0 # 基準となるタイムスタンプのナノ秒
    
    # 現実的なデータの範囲を定義
    road_points_x_range = [0, 50] # 車両からの前方距離（メートル）
    road_points_y_range = [-5, 5]  # 左右の幅（車線幅を想定）
    road_points_z_range = [-1.5, -1.0] # 路面の高さ（地面を想定）
    
    # 各フレームのデータを生成
    for i in range(num_frames):
        # タイムスタンプを更新
        current_nanosec = base_timestamp_nanosec + i * interval_ms * 1000000
        current_sec = base_timestamp_sec + current_nanosec // 1000000000
        current_nanosec %= 1000000000
        
        # 地面を表す点を生成
        num_ground_points = 100
        ground_x = np.random.uniform(road_points_x_range[0], road_points_x_range[1], num_ground_points)
        ground_y = np.random.uniform(road_points_y_range[0], road_points_y_range[1], num_ground_points)
        ground_z = np.random.uniform(road_points_z_range[0], road_points_z_range[1], num_ground_points)
        
        # 縁石（道路の端）の点をシミュレーション
        num_curb_points = 10
        curb_x = np.random.uniform(10, 40, num_curb_points)
        curb_y_left = np.random.uniform(road_points_y_range[0] - 1, road_points_y_range[0], num_curb_points)
        curb_y_right = np.random.uniform(road_points_y_range[1], road_points_y_range[1] + 1, num_curb_points)
        curb_z = np.random.uniform(-0.8, -0.5, num_curb_points * 2)
        
        points = []
        for j in range(num_ground_points):
            points.append([float(ground_x[j]), float(ground_y[j]), float(ground_z[j])])
        for j in range(num_curb_points):
            points.append([float(curb_x[j]), float(curb_y_left[j]), float(curb_z[j])])
            points.append([float(curb_x[j]), float(curb_y_right[j]), float(curb_z[j])])
        
        # 1つのフレームデータを作成
        msgs.append({
            "header": {
                "stamp": {
                    "sec": current_sec,
                    "nanosec": current_nanosec
                },
                "frame_id": "lidar_frame"
            },
            "data": points
        })
        
    return msgs

# 実行部分
output_dir = 'src'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

lidar_data = generate_realistic_lidar_data()
# 生成したデータをJSONファイルとして保存
with open(os.path.join(output_dir, 'lidar_data.json'), 'w') as f:
    json.dump(lidar_data, f, indent=2)

print('Successfully generated lidar_data.json with 300 frames.')