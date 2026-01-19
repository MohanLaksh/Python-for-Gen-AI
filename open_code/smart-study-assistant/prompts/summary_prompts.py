SUMMARIZER_SYSTEM_PROMPT = """You are an expert summarizer specializing in educational content. Your role is to condense information while retaining the most important concepts and relationships.

Your summaries should:
1. Capture the main ideas and key points
2. Maintain logical flow and coherence
3. Be significantly shorter than the original
4. Preserve critical details and relationships
5. Be easy to understand and review

Focus on clarity, conciseness, and completeness.
"""

SUMMARIZER_BULLET_TEMPLATE = """Summarize the following content about {topic} using bullet points.

Structure:
```markdown
# Summary of {topic}

## Key Points
- Main point 1
- Main point 2
- ...

## Important Details
- Important detail 1
- Important detail 2
- ...

## Key Takeaways
- Takeaway 1
- Takeaway 2
- ...
```

Content to summarize:
{content}
"""

SUMMARIZER_STUDY_GUIDE_TEMPLATE = """Create a study guide from the following content about {topic}.

Format as:
```markdown
# Study Guide: {topic}

## Overview
{Brief overview (2-3 sentences)}

## Key Concepts
{List 5-7 key concepts with brief explanations}

## Important Terms
{Define 5-10 important terms}

## Key Relationships
{Explain how concepts relate to each other}

## Summary Points
{3-5 summary bullets}

## Self-Check Questions
{3-5 questions to test understanding}
```

Content:
{content}
"""

SUMMARIZER_CONDENSED_TEMPLATE = """Create a highly condensed summary of the following content.

Aim for 20-25% of the original length while keeping:
- Main ideas
- Critical details
- Key relationships
- Important conclusions

Format:
```markdown
{Topic} Summary

{Condensed content in 1-2 paragraphs}
```

Content:
{content}
"""

SUMMARIZER_HIERARCHICAL_TEMPLATE = """Create a hierarchical summary of the following content using headings and subheadings.

Structure:
```markdown
# {Topic}

## Main Section 1
### Subsection
- Detail
- Detail

## Main Section 2
### Subsection
- Detail
- Detail
```

Content:
{content}
"""
