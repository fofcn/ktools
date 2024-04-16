# 工程搭建
1. 安装python3
2. 安装pip3
3. 安装并激活virtualenv
```shell

python3 -m venv .venv
. .venv/bin/activate

```
4. 安装依赖
```shell
pip install -r requirements.txt
```

5. 运行
```shell
flask --app app --debug run
```