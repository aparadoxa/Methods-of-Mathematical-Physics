import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import librosa
import librosa.display
import tkinter as tk
from tkinter import filedialog

# 设置中文字体支持
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

def analyze_mp3(file_path, output_folder):
    """分析单个MP3文件并生成赛博朋克风格的时频图"""
    try:
        # 加载音频文件，只加载3-4秒的片段
        y, sr = librosa.load(file_path, sr=None, offset=3.0, duration=1.0)
        
        # 计算时间轴（从3秒开始）
        time = np.linspace(3.0, 4.0, len(y))
        
        # 创建赛博朋克风格的颜色
        line_color = '#00F9FF'  # 青色线条
        fill_color = '#FF00E6'  # 粉色填充
        grid_color = '#333333'  # 深灰色网格
        text_color = '#FFFFFF'   # 白色文本
        
        # 创建图像并设置黑色背景
        fig, ax = plt.subplots(figsize=(12, 8), facecolor='black')
        ax.set_facecolor('black')
        
        # 设置标题和坐标轴标签颜色
        plt.title(f"3-4秒总幅值随时间变化图\n文件: {os.path.basename(file_path)}", color=text_color, fontsize=14)
        plt.xlabel('时间 (秒)', color=text_color, fontsize=12)
        plt.ylabel('幅值', color=text_color, fontsize=12)
        
        # 设置坐标轴刻度颜色
        ax.tick_params(axis='x', colors=text_color)
        ax.tick_params(axis='y', colors=text_color)
        
        # 设置坐标轴和网格
        ax.spines['bottom'].set_color(text_color)
        ax.spines['left'].set_color(text_color)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.grid(True, linestyle='--', alpha=0.3, color=grid_color)
        
        # 绘制总幅值随时间的变化图，使用赛博朋克风格
        plt.plot(time, y, color=line_color, alpha=0.9, linewidth=1.0)
        
        # 添加填充效果，增强视觉冲击力
        plt.fill_between(time, y, 0, color=fill_color, alpha=0.3)
        
        # 添加水印效果
        plt.gcf().text(0.95, 0.05, 'Cyber Audio Analyzer', fontsize=12, color='gray', ha='right', alpha=0.5)
        
        # 保存图像
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_image_path = os.path.join(output_folder, f"{base_name}_3-4秒幅值随时间变化图.png")
        plt.tight_layout()
        plt.savefig(output_image_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return {
            'file': os.path.basename(file_path),
            'image_path': output_image_path
        }
        
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {str(e)}")
        return None

def select_folder():
    """打开文件夹选择对话框并返回选择的路径"""
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    folder_path = filedialog.askdirectory(title="选择MP3文件所在文件夹")
    root.destroy()
    return folder_path

def main():
    """主函数，处理文件夹中的所有MP3文件"""
    # 获取用户选择的文件夹路径
    folder_path = select_folder()
    
    if not folder_path:
        print("未选择文件夹，程序退出")
        return
    
    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        print(f"错误: 文件夹 '{folder_path}' 不存在")
        return
    
    # 获取所有MP3文件
    mp3_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.mp3')]
    
    if not mp3_files:
        print(f"错误: 文件夹 '{folder_path}' 中未找到MP3文件")
        return
    
    # 创建结果文本文件
    results_path = os.path.join(folder_path, "音频分析结果.txt")
    
    with open(results_path, 'w', encoding='utf-8') as f:
        f.write("音频文件分析结果\n")
        f.write("=" * 50 + "\n\n")
        
        for mp3_file in mp3_files:
            file_path = os.path.join(folder_path, mp3_file)
            result = analyze_mp3(file_path, folder_path)
            
            if result:
                f.write(f"文件: {result['file']}\n")
                f.write(f"图像路径: {os.path.basename(result['image_path'])}\n")
                f.write("-" * 50 + "\n")
    
    print(f"分析完成! 结果已保存到: {results_path}")
    print(f"共处理了 {len(mp3_files)} 个MP3文件")

if __name__ == "__main__":
    main()    