import os
import subprocess
from pyntcloud import PyntCloud
import numpy as np
from glob import glob

def process(path, vox=12, is_mesh=False):
    pc_mesh = PyntCloud.from_file(path)
    mesh = pc_mesh.mesh
    coords = ['x', 'y', 'z']
    pc_mesh.points[coords] = pc_mesh.points[coords].astype('float64', copy=False)
    pc_mesh.mesh = mesh
    if is_mesh:
        pc = pc_mesh.get_sample("mesh_random", n=500000, as_PyntCloud=True)
    else:
        pc = pc_mesh
    points = pc.points[coords].values
    print(np.min(points, axis=0))
    points = points - np.min(points, axis=0, keepdims=True)
    print(np.min(points, axis=0))
    print(np.max(points, axis=0))
    print(np.max(points))
    points = points / np.max(points)
    points = points * (2 ** vox - 1)
    points = np.round(points)
    pc.points[coords] = points
    colors = ['red', 'green', 'blue'] # ['green', 'blue', 'red'] it is order-sensitive, here needs the original order.
    other_scalars = list(set(pc.points.columns) - set(coords) - set(colors))
    # print(pc.points.shape)
    pc.points = pc.points.drop(columns=other_scalars)
    # print(pc.points.shape)
    pc.points[colors] = pc.points.groupby(by=coords).transform('mean').astype('uint8', copy=False)
    pc.points = pc.points.drop_duplicates()
    pc.to_file('{}_vox{}.ply'.format(path[:-4], vox))

def batch_sample_ply(input_folder, output_folder, compare_path, sample_points=10000000):
    """
    批量处理带纹理的OBJ文件，生成采样点云PLY
    :param input_folder: OBJ文件存放目录（需包含.mtl和纹理图片）
    :param output_folder: 输出PLY文件的目录
    :param compare_path: CloudCompare可执行文件路径
    :param sample_points: 采样点数（默认1000万）
    """
    # 创建输出目录
    os.makedirs(output_folder, exist_ok=True)

    # 遍历输入目录中的OBJ文件
    for obj_file in os.listdir(input_folder):
        if obj_file.lower().endswith('.obj'):
            input_path = os.path.join(input_folder, obj_file)
            output_name = os.path.splitext(obj_file)[0] + ".ply"
            output_path = os.path.join(output_folder, output_name)

            # 构建CloudCompare命令行参数
            cmd = [
                f'"{compare_path}"',  # 处理路径中的空格
                '-SILENT',
                '-NO_TIMESTAMP',
                '-O', f'"{input_path}"',  # 加载带纹理的OBJ文件
                '-SAMPLE_MESH', 'POINTS', str(sample_points),  # 采样1000万点
                '-C_EXPORT_FMT', 'PLY',  # 设置输出格式为PLY
                '-SAVE_CLOUDS', 'FILE', f'"{output_path}"'  # 保存点云
            ]

            # 执行命令
            try:
                subprocess.run('  '.join(cmd), check=True, shell=True)
                print(f"成功处理: {obj_file}")
            except subprocess.CalledProcessError as e:
                print(f"处理失败: {obj_file}\n错误信息: {e}")


if __name__ == "__main__":


    # 配置参数
    config = {
        "input_folder": "F:/DPC/100",
        "output_folder": "F:/DPC/100/100",
        "compare_path": "C:\\Program Files\\CloudCompare\\CloudCompare.exe",
        "sample_points": 10000000  # 1000万采样点
    }

    # 执行批处理
    batch_sample_ply(**config)

    print('Start!')
    seqs = glob('F:/DPC/100/100/*.ply', recursive=True)
    for path in seqs:
        print(path)
        for vox in range(10, 11):
            process(path, vox)


