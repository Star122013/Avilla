from __future__ import annotations

from typing import TYPE_CHECKING

from avilla.core.ryanvk.capability import Capability
from avilla.core.ryanvk.descriptor.pull import PullFn
from avilla.core.ryanvk.descriptor.query import QuerySchema
from avilla.core.ryanvk.descriptor.target import TargetFn

if TYPE_CHECKING:
    from avilla.core.context import Context
    from avilla.core.selector import Selector


class CoreCapability(Capability):
    pull = PullFn()
    query = QuerySchema()

    @TargetFn
    async def get_context(self, *, via: Selector | None = None) -> Context:
        ...
