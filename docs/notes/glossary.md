# 概念卡

每张卡：一句话定义 + 一个我自己撞上的实例。只收真正卡住过我的词。

## 虚拟环境（venv）

一个独立的 Python + 独立第三方包目录，不污染系统。
实例：source .venv/bin/activate 后 python -V 才是 3.11；uv run 会自动进这个房间。
自检：which python 是否指向 .venv/bin/python

## lock 文件（uv.lock）

锁定每个依赖的确切版本，保证别人装出一样的环境。
实例：我用 uv pip install torch 装了但没登记，CI 上 uv sync 装不到，报 ModuleNotFoundError。
记住：uv pip install 是「我现在要用」，uv add 是「这个项目需要」。
自检：grep -c '^name = "torch"' uv.lock

## 退出码（exit code）

命令结束时返回 0（成功）或非 0（失败）；CI 靠它判断红绿。
实例：compare.py 检测到回退就 return 1，门禁才真正拦得住合并。
自检：echo $? ；a && b 表示 a 成功才跑 b
