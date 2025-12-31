"""Load and parse agent markdown files with YAML frontmatter."""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class AgentDefinition:
    """Represents a parsed agent definition."""

    path: Path
    name: str
    description: str
    agent_id: str
    agent_type: str
    version: str
    skills: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    knowledge: list[str] = field(default_factory=list)
    interactions: dict[str, Any] = field(default_factory=dict)
    body_content: str = ""
    raw_frontmatter: dict[str, Any] = field(default_factory=dict)


class AgentLoader:
    """Load agent definitions from markdown files."""

    # Regex to extract YAML frontmatter
    FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)

    def __init__(self, agents_dir: Path):
        """Initialize loader with agents directory.

        Args:
            agents_dir: Path to directory containing agent markdown files
        """
        self.agents_dir = Path(agents_dir)

    def load_agent(self, path: Path) -> AgentDefinition:
        """Load a single agent definition from markdown file.

        Args:
            path: Path to agent markdown file

        Returns:
            AgentDefinition with parsed frontmatter and body

        Raises:
            ValueError: If frontmatter is missing or invalid
        """
        content = path.read_text(encoding="utf-8")

        # Extract frontmatter and body
        match = self.FRONTMATTER_PATTERN.match(content)
        if not match:
            raise ValueError(f"No frontmatter found in {path}")

        frontmatter_text = match.group(1)
        body_content = match.group(2).strip()

        # Parse YAML frontmatter
        try:
            frontmatter = yaml.safe_load(frontmatter_text)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in {path}: {e}")

        if not isinstance(frontmatter, dict):
            raise ValueError(f"Frontmatter must be a dict in {path}")

        # Extract required fields with defaults
        return AgentDefinition(
            path=path,
            name=frontmatter.get("name", ""),
            description=frontmatter.get("description", ""),
            agent_id=frontmatter.get("agent_id", ""),
            agent_type=frontmatter.get("agent_type", ""),
            version=frontmatter.get("version", ""),
            skills=frontmatter.get("skills", []),
            tags=frontmatter.get("tags", []),
            knowledge=frontmatter.get("knowledge", []),
            interactions=frontmatter.get("interactions", {}),
            body_content=body_content,
            raw_frontmatter=frontmatter,
        )

    def load_all_agents(self) -> list[AgentDefinition]:
        """Load all agent definitions from agents directory.

        Returns:
            List of AgentDefinition objects

        Raises:
            ValueError: If agents_dir does not exist
        """
        if not self.agents_dir.exists():
            raise ValueError(f"Agents directory not found: {self.agents_dir}")

        agents = []
        for agent_file in self.agents_dir.rglob("*.md"):
            # Skip BASE-AGENT.md files (they are templates, not agents)
            if agent_file.name.startswith("BASE-AGENT"):
                continue

            try:
                agent = self.load_agent(agent_file)
                agents.append(agent)
            except ValueError as e:
                # Log but continue - some files may not be valid agents
                print(f"Warning: Skipping {agent_file}: {e}")
                continue

        return agents

    def get_agents_by_type(self, agent_type: str) -> list[AgentDefinition]:
        """Get all agents of a specific type.

        Args:
            agent_type: Agent type to filter by (e.g., 'engineer', 'qa', 'ops')

        Returns:
            List of AgentDefinition objects matching the type
        """
        all_agents = self.load_all_agents()
        return [agent for agent in all_agents if agent.agent_type == agent_type]
