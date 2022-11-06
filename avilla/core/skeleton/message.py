from __future__ import annotations

from graia.amnesia.message import MessageChain

from avilla.core.trait import Fn, Trait
from avilla.core.utilles.selector import Selector


# MessageFetch => rs.pull(Message, target=...)
class MessageSend(Trait):
    @Fn
    async def send(self, message: MessageChain, *, reply: Selector | None = None) -> Selector:
        ...


class MessageRevoke(Trait):
    @Fn
    async def revoke(self, message: Selector) -> None:
        ...


class MessageEdit(Trait):
    @Fn
    async def edit(self, message: Selector, content: MessageChain) -> None:
        ...
