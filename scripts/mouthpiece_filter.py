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
        analysis = {
            "intent": self._detect_intent(text),
            "concepts": self._extract_concepts(text),
            "metaphors": self._extract_metaphors(text) if self.config["extract_metaphors"] else [],
            "tone": self._detect_tone(text),
            "complexity": self._assess_complexity(text),
            "key_verbs": self._extract_key_verbs(text),
            "questions": self._extract_questions(text),
        }
        return analysis

    def _detect_intent(self, text: str) -> str:
        """Detect the primary intent of the text."""
        text_lower = text.lower()

        # Intent patterns
        if any(word in text_lower for word in ["create", "build", "implement", "make", "develop"]):
            return "creation"
        elif any(word in text_lower for word in ["fix", "repair", "solve", "debug", "resolve"]):
            return "problem_solving"
        elif any(word in text_lower for word in ["explain", "understand", "learn", "how", "why", "what"]):
            return "understanding"
        elif any(word in text_lower for word in ["improve", "optimize", "enhance", "better", "refactor"]):
            return "improvement"
        elif any(word in text_lower for word in ["design", "architect", "plan", "structure"]):
            return "design"
        elif any(word in text_lower for word in ["analyze", "review", "examine", "inspect"]):
            return "analysis"
        else:
            return "general"

    def _extract_concepts(self, text: str) -> List[str]:
        """Extract key concepts from the text."""
        # Simple concept extraction - looks for capitalized words, quoted terms, and technical terms
        concepts = []

        # Capitalized words (potential proper nouns or important concepts)
        concepts.extend(re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text))

        # Quoted terms
        concepts.extend(re.findall(r'"([^"]+)"', text))
        concepts.extend(re.findall(r"'([^']+)'", text))

        # Technical-looking terms (contains underscores, dots, or mixed case)
        concepts.extend(re.findall(r'\b\w+[._]\w+\b', text))
        concepts.extend(re.findall(r'\b[a-z]+[A-Z]\w+\b', text))  # camelCase

        return list(set(concepts))  # Remove duplicates

    def _extract_metaphors(self, text: str) -> List[str]:
        """Extract metaphorical language that adds color and meaning."""
        # Pattern words that often indicate metaphorical language
        metaphor_indicators = [
            "like", "as if", "seems", "feels like", "reminds me of",
            "poetry", "blossomed", "flowers", "blooms", "seeds",
            "river", "ocean", "mountain", "storm", "light", "shadow"
        ]

        metaphors = []
        sentences = re.split(r'[.!?]+', text)

        for sentence in sentences:
            if any(indicator in sentence.lower() for indicator in metaphor_indicators):
                metaphors.append(sentence.strip())

        return metaphors

    def _detect_tone(self, text: str) -> str:
        """Detect the emotional tone of the text."""
        text_lower = text.lower()

        # Simple tone detection
        if any(word in text_lower for word in ["urgent", "immediately", "asap", "critical", "emergency"]):
            return "urgent"
        elif any(word in text_lower for word in ["please", "could you", "would you", "kindly"]):
            return "polite"
        elif any(word in text_lower for word in ["excited", "amazing", "wonderful", "love", "great"]):
            return "enthusiastic"
        elif any(word in text_lower for word in ["confused", "unclear", "not sure", "maybe", "perhaps"]):
            return "uncertain"
        else:
            return "neutral"

    def _assess_complexity(self, text: str) -> str:
        """Assess the complexity level of the request."""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)

        avg_sentence_length = len(words) / max(len(sentences), 1)

        if avg_sentence_length > 20 or len(self._extract_concepts(text)) > 5:
            return "complex"
        elif avg_sentence_length > 10:
            return "moderate"
        else:
            return "simple"

    def _extract_key_verbs(self, text: str) -> List[str]:
        """Extract action verbs that indicate what should be done."""
        # Common action verbs in technical contexts
        action_verbs = [
            "create", "build", "implement", "develop", "design",
            "fix", "solve", "debug", "repair", "resolve",
            "optimize", "improve", "enhance", "refactor",
            "analyze", "review", "examine", "test",
            "explain", "describe", "document", "clarify",
            "integrate", "connect", "combine", "merge",
            "transform", "convert", "translate", "filter",
        ]

        found_verbs = []
        text_lower = text.lower()

        for verb in action_verbs:
            if verb in text_lower:
                found_verbs.append(verb)

        return found_verbs

    def _extract_questions(self, text: str) -> List[str]:
        """Extract questions from the text."""
        # Find sentences ending with question marks
        questions = re.findall(r'([^.!?]*\?)', text)
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
        context_indicators = ["background", "context", "currently", "existing", "we have", "i have"]
        return any(indicator in text.lower() for indicator in context_indicators)

    def _has_constraints(self, text: str) -> bool:
        """Check if the text specifies constraints."""
        constraint_indicators = ["must", "should", "need to", "required", "constraint", "limitation"]
        return any(indicator in text.lower() for indicator in constraint_indicators)

    def _has_examples(self, text: str) -> bool:
        """Check if the text includes examples."""
        example_indicators = ["example", "for instance", "such as", "like", "e.g.", "i.e."]
        return any(indicator in text.lower() for indicator in example_indicators)

    def _has_steps(self, text: str) -> bool:
        """Check if the text contains step-by-step information."""
        # Look for numbered lists or step indicators
        return bool(re.search(r'\b(?:step\s+)?\d+[\.:)]|\bfirst\b|\bsecond\b|\bthen\b|\bfinally\b', text.lower()))

    def _identify_sections(self, text: str) -> List[str]:
        """Identify logical sections in the text."""
        sections = []

        # Split by double newlines or paragraph indicators
        paragraphs = re.split(r'\n\s*\n', text)

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

    def _build_structured_prompt(self, text: str, analysis: Dict, structure: Dict) -> str:
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
            prompt_parts.append(f"_\"{analysis['metaphors'][0]}\"_\n" if analysis["metaphors"] else "")
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
        sentences = re.split(r'[.!?]+', text)
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
                output.append(f"  Concepts found: {result['metadata']['concept_count']}")
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
        """
    )

    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("text", nargs="?", help="Text to transform")
    input_group.add_argument("--file", "-f", help="Read text from file")
    input_group.add_argument("--stdin", action="store_true", help="Read from stdin")

    # Configuration options
    parser.add_argument("--config", "-c", help="Path to config JSON file")
    parser.add_argument("--format", choices=["full", "prompt_only", "json"],
                       default="full", help="Output format")
    parser.add_argument("--no-poetry", action="store_true",
                       help="Don't preserve poetic elements")
    parser.add_argument("--no-voice", action="store_true",
                       help="Don't maintain original voice")
    parser.add_argument("--output", "-o", help="Write output to file")

    args = parser.parse_args()

    # Get input text
    if args.text:
        text = args.text
    elif args.file:
        with open(args.file, 'r') as f:
            text = f.read()
    elif args.stdin:
        text = sys.stdin.read()

    # Load configuration
    config = None
    if args.config:
        with open(args.config, 'r') as f:
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
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Output written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
