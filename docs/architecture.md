架构设计
==============
<div style="align: center">![系统架构图](https://github.com/Beatles1314/PyParser/blob/dev/docs/imgs/architecture.png)
</div>
系统的主要部分有：
* RedisMonitor：监控爬虫的结果队列，从爬虫的结果队列中获取结果并推送给下游处理。
* save_content_worker：网页持久化消费者，用于将原始网页进行持久化。
* parse_worker：数据解析消费者，加载解析脚本，对原始网页进行解析。
* validate_worker：数据校验消费者，加载校验脚本，对解析结果进行进一步校验。
* storage_worker：入库消费者，对通过校验的数据进行入库处理。