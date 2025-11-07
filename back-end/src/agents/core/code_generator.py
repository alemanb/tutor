"""Code Generator Agent - Agent 1 in the Educational Multi-Agent System.

This agent is responsible for generating educational code based on user prompts.
It outputs code in the format specified in docs/ai_agent_json_format/1.json.
"""

from datetime import datetime
from agno.agent import Agent, RunOutput
from agno.models.anthropic import Claude
from ..models.schemas import CodeGenerationRequest, CodeGenerationOutput


class CodeGeneratorAgent:
    """Agent responsible for generating educational code based on user prompts.

    This agent uses Claude Sonnet 4.0 to generate clean, well-structured code
    that is suitable for educational purposes. The output matches the 1.json format.

    Attributes:
        agent: The underlying Agno Agent instance
        model_id: Claude model identifier (default: claude-sonnet-4-20250514)
    """

    def __init__(self, model_id: str = "claude-sonnet-4-20250514"):
        """Initialize the Code Generator Agent.

        Args:
            model_id: Claude model identifier to use for code generation
        """
        self.model_id = model_id
        self.agent = Agent(
            id="code-generator",
            name="Code Generator",
            model=Claude(id=model_id),
            description="You are an educational code generator that creates clean, well-structured code without any comments.",
            instructions=[
                "Generate clean, well-structured code based on user requests.",
                "IMPORTANT: Do NOT include any comments in the code. Generate only executable code.",
                "Do NOT use comment syntax like #, //, /* */, ---, or similar in any programming language.",
                "The code will be explained separately by another agent, so comments are not needed.",
                "Use \\n for line breaks and \\n\\n for blank lines in the generated code.",
                "Focus on educational clarity through clean code structure and meaningful variable/function names.",
                "Ensure the code is syntactically correct and follows language conventions.",
                "For educational purposes, prioritize readability through clear naming and structure.",
            ],
            markdown=False,  # We want structured output, not markdown
            output_schema=CodeGenerationOutput,
        )

    def generate_code(self, request: CodeGenerationRequest) -> CodeGenerationOutput:
        """Generate code synchronously based on user request.

        Args:
            request: CodeGenerationRequest with prompt, language, and optional context

        Returns:
            CodeGenerationOutput matching the 1.json format with date, language, and code

        Raises:
            Exception: If code generation fails or validation errors occur
        """
        current_date = datetime.now().isoformat()

        # Build the prompt for Claude
        prompt = self._build_prompt(request)

        try:
            # Run the agent and get structured output
            response: RunOutput = self.agent.run(prompt)

            # Extract the content (should be CodeGenerationOutput)
            if isinstance(response.content, CodeGenerationOutput):
                output = response.content
            else:
                # If response is a dict, convert to CodeGenerationOutput
                output = CodeGenerationOutput(**response.content)

            # Ensure date is set (in case model didn't include it)
            if not output.date:
                output.date = current_date

            # Ensure language matches request
            if output.language != request.language:
                output.language = request.language

            return output

        except Exception as e:
            raise Exception(f"Code generation failed: {str(e)}")

    async def agenerate_code(self, request: CodeGenerationRequest) -> CodeGenerationOutput:
        """Generate code asynchronously based on user request.

        Args:
            request: CodeGenerationRequest with prompt, language, and optional context

        Returns:
            CodeGenerationOutput matching the 1.json format with date, language, and code

        Raises:
            Exception: If code generation fails or validation errors occur
        """
        current_date = datetime.now().isoformat()

        # Build the prompt for Claude
        prompt = self._build_prompt(request)

        try:
            # Run the agent asynchronously and get structured output
            response: RunOutput = await self.agent.arun(prompt)

            # Extract the content (should be CodeGenerationOutput)
            if isinstance(response.content, CodeGenerationOutput):
                output = response.content
            else:
                # If response is a dict, convert to CodeGenerationOutput
                output = CodeGenerationOutput(**response.content)

            # Ensure date is set (in case model didn't include it)
            if not output.date:
                output.date = current_date

            # Ensure language matches request
            if output.language != request.language:
                output.language = request.language

            return output

        except Exception as e:
            raise Exception(f"Async code generation failed: {str(e)}")

    def _build_prompt(self, request: CodeGenerationRequest) -> str:
        """Build the prompt for Claude based on the request.

        Args:
            request: CodeGenerationRequest with prompt, language, and context

        Returns:
            Formatted prompt string for the agent
        """
        prompt_parts = [
            f"Generate {request.language} code for the following request:",
            "",
            request.prompt,
        ]

        if request.context:
            prompt_parts.extend([
                "",
                f"Additional context: {request.context}",
            ])

        prompt_parts.extend([
            "",
            "Important formatting requirements:",
            "- Use \\n for single line breaks",
            "- Use \\n\\n for blank lines (double line breaks)",
            "- Ensure code is syntactically correct and follows best practices",
            "- Include helpful comments for educational purposes",
            f"- Return valid {request.language} code only",
        ])

        return "\n".join(prompt_parts)

    def __repr__(self) -> str:
        """String representation of the agent."""
        return f"CodeGeneratorAgent(model_id='{self.model_id}')"
