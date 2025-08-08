import re

def read_and_sort_fasta(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()

    entries = []
    current_entry = []

    for line in lines:
        if line.startswith('>EER') and current_entry:
            # 当遇到一个新的KGN条目时，保存当前条目，并开始一个新条目
            entries.append(''.join(current_entry))
            current_entry = [line]
        else:
            # 否则，继续添加到当前条目
            current_entry.append(line)

    # 添加最后一个条目
    if current_entry:
        entries.append(''.join(current_entry))

    # 使用正则表达式提取KGN后的数字进行排序
    entries.sort(key=lambda x: int(re.search(r'>EER(\d+)', x).group(1)))

    # 生成排序后的数据
    sorted_data = ''.join(entries)
    return sorted_data

# 指定你的文件路径
#file_path = "C:\\Users\\yuhan\\Downloads\\Plant BGC Data-20240728T015212Z-001\\Plant BGC Data\\Cucumis sativus (Cucumber)\\Cucumis_sativus.ASM407v2.cdna.all.fa"
file_path = r"C:\Users\yuhan\Downloads\Plant BGC Data-20240728T015212Z-001\Plant BGC Data\Sorghum bicolor (Great Millet)\cdna\Sorghum_bicolor.Sorghum_bicolor_NCBIv3.cdna.all.fa"
# 读取、排序并打印结果
sorted_cdna_data = read_and_sort_fasta(file_path)
print(sorted_cdna_data)

# 保存到新文件
output_path = "C:\\Users\\yuhan\\Downloads\\sorted_cdna.fa"
with open(output_path, 'w') as file:
    file.write(sorted_cdna_data)
