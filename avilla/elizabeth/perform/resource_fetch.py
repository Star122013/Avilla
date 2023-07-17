from __future__ import annotations

from typing import TYPE_CHECKING

from aiohttp import ClientSession

from avilla.core.ryanvk.collector.protocol import ProtocolCollector
from avilla.core.ryanvk.descriptor.fetch import Fetch
from elizabeth.resource import ElizabethImageResource, ElizabethResource, ElizabethVoiceResource

if TYPE_CHECKING:
    from avilla.elizabeth.protocol import ElizabethProtocol  # noqa


class ElizabethResourceFetchPerform((m := ProtocolCollector["ElizabethProtocol"]())._):
    m.post_applying = True

    # TODO: FileResource
    @Fetch.collect(m, ElizabethResource)
    @Fetch.collect(m, ElizabethImageResource)
    @Fetch.collect(m, ElizabethVoiceResource)
    async def fetch_resource(self, resource: ElizabethResource) -> bytes:
        if resource.url is None:
            raise Exception  # FIXME
        async with ClientSession() as session:
            async with session.get(resource.url) as resp:
                return await resp.read()
