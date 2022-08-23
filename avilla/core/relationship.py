from __future__ import annotations

from collections import ChainMap
from contextlib import AsyncExitStack
from inspect import isclass
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    Generic,
    Iterable,
    TypeVar,
    cast,
    overload,
)

from graia.amnesia.message import Element, MessageChain, Text
from typing_extensions import Unpack

from avilla.core.account import AbstractAccount

# from avilla.core.action.middleware import ActionMiddleware
from avilla.core.cell import Cell, CellOf
from avilla.core.context import ctx_relationship
from avilla.core.message import Message
from avilla.core.resource import Resource
from avilla.core.skeleton.message import MessageTrait
from avilla.core.traitof import Trait
from avilla.core.traitof.context import GLOBAL_SCOPE, Scope
from avilla.core.utilles.selector import Selectable, Selector

from .traitof.signature import ArtifactSignature, CompleteRule, Pull, ResourceFetch

if TYPE_CHECKING:
    from avilla.core.protocol import BaseProtocol

_T = TypeVar("_T")
_M = TypeVar("_M", bound=Cell)
_TboundTrait = TypeVar("_TboundTrait", bound=Trait)


class Relationship:
    ctx: Selector
    mainline: Selector
    self: Selector
    via: Selector | None = None

    account: AbstractAccount
    cache: dict[str, Any]

    protocol: "BaseProtocol"

    _artifacts: ChainMap[ArtifactSignature, Any]
    # _middlewares: list[ActionMiddleware]

    def __init__(
        self,
        protocol: "BaseProtocol",
        ctx: Selector,
        mainline: Selector,
        selft: Selector,
        account: AbstractAccount,
        via: Selector | None = None,
        # middlewares: list[ActionMiddleware] | None = None,
    ) -> None:
        self.ctx = ctx
        self.mainline = mainline
        self.self = selft
        self.via = via
        self.account = account
        self.protocol = protocol
        # self._middlewares = middlewares or []
        self.cache = {"meta": {}}
        self._artifacts = ChainMap(
            self.protocol.impl_namespace.get(Scope(self.mainline.path_without_land, self.self.path_without_land), {}),
            self.protocol.impl_namespace.get(Scope(self.mainline.path_without_land), {}),
            self.protocol.impl_namespace.get(Scope(self=self.self.path_without_land), {}),
            self.protocol.impl_namespace.get(GLOBAL_SCOPE, {}),
            self.avilla.global_artifacts,
        )

    @property
    def avilla(self):
        return self.protocol.avilla

    @property
    def land(self):
        return self.protocol.land

    @property
    def is_resource(self) -> bool:
        # TODO: Auto inference for implementations of a "ctx"
        ...

    @property
    def app_current(self) -> Relationship | None:
        return ctx_relationship.get(None)

    """
    @property
    def query(self):
        return RelationshipQuerier(self)
    """

    def complete(self, selector: Selector, with_land: bool = False):
        output_rule = self._artifacts.get(CompleteRule(selector.path_without_land))
        if output_rule is not None:
            output_rule = cast(str, output_rule)
            selector = Selector().mixin(output_rule, selector, self.ctx, self.mainline)
        if with_land and list(selector.pattern.keys())[0] != "land":
            selector.pattern = {"land": self.land.name, **selector.pattern}
        return selector

    async def fetch(self, resource: Resource[_T]) -> _T:
        fetcher = self._artifacts.get(ResourceFetch(type(resource)))
        if fetcher is None:
            raise NotImplementedError(
                f'cannot fetch "{resource.selector}" '
                + f' because no available fetch implement found in "{self.protocol.__class__.__name__}"'
            )
        return await fetcher(self, resource)

    async def pull(
        self,
        path: type[_M] | CellOf[Unpack[tuple[Any, ...]], _M],
        target: Selector | Selectable | None = None,
        *,
        flush: bool = False,
    ) -> _M:
        if isinstance(target, Selectable):
            target = target.to_selector()
        if target is not None:
            cached = self.cache["meta"].get(target)
            if cached is not None and path in cached:
                if flush:
                    del cached[path]
                elif not path.has_params():
                    return cached[path]

        puller = self._artifacts.get(Pull(target.path_without_land if target is not None else None, path))
        if puller is None:
            raise NotImplementedError(
                f'cannot pull "{path}"'
                + (f' for "{target.path_without_land}"' if target is not None else "")
                + f' because no available implement found in "{self.protocol.__class__.__name__}"'
            )
        puller = cast("Callable[[Relationship, Selector | None], Awaitable[_M]]", puller)
        result = await puller(self, target)
        if target is not None and not path.has_params():
            cached = self.cache["meta"].setdefault(target, {})
            cached[path] = result
        return result

    def cast(
        self,
        trait: type[_TboundTrait],
        path: type[Cell] | CellOf[Unpack[tuple[Any, ...]], Cell] | None = None,
        target: Selector | Selectable | None = None,
    ) -> _TboundTrait:
        if isinstance(target, Selectable):
            target = target.to_selector()
        return trait(self, path, target)

    def send_message(
        self, message: MessageChain | str | Iterable[str | Element], *, reply: Message | Selector | str | None = None
    ):
        if isinstance(message, str):
            message = MessageChain([Text(message)])
        elif not isinstance(message, MessageChain):
            message = MessageChain([]).extend(list(message))
        else:
            message = MessageChain([i if isinstance(i, Element) else Text(i) for i in message])

        if isinstance(reply, Message):
            reply = reply.to_selector()
        elif isinstance(reply, str):
            reply = self.mainline.copy().message(reply)

        return self.cast(MessageTrait).send(message, reply=reply)

    # TODO: more shortcuts, like `accept_request` etc.

    @overload
    async def check(self) -> None:
        # 检查 Relationship 的存在性.
        # 如 Relationship 的存在性无法被验证为真, 则 Relationship 不成立, 抛出错误.
        ...

    @overload
    async def check(self, target: Selector, strict: bool = False) -> bool:
        # 检查 target 相对于当前关系 Relationship 的存在性.
        # 注意, 这里是 "相对于当前关系", 如 Github 的项目若为 Private, 则对于外界/Amonymous来说是不存在的, 即使他从客观上是存在的.
        # 注意, target 不仅需要相对于当前关系是存在的, 由于关系本身处在一个 mainline 之中,
        # mainline 相当于工作目录或者是 docker 那样的应用容器, 后者是更严谨的比喻,
        # 因为有些操作**只能**在处于一个特定的 mainline 中才能完成, 这其中包含了访问并操作某些 target.
        # 在 strict 模式下, target 被视作包含 "仅在当前 mainline 中才能完成的操作" 的集合中,
        # 表示其访问或是操作必须以当前 mainline 甚至是 current(account) 为基础.
        # 如果存在可能的 via, 则会先检查 via 的存在性, 因为 via 是维系这段关系的基础.
        ...

    async def check(self, target: Selector | None = None, strict: bool = False) -> bool | None:
        ...


"""
    @overload
    async def meta(self, operator: type[_M], /, *, flush: bool = False) -> _M:
        ...

    @overload
    async def meta(self, target: Any, operator: type[_M], /, *, flush: bool = False) -> _M:
        ...

    @overload
    async def meta(self, operator: CellOf[Unpack[tuple[Any, ...]], _M], /, *, flush: bool = False) -> _M:
        ...

    @overload
    async def meta(self, target: Any, operator: CellOf[Unpack[tuple[Any, ...]], _M], /, *, flush: bool = False) -> _M:
        ...

    @overload
    async def meta(self, operator: CellCompose[Unpack[Ts]], /, *, flush: bool = False) -> tuple[Unpack[Ts]]:
        ...

    @overload
    async def meta(
        self, target: Any, operator: CellCompose[Unpack[Ts]], /, *, flush: bool = False
    ) -> tuple[Unpack[Ts]]:
        ...

    # TODO: use the model of rs.exec to implement `rs.fn`
    async def meta(self, op_or_target: Any, maybe_op: Any = None, /, *, flush: bool = False) -> Any:
        op, target = cast(
            tuple["type[_M] | CellOf[Unpack[tuple[Any, ...]], _M]", Any],
            (op_or_target, None) if maybe_op is None else (maybe_op, op_or_target),
        )
        with ctx_relationship.use(self):
            if isinstance(op, (CellOf, CellCompose)) or isinstance(op, type) and issubclass(op, Cell):
                modify = None
                model = op
            elif isinstance(op, MetadataModifies):
                modify = op
                model = op.model
            else:
                raise TypeError(f"{op_or_target} & {maybe_op} is not a supported metadata operation for rs.meta.")

            target = target or model.get_default_target(self)

            if target is None:
                raise ValueError(
                    f"{model}'s modify is not a supported metadata for rs.meta, which requires a categorical target."
                )
            if result := self.cache.get("meta", {}).get(target, {}).get(op, None):
                if flush:
                    del self.cache["meta"][target][op]
                elif not model.has_params():
                    return result
            if isinstance(target, Selector):
                if isinstance(target, DynamicSelector):
                    raise TypeError(f"Use rs.query for dynamic selector {target}!")
                target_ref = target
            elif not isinstance(target, Selectable):
                raise ValueError(f"{target} is not a supported target for rs.meta, which requires to be selectable.")
            else:
                target_ref = target.to_selector()
            if isinstance(target, Resource):
                provider = get_provider(target, self)
                if provider is None:
                    raise ValueError(f"cannot find a valid provider for resource {target} to use rs.meta")
                source = provider.get_metadata_source()
            else:
                source = self.protocol.get_metadata_provider(target_ref)

            if source is None:
                if modify is None:
                    raise ValueError(
                        f"{model} is not a supported metadata at present, which not ordered by any source."
                    )
                raise ValueError(
                    f"{model}'s modify is not a supported metadata at present, which not ordered by any source."
                )

            if modify is None:
                result = await source.fetch(target, model)
                model.clear_params()
                self.cache.setdefault("meta", {}).setdefault(target, {})[op] = result
                return result
            return await source.modify(target, cast(MetadataModifies[Selector], modify))
"""
