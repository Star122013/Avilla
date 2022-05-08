from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from avilla.core.metadata.model import Metadata, meta_field

if TYPE_CHECKING:
    from avilla.core.relationship import Relationship
    from avilla.core.resource import Resource


class Mainline(Metadata):
    name: str = meta_field("mainline.name")
    description: str = meta_field("mainline.description")
    avatar: Resource = meta_field("mainline.avatar")
    max_count: int | None = meta_field("mainline.max_count")
    current_count: int | None = meta_field("mainline.current_count")

    @classmethod
    def default_target_by_relationship(cls, relationship: Relationship):
        return relationship.mainline

class Contact(Metadata):
    name: str = meta_field("contact.name")
    nickname: str = meta_field("contact.nickname")
    avatar: Resource = meta_field("contact.avatar")

    @classmethod
    def default_target_by_relationship(cls, relationship: Relationship):
        return relationship.current


class Member(Contact, Metadata):
    budget: str = meta_field("member.budget")
    muted: bool = meta_field("member.muted")
    joined_at: datetime | None = meta_field("member.joined_at")
    last_active_at: datetime | None = meta_field("member.last_active_at")

    @classmethod
    def default_target_by_relationship(cls, relationship: Relationship):
        return relationship.ctx


class Request(Metadata):
    comment: str | None = meta_field("request.comment")
    reason: str | None = meta_field("request.reason")
    has_question: bool = meta_field("request.has_question")
    questions: dict[int, str] | None = meta_field("request.questions")
    answers: dict[int, str] | None = meta_field("request.answers")

    @property
    def qa(self) -> dict[str, str] | None:
        if self.questions is None or self.answers is None:
            return None
        return {question: self.answers[index] for index, question in self.questions.items()}

    @classmethod
    def default_target_by_relationship(cls, relationship: Relationship):
        return relationship.ctx

class Self(Contact, Metadata):
    muted: bool = meta_field("self.muted")
    mute_period: int | None = meta_field("self.mute_period")
    budget: str = meta_field("self.budget")
    joined_at: datetime | None = meta_field("self.joined_at")
    last_active_at: datetime | None = meta_field("self.last_active_at")

    @classmethod
    def default_target_by_relationship(cls, relationship: Relationship):
        return relationship.current