# Jinja2 for Prompt Engineering
## A Comprehensive Guide for Gen AI Developers

---

## Table of Contents

1. [Introduction to Jinja2](#introduction-to-jinja2)
2. [Why Use Jinja2 for Prompts?](#why-use-jinja2-for-prompts)
3. [Jinja2 Basics](#jinja2-basics)
4. [Core Syntax and Features](#core-syntax-and-features)
5. [Prompt Engineering Patterns](#prompt-engineering-patterns)
6. [Advanced Techniques](#advanced-techniques)
7. [Best Practices](#best-practices)
8. [Complete Examples](#complete-examples)
9. [Real-World Use Cases](#real-world-use-cases)
10. [Troubleshooting](#troubleshooting)

---

## Introduction to Jinja2

Jinja2 is a powerful, modern templating engine for Python that allows you to generate dynamic text content. In the context of Gen AI development, Jinja2 is invaluable for creating reusable, maintainable, and flexible prompt templates.

Think of Jinja2 as a way to write prompts with placeholders that can be filled in programmatically, enabling you to create sophisticated prompt generation systems that scale across different use cases, users, and contexts.

### What Makes Jinja2 Ideal for Prompts?

- **Dynamic Content Generation**: Insert variables, conditionals, and loops into your prompts
- **Template Reusability**: Write once, use everywhere with different contexts
- **Separation of Concerns**: Keep prompt engineering separate from application logic
- **Version Control**: Track changes to prompts independently from code
- **Team Collaboration**: Non-developers can modify templates without touching code

---

## Why Use Jinja2 for Prompts?

### Key Benefits

**1. Reusability**
- Write once, use many times with different variables
- Create template libraries for common use cases
- Share templates across projects and teams

**2. Maintainability**
- Update prompts in one place instead of scattered throughout code
- Easier to test and iterate on prompt designs
- Clear separation between prompt logic and application code

**3. Dynamic Content**
- Conditionally include or exclude sections based on context
- Adapt prompts to user expertise levels, preferences, or history
- Generate prompts with varying complexity

**4. Type Safety**
- Validate inputs before rendering prompts
- Catch errors early in development
- Document expected variables clearly

**5. Collaboration**
- Prompt engineers can work independently from developers
- Non-technical team members can modify templates
- Version control for prompts just like code

**6. Consistency**
- Ensure consistent formatting across all prompts
- Standardize tone, structure, and instructions
- Easy to enforce organizational guidelines

---

## Jinja2 Basics

### Installation

```bash
pip install jinja2
```

### Basic Usage

```python
from jinja2 import Template

# Simple template
template = Template("Hello, {{ name }}!")
output = template.render(name="Alice")
print(output)  # Output: Hello, Alice!
```

### Loading Templates from Files

```python
from jinja2 import Environment, FileSystemLoader

# Set up template environment
env = Environment(loader=FileSystemLoader('templates'))

# Load and render template
template = env.get_template('my_prompt.j2')
output = template.render(
    user_name="Alice",
    task="code review",
    expertise_level="intermediate"
)
```

### Environment Configuration

```python
from jinja2 import Environment, FileSystemLoader

env = Environment(
    loader=FileSystemLoader('templates'),
    trim_blocks=True,        # Remove first newline after block
    lstrip_blocks=True,      # Remove leading spaces before blocks
    autoescape=False         # Don't escape HTML (we're not generating HTML)
)
```

---

## Core Syntax and Features

### 4.1 Variable Interpolation

Use double curly braces `{{ }}` to insert variables:

**Template:**
```jinja2
You are an AI assistant helping {{ user_name }}.
The current task is: {{ task_description }}
User's expertise level: {{ expertise_level }}
```

**Python:**
```python
template.render(
    user_name="Bob",
    task_description="debug a Python script",
    expertise_level="beginner"
)
```

**Output:**
```
You are an AI assistant helping Bob.
The current task is: debug a Python script
User's expertise level: beginner
```

### 4.2 Conditional Statements

Use `{% if %}` for conditional logic:

**Template:**
```jinja2
You are a {{ role }} assistant.

{% if expertise_level == 'beginner' %}
Please explain concepts in simple terms with examples.
Avoid technical jargon and provide step-by-step guidance.
{% elif expertise_level == 'intermediate' %}
Provide detailed explanations with technical context.
Include best practices and common pitfalls.
{% else %}
Assume advanced knowledge and focus on nuances.
Discuss edge cases and performance implications.
{% endif %}
```

**More Conditional Examples:**
```jinja2
{# Check if variable exists #}
{% if user_preferences is defined %}
User preferences: {{ user_preferences }}
{% endif %}

{# Check for None #}
{% if response is not none %}
Previous response: {{ response }}
{% endif %}

{# Logical operators #}
{% if score > 80 and attempts < 3 %}
Great job! You passed on the first try.
{% endif %}

{# Check list length #}
{% if items|length > 0 %}
Found {{ items|length }} items.
{% endif %}
```

### 4.3 Loops

Use `{% for %}` to iterate over lists:

**Template:**
```jinja2
Consider the following requirements:
{% for requirement in requirements %}
{{ loop.index }}. {{ requirement }}
{% endfor %}

Please ensure your response addresses all {{ requirements|length }} requirements.
```

**Loop Variables:**
```jinja2
{% for item in items %}
- Item {{ loop.index }} of {{ loop.length }}: {{ item }}
  {% if loop.first %}(This is the first item){% endif %}
  {% if loop.last %}(This is the last item){% endif %}
{% endfor %}
```

**Looping Over Dictionaries:**
```jinja2
{% for key, value in user_data.items() %}
{{ key }}: {{ value }}
{% endfor %}
```

**Empty Loop Handling:**
```jinja2
{% for example in examples %}
- {{ example }}
{% else %}
No examples available.
{% endfor %}
```

### 4.4 Filters

Filters modify variables using the `|` pipe symbol:

**Common Filters:**
```jinja2
{# String manipulation #}
User name: {{ user_name | upper }}
Title: {{ title | title }}
Description: {{ description | capitalize }}

{# Truncation #}
Short version: {{ long_text | truncate(100) }}
Word limit: {{ content | truncate(200, True, '...') }}

{# Lists #}
Total items: {{ items | length }}
Joined: {{ tags | join(', ') }}
First item: {{ items | first }}
Last item: {{ items | last }}

{# Defaults #}
Value: {{ optional_var | default('N/A') }}
Name: {{ name | default('Guest', true) }}  # true = apply even if empty string

{# Replacement #}
Clean text: {{ text | replace('bad', 'good') }}

{# Formatting #}
Formatted: {{ number | round(2) }}
Absolute: {{ value | abs }}
```

**Chaining Filters:**
```jinja2
{{ user_name | trim | lower | title }}
{{ items | select('defined') | list | join(', ') }}
```

### 4.5 Comments

Use `{# #}` for comments that won't appear in output:

```jinja2
{# This is a comment explaining the template logic #}
{# TODO: Add more examples for advanced users #}
{# 
   Multi-line comment
   for longer explanations
#}

You are an AI assistant.
```

### 4.6 Whitespace Control

Add `-` to strip whitespace:

**Without whitespace control:**
```jinja2
{% for item in items %}
  {{ item }}
{% endfor %}
```

**Output:**
```

  Apple

  Banana

  Cherry

```

**With whitespace control:**
```jinja2
{% for item in items -%}
{{ item }}
{% endfor -%}
```

**Output:**
```
Apple
Banana
Cherry
```

**Mixed control:**
```jinja2
{%- if condition -%}
  Text here
{%- endif %}
```

---

## Prompt Engineering Patterns

### 5.1 System Message Templates

Create reusable system messages with role-specific instructions:

**Template: `system_message.j2`**
```jinja2
You are {{ assistant_role }}, a specialized AI assistant.

Your primary responsibilities:
{% for responsibility in responsibilities -%}
- {{ responsibility }}
{% endfor %}

{% if constraints -%}
Constraints and limitations:
{% for constraint in constraints -%}
- {{ constraint }}
{% endfor %}
{% endif %}

{% if examples -%}
Examples of good responses:
{% for example in examples %}
Input: {{ example.input }}
Output: {{ example.output }}
{% if example.explanation -%}
Why this is good: {{ example.explanation }}
{% endif %}
{% endfor %}
{% endif %}

Always respond in {{ tone | default('a professional and helpful') }} tone.

{% if output_format -%}
Format your response as: {{ output_format }}
{% endif %}
```

**Usage Example:**
```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('system_message.j2')

context = {
    'assistant_role': 'Code Review Expert',
    'responsibilities': [
        'Review code for bugs and security issues',
        'Suggest performance improvements',
        'Ensure code follows best practices',
        'Provide constructive feedback'
    ],
    'constraints': [
        'Focus on Python and JavaScript only',
        'Provide specific line numbers for issues',
        'Limit suggestions to 5 most critical items'
    ],
    'tone': 'constructive and educational',
    'output_format': 'structured markdown with sections for bugs, improvements, and praise'
}

prompt = template.render(**context)
```

### 5.2 Few-Shot Learning Templates

Dynamically include examples based on the task:

**Template: `few_shot.j2`**
```jinja2
Task: {{ task_description }}

{% if task_explanation -%}
{{ task_explanation }}
{% endif %}

{% if examples -%}
Here are some examples to guide your response:

{% for example in examples -%}
Example {{ loop.index }}:
Input: {{ example.input }}
Output: {{ example.output }}
{% if example.explanation -%}
Explanation: {{ example.explanation }}
{% endif %}

{% endfor -%}
{% endif %}

Now, please complete the following:
Input: {{ user_input }}
{% if additional_instructions -%}

Additional instructions:
{{ additional_instructions }}
{% endif %}
```

**Usage Example:**
```python
context = {
    'task_description': 'Classify the sentiment of text as positive, negative, or neutral',
    'task_explanation': 'Consider the overall emotional tone and context.',
    'examples': [
        {
            'input': 'I love this product! Best purchase ever.',
            'output': 'Positive',
            'explanation': 'Strong positive words like "love" and "best"'
        },
        {
            'input': 'The service was okay, nothing special.',
            'output': 'Neutral',
            'explanation': 'Moderate language without strong emotions'
        },
        {
            'input': 'Terrible experience. Would not recommend.',
            'output': 'Negative',
            'explanation': 'Clear negative sentiment with warning to others'
        }
    ],
    'user_input': 'The food was decent but the wait time was too long.'
}

prompt = template.render(**context)
```

### 5.3 Context-Aware Prompts

Adapt prompts based on available context:

**Template: `context_aware.j2`**
```jinja2
You are helping with: {{ task_type }}

{% if user_history -%}
Previous interactions (last 3):
{% for interaction in user_history[-3:] -%}
- {{ interaction.timestamp }}: {{ interaction.summary }}
  Result: {{ interaction.result }}
{% endfor %}
{% endif %}

{% if user_preferences -%}
User preferences:
{% for key, value in user_preferences.items() -%}
- {{ key | replace('_', ' ') | title }}: {{ value }}
{% endfor %}
{% endif %}

{% if context_documents -%}
Relevant context documents:
{% for doc in context_documents -%}
### {{ doc.title }}
{{ doc.content | truncate(200) }}
{% endfor %}
{% endif %}

Current request: {{ current_request }}

{% if user_expertise -%}
Note: User expertise level is {{ user_expertise }}. Adjust explanations accordingly.
{% endif %}
```

### 5.4 Multi-Step Reasoning Templates

**Template: `chain_of_thought.j2`**
```jinja2
Problem: {{ problem }}

Please solve this step by step:

{% for step in reasoning_steps -%}
Step {{ loop.index }}: {{ step }}
{% endfor %}

{% if include_verification -%}
After completing all steps, verify your answer by:
{% for check in verification_steps -%}
- {{ check }}
{% endfor %}
{% endif %}

{% if show_work -%}
Show your work for each step.
{% endif %}

{% if confidence_required -%}
Provide a confidence level (0-100%) for your final answer.
{% endif %}
```

**Usage Example:**
```python
context = {
    'problem': 'Calculate the compound interest on $10,000 at 5% annual rate for 3 years',
    'reasoning_steps': [
        'Identify the principal amount, interest rate, and time period',
        'Apply the compound interest formula: A = P(1 + r/n)^(nt)',
        'Calculate the total amount',
        'Subtract principal to find the interest earned'
    ],
    'include_verification': True,
    'verification_steps': [
        'Check if the result makes logical sense',
        'Verify units and calculations',
        'Compare with simple interest as a sanity check'
    ],
    'show_work': True,
    'confidence_required': True
}
```

### 5.5 Role-Based Prompts with Persona

**Template: `persona_prompt.j2`**
```jinja2
{# Define persona characteristics #}
{% set personas = {
    'teacher': {
        'style': 'patient and explanatory',
        'approach': 'break down complex topics',
        'language': 'simple and clear'
    },
    'expert': {
        'style': 'authoritative and precise',
        'approach': 'provide deep insights',
        'language': 'technical and nuanced'
    },
    'friend': {
        'style': 'casual and supportive',
        'approach': 'relate to common experiences',
        'language': 'conversational and warm'
    }
} %}

{% set current_persona = personas[persona_type] %}

You are acting as a {{ persona_type }}.

Communication style: {{ current_persona.style }}
Approach: {{ current_persona.approach }}
Language level: {{ current_persona.language }}

{{ task_description }}

{% if persona_type == 'teacher' -%}
Remember to:
- Use analogies and examples
- Check for understanding
- Encourage questions
{% elif persona_type == 'expert' -%}
Remember to:
- Cite sources when relevant
- Discuss edge cases
- Provide industry context
{% elif persona_type == 'friend' -%}
Remember to:
- Be encouraging and positive
- Share relatable examples
- Keep it conversational
{% endif %}
```

---

## Advanced Techniques

### 6.1 Macros for Reusable Components

Macros are like functions for templates:

**Template: `macros.j2`**
```jinja2
{# Macro to format an example #}
{% macro format_example(input, output, explanation=None) -%}
---
Input: {{ input }}
Expected Output: {{ output }}
{% if explanation -%}
Reasoning: {{ explanation }}
{% endif -%}
---
{%- endmacro %}

{# Macro to create a code block #}
{% macro code_block(code, language='python') -%}
```{{ language }}
{{ code }}
```
{%- endmacro %}

{# Macro for structured output format #}
{% macro structured_response(sections) -%}
{% for section in sections -%}
## {{ section.title }}
{{ section.content }}

{% endfor -%}
{%- endmacro %}
```

**Using Macros:**
```jinja2
{% from 'macros.j2' import format_example, code_block %}

Here are examples of good responses:

{{ format_example('What is 2+2?', '4', 'Basic arithmetic') }}
{{ format_example('Reverse "hello"', '"olleh"', 'String reversal') }}

Here's sample code:
{{ code_block('def hello():\n    print("Hello!")', 'python') }}
```

### 6.2 Template Inheritance

Create base templates and extend them for specific use cases:

**Base Template: `base_prompt.j2`**
```jinja2
You are {{ role }}.

{% block instructions %}
{# Default instructions - can be overridden #}
Follow these general guidelines:
- Be helpful and accurate
- Provide clear explanations
- Ask clarifying questions when needed
{% endblock %}

{% block context %}
{# Optional context section #}
{% endblock %}

{% block examples %}
{# Optional examples section #}
{% endblock %}

{% block constraints %}
{# Optional constraints section #}
{% endblock %}

{% block output_format %}
Provide your response in a clear, structured format.
{% endblock %}
```

**Specific Template: `translation_prompt.j2`**
```jinja2
{% extends 'base_prompt.j2' %}

{% block instructions %}
Translate the following text from {{ source_language }} to {{ target_language }}.

Requirements:
- Maintain the original meaning and tone
- Preserve formatting and structure
- Use natural, idiomatic expressions in the target language
- Handle cultural references appropriately
{% endblock %}

{% block constraints %}
- Do not translate proper nouns unless commonly translated
- Maintain technical terminology accurately
- Indicate if something is untranslatable with [UNTRANSLATABLE: original text]
{% endblock %}

{% block output_format %}
Provide:
1. The translation
2. Any notes on translation choices (if complex)
3. Confidence level: High/Medium/Low
{% endblock %}
```

**Usage:**
```python
template = env.get_template('translation_prompt.j2')
prompt = template.render(
    role='Expert Translator',
    source_language='English',
    target_language='Spanish'
)
```

### 6.3 Custom Filters

Create custom filters for domain-specific formatting:

```python
from jinja2 import Environment, FileSystemLoader

def format_code(text, language='python'):
    """Format text as a code block."""
    return f"```{language}\n{text}\n```"

def summarize_list(items, max_items=3):
    """Summarize a long list."""
    if len(items) <= max_items:
        return ', '.join(str(item) for item in items)
    else:
        shown = ', '.join(str(item) for item in items[:max_items])
        return f"{shown}, and {len(items) - max_items} more"

def truncate_middle(text, max_length=100):
    """Truncate from the middle, keeping start and end."""
    if len(text) <= max_length:
        return text
    half = (max_length - 3) // 2
    return f"{text[:half]}...{text[-half:]}"

def format_chat_history(messages, max_messages=5):
    """Format chat history in a readable way."""
    formatted = []
    for msg in messages[-max_messages:]:
        role = msg.get('role', 'unknown')
        content = msg.get('content', '')
        formatted.append(f"{role.upper()}: {content}")
    return '\n'.join(formatted)

# Set up environment with custom filters
env = Environment(loader=FileSystemLoader('templates'))
env.filters['code'] = format_code
env.filters['summarize'] = summarize_list
env.filters['truncate_middle'] = truncate_middle
env.filters['format_chat'] = format_chat_history
```

**Using Custom Filters in Templates:**
```jinja2
{{ python_code | code('python') }}

Tags: {{ all_tags | summarize(5) }}

File path: {{ long_path | truncate_middle(50) }}

Previous conversation:
{{ chat_history | format_chat(10) }}
```

### 6.4 Template Tests

Use built-in tests for conditional logic:

```jinja2
{# Check if variable is defined #}
{% if user_input is defined -%}
User provided: {{ user_input }}
{% else -%}
No input provided. Please provide input.
{% endif %}

{# Check if iterable #}
{% if items is iterable -%}
Processing {{ items | length }} items...
{% endif %}

{# Check for None #}
{% if response is none -%}
No previous response available.
{% endif %}

{# Check data types #}
{% if count is number -%}
Count: {{ count }}
{% endif %}

{% if message is string -%}
Message: {{ message }}
{% endif %}

{# Check if divisible #}
{% if page_number is divisibleby(2) -%}
This is an even page.
{% endif %}

{# Check if in sequence #}
{% if 'admin' in user_roles -%}
Admin access granted.
{% endif %}
```

### 6.5 Include Statements

Modularize prompts by including partial templates:

**Template: `main_prompt.j2`**
```jinja2
{% include 'common_instructions.j2' %}

{% include 'safety_guidelines.j2' %}

Specific task: {{ task_description }}

{% if advanced_mode -%}
{% include 'advanced_features.j2' %}
{% endif %}

{% if include_examples -%}
{% include 'examples/' + task_type + '.j2' %}
{% endif %}
```

**Template: `common_instructions.j2`**
```jinja2
General Instructions:
- Be accurate and truthful
- Cite sources when making factual claims
- Acknowledge uncertainty when appropriate
- Respect user privacy and data security
```

**Template: `safety_guidelines.j2`**
```jinja2
Safety Guidelines:
- Do not provide harmful or dangerous information
- Refuse inappropriate requests politely
- Consider ethical implications of responses
```

### 6.6 Dynamic Template Selection

```python
def get_template_name(task_type, complexity):
    """Dynamically select template based on parameters."""
    template_map = {
        ('code_review', 'simple'): 'code_review_basic.j2',
        ('code_review', 'complex'): 'code_review_advanced.j2',
        ('translation', 'simple'): 'translation_basic.j2',
        ('translation', 'complex'): 'translation_expert.j2',
    }
    return template_map.get((task_type, complexity), 'default.j2')

# Usage
template_name = get_template_name('code_review', 'complex')
template = env.get_template(template_name)
```

---

## Best Practices

### 7.1 Template Organization

**Directory Structure:**
```
templates/
├── base/
│   ├── system_message.j2
│   ├── base_prompt.j2
│   └── base_chat.j2
├── prompts/
│   ├── code_review.j2
│   ├── translation.j2
│   ├── data_analysis.j2
│   └── customer_support.j2
├── partials/
│   ├── common_instructions.j2
│   ├── safety_guidelines.j2
│   └── examples.j2
├── macros/
│   ├── formatting.j2
│   └── validation.j2
└── personas/
    ├── teacher.j2
    ├── expert.j2
    └── assistant.j2
```

**Naming Conventions:**
- Use descriptive, lowercase names with underscores: `code_review_advanced.j2`
- Suffix with `.j2` or `.jinja2` for clarity
- Group related templates in subdirectories
- Use prefixes for template types: `base_`, `macro_`, `partial_`

### 7.2 Variable Naming and Documentation

**Document variables at the top of templates:**
```jinja2
{#
Template: code_review.j2
Description: Generate code review prompts

Required variables:
  - language (str): Programming language (e.g., 'python', 'javascript')
  - code_snippet (str): Code to review
  - review_type (str): Type of review ('security', 'performance', 'style')

Optional variables:
  - context (str): Additional context about the code
  - constraints (list): List of specific constraints
  - previous_reviews (list): Past review history

Example usage:
  template.render(
      language='python',
      code_snippet='def foo(): pass',
      review_type='style'
  )
#}

You are reviewing {{ language }} code for {{ review_type }} issues.
...
```

**Variable Naming Best Practices:**
- Use descriptive snake_case names: `user_expertise_level` not `uel`
- Be consistent across templates
- Use plurals for lists: `items`, `examples`, `constraints`
- Use boolean prefixes: `is_`, `has_`, `should_`, `include_`
- Group related variables with common prefixes: `user_name`, `user_email`, `user_role`

### 7.3 Error Handling and Validation

```jinja2
{# Provide defaults for optional variables #}
{% set expertise = expertise_level | default('intermediate') %}
{% set max_tokens = max_tokens | default(1000) %}

{# Validate required variables #}
{% if not task_description -%}
{{ raise('Error: task_description is required') }}
{% endif %}

{# Handle missing or empty data gracefully #}
{% if examples is defined and examples | length > 0 -%}
Examples:
{% for ex in examples -%}
- {{ ex }}
{% endfor %}
{% else -%}
No examples available. Proceeding without examples.
{% endif %}

{# Validate data types #}
{% if user_id is not number -%}
Warning: user_id should be a number, got {{ user_id }}
{% endif %}

{# Check for valid enum values #}
{% set valid_levels = ['beginner', 'intermediate', 'advanced'] %}
{% if expertise_level not in valid_levels -%}
Warning: Invalid expertise level. Using default.
{% set expertise_level = 'intermediate' %}
{% endif %}
```

**Python-side validation:**
```python
from jinja2 import Template, TemplateSyntaxError, UndefinedError

def render_safe(template, context):
    """Render template with error handling."""
    try:
        # Validate required fields
        required = ['task_description', 'user_id']
        missing = [f for f in required if f not in context]
        if missing:
            raise ValueError(f"Missing required fields: {missing}")
        
        # Render template
        return template.render(**context)
    
    except TemplateSyntaxError as e:
        print(f"Template syntax error: {e}")
        return None
    except UndefinedError as e:
        print(f"Undefined variable: {e}")
        return None
    except Exception as e:
        print(f"Error rendering template: {e}")
        return None
```

### 7.4 Performance Optimization

**1. Cache compiled templates:**
```python
from jinja2 import Environment, FileSystemLoader

# Create environment once (global or singleton)
env = Environment(
    loader=FileSystemLoader('templates'),
    auto_reload=False  # Disable in production
)

# Templates are automatically cached
template = env.get_template('my_prompt.j2')  # Cached
```

**2. Minimize template complexity:**
```jinja2
{# ❌ BAD: Complex logic in template #}
{% for item in items %}
  {% if item.status == 'active' and item.score > 50 and item.category in allowed_categories %}
    {% set processed = expensive_operation(item) %}
    {{ processed }}
  {% endif %}
{% endfor %}

{# ✅ GOOD: Process in Python, simple iteration in template #}
{% for item in preprocessed_items %}
  {{ item }}
{% endfor %}
```

```python
# Do complex processing in Python
def prepare_context(items, allowed_categories):
    preprocessed = []
    for item in items:
        if item.status == 'active' and item.score > 50:
            if item.category in allowed_categories:
                preprocessed.append(expensive_operation(item))
    return preprocessed

context = {
    'preprocessed_items': prepare_context(items, allowed_categories)
}
```

**3. Use template inheritance efficiently:**
```jinja2
{# ❌ BAD: Deeply nested inheritance #}
base.j2 -> intermediate.j2 -> specific.j2 -> very_specific.j2

{# ✅ GOOD: Shallow inheritance with includes #}
base.j2 -> specific.j2 (with includes)
```

### 7.5 Version Control Best Practices

**1. Track templates with code:**
```
.gitignore should NOT ignore template files
Commit templates alongside code changes
Tag template versions with code releases
```

**2. Add meaningful comments:**
```jinja2
{#
Version: 2.1.0
Last updated: 2024-02-01
Author: AI Team
Changes: Added support for multi-language code review
#}
```

**3. Use feature flags for template changes:**
```jinja2
{% if enable_new_format %}
  {# New experimental format #}
  {% include 'new_format.j2' %}
{% else %}
  {# Stable legacy format #}
  {% include 'legacy_format.j2' %}
{% endif %}
```

### 7.6 Security Considerations

**1. Sanitize user inputs:**
```python
import html
from jinja2 import Environment, select_autoescape

# For HTML output, use autoescaping
env = Environment(
    autoescape=select_autoescape(['html', 'xml'])
)

# For prompts, sanitize manually if needed
def sanitize_input(user_input):
    # Remove potentially harmful characters
    forbidden = ['{{', '}}', '{%', '%}', '{#', '#}']
    sanitized = user_input
    for char in forbidden:
        sanitized = sanitized.replace(char, '')
    return sanitized

context = {
    'user_input': sanitize_input(raw_user_input)
}
```

**2. Validate template paths:**
```python
import os

def safe_load_template(template_name, allowed_dir='templates'):
    """Prevent directory traversal attacks."""
    # Normalize path
    template_path = os.path.normpath(os.path.join(allowed_dir, template_name))
    
    # Ensure it's within allowed directory
    if not template_path.startswith(os.path.abspath(allowed_dir)):
        raise ValueError("Invalid template path")
    
    return env.get_template(template_name)
```

**3. Limit template functionality:**
```python
from jinja2 import Environment, StrictUndefined

env = Environment(
    undefined=StrictUndefined,  # Raise errors on undefined variables
    autoescape=False            # We're not generating HTML
)

# Don't pass dangerous functions to templates
# ❌ BAD
context = {
    'eval': eval,  # NEVER DO THIS
    'os': os       # NEVER DO THIS
}

# ✅ GOOD
context = {
    'format_date': safe_date_formatter,
    'truncate': safe_truncate
}
```

**4. Review generated prompts:**
```python
def generate_and_log_prompt(template, context):
    """Generate prompt and log for security review."""
    prompt = template.render(**context)
    
    # Log for security auditing
    logger.info(f"Generated prompt for user {context.get('user_id')}")
    logger.debug(f"Prompt content: {prompt[:200]}...")
    
    # Optional: Check for injection patterns
    if suspicious_pattern_detected(prompt):
        logger.warning("Suspicious pattern in generated prompt")
        # Handle appropriately
    
    return prompt
```

### 7.7 Testing Templates

**Unit test templates:**
```python
import pytest
from jinja2 import Environment, FileSystemLoader

@pytest.fixture
def env():
    return Environment(loader=FileSystemLoader('templates'))

def test_code_review_template(env):
    template = env.get_template('code_review.j2')
    
    context = {
        'language': 'python',
        'code_snippet': 'def hello(): pass',
        'review_type': 'style'
    }
    
    result = template.render(**context)
    
    # Assert expected content
    assert 'python' in result.lower()
    assert 'style' in result.lower()
    assert 'def hello()' in result

def test_missing_required_variable(env):
    template = env.get_template('code_review.j2')
    
    # Should handle missing variables gracefully
    with pytest.raises(Exception):
        template.render(language='python')  # Missing required fields

def test_conditional_sections(env):
    template = env.get_template('system_message.j2')
    
    # With examples
    result_with = template.render(
        assistant_role='Coder',
        responsibilities=['Code'],
        examples=[{'input': 'a', 'output': 'b'}]
    )
    assert 'Examples' in result_with
    
    # Without examples
    result_without = template.render(
        assistant_role='Coder',
        responsibilities=['Code']
    )
    assert 'Examples' not in result_without
```

---

## Complete Examples

### 8.1 Code Assistant Template

**Template: `templates/code_assistant.j2`**
```jinja2
{#
Code Assistant Prompt Template
Required: language, task
Optional: context, code_snippet, constraints, style_guide
#}

You are an expert {{ language }} developer with deep knowledge of best practices, design patterns, and the {{ language }} ecosystem.

**Task:** {{ task }}

{% if context -%}
**Context:**
{{ context }}

{% endif -%}

{% if code_snippet -%}
**Current Code:**
```{{ language }}
{{ code_snippet }}
```

{% endif -%}

{% if style_guide -%}
**Style Guide:**
Follow {{ style_guide }} conventions.

{% endif -%}

{% if constraints -%}
**Requirements and Constraints:**
{% for constraint in constraints -%}
- {{ constraint }}
{% endfor %}

{% endif -%}

**Please provide:**

1. **Explanation**: Describe your approach and reasoning
2. **Implementation**: Complete, working code solution
3. **Usage Example**: Show how to use your solution
4. **Edge Cases**: Discuss potential edge cases and how your solution handles them
{% if include_tests -%}
5. **Tests**: Provide unit tests for your solution
{% endif %}

{% if optimization_focus -%}
**Special Focus:** {{ optimization_focus }}
{% endif %}
```

**Python Usage:**
```python
from jinja2 import Environment, FileSystemLoader

env = Environment(
    loader=FileSystemLoader('templates'),
    trim_blocks=True,
    lstrip_blocks=True
)

template = env.get_template('code_assistant.j2')

prompt = template.render(
    language='Python',
    task='Create a function to validate email addresses',
    constraints=[
        'Use regular expressions',
        'Handle international domains',
        'Return both validation result and error message',
        'Include type hints',
        'Add comprehensive docstring'
    ],
    include_tests=True,
    optimization_focus='Performance and readability'
)

print(prompt)

# Send to LLM
# response = llm_client.generate(prompt)
```

### 8.2 Data Analysis Template

**Template: `templates/data_analysis.j2`**
```jinja2
{#
Data Analysis Prompt Template
Required: dataset_description, analysis_goals
Optional: columns, sample_data, output_format, constraints
#}

You are an experienced data scientist proficient in Python, pandas, numpy, and data visualization libraries.

**Dataset Description:**
{{ dataset_description }}

{% if columns -%}
**Dataset Schema:**
{% for col in columns -%}
- **{{ col.name }}** ({{ col.type }})
  {%- if col.description %}: {{ col.description }}{% endif %}
  {%- if col.sample_values %} | Examples: {{ col.sample_values | join(', ') }}{% endif %}
{% endfor %}

{% endif -%}

**Analysis Goals:**
{% for goal in analysis_goals -%}
{{ loop.index }}. {{ goal }}
{% endfor %}

{% if constraints -%}

**Constraints:**
{% for constraint in constraints -%}
- {{ constraint }}
{% endfor %}
{% endif %}

{% if sample_data -%}

**Sample Data:**
```
{{ sample_data }}
```
{% endif %}

{% if output_format == 'code' -%}

**Output Requirements:**
- Provide complete, executable Python code
- Use pandas, matplotlib/seaborn for visualization
- Include comments explaining each step
- Handle missing data appropriately
- Add error handling

{% elif output_format == 'insights' -%}

**Output Requirements:**
- Provide key insights and findings
- Include statistical summaries
- Recommend actionable next steps
- Highlight any data quality issues

{% else -%}

**Output Requirements:**
Provide both:
1. Python code for the analysis
2. Written insights and recommendations
3. Suggestions for visualizations

{% endif -%}

{% if statistical_significance -%}
Note: Include statistical significance testing where appropriate (p-values, confidence intervals).
{% endif %}
```

**Usage:**
```python
prompt = template.render(
    dataset_description='Customer purchase history for an e-commerce platform',
    columns=[
        {
            'name': 'customer_id',
            'type': 'int',
            'description': 'Unique customer identifier'
        },
        {
            'name': 'purchase_date',
            'type': 'datetime',
            'description': 'Date of purchase'
        },
        {
            'name': 'amount',
            'type': 'float',
            'description': 'Purchase amount in USD',
            'sample_values': ['29.99', '149.50', '5.99']
        },
        {
            'name': 'category',
            'type': 'string',
            'description': 'Product category',
            'sample_values': ['Electronics', 'Clothing', 'Books']
        }
    ],
    analysis_goals=[
        'Identify customer segments based on purchasing behavior',
        'Analyze seasonal trends in purchases',
        'Calculate customer lifetime value',
        'Find correlations between product categories'
    ],
    output_format='both',
    constraints=[
        'Handle missing values appropriately',
        'Normalize currency values if needed',
        'Consider time zones for datetime data'
    ],
    statistical_significance=True
)
```

### 8.3 Customer Support Template

**Template: `templates/customer_support.j2`**
```jinja2
{#
Customer Support Prompt Template
Required: customer_tier, issue_type
Optional: previous_tickets, sentiment, customer_context, urgency
#}

You are a customer support specialist for {{ company_name | default('our company') }}.

**Customer Profile:**
- Tier: {{ customer_tier | upper }}
- Issue Category: {{ issue_type }}
{% if customer_since -%}
- Customer Since: {{ customer_since }}
{% endif -%}
{% if sentiment -%}
- Detected Sentiment: {{ sentiment | upper }}
{% endif -%}
{% if urgency -%}
- Urgency Level: {{ urgency | upper }}
{% endif %}

{% if previous_tickets and previous_tickets | length > 0 -%}

**Recent Ticket History:**
{% for ticket in previous_tickets[:3] -%}
- {{ ticket.date }}: {{ ticket.issue }} → {{ ticket.status }}
  {%- if ticket.resolution %} ({{ ticket.resolution }}){% endif %}
{% endfor %}
{% endif %}

{% if customer_context -%}

**Additional Context:**
{{ customer_context }}
{% endif %}

{% if customer_tier == 'premium' or customer_tier == 'enterprise' -%}

⚠️ **PRIORITY CUSTOMER**: This is a {{ customer_tier }} customer. Provide exceptional service:
- Prioritize rapid resolution
- Offer proactive solutions
- Consider white-glove treatment
- Escalate if needed
{% endif %}

{% if sentiment == 'frustrated' or sentiment == 'angry' -%}

⚠️ **CUSTOMER DISTRESS DETECTED**: Customer appears {{ sentiment }}.
**Response Strategy:**
- Lead with empathy and acknowledgment
- Avoid defensive language
- Focus on immediate solutions
- Offer compensation if appropriate
- Escalate to supervisor if needed
{% endif %}

{% if urgency == 'critical' -%}

🚨 **CRITICAL ISSUE**: Immediate action required.
- Provide fastest possible resolution
- Notify relevant teams
- Follow up proactively
{% endif %}

**Response Guidelines:**
1. **Acknowledge**: Recognize the customer's issue and feelings
2. **Clarify**: Ask questions if more information is needed
3. **Solve**: Provide clear, actionable solutions
4. **Follow-up**: Offer next steps and ongoing support

{% if available_solutions -%}
**Available Solutions:**
{% for solution in available_solutions -%}
- {{ solution }}
{% endfor %}
{% endif %}

{% if knowledge_base_articles -%}

**Relevant Knowledge Base:**
{% for article in knowledge_base_articles -%}
- [{{ article.title }}]({{ article.url }})
{% endfor %}
{% endif %}

**Tone:** {{ tone | default('Professional, empathetic, and solution-focused') }}

{% if customer_tier == 'premium' -%}
**Premium Benefits to Mention:**
- Priority support
- Dedicated account manager
- Extended warranty/guarantees
- Exclusive features access
{% endif %}
```

**Usage:**
```python
prompt = template.render(
    company_name='TechCorp',
    customer_tier='premium',
    issue_type='billing discrepancy',
    customer_since='2022-03-15',
    sentiment='frustrated',
    urgency='high',
    previous_tickets=[
        {
            'date': '2024-01-15',
            'issue': 'Login problems',
            'status': 'Resolved',
            'resolution': 'Password reset sent'
        },
        {
            'date': '2024-01-20',
            'issue': 'Feature request',
            'status': 'In Progress'
        }
    ],
    customer_context='Customer mentioned they have recommended our service to 3 colleagues',
    available_solutions=[
        'Issue immediate refund',
        'Apply account credit',
        'Escalate to billing department',
        'Offer one month free service'
    ],
    tone='Warm, apologetic, and solution-oriented'
)
```

### 8.4 Content Generation Template

**Template: `templates/content_generator.j2`**
```jinja2
{#
Content Generation Template
Required: content_type, topic, target_audience
Optional: tone, keywords, length, style_examples, constraints
#}

Create {{ content_type }} about: **{{ topic }}**

**Target Audience:** {{ target_audience }}
**Tone:** {{ tone | default('Professional and engaging') }}
{% if length -%}
**Target Length:** {{ length }}
{% endif %}

{% if keywords -%}
**Key Points to Include:**
{% for keyword in keywords -%}
- {{ keyword }}
{% endfor %}
{% endif %}

{% if seo_keywords -%}

**SEO Keywords** (use naturally):
{{ seo_keywords | join(', ') }}
{% endif %}

{% if content_type == 'blog post' -%}

**Structure Requirements:**
1. **Introduction** (100-150 words)
   - Hook that grabs attention
   - Brief overview of what reader will learn
   - Why this topic matters

2. **Main Body** (use clear subheadings)
   - Break down complex ideas
   - Use examples and analogies
   - Include data/statistics if relevant
   - Add bullet points for readability

3. **Conclusion** (75-100 words)
   - Summarize key takeaways
   - Call-to-action
   - Next steps or resources

{% elif content_type == 'social media post' -%}

**Requirements:**
- Attention-grabbing opening (first 10 words are crucial)
- Include 2-3 relevant hashtags
- Encourage engagement (question, poll, or CTA)
- Platform: {{ platform | default('General') }}
{% if platform == 'LinkedIn' -%}
- Professional tone, industry insights
- Use line breaks for readability
{% elif platform == 'Twitter' -%}
- Concise and punchy
- Thread format if needed
{% elif platform == 'Instagram' -%}
- Visual-first approach
- Emoji usage encouraged
- Story-telling style
{% endif %}

{% elif content_type == 'email' -%}

**Structure Requirements:**
1. **Subject Line** (compelling, under 50 characters)
2. **Preview Text** (supports subject line)
3. **Body:**
   - Personalized greeting
   - Clear value proposition
   - Scannable format (short paragraphs, bullets)
   - Strong call-to-action
4. **Signature** (professional closing)

{% if email_type -%}
**Email Type:** {{ email_type }}
{% if email_type == 'promotional' -%}
- Highlight benefits over features
- Create urgency if appropriate
- Include social proof
{% elif email_type == 'newsletter' -%}
- Mix of valuable content
- Clear sections
- Multiple CTAs
{% elif email_type == 'onboarding' -%}
- Welcome and reassure
- Clear next steps
- Helpful resources
{% endif %}
{% endif %}

{% elif content_type == 'product description' -%}

**Requirements:**
- Lead with benefits, not just features
- Use sensory language
- Address customer pain points
- Include specifications/details
- End with strong CTA
{% if product_details -%}

**Product Details:**
{% for key, value in product_details.items() -%}
- {{ key }}: {{ value }}
{% endfor %}
{% endif %}

{% endif %}

{% if brand_voice -%}

**Brand Voice Guidelines:**
{{ brand_voice }}
{% endif %}

{% if constraints -%}

**Constraints:**
{% for constraint in constraints -%}
- {{ constraint }}
{% endfor %}
{% endif %}

{% if style_examples -%}

**Style Examples:**
{% for example in style_examples -%}

Example {{ loop.index }}:
{{ example.text }}
{% if example.note -%}
Note: {{ example.note }}
{% endif %}
{% endfor %}
{% endif %}

{% if competitor_analysis -%}

**Differentiation:**
Stand out from competitors by:
{% for point in competitor_analysis -%}
- {{ point }}
{% endfor %}
{% endif %}

{% if call_to_action -%}

**Primary Call-to-Action:** {{ call_to_action }}
{% endif %}
```

**Usage:**
```python
prompt = template.render(
    content_type='blog post',
    topic='The Future of AI in Healthcare',
    target_audience='Healthcare professionals and medical administrators',
    tone='Authoritative yet accessible',
    length='1200-1500 words',
    keywords=[
        'AI diagnostics',
        'Machine learning in medicine',
        'Patient care automation',
        'Healthcare efficiency'
    ],
    seo_keywords=['AI healthcare', 'medical AI', 'healthcare technology', 'AI diagnosis'],
    constraints=[
        'Back claims with research or data',
        'Address common concerns about AI in healthcare',
        'Include real-world examples or case studies',
        'Avoid overly technical jargon'
    ],
    brand_voice='We are forward-thinking but grounded. We embrace innovation while respecting tradition.',
    call_to_action='Download our free whitepaper on AI implementation in healthcare'
)
```

### 8.5 Educational Content Template

**Template: `templates/educational_content.j2`**
```jinja2
{#
Educational Content Template
Required: topic, learning_level, learning_objectives
Optional: prerequisites, examples, exercises, teaching_style
#}

**Topic:** {{ topic }}
**Learning Level:** {{ learning_level | title }}

{% if prerequisites -%}
**Prerequisites:**
{% for prereq in prerequisites -%}
- {{ prereq }}
{% endfor %}

{% endif -%}

**Learning Objectives:**
By the end of this lesson, learners will be able to:
{% for objective in learning_objectives -%}
{{ loop.index }}. {{ objective }}
{% endfor %}

{% if learning_level == 'beginner' -%}

**Teaching Approach:**
- Use simple, clear language
- Provide plenty of examples
- Break down complex concepts into small steps
- Use analogies and real-world connections
- Encourage questions and check understanding frequently
- Avoid jargon or explain it thoroughly

{% elif learning_level == 'intermediate' -%}

**Teaching Approach:**
- Build on foundational knowledge
- Introduce more complex concepts and edge cases
- Discuss best practices and common pitfalls
- Provide practical applications
- Encourage critical thinking

{% elif learning_level == 'advanced' -%}

**Teaching Approach:**
- Assume strong foundational knowledge
- Focus on nuances and sophisticated applications
- Discuss performance implications and trade-offs
- Include industry best practices
- Explore cutting-edge developments

{% endif -%}

{% if teaching_style -%}

**Teaching Style:** {{ teaching_style }}
{% endif %}

**Content Structure:**

1. **Introduction**
   - What is {{ topic }}?
   - Why is it important?
   - Real-world relevance

2. **Core Concepts**
   - Fundamental principles
   - Key terminology
   {% if learning_level == 'beginner' -%}
   - Simple examples for each concept
   {% else -%}
   - Detailed explanations
   {% endif %}

3. **Practical Application**
   {% if examples -%}
   Use these examples:
   {% for example in examples -%}
   - {{ example }}
   {% endfor %}
   {% else -%}
   - Provide relevant, practical examples
   - Show step-by-step problem solving
   {% endif %}

4. **Common Mistakes**
   - What learners often get wrong
   - How to avoid these mistakes

{% if exercises -%}
5. **Practice Exercises**
   {% for exercise in exercises -%}
   Exercise {{ loop.index }}: {{ exercise.description }}
   {% if exercise.difficulty -%}
   Difficulty: {{ exercise.difficulty }}
   {% endif %}
   {% endfor %}
{% else -%}
5. **Practice Exercises**
   - Provide 3-5 exercises of increasing difficulty
   - Include solutions or hints
{% endif %}

6. **Summary and Next Steps**
   - Key takeaways
   - How this connects to broader learning path
   - Suggested resources for further learning

{% if interactive_elements -%}

**Interactive Elements to Include:**
{% for element in interactive_elements -%}
- {{ element }}
{% endfor %}
{% endif %}

{% if assessment_criteria -%}

**Assessment Focus:**
{% for criterion in assessment_criteria -%}
- {{ criterion }}
{% endfor %}
{% endif %}
```

**Usage:**
```python
prompt = template.render(
    topic='Recursion in Programming',
    learning_level='intermediate',
    prerequisites=[
        'Basic understanding of functions',
        'Familiarity with loops',
        'Understanding of call stack'
    ],
    learning_objectives=[
        'Explain how recursion works',
        'Identify problems suitable for recursive solutions',
        'Write recursive functions with proper base cases',
        'Optimize recursive solutions to avoid stack overflow',
        'Convert between recursive and iterative solutions'
    ],
    teaching_style='Socratic method with guided discovery',
    examples=[
        'Factorial calculation',
        'Fibonacci sequence',
        'Tree traversal',
        'Merge sort algorithm'
    ],
    exercises=[
        {
            'description': 'Write a recursive function to calculate sum of array',
            'difficulty': 'Easy'
        },
        {
            'description': 'Implement recursive binary search',
            'difficulty': 'Medium'
        },
        {
            'description': 'Solve Tower of Hanoi problem recursively',
            'difficulty': 'Hard'
        }
    ],
    interactive_elements=[
        'Step-by-step visualization of recursive calls',
        'Code playground for experimentation',
        'Quiz questions after each section'
    ]
)
```

---

## Real-World Use Cases

### 9.1 Multi-Model Prompt Router

Create different prompts for different LLM models:

```python
from jinja2 import Environment, FileSystemLoader

class PromptRouter:
    def __init__(self, template_dir='templates'):
        self.env = Environment(loader=FileSystemLoader(template_dir))
    
    def get_prompt(self, task_type, model_type, **kwargs):
        """
        Route to appropriate template based on task and model.
        
        Different models may need different prompting styles:
        - GPT models: Detailed, structured
        - Claude: Conversational, with XML tags
        - Llama: Concise, direct instructions
        """
        template_map = {
            ('code_review', 'gpt'): 'code_review_gpt.j2',
            ('code_review', 'claude'): 'code_review_claude.j2',
            ('code_review', 'llama'): 'code_review_llama.j2',
        }
        
        template_name = template_map.get(
            (task_type, model_type),
            f'{task_type}_default.j2'
        )
        
        template = self.env.get_template(template_name)
        return template.render(**kwargs)

# Usage
router = PromptRouter()

# For GPT
gpt_prompt = router.get_prompt(
    'code_review',
    'gpt',
    language='python',
    code='...'
)

# For Claude
claude_prompt = router.get_prompt(
    'code_review',
    'claude',
    language='python',
    code='...'
)
```

### 9.2 A/B Testing Prompts

Test different prompt variations:

```python
import random
from jinja2 import Environment, FileSystemLoader

class PromptABTester:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader('templates'))
        self.results = {'A': [], 'B': []}
    
    def get_variant_prompt(self, template_base, user_id, **kwargs):
        """
        Consistently assign users to variant A or B based on user_id.
        """
        # Consistent hashing for same user
        variant = 'A' if hash(user_id) % 2 == 0 else 'B'
        
        template_name = f'{template_base}_variant_{variant}.j2'
        template = self.env.get_template(template_name)
        
        return template.render(variant=variant, **kwargs), variant
    
    def log_result(self, variant, success, metrics):
        """Log results for analysis."""
        self.results[variant].append({
            'success': success,
            'metrics': metrics
        })
    
    def get_winning_variant(self):
        """Determine which variant performs better."""
        a_success_rate = sum(r['success'] for r in self.results['A']) / len(self.results['A'])
        b_success_rate = sum(r['success'] for r in self.results['B']) / len(self.results['B'])
        
        return 'A' if a_success_rate > b_success_rate else 'B'

# Usage
tester = PromptABTester()

prompt, variant = tester.get_variant_prompt(
    'customer_support',
    user_id='user123',
    issue_type='billing'
)

# ... use prompt and get response ...

tester.log_result(variant, success=True, metrics={'response_time': 2.3})
```

### 9.3 Localized Prompts

Create multilingual prompts:

**Template: `templates/support_base.j2`**
```jinja2
{% import 'translations/' + language + '.j2' as t %}

{{ t.greeting }}, {{ customer_name }}!

{{ t.issue_category }}: {{ issue_type }}

{{ t.our_team }} {{ t.help_you }}.

{% if urgency == 'high' %}
{{ t.priority_notice }}
{% endif %}

{{ t.thanks }},
{{ t.support_team }}
```

**Template: `templates/translations/en.j2`**
```jinja2
{% set greeting = "Hello" %}
{% set issue_category = "Issue Category" %}
{% set our_team = "Our team is here to" %}
{% set help_you = "help you" %}
{% set priority_notice = "We're treating this as high priority." %}
{% set thanks = "Thank you" %}
{% set support_team = "Support Team" %}
```

**Template: `templates/translations/es.j2`**
```jinja2
{% set greeting = "Hola" %}
{% set issue_category = "Categoría del problema" %}
{% set our_team = "Nuestro equipo está aquí para" %}
{% set help_you = "ayudarle" %}
{% set priority_notice = "Estamos tratando esto como alta prioridad." %}
{% set thanks = "Gracias" %}
{% set support_team = "Equipo de Soporte" %}
```

### 9.4 Prompt Chaining System

Chain multiple prompts together:

```python
from jinja2 import Environment, FileSystemLoader

class PromptChain:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader('templates'))
        self.chain = []
    
    def add_step(self, template_name, depends_on=None):
        """Add a step to the prompt chain."""
        self.chain.append({
            'template': template_name,
            'depends_on': depends_on
        })
        return self
    
    def execute(self, llm_client, initial_context):
        """Execute the prompt chain."""
        results = {}
        context = initial_context.copy()
        
        for i, step in enumerate(self.chain):
            # Wait for dependencies
            if step['depends_on']:
                context[step['depends_on']] = results[step['depends_on']]
            
            # Render template
            template = self.env.get_template(step['template'])
            prompt = template.render(**context)
            
            # Execute
            response = llm_client.generate(prompt)
            results[f'step_{i}'] = response
            
            # Add to context for next step
            context[f'previous_response'] = response
        
        return results

# Usage
chain = PromptChain()
chain.add_step('analyze_requirements.j2')
chain.add_step('generate_architecture.j2', depends_on='step_0')
chain.add_step('write_code.j2', depends_on='step_1')
chain.add_step('write_tests.j2', depends_on='step_2')

results = chain.execute(llm_client, {
    'project_description': 'Build a REST API for todo management'
})
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: Undefined Variable Errors

**Problem:**
```
jinja2.exceptions.UndefinedError: 'user_name' is undefined
```

**Solution:**
```jinja2
{# Option 1: Use default filter #}
Hello, {{ user_name | default('Guest') }}!

{# Option 2: Check if defined #}
{% if user_name is defined %}
Hello, {{ user_name }}!
{% endif %}

{# Option 3: Set default at top of template #}
{% set user_name = user_name | default('Guest') %}
```

#### Issue 2: Extra Whitespace in Output

**Problem:**
```
Output has too many blank lines or spaces
```

**Solution:**
```jinja2
{# Use whitespace control #}
{% for item in items -%}
{{ item }}
{%- endfor %}

{# Configure environment #}
```
```python
env = Environment(
    trim_blocks=True,
    lstrip_blocks=True
)
```

#### Issue 3: Template Not Found

**Problem:**
```
jinja2.exceptions.TemplateNotFound: my_template.j2
```

**Solution:**
```python
import os

# Debug: Check template directory
template_dir = 'templates'
print(f"Looking in: {os.path.abspath(template_dir)}")
print(f"Files: {os.listdir(template_dir)}")

# Ensure correct loader
env = Environment(loader=FileSystemLoader(template_dir))

# Use absolute path if needed
env = Environment(loader=FileSystemLoader('/absolute/path/to/templates'))
```

#### Issue 4: Slow Template Rendering

**Problem:**
```
Template rendering is taking too long
```

**Solution:**
```python
# 1. Cache compiled templates
env = Environment(
    loader=FileSystemLoader('templates'),
    auto_reload=False,  # Disable in production
    cache_size=400      # Increase cache size
)

# 2. Move complex logic to Python
# ❌ Slow
{% for item in items %}
  {% if complex_function(item) %}
    {{ item }}
  {% endif %}
{% endfor %}

# ✅ Fast
preprocessed = [item for item in items if complex_function(item)]
{{ preprocessed }}

# 3. Use bytecode cache
from jinja2 import FileSystemBytecodeCache
env = Environment(
    loader=FileSystemLoader('templates'),
    bytecode_cache=FileSystemBytecodeCache('/tmp/jinja_cache')
)
```

#### Issue 5: Special Characters Breaking Templates

**Problem:**
```
Characters like {{, }}, {%, %} in content break the template
```

**Solution:**
```jinja2
{# Option 1: Use raw block #}
{% raw %}
This text contains {{ special }} characters
{% endraw %}

{# Option 2: Escape with variable delimiter #}
{{ '{{' }} this looks like a variable {{ '}}' }}

{# Option 3: Use string literals #}
{% set code_example = "{{ variable }}" %}
```

#### Issue 6: Recursive Include Errors

**Problem:**
```
Template includes itself, causing recursion
```

**Solution:**
```jinja2
{# Avoid circular includes #}
{# ❌ Bad: a.j2 includes b.j2, b.j2 includes a.j2 #}

{# ✅ Good: Use template inheritance or macros instead #}
{% extends 'base.j2' %}

{# Or use a flag to prevent recursion #}
{% if not already_included %}
  {% set already_included = true %}
  {% include 'partial.j2' %}
{% endif %}
```

### Debugging Tips

**1. Enable Debug Mode:**
```python
from jinja2 import Environment, DebugUndefined

env = Environment(
    undefined=DebugUndefined  # Shows undefined variables in output
)
```

**2. Print Variable Values:**
```jinja2
{# Debug output #}
<!-- DEBUG: user_name = {{ user_name }} -->
<!-- DEBUG: items length = {{ items | length }} -->
```

**3. Use Template Comments for Logging:**
```jinja2
{# Entering loop: {{ items | length }} items #}
{% for item in items %}
  {# Processing item {{ loop.index }} #}
  {{ item }}
{% endfor %}
{# Loop complete #}
```

**4. Validate Context Before Rendering:**
```python
def validate_context(template_name, context):
    """Validate that context has all required variables."""
    required_vars = {
        'code_review.j2': ['language', 'code_snippet'],
        'customer_support.j2': ['customer_tier', 'issue_type'],
    }
    
    required = required_vars.get(template_name, [])
    missing = [var for var in required if var not in context]
    
    if missing:
        raise ValueError(f"Missing required variables: {missing}")
    
    return True
```

---

## Conclusion

Jinja2 is an essential tool for modern prompt engineering in Gen AI applications. By mastering its features—from basic variable interpolation to advanced macros and template inheritance—you can create sophisticated, maintainable, and scalable prompt systems.

### Key Takeaways

1. **Separate concerns**: Keep prompts in templates, logic in code
2. **Use structure**: Organize templates logically with clear naming
3. **Be consistent**: Standardize variable names and patterns
4. **Handle errors**: Validate inputs and provide defaults
5. **Optimize**: Cache templates and minimize complex logic
6. **Test thoroughly**: Unit test templates like you test code
7. **Document well**: Comment templates and track versions

### Next Steps

1. Start with simple templates for your most common prompts
2. Build a library of reusable macros and base templates
3. Implement A/B testing to optimize prompt effectiveness
4. Create a style guide for your team's template patterns
5. Monitor and iterate based on LLM response quality

### Additional Resources

- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [Template Designer Documentation](https://jinja.palletsprojects.com/en/latest/templates/)
- [API Reference](https://jinja.palletsprojects.com/en/latest/api/)

---

**Version:** 1.0.0  
**Last Updated:** February 2026  
**Author:** MicroDegree - Gen AI Developers Team