"""读取示例 K 线 CSV 并打印摘要（pandas day1）。"""

from pathlib import Path  # 导入 pathlib，用于便捷地处理文件路径

import pandas as pd  # 导入 pandas，进行数据分析和数据处理

import matplotlib.pyplot as plt  # 导入 matplotlib 的 pyplot，用于绘图

# OHLC K 线绘制（需单独安装 mpl_finance / mplfinance 等兼容包）
from mpl_finance import candlestick2_ochl  # 导入专门的 K 线蜡烛图绘制函数

# 直接运行本文件时为 "__main__"；被 import 时为模块名
print(f"{__name__}")  # 打印当前模块名，通常直接运行时为"__main__"

class TestPandasKline:
    """读取示例 K 线数据并绘制图表的演示类。"""

    def test_kline_chart(self):
        """读取示例 K 线 CSV 并尝试绘制图表。"""
        # 获取当前脚本所在目录下的 CSV 文件路径（防止因工作目录不同找不到文件）
        csv_path = Path(__file__).resolve().parent / "stock_jan_feb_2026_demo.csv"
        # 读取 CSV 文件到 DataFrame
        df = pd.read_csv(csv_path)
        print(f"df: {df}")  # 打印读取到的数据，方便检查

        # 创建一个新的 matplotlib 图像对象（即新建一个画布）
        fig = plt.figure()
        # 在画布上添加一个子图（返回 Axes 对象），这里设置为 1 行 1 列的第 1 个（也是唯一一个）
        # 添加子图的目的是为了获取 axes 对象，所有的绘图操作都在 axes 上进行，便于后续管理和复用多个子图；
        # 如果你只画一张图，也需要先获取一个 axes，它是 matplotlib 面向对象绘图的核心。这样你的 K 线会画到正确的位置和坐标系。
        axes = fig.add_subplot(111)  # 变量名 axes 是 "axis" 的复数，表示子图的坐标轴对象（matplotlib 面向对象绘图的核心）

        # 用 candlestick2_ochl 绘制 K 线图，指定开盘、最高、最低、收盘数据和颜色
        candlestick2_ochl(
            ax=axes,  # 传入子图 axes
            opens=df["开盘价"].values,    # 开盘价数组
            closes=df["收盘价"].values,  # 收盘价数组
            highs=df["最高价"].values,   # 最高价数组
            lows=df["最低价"].values,    # 最低价数组
            width=0.75,                 # K 线宽度
            colorup="red",              # 收盘价高于开盘价时 K 线颜色（涨，红色）
            colordown="green",          # 收盘价低于开盘价时 K 线颜色（跌，绿色）
        )
        # 设置 x 轴刻度为行号索引，旋转 30 度便于显示
        plt.xticks(range(len(df.index.values)), df.index.values)
        axes.grid(True)  # 显示网格线
        plt.title("K-line")  # 图表标题
        plt.show()  # 展示图表

    def main(self):
        """程序入口：打印提示并调用 K 线演示逻辑。"""
        print("main")  # 打印 main，标记主流程启动
        self.test_kline_chart()  # 调用 K 线测试函数

# 仅在被 python 直接执行时运行，import 本模块时不执行
if __name__ == "__main__":
    TestPandasKline().main()  # 创建 K 线测试类实例，并运行主流程
