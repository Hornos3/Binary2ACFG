# coding=utf-8

import os
import sys
import shutil

'''
    main文件argv参数解释：
        1. 要分析的可执行文件路径
        2. idaq.exe路径
        3. 是否是库文件，如果是则为库文件名，否则为'-'
        4. 库版本（如果库版本未知则填'-'）
        5. 架构（默认为mips）
'''
if __name__ == '__main__':
    if len(sys.argv) != 6:
        print 'argument error'
        exit(0)

    if not os.path.isdir('.\\firmware'):
        os.mkdir('.\\firmware')

    exe = sys.argv[1]  # 可执行文件路径
    ida_path = sys.argv[2]  # idaq.exe路径
    lib = sys.argv[3]   # 库名
    version = sys.argv[4]   # 库版本
    arch = sys.argv[5]    # 架构

    newname = ''        # 获取函数名：库名+版本+架构+文件名
    if lib != '-':
        if version != '-':
            newname = lib + '_' + version + '_' + arch + "_" + exe
        else:
            newname = lib + '_' + 'unknown_version' + '_' + arch + '_' + exe
    else:
        newname = 'firmware_' + arch + '_' + exe

    os.mkdir(".\\firmware\\" + newname.split("\\")[-1])

    os.system(('{} -c '
              '-S".\\raw-feature-extractor\\preprocessing_ida.py" '
              '{}').format(ida_path, exe))
    # os.system("python diy.py " + testpath + ".ida")
    os.rename(exe + ".ida", newname + ".ida")
    # print "python sql.py " + newname + ".ida"
    # os.system("python sql.py " + newname + ".ida " + index)
    shutil.move(exe, ".\\firmware\\" + newname + "\\" + exe)
    try:
        shutil.move(exe + ".idb", ".\\firmware\\" + newname + "\\" + exe + ".idb")
    except Exception:
        shutil.move(exe + ".i64", ".\\firmware\\" + newname + "\\" + exe + ".i64")
    finally:
        shutil.copy(newname + ".ida", ".\\firmware\\" + newname + "\\" + newname + ".ida")
        shutil.move(newname + '.ida', '.\\ida_files\\' + newname + '.ida')