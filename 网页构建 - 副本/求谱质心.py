import os
import librosa
import numpy as np

def weighted_average_frequency(mp3_path):
    """计算MP3音频按幅值加权的平均频率
    
    参数:
        mp3_path (str): MP3文件路径
    
    返回:
        float: 加权平均频率 (Hz)
    """
    try:
        y, sr = librosa.load(mp3_path, sr=None)
        D = librosa.stft(y)
        S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
        frequencies = librosa.fft_frequencies(sr=sr, n_fft=2048)
        
        weighted_frequencies = []
        for i in range(S_db.shape[1]):
            frame_spectrum = S_db[:, i]
            linear_spectrum = librosa.db_to_amplitude(frame_spectrum)
            if np.sum(linear_spectrum) > 0:
                weighted_freq = np.sum(frequencies * linear_spectrum) / np.sum(linear_spectrum)
                weighted_frequencies.append(weighted_freq)
        
        return np.mean(weighted_frequencies) if weighted_frequencies else 0.0
    except Exception as e:
        print(f"处理文件 {mp3_path} 时出错: {str(e)}")
        return None

def analyze_folder(input_folder):
    """分析文件夹中的所有MP3文件并输出结果到TXT文件
    
    参数:
        input_folder (str): 输入文件夹路径
    """
    if not os.path.exists(input_folder):
        print(f"错误: 文件夹 '{input_folder}' 不存在")
        return
    
    mp3_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.mp3')]
    
    if not mp3_files:
        print(f"文件夹 '{input_folder}' 中未找到MP3文件")
        return
    
    output_file = os.path.join(input_folder, "音频频率分析结果.txt")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("音频文件名称\t加权平均频率(Hz)\n")
        f.write("-" * 40 + "\n")
        
        for mp3_file in mp3_files:
            mp3_path = os.path.join(input_folder, mp3_file)
            avg_freq = weighted_average_frequency(mp3_path)
            
            if avg_freq is not None:
                f.write(f"{mp3_file}\t{avg_freq:.2f}\n")
                print(f"已分析: {mp3_file} - 平均频率: {avg_freq:.2f} Hz")
    
    print(f"\n分析完成，结果已保存至: {output_file}")

# 使用示例 - 直接在Python环境中调用
folder_path = "./素材/视频素材"
analyze_folder(folder_path)    