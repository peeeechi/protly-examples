#%% 
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os
import open3d as o3d
from open3d.visualization.draw_plotly import *

# os.path.dirname(os.path.abspath(__file__)) を使ってスクリプトのディレクトリパスを取得
script_dir = os.path.dirname(os.path.abspath(__file__))
pcd_file_path = os.path.join(script_dir, 'sample.pcd')

try:
    # print("PCDファイルを読み込んでいます...")
    # Open3Dを使ってPCDファイルを読み込む
    pcd = o3d.io.read_point_cloud(pcd_file_path)
    pcd = pcd.voxel_down_sample(voxel_size=1.5)

    # グラフタイトルをカスタマイズ
    fig_title = 'Point Cloud Data Visualization (Open3D + Plotly)'

    # o3d.visualization.draw_plotlyを使ってPlotlyのFigureを生成
    # ここでOpen3Dから直接PlotlyのFigureに変換されます
    fig = get_plotly_fig([pcd], width=None, height=None)

    print(fig.data)

    # 出力ディレクトリ（プロジェクトルートの 'output'）へのパスを生成
    output_dir = os.path.join(os.path.dirname(script_dir), 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # グラフをHTMLファイルとして保存
    fig.write_html(os.path.join(output_dir, 'pcd_graph.html'))
    print('Successfully generated pcd_graph.html')

except Exception as e:
    print(f"エラーが発生しました: {e}")