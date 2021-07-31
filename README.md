# Avilla - The next-gen framework for IM development

> "艾维莉亚(Avilla) .......希望这位楚楚可怜的少女, 能和她的血亲, 一位有着许多故事的可怜少女, 在旅途中创造故事的同时, 找到她们的新的故乡."

Avilla 被定义为 `Graia Project` 的 "下一代" 框架实现,
通过对 [`Onebot`](https://github.com/botuniverse/onebot), [`Telegram Bot API`](https://core.telegram.org/bots) 及其他的基于不同即时通讯软件实现的各式对接接口进行总结,
并抽象 `Relationship` 这一最为基本的模型, 构造了一个理论上可以实现零成本切换对接平台的框架.

## Roadmap

 - [x] `Avilla Protocol`: 对各式常见的行为进行抽象, 并通过可扩展的模型, 实现尽可能的功能可迁移性.
    - [x] `Network API`: 统一的网络通信兼容层, 全面支持 `Client`(客户端) 与 `Service`(服务端) 的通信方式.
    - [x] `Transformer API`: 模仿 `dart::io` 中的设计, 用于处理获得的二进制信息.
    - [x] `Resource API`: 对含多媒体内容的消息的抽象.
    - [] `Completed Design`: 设计并不完善, 还需要后续提供修改.
 - [] `Avilla for Onebot`: 对  [`Onebot`](https://github.com/botuniverse/onebot) 的协议实现.
    - [] `Avilla for go-cqhttp`: 对 [`go-cqhttp`](https://github.com/Mrs4s/go-cqhttp) 的扩展 API 的支持.
 - [] `Avilla for Telegram`: 对 [`Telegram Bot API`](https://core.telegram.org/bots) 的协议实现.
 - [] `Avilla for mirai-api-http`: 对 [`mirai-api-http`](https://github.com/project-mirai/mirai-api-http) 的支持.
 - And more...

## 我们的愿景
创造出比这之前还要更加具有潜力和创造性的作品, 借此有力促进社区的发展, 助力社区的艺术家们 (Developers & Artists) 创作出更加精彩的作品.

## 相关项目

星座的光芒是由一个个星点共同组成的, 震撼人心的作品也绝不会是一个人的功绩.  
没有这些项目, Avilla 的实现就无从谈起.  
排名不分顺序, 可能有许遗漏, 这里仅列出部分较为重要的项目.

 - [Nonebot Team](https://github.com/nonebot):
    - [Nonebot v2](https://github.com/nonebot/nonebot2): 优秀的框架, 众多灵感正来源于此.(例如 Onebot 实现的部分)
    - [aiocqhttp](https://github.com/nonebot/aiocqhttp): 开发 Avilla for Onebot 时的参考实现.
 - [Mamoe Technologies](https://github.com/mamoe):
    - [mirai](https://github.com/mamoe/mirai): the Beginning, 真正做到了 "功施至今".
    - [mirai-api-http](https://github.com/project-mirai/mirai-api-http): python-mirai 项目曾一直服务的对象, 个人认为尚具有极大的发展空间.
 - [Onebot Spec](https://github.com/botuniverse/onebot): Avilla for Onebot 所依据的实现规范, 同时也是 Avilla Protocol 设计时的参考之一.
 - [go-cqhttp](https://github.com/Mrs4s/go-cqhttp): 可能是现在运用最为广泛的 Onebot v11 实现.

无论如何, Avilla 都是 Graia Project 下的一个子项目, 用到了其中的以下项目:
 - [Broadcast Control](https://github.com/GraiaProject/BroadcastControl): 事件系统实现, 最为锋利的魔剑(Magic Sword).

衷心感谢这些以及其他未被提及的项目.

## 开源协议

Avilla 和 Avilla for Onebot, 这二者都使用 MIT 作为开源协议, 但若引用到 GPL/AGPL/LGPL 等的项目, 仍需要遵循相关规则.