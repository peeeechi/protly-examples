import plotly.graph_objects as go
import json
import numpy as np
import os
from datetime import datetime

# JSONファイルからデータを読み込み
with open('src/lidar_data.json', 'r') as f:
    ros_msgs = json.load(f)

# タイムスタンプをhh:mm:ss.sss形式に変換
timestamps = []
for msg in ros_msgs:
    ts_sec = msg['header']['stamp']['sec']
    ts_nanosec = msg['header']['stamp']['nanosec']
    timestamp_float = ts_sec + ts_nanosec / 1e9
    dt_object = datetime.fromtimestamp(timestamp_float)
    formatted_ts = dt_object.strftime('%H:%M:%S.%f')[:-3]
    timestamps.append(formatted_ts)

# 全ての点群データから、x, y, zの最大値と最小値を計算
all_points_flat = [p for msg in ros_msgs for p in msg['data']]
all_points = np.array(all_points_flat)

max_val = np.max(all_points)
min_val = np.min(all_points)
buffer = (max_val - min_val) * 0.1
axis_range = [min_val - buffer, max_val + buffer]

# 各フレームのグラフデータを生成
frames = [
    go.Frame(data=[
        go.Scatter3d(
            x=[p[0] for p in msg['data']],
            y=[p[1] for p in msg['data']],
            z=[p[2] for p in msg['data']],
            mode='markers',
            marker=dict(size=5, opacity=0.8)
        )
    ],
    name=timestamps[i])
    for i, msg in enumerate(ros_msgs)
]

# 初期表示用のデータ（最初のフレーム）を作成
initial_data = [
    go.Scatter3d(
        x=[p[0] for p in ros_msgs[0]['data']],
        y=[p[1] for p in ros_msgs[0]['data']],
        z=[p[2] for p in ros_msgs[0]['data']],
        mode='markers',
        marker=dict(size=5, opacity=0.8)
    )
]

# グラフ全体のレイアウトとアニメーションの設定
fig = go.Figure(
    data=initial_data,
    frames=frames,
    layout=go.Layout(
        # 再生・停止ボタンをスライダーの下に配置
        updatemenus=[dict(
            type="buttons",
            direction="left",
            buttons=[
                dict(
                    label="▶",
                    method="animate",
                    args=[None, {"frame": {"duration": 100, "redraw": True}, "fromcurrent": True}]
                ),
                dict(
                    label="⏸",
                    method="animate",
                    args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}]
                )
            ],
            pad={"r": 10, "t": 87},
            showactive=False,
            x=0.08,
            xanchor="left",
            y=-0.15, # このy座標でスライダーの下に配置
            yanchor="top"
        )],
        # スライダーの設定
        sliders=[dict(
            steps=[
                dict(
                    args=[[t], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}],
                    label=t,
                    method="animate"
                )
                for t in timestamps
            ],
            transition=dict(duration=0),
            x=0.08,
            y=-0.05,
            len=0.9
        )],
        title='LiDAR Data with ROS Timestamp Slider',
        scene=dict(
            xaxis=dict(range=axis_range, autorange=False),
            yaxis=dict(range=axis_range, autorange=False),
            zaxis=dict(range=axis_range, autorange=False),
            aspectmode='cube'
        )
    )
)

# 生成したグラフをHTMLファイルとして保存
output_dir = 'output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

fig.write_html(os.path.join(output_dir, 'slider_graph.html'))
print('Successfully generated slider_graph.html')