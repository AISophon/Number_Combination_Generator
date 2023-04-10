import itertools
import re
import os

#定义递归函数用于生成表达式
def generate_expr(nums):
    if len(nums) == 1:
        yield nums[0]
    else:
        for i in range(1, len(nums)):
            left_nums = nums[:i]
            right_nums = nums[i:]

            # 枚举运算符
            for op in ['+', '-', '*', '/','']:
                
                # 递归调用生成左右两侧的表达式
                for left_expr in generate_expr(left_nums):
                    for right_expr in generate_expr(right_nums):
                        
                        # 生成括号表达式
                        yield f'({left_expr}{op}{right_expr})'
                        
                        # 生成不带括号的表达式
                        yield f'{left_expr}{op}{right_expr}'

# 用户输入正整数列表
with open('input.txt', 'r') as f:
    nums = f.read().split()
    nums = [int(num) for num in nums]

nums = [int(num) for num in nums]

# 打开输出文件并将表达式写入其中
with open('all_expression.txt', 'w') as f:
    for expr in generate_expr(nums):
        f.write(expr + '\n')

print('已枚举完毕')

with open('all_expression.txt', 'r') as input_file, open('calculated.txt', 'w') as output_file:
     # 逐行读取输入文件
     for line in input_file:
       try:
           # 尝试计算表达式
          if eval(line.strip()) is not None:
              # 如果成功，写入结果到输出文件中
             result = eval(line.strip())
             output_file.write(str(result) + ': "' + line.strip() + '"\n')
       except:
         # 如果失败，则跳过该行表达式
         pass

print("已计算并储存完毕")

# 打开文件
with open('calculated.txt', 'r') as f:
    # 读取所有行
    lines = f.readlines()

# 定义一个字典，用于记录以数字为键、以行内容为值的映射关系
results = {}

# 遍历每一行
for line in lines:
    # 将每一行按冒号分割成两部分
    parts = line.strip().split(':')

    # 判断冒号前面的部分是否为整数
    if parts[0].isdigit() or (len(parts[0]) > 1 and parts[0][0] in ['-', '+'] and parts[0][1:].isdigit()):
        # 如果是整数，则将以该整数为键的值更新为当前行的内容
        num = int(parts[0])
        # 如果该数已经在字典中出现过，则将当前行内容与之前的值比较，选取较短的那个作为最终值
        if num in results:
            results[num] = min(results[num], line)
        else:
            results[num] = line

# 对字典的键进行排序
sorted_keys = sorted(results.keys(), reverse=True)

# 打开输出文件
with open('screened.txt', 'w') as f:
    # 将排好序的键对应的值写入文件中
    for num in sorted_keys:
        f.write(results[num])

print('筛选完毕')

with open('screened.txt', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    new_line = re.sub(r'"(.)(.*)(.)"', r'"\2"', line)
    new_lines.append(new_line)

with open('end.txt', 'w') as f:
    f.writelines(new_lines)

os.remove('all_expression.txt')
os.remove('calculated.txt')
os.remove('screened.txt')

print('程序运行完毕')
