from git import Repo
import re
import os
# 需要第三方库 GitPython
global g
#################################################################################
# 所有项目存放的路径.比如我的项目于在C:\新建文件夹\英雄传release.此时应把引号内替换为C:/新建文件夹
# 需要用/ 不要用\
# 需要用/ 不要用\
# 需要用/ 不要用\
cfg = "D:/ayxz"
#################################################################################
c = 1
while c == 1:
    needresult = []
    needclean = []
    needresultstate = 0  # 0为不需要还原
    needcleanstate = 0  # 0为不需要清理
    x = 0
    urllist = ['占位', ]

    dirs = os.listdir(cfg)
    for file in dirs:
        url = (cfg + "/" + file)
        urllist.append(url)
        x = x + 1
        where = (str(x) + '....' + file)
        print(where)
    go = input('输入你要拉取的项目的序号...')
    try:
        go = int(go)
        url = urllist[go]
        print(str(go) + '...' + url)
        urllist.clear()
    except Exception as eeeeee:
        print("----------------------------------------------------")
        print('输入的数字错误，请重新选择...')
        continue
    #####################
    # 默认拉取
    try:
        repo = Repo(url)
        g = repo.git
    except Exception as eeeeee:
        print("----------------------------------------------------")
        print('非GIT控制的目录，请重新选择...')
        continue
    try:
        print('拉取中，请等待...')
        s = g.pull()
    except Exception as e:
        # print(e)
        # print("----------------------------------------------------")
        print('拉取失败...')
        n = re.split(r'[\n\t]', str(e))
        n0 = [i for i in n if i != '']
        # print(n0)
        # 查找需要还原的文件
        try:
            need_result_star = n0.index(
                "  stderr: 'error: Your local changes to the following files would be overwritten by merge:")
            # print(need_result_star)
            need_result_end = n0.index('Please commit your changes or stash them before you merge.')
            # print(need_result_end)
        except Exception as ee:
            needresultstate = 0
        else:
            needresultstate = 1
            needresult = n0[need_result_star + 1:need_result_end]
            print('需要还原的文件有:')
            for i in needresult:
                print(url + '/' + i)

        # 查找需要清理的文件
        try:
            if needresultstate == 0:
                need_clean_star = n0.index(
                    "  stderr: 'error: The following untracked working tree files would be overwritten by merge:")
            else:
                need_clean_star = n0.index(
                    'error: The following untracked working tree files would be overwritten by merge:')
            # print(need_clean_star)
            need_clean_end = n0.index('Please move or remove them before you merge.')
            # print(need_clean_end)
        except Exception as eee:
            needcleanstate = 0
        else:
            needcleanstate = 1
            needclean = n0[need_clean_star + 1:need_clean_end]
            print('需要清理的文件有:')
            for i in needclean:
                print(url + '/' + i)
        if needresultstate == 0 and needcleanstate == 0:
            print(e)
            print('无法自动解决报错,请手动解决...')
            continue
        # 清理下列表
        n.clear()
        n0.clear()
        stop = input('按下enter执行清理/还原...')
        if not stop == '':
            print('取消清理/还原操作...')
            print("----------------------------------------------------")
            continue

    else:
        print(s)
        print('拉取成功...')
    print("----------------------------------------------------")
    # 一键清理
    if needresultstate == 1:
        for i in needresult:
            print("还原   " + url + '/' + i)
            try:
                g.checkout(i)
            except Exception as eee:
                print('还原失败，请手动确认文件状态   ' + i)

    # 一键清理
    if needcleanstate == 1:
        for i in needclean:
            print("清理   " + url + '/' + i)
            try:
                g.clean('-f', i)
            except Exception as eee:
                print('清理失败，请手动确认文件状态   ' + i)

    #  再次拉取
    if needcleanstate == 1 or needresultstate == 1:
        print('清理/还原文件成功...')
        try:
            print('重新拉取中，请等待...')
            s = g.pull()
        except Exception as eeeee:
            print("----------------------------------------------------")
            print(eeeee)
            print("----------------------------------------------------")
            print('再次拉取失败，请查看上方的报错,手动解决...')
        else:
            print(s)
            print("拉取成功...")

    needresult.clear()
    needclean.clear()
    stop = str(input('按任意键继续...'))
    print("----------------------------------------------------")
