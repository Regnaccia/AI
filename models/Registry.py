from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field, ConfigDict


# ============================================================
# Helpers
# ============================================================

def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def utcnow() -> datetime:
    return datetime.utcnow()


# ============================================================
# Enums
# ============================================================

class ProjectStatus(str, Enum):
    INGEST_IN_PROGRESS = "ingest_in_progress"
    AWAITING_USER = "awaiting_user"
    PREANALYSIS_READY = "preanalysis_ready"
    IN_TECHNICAL_ANALYSIS = "in_technical_analysis"
    IN_EXECUTION = "in_execution"
    IN_REVIEW = "in_review"
    DONE = "done"
    BLOCKED = "blocked"


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    BLOCKED_BY_USER = "blocked_by_user"
    DONE = "done"
    CANCELLED = "cancelled"


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class QuestionTarget(str, Enum):
    USER = "user"
    INGEST_AGENT = "ingest_agent"
    TECHNICAL_AGENT = "technical_agent"
    ORCHESTRATOR = "orchestrator"
    UI_AGENT = "ui_agent"
    BACKEND_AGENT = "backend_agent"
    HARDWARE_AGENT = "hardware_agent"
    DEBUG_AGENT = "debug_agent"
    REVIEW_AGENT = "review_agent"


class AgentName(str, Enum):
    ORCHESTRATOR = "orchestrator"
    INGEST_AGENT = "ingest_agent"
    TECHNICAL_AGENT = "technical_agent"
    UI_AGENT = "ui_agent"
    BACKEND_AGENT = "backend_agent"
    HARDWARE_AGENT = "hardware_agent"
    DEBUG_AGENT = "debug_agent"
    REVIEW_AGENT = "review_agent"
    RESEARCH_AGENT = "research_agent"


class EventType(str, Enum):
    PROJECT_CREATED = "project_created"
    USER_PROMPT_RECEIVED = "user_prompt_received"
    INGEST_COMPLETED = "ingest_completed"
    USER_INPUT_REQUIRED = "user_input_required"
    USER_REPLY_RECEIVED = "user_reply_received"
    TASK_CREATED = "task_created"
    TASK_ASSIGNED = "task_assigned"
    TASK_UPDATED = "task_updated"
    TASK_COMPLETED = "task_completed"
    DECISION_RECORDED = "decision_recorded"
    ARTIFACT_CREATED = "artifact_created"


class DecisionStatus(str, Enum):
    PROPOSED = "proposed"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"


# ============================================================
# Core leaf models
# ============================================================

class ProjectMeta(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(default_factory=lambda: new_id("proj"))
    name: str
    status: ProjectStatus = ProjectStatus.INGEST_IN_PROGRESS
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)
    version: int = 1


class Intent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    primary_goal: str
    user_types: list[str] = Field(default_factory=list)
    expected_outcomes: list[str] = Field(default_factory=list)


class Scope(BaseModel):
    model_config = ConfigDict(extra="forbid")

    domains: list[str] = Field(default_factory=list)
    features_explicit: list[str] = Field(default_factory=list)
    features_implicit: list[str] = Field(default_factory=list)
    exclusions: list[str] = Field(default_factory=list)


class Ambiguity(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(default_factory=lambda: new_id("amb"))
    topic: str
    description: str
    severity: Priority = Priority.MEDIUM
    resolved: bool = False


class OpenQuestion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(default_factory=lambda: new_id("q"))
    related_to: str | None = None
    question: str
    target: QuestionTarget
    priority: Priority = Priority.MEDIUM
    answered: bool = False
    answer: str | None = None


class Assumption(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(default_factory=lambda: new_id("ass"))
    description: str
    confidence: Literal["low", "medium", "high"] = "medium"
    needs_confirmation: bool = True
    confirmed: bool = False


class Constraint(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(default_factory=lambda: new_id("con"))
    description: str
    source: Literal["user", "agent", "system"] = "user"


class Knowledge(BaseModel):
    model_config = ConfigDict(extra="forbid")

    entities_identified: list[str] = Field(default_factory=list)
    relationships: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class Task(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(default_factory=lambda: new_id("task"))
    type: str
    goal: str
    owner: AgentName
    status: TaskStatus = TaskStatus.TODO
    priority: Priority = Priority.MEDIUM

    depends_on: list[str] = Field(default_factory=list)
    blocked_by: list[str] = Field(default_factory=list)
    related_questions: list[str] = Field(default_factory=list)

    input_refs: list[str] = Field(default_factory=list)
    output_refs: list[str] = Field(default_factory=list)

    needs_user_input: bool = False
    handoff_target: AgentName | None = None

    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)


class UserInteractionState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pending_questions: list[str] = Field(default_factory=list)
    last_request_type: str | None = None
    last_request_at: datetime | None = None
    waiting_for_user: bool = False


class Event(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(default_factory=lambda: new_id("evt"))
    type: EventType
    timestamp: datetime = Field(default_factory=utcnow)
    actor: AgentName | Literal["user", "system"] = "system"
    related_task: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)


class Decision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(default_factory=lambda: new_id("dec"))
    title: str
    description: str
    status: DecisionStatus = DecisionStatus.PROPOSED
    made_by: AgentName | Literal["user", "system"]
    related_task: str | None = None
    created_at: datetime = Field(default_factory=utcnow)


class Artifact(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(default_factory=lambda: new_id("art"))
    kind: str
    title: str
    content_ref: str | None = None
    produced_by: AgentName
    related_task: str | None = None
    created_at: datetime = Field(default_factory=utcnow)


class AgentState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: AgentName
    active: bool = True
    current_task_id: str | None = None
    last_seen_at: datetime | None = None


# ============================================================
# Registry root
# ============================================================

class Registry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    project: ProjectMeta
    intent: Intent | None = None
    scope: Scope | None = None

    ambiguities: list[Ambiguity] = Field(default_factory=list)
    open_questions: list[OpenQuestion] = Field(default_factory=list)
    assumptions: list[Assumption] = Field(default_factory=list)
    constraints: list[Constraint] = Field(default_factory=list)
    knowledge: Knowledge = Field(default_factory=Knowledge)

    tasks: list[Task] = Field(default_factory=list)
    decisions: list[Decision] = Field(default_factory=list)
    artifacts: list[Artifact] = Field(default_factory=list)
    events: list[Event] = Field(default_factory=list)

    user_interaction: UserInteractionState = Field(default_factory=UserInteractionState)
    agents: list[AgentState] = Field(default_factory=list)

    # --------------------------------------------------------
    # Basic mutation helpers
    # --------------------------------------------------------

    def touch(self) -> None:
        self.project.updated_at = utcnow()
        self.project.version += 1

    def add_event(
        self,
        event_type: EventType,
        *,
        actor: AgentName | Literal["user", "system"] = "system",
        related_task: str | None = None,
        payload: dict[str, Any] | None = None,
    ) -> Event:
        event = Event(
            type=event_type,
            actor=actor,
            related_task=related_task,
            payload=payload or {},
        )
        self.events.append(event)
        self.touch()
        return event

    def add_ambiguity(
        self,
        *,
        topic: str,
        description: str,
        severity: Priority = Priority.MEDIUM,
    ) -> Ambiguity:
        ambiguity = Ambiguity(topic=topic, description=description, severity=severity)
        self.ambiguities.append(ambiguity)
        self.touch()
        return ambiguity

    def add_question(
        self,
        *,
        question: str,
        target: QuestionTarget,
        priority: Priority = Priority.MEDIUM,
        related_to: str | None = None,
    ) -> OpenQuestion:
        q = OpenQuestion(
            question=question,
            target=target,
            priority=priority,
            related_to=related_to,
        )
        self.open_questions.append(q)

        if target == QuestionTarget.USER:
            self.user_interaction.pending_questions.append(q.id)
            self.user_interaction.waiting_for_user = True
            self.user_interaction.last_request_type = "clarification"
            self.user_interaction.last_request_at = utcnow()
            self.project.status = ProjectStatus.AWAITING_USER

        self.touch()
        return q

    def add_task(
        self,
        *,
        type: str,
        goal: str,
        owner: AgentName,
        status: TaskStatus = TaskStatus.TODO,
        priority: Priority = Priority.MEDIUM,
        depends_on: list[str] | None = None,
        blocked_by: list[str] | None = None,
        related_questions: list[str] | None = None,
        needs_user_input: bool = False,
        handoff_target: AgentName | None = None,
    ) -> Task:
        task = Task(
            type=type,
            goal=goal,
            owner=owner,
            status=status,
            priority=priority,
            depends_on=depends_on or [],
            blocked_by=blocked_by or [],
            related_questions=related_questions or [],
            needs_user_input=needs_user_input,
            handoff_target=handoff_target,
        )
        self.tasks.append(task)
        self.touch()
        return task

    def answer_question(self, question_id: str, answer: str) -> OpenQuestion:
        question = self.get_question(question_id)
        question.answered = True
        question.answer = answer

        if question_id in self.user_interaction.pending_questions:
            self.user_interaction.pending_questions.remove(question_id)

        if not self.user_interaction.pending_questions:
            self.user_interaction.waiting_for_user = False
            if self.project.status == ProjectStatus.AWAITING_USER:
                self.project.status = ProjectStatus.INGEST_IN_PROGRESS

        self.touch()
        return question

    def get_question(self, question_id: str) -> OpenQuestion:
        for q in self.open_questions:
            if q.id == question_id:
                return q
        raise ValueError(f"Question not found: {question_id}")

    def get_task(self, task_id: str) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise ValueError(f"Task not found: {task_id}")

    def set_task_status(self, task_id: str, status: TaskStatus) -> Task:
        task = self.get_task(task_id)
        task.status = status
        task.updated_at = utcnow()
        self.touch()
        return task

    def register_agent(self, name: AgentName) -> AgentState:
        existing = next((a for a in self.agents if a.name == name), None)
        if existing:
            return existing

        agent_state = AgentState(name=name, last_seen_at=utcnow())
        self.agents.append(agent_state)
        self.touch()
        return agent_state

    def assign_task(self, task_id: str, owner: AgentName) -> Task:
        task = self.get_task(task_id)
        task.owner = owner
        task.updated_at = utcnow()

        agent = self.register_agent(owner)
        agent.current_task_id = task.id
        agent.last_seen_at = utcnow()

        self.touch()
        return task