import subprocess

def load_str_array(file):
    f = open(file)
    res = [line for line in f]
    f.close()
    return res

if __name__ == '__main__':
    COUNT = 1
    pythonmodels = ['task_0.py', 'task_a1.py', 'task_a2.py', 'task_a3.py',
                    'task_b1.py', 'task_b2.py', 'task_b3.py', 'task_c.py',
                    'task_res.py']
    stat = {x : {} for x in pythonmodels}
    for it in range(COUNT):
        for model in pythonmodels:
            logfile = model + '.txt'
            statfile = model + '_stat.txt'
            with open(logfile, 'w') as f:
                subprocess.call(['python3', model], stdout=f)
            with open(statfile, 'w') as f:
                with open(logfile, 'r') as g:
                    subprocess.call(['./stat'], stdout=f, stdin=g)
            tmpstat = load_str_array(statfile)
            tmpstat = [line.split(': ') for line in tmpstat]
            prefix = ''
            for node in tmpstat:
                if node[0] == 'status for elem':
                    prefix = node[1][: len(node[1]) - 1]
                    prefix.replace('\n', '')
                else:
                    if prefix + ' ' + node[0] in stat[model]:
                        stat[model][prefix + ' ' + node[0]] += float(node[1])
                    else:
                        stat[model][prefix + ' ' + node[0]] = float(node[1])
    for model in stat:
        #print(stat[model])
        for node in stat[model]:
            print(model, node, stat[model][node])