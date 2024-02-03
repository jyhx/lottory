import random
from flask import request, send_file
from run import app
from oppo_lottery.dao import queryIdByName, getPersonById, getAllPersonCanLottery, iCurLotteryIndex, getAllWinner, \
    resetByStr, getCurData
from oppo_lottery.response import make_succ_empty_response, make_succ_response, make_err_response


@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return send_file('index.html')


@app.route('/result.html')
def result():
    """
    :return: 返回result页面
    """
    return send_file('result.html')


@app.route('/api/check', methods=['POST'])
def check():
    """
    签到
    """
    # 获取请求体参数
    params = request.get_json()

    if 'name' not in params:
        return make_err_response('参数错误')
    iId = queryIdByName(params['name'])
    if iId == 0:
        return make_err_response('查无此人')

    p = getPersonById(iId)
    p.check = 1
    return make_succ_response({'name': p.name, 'seat1': p.seat1, 'seat2': p.seat2})


@app.route('/api/get_lottery_info', methods=['POST'])
def get_lottery_info():
    ret = {
        'lottery_cfg': app.config['LOTTERY'][iCurLotteryIndex] if iCurLotteryIndex < len(
            app.config['LOTTERY']) else {},
        'lottery_person': [],
    }
    for p in getAllPersonCanLottery(True):
        ret['lottery_person'].append({'name': p.name, 'reward': p.reward})
    return make_succ_response(ret)


@app.route('/api/draw_lucky', methods=['POST'])
def draw_lucky():
    global iCurLotteryIndex
    if iCurLotteryIndex >= len(app.config['LOTTERY']):
        return make_err_response('奖品已抽完')

    cfgLottery = app.config['LOTTERY'][iCurLotteryIndex]
    lstCandidate = getAllPersonCanLottery(False)
    if len(lstCandidate) < cfgLottery['count']:
        return make_err_response('抽奖人数不足')

    random.shuffle(lstCandidate)
    for i in range(cfgLottery['count']):
        lstCandidate[i].desc = cfgLottery['desc']
        lstCandidate[i].lottery = cfgLottery['index']
        lstCandidate[i].reward = cfgLottery['reward']

    ret = {
        'lottery_cfg': app.config['LOTTERY'][iCurLotteryIndex],
        'has_next': iCurLotteryIndex < len(app.config['LOTTERY']) - 1,
        'lottery_person': [],
        'lucky_person': [],
    }
    iCurLotteryIndex += 1

    for p in getAllPersonCanLottery(True):
        ret['lottery_person'].append({'name': p.name, 'reward': p.reward})
    for p in lstCandidate[:cfgLottery['count']]:
        ret['lucky_person'].append({'name': p.name, 'reward': p.reward})
    return make_succ_response(ret)


@app.route('/api/get_lucky_person', methods=['POST'])
def get_lucky_person():
    ret = {
        'lucky_person': [],
    }
    for p in getAllWinner():
        ret['lucky_person'].append(
            {'name': p.name, 'reward': p.reward, 'lottery': p.lottery, 'desc': p.desc})
    return make_succ_response(ret)


@app.route('/api/clear_lottory_info', methods=['POST'])
def clear_lottory_info():
    global iCurLotteryIndex
    iCurLotteryIndex = 0
    for p in getAllWinner():
        p.lottery = 0
        p.desc = ""
        p.reward = ""
    return make_succ_empty_response()


@app.route('/admin', methods=['GET', 'POST'])
def clear_all():
    if request.method == 'GET':
        return send_file('admin.html')
    if request.method == 'POST':
        # 获取请求体参数
        params = request.get_json()
        if 'salt' not in params or 'data' not in params or 'op' not in params:
            return make_err_response('参数错误')
        salt = params['salt']
        data = params['data']
        op = params['op']
        if salt != 'sa18225052':
            return make_err_response('权限不足')
        if op == 'add':
            pass
        if op == 'reset':
            resetByStr(data)
            return make_succ_empty_response()
        if op == 'get_info':
            return make_succ_response(getCurData())
    return make_err_response('无对应操作')
