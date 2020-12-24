# 随机生成测试数据
## 描述
日常系统开发时候测试人员往往需要造好多测试数据，但是让人头疼的就是找生成各类测试数据，包括用户的基础信息，公司的基础信息等各类基础信息，本文件继承自Faker之上又封装了一些新方法，可配合使用，减轻测试人员寻找测试数据的麻烦。并且支持直接连接数据库，这样便可以直接将测试数据入库，减少工作量。
## 文件目录结构
```
│  config.yaml             # 数据库连接配置文件
│  FakerDoc.py             # 测试数据生成模块Faker的简要文档
│  msgStaticClass.py       # 随机生成各类测试数据类
│  test.py                 # 测试方法
├─config
│  │  Logger.py            # 日志记录
│  │  MongoContent.py      # MongoDB连接配置类
│  │  MysqlContent.py      # MySQL连接配置类
│  │  ReadConfig.py        # 读取配置文件类
│  │  TimeStamp.py         # python操作日志类
├─doc
│      com.txt             # 随机生成企业数据，可继续追加
```
# 使用方法
1. pip install Faker
2. 原生faker方法可查找FakerDoc.py文档，如果你通过pycharm便可直接通过编辑器查看方法使用；
3. msgStaticClass测试数据生成类，可用faker继承之后的方法，也可以faker原生方法;
4. 具体可查看FakerDoc及msgStaticClass注释