import os
import re

configs = {}
path = 'template/'


def parse_properties(filename):
    res = {}
    with open(path + filename, 'r') as f:
        s = f.read()
        s = s.replace('\\\n', '')
        lines = s.split('\n')
        for line in lines:
            sharp_idx = line.find('#')
            if sharp_idx != -1:
                line = line[0:sharp_idx]
            item = line.split('=')
            if len(item) < 2:
                continue
            res[item[0]] = item[1]
    return res


if __name__ == '__main__':
    with open(path + 'index.html', 'r') as f:
        temp = f.read()
        addition = re.findall(r'@{(.*?)}', temp)
        all_part = re.split(r'@{.*?}', temp)

    addition.append('')
    items = list(zip(all_part, addition))
    # print(items)

    files = os.listdir(path)
    for file in files:
        if not os.path.isdir(file) and file.endswith('.properties'):
            if file == 'i18n.properties':
                continue
            lang = file[5:10]
            config = parse_properties(file)
            configs[lang] = config

    for lang, config in configs.items():
        print(lang)
        print(config)
        os.makedirs(lang, exist_ok=True)
        s = ''
        with open(lang + '/index.html', 'w') as f:
            for content, key in items:
                s += content + config.get(key, '')
            f.write(s)
