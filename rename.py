import os

path = './'


# rename images downloaded from twitter
def rename():
    filelist = os.listdir(path)
    total_num = len(filelist)
    i = 0o0001
    for item in filelist:
        if item.endswith('.jpg'):
            src = os.path.join(os.path.abspath(path), item)
            dst = os.path.join(os.path.abspath(path), 'pic' + str(i) + '.jpg')
            try:
                os.rename(src, dst)
                print('converting %s to %s ...' % (src, dst))
                i = i + 1
            except:
                continue
    print('total %d to rename & converted %d jpgs' % (total_num, i))

rename()