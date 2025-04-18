import streamlit as st
import pandas as pd
import time
from pymexc import futures

# 初始化 futures 客户端
futures_client = futures.HTTP(api_key="mx0vglpaI9sczR8Izx", api_secret="3b1ce2586d18418f864a8004a6b46fa1")

def get_position():
    position = futures_client.open_positions("ETH_USDT").get("data", [])
    lastPrice = futures_client.ticker("ETH_USDT").get("data").get('lastPrice')
    for item in position:
        s_income = (lastPrice - item["openAvgPrice"]) * item["holdVol"] / 100
        s_income = s_income > 0 and item["positionType"] == 1 and s_income or \
                   s_income > 0 and item["positionType"] == 2 and -s_income or \
                   s_income < 0 and item["positionType"] == 1 and s_income or \
                   s_income < 0 and item["positionType"] == 2 and -s_income
        item["positionType"] = item["positionType"] == 1 and "多" or item["positionType"] == 2 and "空" or "error"
        item["s_income"] = s_income
    return position

def get_account():
    equity = futures_client.asset("USDT").get("data").get('equity')
    return equity

def last_price():
    lastPrice = futures_client.ticker("ETH_USDT").get("data").get('lastPrice')
    return lastPrice

def get_1x_value(x):
    if x < 500:
        return 1
    elif 500 <= x < 100000:
        return ((x - 500) // 1000 + 1) * 10
    else:
        return 1  # 或其他默认值

def get_data():
    data = []
    position = get_position()
    equity = get_account()
    _1x_value = int(get_1x_value(equity))
    lastPrice = last_price()
    for item in position:
        symbol = '%s>%s>%s' % (item["symbol"].replace('_USDT', ''), item["leverage"], item["positionType"])
        income = int(item["s_income"] / (_1x_value))
        holdVol = '%.1f     |   %.1f' % (item['holdAvgPrice'], lastPrice)
        data.append({
            "交易对": symbol,
            '均价/当前价': holdVol,
            '开仓数量': float(item['holdVol'] / (100 * _1x_value)),
            '收入': income,
            '余额': int(equity / _1x_value),
            '强平价': item['liquidatePrice'],
            '建议': "%s开%s平 && 基数%s(实际%.1f)" % (_1x_value, int(_1x_value / 2), int(equity / _1x_value), float(equity)),
        })
    return pd.DataFrame(data)

# 页面设置
st.set_page_config(page_title="实时交易展示", layout="wide")

# 标题
st.title("")

# 提示说明
st.markdown("""
    <div style='text-align: center; font-size: 20px; color: #FF6347;'>莫贪心，贪多嚼不烂</div>
    <hr style='border: 1px solid #FF6347;'/>
""", unsafe_allow_html=True)

# 表格样式优化
def style_df(df):
    def color_income(val):
        if val > 0:
            return "color: green; font-weight: bold"  # 收益为正数时显示绿色
        elif val < 0:
            return "color: red; font-weight: bold"  # 收益为负数时显示红色
        return ""

    def color_stock(val):
        if '空' in val:
            return "color: red; font-weight: bold"  # 交易对使用橙色显示
        if '多' in val:
            return "color: green; font-weight: bold"

    return df.style \
        .applymap(color_stock, subset=["交易对"]) \
        .applymap(color_income, subset=["收入"]) \
        .format({
            "收入": "{:+.2f}",
            "开仓数量": "{:.2f}",
            "余额": "{:.2f}",
            "强平价": "{:.2f}",
        }) \
        .set_properties(**{
            'background-color': '#F9F9F9',
            'border': '1px solid #ddd',
            'font-size': '14px',
        }) \
        .set_table_styles([{
            'selector': 'thead th',
            'props': [('background-color', '#FF6347'), ('color', 'white'), ('font-weight', 'bold')]
        }, {
            'selector': 'tbody td',
            'props': [('text-align', 'center')]
        }])

# 用 placeholder 来刷新表格
placeholder = st.empty()

# 控制刷新间隔时间（秒）
refresh_interval = st.sidebar.slider("刷新间隔（秒）", 1, 10, 2)

# 数据展示与更新循环
while True:
    df = get_data()
    styled_df = style_df(df)

    # 渲染样式化后的 DataFrame
    with placeholder.container():
        st.write(styled_df, use_container_width=True)
        st.markdown(f"<p style='text-align: right; color: gray;'>更新时间：{time.strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)

    time.sleep(refresh_interval)
