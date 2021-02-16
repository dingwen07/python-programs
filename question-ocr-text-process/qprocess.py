from os import replace


text = '''
单选I 6.小董开发了邮政编码识别程序，能够根据国内邮政编码快速查询到对应的省市，为了能够快速完成开_
本题分值2
发，他直接购买了查询邮编信息的API,作为一个独立开发者资金毕竟有限，他方面希望服务更多的用
户，另一方面不希望其API被无效使用或浪费，请问他该采用什么来实现要求呢?
◎A.使用流量控制对该账号下所有APP的流量总和限制，防止被过度使用
O B. 采用入参透传模式,让后端服务来获知原始的参数，进而优化API调用，减少调用次数
O C.使用流量控制, 针对API、 用户和应用三个对象设置不同策略，针对某些APP设置例外流控，保证正常API调用，减少非必要调用
O D.采用入参映射模式， 定义参数预校验规则，降低后端处理的非法请求，从而减少调用次数
Q E.采用入参透传模式 ,通过预定义规则筛选合理的访问请求，从而只进行有效响应，降低使用次数

'''

punctuation = """！？，｡＂＃＄％＆＇（）＊＋－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿—﹏"""

replace_list = [
    ('选择- -项:', '', True),
    ('选择- -项：', '', True),
    ('选择一项:', '', True),
    ('选择一项：', '', True),
    ('选择- -项或多项:', '', True),
    ('选择- -项或多项：', '', True),
    ('选择一项或多项:', '', True),
    ('选择一项或多项：', '', True),
    ('本题分值2\n', '', True),
    ('本题分值 2\n', '', True),
    ('单选', '', False),
    ('多选', '', False),
    ('- -个', '一个', True),
    ('- 个', '一个', True),
    ('一一个', '一个', False),
    ('一 个', '一个', False),
    ('- -方面', '一方面', True),
    ('同- -', '同一', True),
    ('， ', '，', True),
    (' ，', '，', True),
    ('。 ', '。', True),
    (' 。', '。', True),
    ('、 ', '、', True),
    (' 、', '、', True),
    ('1oT', 'IoT', True),
    ('↓', '[@[%[!!!]%]@]', False),
    ('\nA ', '\nA.', False),
    ('\nB ', '\nB.', False),
    ('\nC ', '\nC.', False),
    ('\nD ', '\nD.', False),
    ('0SS', 'OSS', False),

]

cn_replace_list_ss = [
    (', ', '，', True),
    (' ,', '，', True),
    (',', '，', True),
]

cn_replace_list = [
    ('-', '一', False),
    ('- ', '一', False),
    (' -', '一', False),
    ('- -', '一', True),
    (';', '；', True),
    ('?', '？', True),
    (':', '：', True),
    (' .', '，', False),

]

def is_chinese_char(char):
    return char in punctuation or '\u4e00' <= char <= '\u9fff'

def question_process(text):
    warn = False
    warn_msg = []
    text = text.strip('\n')

    option_list = ['a', 'A', 'b', 'B', 'c', 'C', 'd', 'D', 'e', 'E', 'f', 'F']
    options_found = []
    option_pos = []
    for _index, _option in enumerate(option_list):
        _option_found = False
        _option_pos = text.find(_option + '.')
        if _option_pos != -1 and text[_option_pos + 2] == ' ':
            text = text[0:_option_pos + 2] + text[_option_pos + 3:]
        _option_pos = text.find(_option + '.')
        if _option_pos != -1 and text[_option_pos - 1] == ' ':
            text = text[0:_option_pos - 1] + text[_option_pos:]
        _option_pos = text.find(_option + '.')
        if _option_pos != -1 and text[_option_pos - 2] == '\n':
            text = text[0:_option_pos - 1] + text[_option_pos:]
        _option_pos = text.find(_option + '.')
        if _option_pos != -1 and text[_option_pos - 1] == '\n' and _index % 2 == 0:
            text = text[0:_option_pos] + option_list[_index + 1] + text[_option_pos + 1:]

        _option_pos = text.find(_option + '.')
        _option_found = _option_pos != -1
        if _option_found and text[_option_pos - 1] == '\n':
            try:
                _option_found_index = options_found.index(_option.lower())
                warn = True
                warn_msg.append('answer "{}" in position {} duplicate'.format(_option.upper(), str(_option_pos)))
                if option_pos[_option_found_index] > _option_pos:
                    options_found.remove(_option.lower())
                    options_found.append(_option.lower())
                    option_pos.pop(_option_found_index)
                    option_pos.append(_option_pos)
            except ValueError:
                options_found.append(_option.lower())
                option_pos.append(_option_pos)
    print(options_found)
    print(option_pos)

    _option_pos_pre = -1
    for _option_index, _option in enumerate(options_found):
        try:
            if option_list.index(_option) / 2 != _option_index:
                warn = True
                warn_msg.append('answer "{}" not found'.format(option_list[_option_index * 2].upper()))
                options_found.insert(_option_index, option_list[_option_index * 2])
                option_pos.append(len(text) + 1000)
        except ValueError:
            continue
        if option_pos[_option_index] < _option_pos_pre:
            warn = True
            warn_msg.append('answer "{}" in position {} out of order'.format(_option.upper(), str(option_pos[_option_index])))
        _option_pos_pre = option_pos[_option_index]

    for _replace_tuple in cn_replace_list_ss:
        before = _replace_tuple[0]
        after = _replace_tuple[1]
        char_index = text.find(before)
        while char_index != -1:
            if is_chinese_char(text[char_index - 1]) or (is_chinese_char(text[char_index + len(before)]) or text[char_index + len(before)] == '\n'):
                text = text[0:char_index] + after + text[char_index + len(before):]
                if not _replace_tuple[2]:
                    warn = True
                    warn_msg.append('unreliable substitution: "{}" ==> "{}" at position {}'.format(before, after, str(char_index)))
            char_index = text.find(before, char_index + len(after))

    for _replace_tuple in cn_replace_list:
        before = _replace_tuple[0]
        after = _replace_tuple[1]
        char_index = text.find(before)
        while char_index != -1:
            if is_chinese_char(text[char_index - 1]) and (is_chinese_char(text[char_index + len(before)]) or text[char_index + len(before)] == '\n'):
                text = text[0:char_index] + after + text[char_index + len(before):]
                if not _replace_tuple[2]:
                    warn = True
                    warn_msg.append('unreliable substitution: "{}" ==> "{}" at position {}'.format(before, after, str(char_index)))
            char_index = text.find(before, char_index + len(after))

    for _replace_tuple in replace_list:
        before = _replace_tuple[0]
        after = _replace_tuple[1]
        char_index = text.find(before)
        while char_index != -1:
            text = text.replace(before, after, 1)
            if not _replace_tuple[2]:
                warn = True
                warn_msg.append('unreliable substitution: "{}" ==> "{}" at position {}'.format(before, after, str(char_index)))
            char_index = text.find(before, char_index + len(after))

    char_index = text.find('\n')
    while char_index != -1:
        if is_chinese_char(text[char_index - 1]) or is_chinese_char(text[char_index + 1]):
          if not (text[char_index + 1] in option_list and text[char_index + 2] == '.'):  
                text = text[0:char_index] + '' + text[char_index + 1:]
                # text = text.replace('\n', '', 1)
        char_index = text.find('\n', char_index + 1)

    # question number removal
    try:
        point_pos = text.find('.')
        if point_pos < 12:
            if text[point_pos - 1] == ' ':
                int(text[point_pos - 2])
            else:
                int(text[point_pos - 1])
            qnum_text = text[0:point_pos + 1]
            text = text[point_pos + 1:]
            warn = True
            warn_msg.append('question number removed: "{}"'.format(qnum_text))
    except Exception:
        pass


    if text.find('[@[%[!!!]%]@]') != -1:
        warn = True
        warn_msg.append('invalid keywards found')

    return (text, warn, warn_msg)

if __name__ == "__main__":
    pcs = question_process(text)
    print(pcs[0])
    print(pcs[1])
    warn_msg = ''
    for msg in pcs[2]:
        warn_msg += msg + '\n'
    print(warn_msg)
