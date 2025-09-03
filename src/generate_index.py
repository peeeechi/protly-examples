import os
from jinja2 import Environment, FileSystemLoader

def generate_index_html(output_dir, template_dir):
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('index_template.html')

    # outputディレクトリ内のHTMLファイルをリストアップ
    # index.html自体は除外する
    html_files = [f for f in os.listdir(output_dir) if f.endswith('.html') and f != 'index.html']
    html_files.sort()

    rendered_html = template.render(files=html_files)

    index_path = os.path.join(output_dir, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(rendered_html)
    print(f"Successfully generated index.html at {index_path}")

# ファイルパスの設定
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(os.path.dirname(script_dir), 'output')
template_dir = script_dir

# 実行
generate_index_html(output_dir, template_dir)