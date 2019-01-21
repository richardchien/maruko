rom nonebot import on_command, CommandSession
from collections import defaultdict
from nonebot.helpers import context_id
from nonebot import MessageSegment
def create_empty_item():
    return {
        'pet_name': None,  # 宠物姓名
        'pet_status': 0,  # 宠物状态 0 未拥有宠物 1 存活 2 死亡
        'user_status': 0,     # 用于扩展氪金 vip?
    }

data = defaultdict(create_empty_item)

@on_command('pet', aliases=['领养'])
async def adoption(session: CommandSession):
    ctx_id = context_id(session.ctx, mode='user')
    my_data = data[ctx_id]

    if my_data['pet_status'] == 1:
        await session.finish('你已经领养过宠物啦~快去看看它的状态吧')
    elif my_data['pet_status'] == 2:
        await session.finish('你领养的'+str(my_data['pet_name'])+'已经死了，你真是个不称职的主人')
    elif my_data['pet_status'] == 0:
        pet_name = session.get('pet_name', prompt='你想领养的宠物名字是？\n(space 退出宠物系统)')
        pet_name = pet_name.strip()
        my_data['pet_name'] = pet_name
        my_data['pet_status'] = 1
        await session.send('你已经成功领养'+str(my_data['pet_name'])+'啦，快去看看它的状态吧~')

@adoption.args_parser
async def save(session: CommandSession):
    if session.is_first_run:
        return
    session.args[session.current_key] = session.current_arg_text.strip()

@on_command('feed', aliases=['喂食'])
async def feed(session: CommandSession):
    ctx_id = context_id(session.ctx, mode='user')
    my_data = data[ctx_id]
    if my_data['pet_status'] == 2:
        await session.finish('你的宠物已经死了，你真是个不负责的主人')
    elif my_data['pet_status'] == 0:
        await session.finish('你还没领养宠物呢，快去领养吧')
    else:
        my_data['pet_status'] = 2
        await session.send(str(my_data['pet_name'])+'张开血盆大口向你扑来，把你一口吞了\n你的宠物食物中毒死了....')

@on_command('view', aliases=['查看宠物状态', '查看宠物状态'])
async def view(session: CommandSession):
    ctx_id = context_id(session.ctx, mode='user')
    my_data = data[ctx_id]
    QQ_AVATAR_URL_FORMAT = 'https://q1.qlogo.cn/g?b=qq&nk={}&s=40'
    url = QQ_AVATAR_URL_FORMAT.format(session.ctx['user_id'])
    reply = str(MessageSegment.image(url))
    if session.ctx['message_type'] != 'private':
        reply += f'\n' + str(MessageSegment.at(session.ctx['user_id'])+'\n')
    if my_data['pet_status'] == 1:
        session.finish(reply+'你的宠物很饿，快去喂养它吧')
    elif my_data['pet_status'] == 0:
        session.finish('你还没拥有宠物呢，快去领养一个吧')
    elif my_data['pet_status'] == 2:
        session.finish(reply + '你的宠物已经死啦，你真是个不负责的主人')