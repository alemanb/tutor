"""Line Explainer Agent - Agent 2 in the Educational Multi-Agent System.

This agent provides line-by-line educational explanations of generated code.
It outputs explanations in the format specified in docs/ai_agent_json_format/2.json.
"""

from agno.agent import Agent, RunOutput
from agno.models.anthropic import Claude
from ..models.schemas import CodeGenerationOutput, LineExplanationOutput, CodeLine


class LineExplainerAgent:
    """Agent that provides line-by-line educational explanations.

    This agent takes generated code and breaks it down into individual lines,
    providing clear, beginner-friendly explanations for each line. Blank lines
    receive null explanations as per the 2.json format specification.

    Attributes:
        agent: The underlying Agno Agent instance
        model_id: Claude model identifier (default: claude-sonnet-4-20250514)
    """

    def __init__(self, model_id: str = "claude-sonnet-4-20250514"):
        """Initialize the Line Explainer Agent.

        Args:
            model_id: Claude model identifier to use for explanations
        """
        self.model_id = model_id
        self.agent = Agent(
            id="line-explainer",
            name="Line Explainer",
            model=Claude(id=model_id),
            description="You are an educational code explainer that provides line-by-line explanations.",
            instructions=[
                "Explain each line of code from a teaching perspective.",
                "For blank lines (empty or only whitespace), set line_explanation to null.",
                "Provide clear, beginner-friendly explanations that focus on the 'why' not just the 'what'.",
                "Break down complex concepts into simple terms.",
                "Include an overall explanation of what the entire code does.",
                "Maintain the exact line numbers and code as provided.",
                "Ensure explanations are educational and help learners understand the code.",
            ],
            markdown=False,  # We want structured output
            output_schema=LineExplanationOutput,
        )

    def explain_code(self, code_output: CodeGenerationOutput) -> LineExplanationOutput:
        """Split code into lines and provide educational explanations synchronously.

        Args:
            code_output: CodeGenerationOutput from the Code Generator Agent

        Returns:
            LineExplanationOutput matching the 2.json format with line-by-line explanations

        Raises:
            Exception: If explanation generation fails
        """
        prompt = self._build_prompt(code_output)

        try:
            # Run the agent and get structured output
            response: RunOutput = self.agent.run(prompt)

            # Extract the content
            if isinstance(response.content, LineExplanationOutput):
                output = response.content
            else:
                output = LineExplanationOutput(**response.content)

            # Preserve date and language from code generation
            output.date = code_output.date
            output.language = code_output.language

            return output

        except Exception as e:
            raise Exception(f"Line explanation failed: {str(e)}")

    async def aexplain_code(self, code_output: CodeGenerationOutput) -> LineExplanationOutput:
        """Split code into lines and provide educational explanations asynchronously.

        Args:
            code_output: CodeGenerationOutput from the Code Generator Agent

        Returns:
            LineExplanationOutput matching the 2.json format with line-by-line explanations

        Raises:
            Exception: If explanation generation fails
        """
        prompt = self._build_prompt(code_output)

        try:
            # Run the agent asynchronously
            response: RunOutput = await self.agent.arun(prompt)

            # Extract the content
            if isinstance(response.content, LineExplanationOutput):
                output = response.content
            else:
                output = LineExplanationOutput(**response.content)

            # Preserve date and language from code generation
            output.date = code_output.date
            output.language = code_output.language

            return output

        except Exception as e:
            raise Exception(f"Async line explanation failed: {str(e)}")

    def _build_prompt(self, code_output: CodeGenerationOutput) -> str:
        """Build the prompt for Claude to explain code line-by-line.

        Args:
            code_output: CodeGenerationOutput containing the code to explain

        Returns:
            Formatted prompt string for the agent
        """
        # Split code into lines for analysis
        lines = code_output.code.split('\n')

        prompt_parts = [
            f"Analyze this {code_output.language} code and provide line-by-line educational explanations:",
            "",
            "Code to explain:",
            "```" + code_output.language,
            code_output.code,
            "```",
            "",
            "For each line of code:",
            "1. Identify the line number (starting from 1)",
            "2. Extract the exact code from that line",
            "3. Provide an educational explanation (or null for blank/empty lines)",
            "",
            "Important guidelines:",
            "- Blank lines or lines with only whitespace should have line_explanation set to null",
            "- Explain WHY the code does something, not just WHAT it does",
            "- Use beginner-friendly language",
            "- Break down complex concepts into simple terms",
            "- Focus on teaching and helping learners understand",
            "",
            "Also provide an overall explanation of what the entire code does.",
            "",
            f"The code has {len(lines)} line(s) total.",
        ]

        return "\n".join(prompt_parts)

    def __repr__(self) -> str:
        """String representation of the agent."""
        return f"LineExplainerAgent(model_id='{self.model_id}')"
