from __future__ import annotations

from typing import TYPE_CHECKING

from avilla.core.ryanvk.collector.context import ContextCollector
from avilla.core.selector import Selector
from avilla.standard.core.message import MessageSend
from graia.amnesia.message import MessageChain
from avilla.core.ryanvk.staff import Staff

if TYPE_CHECKING:
    from ...account import OneBot11Account  # noqa
    from ...protocol import OneBot11Protocol  # noqa


class OneBot11MessageActionPerform((m := ContextCollector["OneBot11Protocol", "OneBot11Account"]())._):
    m.post_applying = True

    @MessageSend.send.collect(m, "land.group")
    async def send_group_message(
        self,
        target: Selector,
        message: MessageChain,
        *,
        reply: Selector | None = None,
    ) -> Selector:
        result = await self.account.call(
            "send_group_msg",
            {
                "group_id": int(target.pattern["group"]),
                "message": await Staff(self.account).serialize_message(message),
            },
        )
        if result is None:
            raise RuntimeError(f"Failed to send message to {target.pattern['group']}: {message}")
        return Selector().land(self.account.route["land"]).group(target.pattern["group"]).message(result["message_id"])