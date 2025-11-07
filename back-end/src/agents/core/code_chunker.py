"""Code Chunker Agent - Agent 3 in the Educational Multi-Agent System.

This agent groups related code lines into logical chunks for better organization.
It outputs chunks in the format specified in docs/ai_agent_json_format/3.json.
"""

from agno.agent import Agent, RunOutput
from agno.models.anthropic import Claude
from ..models.schemas import LineExplanationOutput, CodeChunkOutput, CodeChunk


class CodeChunkerAgent:
    """Agent that groups related code lines into logical chunks.

    This agent analyzes the line-by-line breakdown and groups related lines
    into meaningful sections (e.g., imports, class definitions, methods, main logic).
    It provides explanations for why lines are grouped together.

    Attributes:
        agent: The underlying Agno Agent instance
        model_id: Claude model identifier (default: claude-sonnet-4-20250514)
    """

    def __init__(self, model_id: str = "claude-sonnet-4-20250514"):
        """Initialize the Code Chunker Agent.

        Args:
            model_id: Claude model identifier to use for chunking
        """
        self.model_id = model_id
        self.agent = Agent(
            id="code-chunker",
            name="Code Chunker",
            model=Claude(id=model_id),
            description="You are a code organization specialist that groups related code lines into logical chunks.",
            instructions=[
                "Group related lines of code into logical, cohesive chunks.",
                "Common groupings include: imports, class definitions, function definitions, main logic, etc.",
                "Each chunk should represent a complete, coherent concept or section.",
                "Provide clear explanations for why lines are grouped together.",
                "Preserve the overall code explanation from the line explainer.",
                "Ensure first_line and last_line accurately reflect the line range.",
                "Include the actual code content in line_code for each chunk.",
            ],
            markdown=False,  # We want structured output
            output_schema=CodeChunkOutput,
        )

    def chunk_code(self, line_output: LineExplanationOutput) -> CodeChunkOutput:
        """Group code lines into logical educational chunks synchronously.

        Args:
            line_output: LineExplanationOutput from the Line Explainer Agent

        Returns:
            CodeChunkOutput matching the 3.json format with logical code chunks

        Raises:
            Exception: If chunking fails
        """
        prompt = self._build_prompt(line_output)

        try:
            # Run the agent and get structured output
            response: RunOutput = self.agent.run(prompt)

            # Extract the content
            if isinstance(response.content, CodeChunkOutput):
                output = response.content
            else:
                output = CodeChunkOutput(**response.content)

            # Preserve metadata
            output.date = line_output.date
            output.language = line_output.language
            output.explanation = line_output.explanation

            return output

        except Exception as e:
            raise Exception(f"Code chunking failed: {str(e)}")

    async def achunk_code(self, line_output: LineExplanationOutput) -> CodeChunkOutput:
        """Group code lines into logical educational chunks asynchronously.

        Args:
            line_output: LineExplanationOutput from the Line Explainer Agent

        Returns:
            CodeChunkOutput matching the 3.json format with logical code chunks

        Raises:
            Exception: If chunking fails
        """
        prompt = self._build_prompt(line_output)

        try:
            # Run the agent asynchronously
            response: RunOutput = await self.agent.arun(prompt)

            # Extract the content
            if isinstance(response.content, CodeChunkOutput):
                output = response.content
            else:
                output = CodeChunkOutput(**response.content)

            # Preserve metadata
            output.date = line_output.date
            output.language = line_output.language
            output.explanation = line_output.explanation

            return output

        except Exception as e:
            raise Exception(f"Async code chunking failed: {str(e)}")

    def _build_prompt(self, line_output: LineExplanationOutput) -> str:
        """Build the prompt for Claude to chunk the code.

        Args:
            line_output: LineExplanationOutput containing line-by-line breakdown

        Returns:
            Formatted prompt string for the agent
        """
        # Build context from line explanations
        lines_context = []
        for line in line_output.code:
            explanation = line.line_explanation or "blank line"
            lines_context.append(
                f"Line {line.line}: {line.line_code} - {explanation}"
            )

        prompt_parts = [
            f"Group this {line_output.language} code into logical, educational chunks:",
            "",
            "Line-by-line breakdown:",
            *lines_context,
            "",
            "Overall code purpose:",
            line_output.explanation,
            "",
            "Grouping guidelines:",
            "- Group all related imports together",
            "- Keep class definitions and their methods together (or separate if large)",
            "- Group related function definitions",
            "- Separate main execution logic",
            "- Group related variable declarations or setup code",
            "- Each chunk should represent a complete concept",
            "",
            "For each chunk, specify:",
            "- first_line: starting line number (1-indexed)",
            "- last_line: ending line number (inclusive)",
            "- line_code: the actual code from first_line to last_line (preserve \\n line breaks)",
            "- line_explanation: why these lines are grouped together and what they accomplish",
            "",
            "Ensure chunks don't overlap and cover all lines sequentially.",
        ]

        return "\n".join(prompt_parts)

    def __repr__(self) -> str:
        """String representation of the agent."""
        return f"CodeChunkerAgent(model_id='{self.model_id}')"
