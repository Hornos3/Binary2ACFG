# 使用指南

此项目需要在pycharm中打开并进行一些配置设置，直接使用命令行无法运行。

打开pycharm后将python文件夹和raw-feature-extractor文件夹设置为源

main.py用于分析二进制文件并生成ida文件

    main文件argv参数解释：
        1. 要分析的可执行文件路径
        2. idaq.exe路径
        3. 是否是库文件，如果是则为库文件名，否则为'-'
        4. 库版本（如果库版本未知则填'-'）
        5. 架构（默认为mips）

main.py运行时会打开IDA_pro窗口，全确认然后就会自动退出

diy.py用于分析ida文件并生成json格式的文件

    diy.py文件argv参数解释：
        1. 要分析的ida文件或文件夹路径（如果是文件夹则会分析文件夹中所有ida文件）
        2. 要生成的json文件名

先使用main.py分析二进制文件，然后使用diy.py获取acfg

ida_files是openssl不同版本部分有漏洞函数的源文件的ida文件

selected_files_...是不同版本有漏洞函数的编译后的mips可执行文件