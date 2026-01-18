#!/usr/bin/env python3
"""
Mouthpiece Filter System
========================

Transforms natural, human writing into polished AI prompts while preserving
the essence and poetry of the original expression.

This filter allows you to write in your natural voice - with all its imperfections,
metaphors, and humanity - and transforms it into structured prompts optimized for
AI interaction.

Usage:
    python mouthpiece_filter.py "your natural writing here"
    python mouthpiece_filter.py --file input.txt
    echo "your text" | python mouthpiece_filter.py --stdin
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class MouthpieceFilter:
    """
    The Mouthpiece Filter transforms natural human writing into AI-optimized prompts.

    It analyzes:
    - Intent and purpose
    - Key concepts and requirements
    - Context and constraints
    - Desired outcomes

    And produces structured prompts that maintain the human voice while
    optimizing for AI comprehension.
    """

    # Pre-compiled patterns for performance

    # Capitalized words (potential proper nouns or important concepts)
    _CAPITALIZED_WORDS = re.compile(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b")

    # Quoted terms
    _QUOTED_DOUBLE = re.compile(r'"([^"]+)"')
    _QUOTED_SINGLE = re.compile(r"'([^']+)'")

    # Technical-looking terms (contains underscores, dots, or mixed case)
    # Combined for efficiency
    _TECHNICAL_TERMS = re.compile(r"\b\w+[._]\w+\b|\b[a-z]+[A-Z]\w+\b")

    _METAPHOR_INDICATORS = [
        "like",
        "as if",
        "seems",
        "feels like",
        "reminds me of",
        "poetry",
        "blossomed",
        "flowers",
        "blooms",
        "seeds",
        "river",
        "ocean",
        "mountain",
        "storm",
        "light",
        "shadow",
    ]
    _METAPHOR_PATTERN = re.compile(
        r"|".join(map(re.escape, _METAPHOR_INDICATORS)), re.IGNORECASE
    )

    _SENTENCE_SPLIT = re.compile(r"[.!?]+")
    _QUESTIONS_PATTERN = re.compile(r"([^.!?]*\?)")
    _STEPS_PATTERN = re.compile(
        r"\b(?:step\s+)?\d+[\.:)]|\bfirst\b|\bsecond\b|\bthen\b|\bfinally\b",
        re.IGNORECASE,
    )
    _PARAGRAPH_SPLIT = re.compile(r"\n\s*\n")

    # Intent patterns (Priority Ordered)
    # Note: Removed \b to match original 'in' behavior and capture variations like "creating"
    _INTENT_PATTERNS = [
        ("creation", re.compile(r"(?:create|build|implement|make|develop)", re.IGNORECASE)),
        ("problem_solving", re.compile(r"(?:fix|repair|solve|debug|resolve)", re.IGNORECASE)),
        ("understanding", re.compile(r"(?:explain|understand|learn|how|why|what)", re.IGNORECASE)),
        ("improvement", re.compile(r"(?:improve|optimize|enhance|better|refactor)", re.IGNORECASE)),
        ("design", re.compile(r"(?:design|architect|plan|structure)", re.IGNORECASE)),
        ("analysis", re.compile(r"(?:analyze|review|examine|inspect)", re.IGNORECASE)),
    ]

    # Tone patterns (Priority Ordered)
    _TONE_PATTERNS = [
        ("urgent", re.compile(r"(?:urgent|immediately|asap|critical|emergency)", re.IGNORECASE)),
        ("polite", re.compile(r"(?:please|could you|would you|kindly)", re.IGNORECASE)),
        ("enthusiastic", re.compile(r"(?:excited|amazing|wonderful|love|great)", re.IGNORECASE)),
        ("uncertain", re.compile(r"(?:confused|unclear|not sure|maybe|perhaps)", re.IGNORECASE)),
    ]

    # Action verbs pattern
    _ACTION_VERBS = [
        "create", "build", "implement", "develop", "design", "fix", "solve", "debug",
        "repair", "resolve", "optimize", "improve", "enhance", "refactor", "analyze",
        "review", "examine", "test", "explain", "describe", "document", "clarify",
        "integrate", "connect", "combine", "merge", "transform", "convert",
        "translate", "filter"
    ]

    # Context indicators
    _CONTEXT_INDICATORS = re.compile(r"(?:background|context|currently|existing|we have|i have)", re.IGNORECASE)

    # Constraint indicators
    _CONSTRAINT_INDICATORS = re.compile(r"(?:must|should|need to|required|constraint|limitation)", re.IGNORECASE)

    # Example indicators
    _EXAMPLE_INDICATORS = re.compile(r"(?:example|for instance|such as|like|e\.g\.|i\.e\.)", re.IGNORECASE)

    def __init__(self, config: Optional[Dict] = None):
        """Initialize the filter with optional configuration."""
        self.config = config or self._default_config()

    def _default_config(self) -> Dict:
        """Default configuration for the filter."""
        return {
            "preserve_poetry": True,
            "extract_metaphors": True,
            "maintain_voice": True,
            "output_format": "structured",  # structured, markdown, json
            "include_analysis": True,
            "style": "conversational",  # conversational, technical, hybrid
        }

    def transform(self, text: str) -> Dict[str, any]:
        """
        Transform natural text into an AI prompt.

        Args:
            text: Natural, human writing to transform

        Returns:
            Dictionary containing the transformed prompt and metadata
        """
        # Analyze the input
        analysis = self._analyze_text(text)

        # Extract structure
        structure = self._extract_structure(text, analysis)

        # Build the prompt
        prompt = self._build_prompt(text, analysis, structure)

        # Create metadata
        metadata = self._create_metadata(text, analysis)

        return {
            "original": text,
            "prompt": prompt,
            "analysis": analysis if self.config["include_analysis"] else None,
            "metadata": metadata,
            "structure": structure,
        }

    def _analyze_text(self, text: str) -> Dict[str, any]:
        """Analyze the text to understand intent and content."""
        # Calculate concepts once to reuse in complexity assessment
        concepts = self._extract_concepts(text)

        analysis = {
            "intent": self._detect_intent(text),
            "concepts": concepts,
            "metaphors": (
                self._extract_metaphors(text)
                if self.config["extract_metaphors"]
                else []
            ),
            "tone": self._detect_tone(text),
            "complexity": self._assess_complexity(text, concepts),
            "key_verbs": self._extract_key_verbs(text),
            "questions": self._extract_questions(text),
        }
        return analysis

    def _detect_intent(self, text: str) -> str:
        """Detect the primary intent of the text."""
        for intent, pattern in self._INTENT_PATTERNS:
            if pattern.search(text):
                return intent
        return "general"

    def _extract_concepts(self, text: str) -> List[str]:
        """Extract key concepts from the text."""
        # Simple concept extraction - looks for capitalized words, quoted terms, and technical terms
        concepts = []

        # Optimization: Use pre-compiled regex patterns
        # Capitalized words (potential proper nouns or important concepts)
        concepts.extend(self._CAPITALIZED_WORDS.findall(text))

        # Quoted terms
        concepts.extend(self._QUOTED_DOUBLE.findall(text))
        concepts.extend(self._QUOTED_SINGLE.findall(text))

        # Technical-looking terms (contains underscores, dots, or mixed case)
        concepts.extend(self._TECHNICAL_TERMS.findall(text))

        return sorted(list(set(concepts)))  # Remove duplicates and sort for determinism

    def _extract_metaphors(self, text: str) -> List[str]:
        """Extract metaphorical language that adds color and meaning."""
        metaphors = []
        sentences = self._SENTENCE_SPLIT.split(text)

        for sentence in sentences:
            if self._METAPHOR_PATTERN.search(sentence):
                metaphors.append(sentence.strip())

        return metaphors

    def _detect_tone(self, text: str) -> str:
        """Detect the emotional tone of the text."""
        for tone, pattern in self._TONE_PATTERNS:
            if pattern.search(text):
                return tone
        return "neutral"

    def _assess_complexity(self, text: str, concepts: List[str] = None) -> str:
        """Assess the complexity level of the request."""
        words = text.split()
        sentences = self._SENTENCE_SPLIT.split(text)

        avg_sentence_length = len(words) / max(len(sentences), 1)

        # Use provided concepts or extract if not provided
        if concepts is None:
            concepts = self._extract_concepts(text)

        if avg_sentence_length > 20 or len(concepts) > 5:
            return "complex"
        elif avg_sentence_length > 10:
            return "moderate"
        else:
            return "simple"

    def _extract_key_verbs(self, text: str) -> List[str]:
        """Extract action verbs that indicate what should be done."""
        found_verbs = []
        for verb in self._ACTION_VERBS:
            if re.search(verb, text, re.IGNORECASE):
                found_verbs.append(verb)
        return found_verbs

    def _extract_questions(self, text: str) -> List[str]:
        """Extract questions from the text."""
        # Find sentences ending with question marks
        questions = self._QUESTIONS_PATTERN.findall(text)
        return [q.strip() for q in questions if q.strip()]

    def _extract_structure(self, text: str, analysis: Dict) -> Dict[str, any]:
        """Extract structural elements from the text."""
        structure = {
            "has_context": self._has_context(text),
            "has_constraints": self._has_constraints(text),
            "has_examples": self._has_examples(text),
            "has_steps": self._has_steps(text),
            "sections": self._identify_sections(text),
        }
        return structure

    def _has_context(self, text: str) -> bool:
        """Check if the text provides context."""
        return bool(self._CONTEXT_INDICATORS.search(text))

    def _has_constraints(self, text: str) -> bool:
        """Check if the text specifies constraints."""
        return bool(self._CONSTRAINT_INDICATORS.search(text))

    def _has_examples(self, text: str) -> bool:
        """Check if the text includes examples."""
        return bool(self._EXAMPLE_INDICATORS.search(text))

    def _has_steps(self, text: str) -> bool:
        """Check if the text contains step-by-step information."""
        # Look for numbered lists or step indicators
        return bool(self._STEPS_PATTERN.search(text))

    def _identify_sections(self, text: str) -> List[str]:
        """Identify logical sections in the text."""
        sections = []

        # Split by double newlines or paragraph indicators
        paragraphs = self._PARAGRAPH_SPLIT.split(text)

        for i, para in enumerate(paragraphs):
            if para.strip():
                sections.append(f"section_{i + 1}")

        return sections

    def _build_prompt(self, text: str, analysis: Dict, structure: Dict) -> str:
        """Build the optimized AI prompt from the analyzed text."""

        if self.config["output_format"] == "json":
            return self._build_json_prompt(text, analysis, structure)
        elif self.config["output_format"] == "markdown":
            return self._build_markdown_prompt(text, analysis, structure)
        else:
            return self._build_structured_prompt(text, analysis, structure)

    def _build_structured_prompt(
        self, text: str, analysis: Dict, structure: Dict
    ) -> str:
        """Build a structured prompt format."""
        prompt_parts = []

        # Title based on intent
        intent_titles = {
            "creation": "Create",
            "problem_solving": "Solve",
            "understanding": "Explain",
            "improvement": "Improve",
            "design": "Design",
            "analysis": "Analyze",
            "general": "Process",
        }
        title = intent_titles.get(analysis["intent"], "Process")

        # Header
        if self.config["preserve_poetry"] and analysis["metaphors"]:
            prompt_parts.append(f"# {title}: {text.split('.')[0].strip()}...\n")
            prompt_parts.append(
                f"_\"{analysis['metaphors'][0]}\"_\n" if analysis["metaphors"] else ""
            )
        else:
            prompt_parts.append(f"# {title}\n")

        # Main objective
        prompt_parts.append("## Objective\n")
        prompt_parts.append(f"{self._extract_main_objective(text, analysis)}\n")

        # Key requirements
        if analysis["key_verbs"]:
            prompt_parts.append("\n## Requirements\n")
            for verb in analysis["key_verbs"][:5]:  # Top 5 verbs
                prompt_parts.append(f"- {verb.capitalize()} the relevant components\n")

        # Concepts and context
        if analysis["concepts"]:
            prompt_parts.append("\n## Key Concepts\n")
            for concept in analysis["concepts"][:7]:  # Top 7 concepts
                prompt_parts.append(f"- {concept}\n")

        # Questions to address
        if analysis["questions"]:
            prompt_parts.append("\n## Questions to Address\n")
            for question in analysis["questions"]:
                prompt_parts.append(f"- {question}\n")

        # Preserve human voice
        if self.config["maintain_voice"]:
            prompt_parts.append("\n## Original Expression\n")
            prompt_parts.append(f"> {text}\n")

        return "".join(prompt_parts)

    def _build_markdown_prompt(self, text: str, analysis: Dict, structure: Dict) -> str:
        """Build a markdown-formatted prompt."""
        return self._build_structured_prompt(text, analysis, structure)

    def _build_json_prompt(self, text: str, analysis: Dict, structure: Dict) -> str:
        """Build a JSON-formatted prompt."""
        prompt_data = {
            "intent": analysis["intent"],
            "objective": self._extract_main_objective(text, analysis),
            "requirements": analysis["key_verbs"],
            "concepts": analysis["concepts"],
            "questions": analysis["questions"],
            "tone": analysis["tone"],
            "complexity": analysis["complexity"],
            "original": text if self.config["maintain_voice"] else None,
        }
        return json.dumps(prompt_data, indent=2)

    def _extract_main_objective(self, text: str, analysis: Dict) -> str:
        """Extract the main objective from the text."""
        # Get the first sentence or up to first period
        sentences = self._SENTENCE_SPLIT.split(text)
        main_sentence = sentences[0].strip() if sentences else text

        # Clean it up
        main_sentence = main_sentence.strip()

        # If it's too short, add context from second sentence
        if len(main_sentence) < 20 and len(sentences) > 1:
            main_sentence += ". " + sentences[1].strip()

        return main_sentence

    def _create_metadata(self, text: str, analysis: Dict) -> Dict[str, any]:
        """Create metadata about the transformation."""
        return {
            "input_length": len(text),
            "word_count": len(text.split()),
            "intent": analysis["intent"],
            "tone": analysis["tone"],
            "complexity": analysis["complexity"],
            "has_metaphors": len(analysis.get("metaphors", [])) > 0,
            "concept_count": len(analysis["concepts"]),
        }

    def format_output(self, result: Dict, format_type: str = "full") -> str:
        """Format the result for display."""
        if format_type == "prompt_only":
            return result["prompt"]
        elif format_type == "json":
            return json.dumps(result, indent=2)
        else:  # full
            output = []
            output.append("=" * 80)
            output.append("MOUTHPIECE FILTER - TRANSFORMATION RESULT")
            output.append("=" * 80)
            output.append("")

            if result["metadata"]:
                output.append("Metadata:")
                output.append(f"  Intent: {result['metadata']['intent']}")
                output.append(f"  Tone: {result['metadata']['tone']}")
                output.append(f"  Complexity: {result['metadata']['complexity']}")
                output.append(
                    f"  Concepts found: {result['metadata']['concept_count']}"
                )
                output.append("")

            output.append("-" * 80)
            output.append("OPTIMIZED PROMPT:")
            output.append("-" * 80)
            output.append("")
            output.append(result["prompt"])
            output.append("")

            if result.get("analysis") and result["analysis"].get("metaphors"):
                output.append("-" * 80)
                output.append("PRESERVED POETRY:")
                output.append("-" * 80)
                for metaphor in result["analysis"]["metaphors"]:
                    output.append(f"  • {metaphor}")
                output.append("")

            output.append("=" * 80)

            return "\n".join(output)


def main():
    """Main CLI interface for the mouthpiece filter."""
    parser = argparse.ArgumentParser(
        description="Transform natural human writing into AI-optimized prompts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python mouthpiece_filter.py "build me a system to track stars"
  python mouthpiece_filter.py --file my_thoughts.txt
  echo "help me understand recursion" | python mouthpiece_filter.py --stdin
  python mouthpiece_filter.py "create magic" --format prompt_only
        """,
    )

    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("text", nargs="?", help="Text to transform")
    input_group.add_argument("--file", "-f", help="Read text from file")
    input_group.add_argument("--stdin", action="store_true", help="Read from stdin")

    # Configuration options
    parser.add_argument("--config", "-c", help="Path to config JSON file")
    parser.add_argument(
        "--format",
        choices=["full", "prompt_only", "json"],
        default="full",
        help="Output format",
    )
    parser.add_argument(
        "--no-poetry", action="store_true", help="Don't preserve poetic elements"
    )
    parser.add_argument(
        "--no-voice", action="store_true", help="Don't maintain original voice"
    )
    parser.add_argument("--output", "-o", help="Write output to file")

    args = parser.parse_args()

    # Get input text
    if args.text:
        text = args.text
    elif args.file:
        with open(args.file, "r") as f:
            text = f.read()
    elif args.stdin:
        text = sys.stdin.read()

    # Load configuration
    config = None
    if args.config:
        with open(args.config, "r") as f:
            config = json.load(f)
    else:
        config = {}

    # Apply CLI overrides
    if args.no_poetry:
        config["preserve_poetry"] = False
    if args.no_voice:
        config["maintain_voice"] = False

    # Create filter and transform
    filter = MouthpieceFilter(config)
    result = filter.transform(text)

    # Format output
    output = filter.format_output(result, args.format)

    # Write or print
    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Output written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
