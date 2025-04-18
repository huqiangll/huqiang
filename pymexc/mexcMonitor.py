# coding=utf-8
import json
import os
import sys
import threading
import time

import futures

futures_client = futures.HTTP(api_key="mx0vgld4AhTPdY8HdV", api_secret="d9ea5b1b78f4458ba4f005120a021b14")


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


i = 1


def position(arg):
    while True:
        tmp = ''
        position = get_position()
        for item in position:
            tmp = tmp + "\033[31m%s-%s-%s\033[0m-> 持仓均价:%s 数量:%s 盈亏:%s      ||     " % (
            item["symbol"], item["leverage"], item["positionType"], item['holdAvgPrice'], float(item['holdVol'] / (100 * arg)), int(item["s_income"] / arg))

        time.sleep(0.5)
        os.system('cls')

        sys.stdout.write('\r' + tmp )
        sys.stdout.flush()


if __name__ == '__main__':
    arg = sys.argv[1]

    threading.Thread(target=position, args=[int(arg)]).start()
