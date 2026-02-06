# Part 1: Assignments

## Overview
These 8 assignments are designed to reinforce and expand upon the concepts covered in Modules 1-4 of the Gen AI Developer Track. Each assignment includes learning objectives, detailed instructions, evaluation criteria, and expected deliverables.

---

## Assignment 1: AI Model Comparison Dashboard

### Learning Objectives
- Understand differences between AI, ML, DL, and Gen AI
- Compare foundation models across different providers
- Evaluate model capabilities for various use cases
- Practice responsible AI assessment

### Description
Build a comparative analysis of at least 5 different LLMs (e.g., GPT-4, Claude, Gemini, Llama, Mistral) across multiple dimensions including capabilities, pricing, context windows, and use cases.

### Tasks

1. **Research Phase**
   - Document the architecture type (transformer, mixture of experts, etc.)
   - Identify whether models are foundation, fine-tuned, or multimodal
   - Note training data cutoff dates and context window sizes
   - Research pricing models for each API

2. **Testing Phase**
   - Design 5 standardized test prompts covering:
     - Creative writing
     - Code generation
     - Data analysis
     - Reasoning and logic
     - Multilingual capabilities
   - Execute each prompt across all models
   - Document response quality, speed, and accuracy

3. **Analysis Phase**
   - Create a comparison matrix with scores (1-10) for each dimension
   - Identify strengths and weaknesses of each model
   - Recommend models for specific business scenarios
   - Document any bias or ethical concerns observed

### Deliverables
- **Markdown Report** (2000-3000 words) with:
  - Executive summary with key findings
  - Detailed comparison tables
  - Sample outputs from each model
  - Use case recommendations
  - Ethical considerations and limitations

### Evaluation Criteria
- Comprehensiveness of research (25%)
- Quality of test prompts and methodology (25%)
- Depth of analysis and insights (30%)
- Practical recommendations (20%)

---

## Assignment 2: Prompt Engineering Playground

### Learning Objectives
- Master advanced prompt engineering techniques
- Understand temperature, top-p, and other parameters
- Apply various prompt patterns effectively
- Practice prompt injection safety

### Description
Create a Python-based prompt engineering toolkit that demonstrates mastery of different prompting strategies and parameters.

### Tasks

1. **Build a Prompt Pattern Library**
   - Implement at least 8 prompt patterns:
     - Zero-shot prompting
     - Few-shot prompting (3-5 examples)
     - Chain-of-thought reasoning
     - Role-based prompting
     - Persona pattern
     - Template pattern
     - Meta-prompting
     - Reflection pattern

2. **Parameter Exploration**
   - Create experiments showing the impact of:
     - Temperature (0.0, 0.5, 0.7, 1.0, 1.5)
     - Top-p (0.1, 0.5, 0.9, 1.0)
     - Max tokens
     - Frequency/presence penalties
   - Document outcomes for each parameter combination

3. **Safety Testing**
   - Test for prompt injection vulnerabilities
   - Implement guardrails to prevent:
     - Harmful content generation
     - PII leakage
     - Jailbreak attempts
   - Create a safe prompt wrapper class

### Deliverables
- **Python Script(s)** with:
  - Modular functions for each prompt pattern
  - Parameter experimentation framework
  - Safety validation layer
  - Comprehensive docstrings

- **Jupyter Notebook** demonstrating:
  - Each prompt pattern with real examples
  - Parameter impact visualization
  - Safety testing results

- **README.md** with:
  - Usage instructions
  - Best practices guide
  - When to use each pattern

### Evaluation Criteria
- Code quality and modularity (25%)
- Diversity and effectiveness of patterns (30%)
- Parameter analysis depth (20%)
- Safety implementations (25%)

---

## Assignment 3: Multi-Provider API Integration Framework

### Learning Objectives
- Master REST API concepts and authentication
- Integrate multiple LLM providers (OpenAI, Bedrock, Gemini, Ollama)
- Implement error handling and retry logic
- Create normalized response formats

### Description
Build a production-ready Python framework that provides a unified interface to interact with multiple LLM providers, with features like automatic failover, response caching, and cost tracking.

### Tasks

1. **Core API Integration**
   - Implement clients for:
     - OpenAI (GPT-4, GPT-3.5)
     - Amazon Bedrock (Claude, Llama)
     - Google Gemini
     - Ollama (local models)
   - Handle authentication for each provider
   - Use environment variables for API keys

2. **Advanced Features**
   - **Unified Interface**: Single method to call any provider
   - **Response Normalization**: Standardize outputs across providers
   - **Error Handling**: Retry logic with exponential backoff
   - **Automatic Failover**: Switch providers on failure
   - **Cost Tracking**: Log token usage and estimated costs
   - **Response Caching**: Avoid duplicate API calls
   - **Async Support**: Implement async methods for batch processing

3. **Validation Layer**
   - Use Pydantic for:
     - Request validation
     - Response validation
     - Configuration management
   - Type hints throughout

4. **Logging & Monitoring**
   - Structured logging for all API calls
   - Performance metrics (latency, tokens/sec)
   - Error rate tracking

### Deliverables
- **Python Package** with:
  - `llm_client.py` - Main client class
  - `providers/` - Individual provider implementations
  - `models.py` - Pydantic models
  - `utils.py` - Helper functions
  - `config.py` - Configuration management

- **Test Suite** with:
  - Unit tests for each provider
  - Integration tests
  - Mock API responses for testing

- **Documentation** with:
  - API reference
  - Usage examples
  - Configuration guide
  - Troubleshooting section

### Evaluation Criteria
- Code architecture and design patterns (30%)
- Error handling and resilience (25%)
- Feature completeness (25%)
- Documentation quality (20%)

---

## Assignment 4: Dynamic Prompt Template System

### Learning Objectives
- Master Jinja2 templating for prompts
- Build reusable prompt components
- Implement context management strategies
- Create domain-specific prompt libraries

### Description
Develop a sophisticated prompt templating system that allows dynamic generation of prompts for various business scenarios with variable substitution, conditional logic, and template inheritance.

### Tasks

1. **Template Architecture**
   - Create base templates for:
     - Data analysis tasks
     - Content generation
     - Code review and generation
     - Customer service responses
     - Report summarization
   - Implement template inheritance
   - Add macros for reusable components

2. **Dynamic Variable System**
   - Support multiple variable types:
     - Strings, numbers, lists, dicts
     - Nested objects
     - Optional parameters with defaults
   - Implement validators for required variables
   - Add type checking

3. **Context Management**
   - Track conversation history
   - Implement sliding window context
   - Calculate and manage token limits
   - Optimize context for different models

4. **Prompt Library**
   - Create 15+ production-ready templates for:
     - Text summarization (different lengths)
     - Sentiment analysis
     - Entity extraction
     - Translation with style preservation
     - Question answering
     - Code explanation and debugging
     - Email drafting (formal, casual, persuasive)
     - Meeting notes generation

5. **Testing Framework**
   - Unit tests for each template
   - Validation tests for variable substitution
   - Integration tests with real LLM APIs

### Deliverables
- **Template Library** with:
  - `templates/` - Jinja2 template files organized by category
  - `template_manager.py` - Template loading and rendering
  - `validators.py` - Input validation logic
  - `context_manager.py` - Context optimization

- **Example Applications**:
  - CLI tool to use templates
  - Jupyter notebook with demonstrations

- **Documentation**:
  - Template reference guide
  - Best practices for prompt design
  - Variable naming conventions

### Evaluation Criteria
- Template design and reusability (30%)
- Context management implementation (25%)
- Library comprehensiveness (25%)
- Code quality and testing (20%)

---

## Assignment 5: Intelligent Document Processing Pipeline

### Learning Objectives
- Understand document chunking strategies
- Implement different embedding techniques
- Compare embedding models and metrics
- Build semantic search capabilities

### Description
Create an end-to-end document processing pipeline that ingests various document formats, chunks them intelligently, generates embeddings, and enables semantic search.

### Tasks

1. **Document Ingestion**
   - Support multiple formats:
     - PDF (with OCR for scanned docs)
     - DOCX
     - TXT
     - Markdown
     - HTML
     - JSON/CSV
   - Extract metadata (title, author, date, etc.)
   - Handle multi-page documents

2. **Chunking Strategies**
   - Implement at least 4 chunking methods:
     - Fixed-size chunking (with overlap)
     - Sentence-based chunking
     - Paragraph-based chunking
     - Semantic chunking (using embeddings)
   - Create comparative analysis of each method
   - Auto-select best strategy based on document type

3. **Embedding Generation**
   - Integrate multiple embedding models:
     - OpenAI text-embedding-3-small/large
     - Sentence-transformers (all-MiniLM-L6-v2)
     - Cohere embeddings
   - Batch processing for efficiency
   - Cache embeddings to avoid recomputation

4. **Similarity Search**
   - Implement distance metrics:
     - Cosine similarity
     - Euclidean distance
     - Dot product
   - Compare metrics on same dataset
   - Visualize embedding spaces using UMAP/t-SNE

5. **Quality Metrics**
   - Calculate chunking quality scores
   - Measure retrieval accuracy
   - Track processing time and costs

### Deliverables
- **Python Package** with:
  - `document_loader.py` - Multi-format ingestion
  - `chunker.py` - Chunking strategies
  - `embedder.py` - Embedding generation
  - `search.py` - Semantic search engine
  - `metrics.py` - Quality evaluation

- **Jupyter Notebook** with:
  - Comparative analysis of chunking methods
  - Embedding model benchmarks
  - Visualization of embedding spaces

- **Test Dataset**:
  - Sample documents (10+ across different formats)
  - Ground truth for retrieval evaluation

- **Report** (Markdown):
  - Methodology explanation
  - Benchmark results
  - Recommendations for different use cases

### Evaluation Criteria
- Implementation completeness (30%)
- Chunking strategy effectiveness (25%)
- Analysis depth and insights (25%)
- Code quality and documentation (20%)

---

## Assignment 6: Advanced RAG System with Hybrid Search

### Learning Objectives
- Build production-ready RAG pipelines
- Implement hybrid search (semantic + keyword)
- Integrate vector databases (Chroma, Pinecone)
- Optimize retrieval quality

### Description
Develop an advanced RAG system that combines semantic search with traditional keyword search, implements reranking, and provides explainable results with source citations.

### Tasks

1. **Vector Database Setup**
   - Implement dual database support:
     - Chroma (local development)
     - Pinecone (production deployment)
   - Create migration utilities between databases
   - Implement collection management (create, update, delete)

2. **Hybrid Search Engine**
   - **Semantic Search**: Vector similarity using embeddings
   - **Keyword Search**: BM25 or TF-IDF
   - **Hybrid Fusion**: Combine results using:
     - Reciprocal Rank Fusion (RRF)
     - Weighted scoring
     - Learned fusion (optional)
   - Implement configurable weights

3. **Reranking Layer**
   - Implement cross-encoder reranking
   - Add diversity filtering to avoid redundant results
   - Implement MMR (Maximal Marginal Relevance)

4. **Query Enhancement**
   - Query expansion using LLMs
   - Hypothetical document embeddings (HyDE)
   - Multi-query generation for comprehensive retrieval

5. **Response Generation**
   - Retrieve top-k relevant chunks
   - Build context-aware prompts
   - Generate answers with source citations
   - Implement answer validation (check if grounded in sources)

6. **Evaluation Framework**
   - Create test queries with ground truth
   - Measure:
     - Retrieval precision and recall
     - Answer accuracy
     - Response latency
   - A/B test different configurations

### Deliverables
- **RAG Application** with:
  - `vector_store.py` - Database abstraction layer
  - `retriever.py` - Hybrid search implementation
  - `reranker.py` - Reranking logic
  - `generator.py` - Response generation with citations
  - `evaluator.py` - Quality metrics

- **Configuration System**:
  - YAML configs for different RAG strategies
  - Environment-based settings

- **Demo Application**:
  - Streamlit UI for testing the RAG system
  - Display retrieved chunks with relevance scores
  - Show source citations

- **Evaluation Report** (Markdown):
  - Benchmark different RAG configurations
  - Ablation study (impact of each component)
  - Recommendations and trade-offs

### Evaluation Criteria
- RAG architecture quality (30%)
- Retrieval accuracy and relevance (30%)
- Implementation completeness (25%)
- Evaluation rigor (15%)

---

## Assignment 7: AI Ethics and Bias Detection System

### Learning Objectives
- Understand AI ethics, bias, and fairness
- Detect and mitigate bias in LLM outputs
- Implement responsible AI practices
- Create governance frameworks

### Description
Build a comprehensive system to detect, measure, and mitigate various types of bias in LLM outputs, with a focus on fairness, privacy, and responsible AI deployment.

### Tasks

1. **Bias Detection Framework**
   - Test for multiple bias types:
     - Gender bias
     - Racial/ethnic bias
     - Age bias
     - Geographic/cultural bias
     - Socioeconomic bias
   - Create standardized test prompts for each category
   - Measure bias using quantitative metrics

2. **Automated Testing Suite**
   - Generate diverse test cases programmatically
   - Test LLMs with:
     - Name variation tests (different ethnic names)
     - Pronoun consistency tests
     - Stereotype detection
     - Counterfactual evaluations
   - Score outputs for fairness

3. **Privacy Protection**
   - Implement PII detection in:
     - Input prompts
     - LLM outputs
   - Create redaction/anonymization utilities
   - Test for data leakage scenarios

4. **Mitigation Strategies**
   - Pre-processing: Prompt engineering to reduce bias
   - In-processing: Use system prompts for fairness
   - Post-processing: Filter and adjust biased outputs
   - Compare effectiveness of each approach

5. **Governance Dashboard**
   - Track bias metrics over time
   - Log all LLM interactions
   - Create audit trails
   - Generate compliance reports

6. **Responsible AI Checklist**
   - Create deployment checklist covering:
     - Model selection criteria
     - Bias testing requirements
     - Privacy safeguards
     - Monitoring procedures
     - Incident response plan

### Deliverables
- **Python Package** with:
  - `bias_detector.py` - Bias testing framework
  - `privacy_guard.py` - PII detection and redaction
  - `mitigation.py` - Bias reduction strategies
  - `governance.py` - Audit logging and reporting

- **Test Suite**:
  - 100+ test cases across bias categories
  - Benchmark results for major LLMs
  - Comparison report

- **Dashboard** (Streamlit):
  - Real-time bias monitoring
  - Historical trends
  - Compliance reporting

- **Documentation**:
  - Ethical AI guidelines
  - Bias mitigation playbook
  - Governance framework

### Evaluation Criteria
- Comprehensiveness of bias testing (30%)
- Privacy protection implementation (25%)
- Mitigation strategy effectiveness (25%)
- Documentation and governance (20%)

---

## Assignment 8: End-to-End GenAI Application: Research Assistant

### Learning Objectives
- Integrate all Part 1 concepts into a production application
- Combine prompt engineering, API integration, and RAG
- Implement user-friendly interfaces
- Deploy with proper error handling and monitoring

### Description
Build a complete research assistant application that helps users analyze academic papers, generate summaries, answer questions, and synthesize insights from multiple sources using RAG and advanced prompting.

### Tasks

1. **Document Management**
   - Upload and process research papers (PDFs)
   - Extract metadata (title, authors, abstract, citations)
   - Organize papers by topic/tags
   - Support batch uploads

2. **Intelligent Processing**
   - Chunk papers using optimal strategy
   - Generate embeddings and store in vector DB
   - Extract key entities (methods, datasets, metrics)
   - Generate structured summaries

3. **Query Interface**
   - Support multiple query types:
     - Simple Q&A ("What datasets were used?")
     - Comparative analysis ("Compare methods in papers A and B")
     - Literature review ("Summarize recent trends in X")
     - Citation network exploration
   - Use appropriate prompt patterns for each query type

4. **Advanced Features**
   - **Multi-document synthesis**: Combine insights from multiple papers
   - **Claim verification**: Check if claims are supported by papers
   - **Research gap identification**: Find understudied areas
   - **Automatic bibliography generation**
   - **Key findings extraction**: Generate bullet points of main contributions

5. **User Interface**
   - Build Streamlit application with:
     - Document upload and management
     - Interactive chat interface
     - Source citation display
     - Export functionality (PDF reports)
   - Add visualization:
     - Citation graphs
     - Topic clustering
     - Timeline of research evolution

6. **Prompt Engineering**
   - Create specialized prompts for:
     - Academic summarization
     - Critical analysis
     - Methodology extraction
     - Future work suggestions
   - Implement chain-of-thought for complex queries

7. **Quality Assurance**
   - Validate retrieved sources
   - Check for hallucinations
   - Ensure proper citations
   - Implement confidence scoring

8. **Performance Optimization**
   - Cache common queries
   - Implement async processing for uploads
   - Optimize vector search parameters
   - Monitor API costs

### Deliverables
- **Complete Application** with:
  - `app.py` - Main Streamlit application
  - `document_processor.py` - PDF processing and chunking
  - `rag_engine.py` - RAG implementation
  - `prompt_library.py` - Academic prompt templates
  - `research_agent.py` - Query orchestration
  - `utils.py` - Helper functions

- **Configuration**:
  - `.env.example` - Environment variables template
  - `config.yaml` - Application settings
  - `requirements.txt` - Dependencies

- **Documentation**:
  - `README.md` - Setup and usage guide
  - `ARCHITECTURE.md` - System design explanation
  - `API_GUIDE.md` - API integration documentation
  - `USER_GUIDE.md` - End-user instructions

- **Demo Materials**:
  - Video walkthrough (5-10 minutes)
  - Sample research papers for testing
  - Example queries and expected outputs

- **Testing**:
  - Unit tests for core functions
  - Integration tests
  - Test dataset with ground truth

### Evaluation Criteria
- Feature completeness and functionality (30%)
- Code quality and architecture (25%)
- User experience and interface design (20%)
- Documentation and deployment readiness (15%)
- Innovation and advanced features (10%)

---

## General Submission Guidelines

### Code Quality Standards
- Follow PEP 8 style guidelines
- Use type hints throughout
- Write comprehensive docstrings
- Include inline comments for complex logic
- Maintain consistent naming conventions

### Documentation Requirements
- README with clear setup instructions
- API documentation for all major functions/classes
- Architecture diagrams where applicable
- Usage examples and tutorials

### Version Control
- Use Git for version control
- Write meaningful commit messages
- Create branches for major features
- Include .gitignore for sensitive files

### Testing
- Minimum 70% code coverage for unit tests
- Include integration tests
- Test edge cases and error conditions
- Document test scenarios

### Deliverable Format
- Submit as GitHub repository (or zip file)
- Include all code, documentation, and test files
- Add sample data/examples where applicable
- Provide environment setup instructions

---

## Assessment Rubric

Each assignment will be evaluated on:

1. **Technical Implementation (40%)**
   - Correctness and completeness
   - Code quality and organization
   - Error handling and edge cases
   - Performance optimization

2. **Understanding of Concepts (30%)**
   - Proper application of learned techniques
   - Depth of analysis and insights
   - Innovation and creativity

3. **Documentation (20%)**
   - Code documentation
   - User guides and README
   - Technical explanations
   - Architecture decisions

4. **Presentation (10%)**
   - Code readability
   - Project organization
   - Demo quality (where applicable)
   - Professional polish

---

## Additional Resources

### Recommended Tools
- **IDEs**: VSCode, PyCharm, Jupyter Lab
- **Version Control**: Git, GitHub/GitLab
- **Testing**: pytest, unittest
- **Documentation**: Sphinx, MkDocs
- **Visualization**: Matplotlib, Plotly, Seaborn

### Learning Resources
- OpenAI API Documentation
- LangChain Documentation
- Hugging Face Transformers Guide
- AWS Bedrock Documentation
- Google Gemini API Guide

### Support
- Office hours: [Schedule]
- Discussion forum: [Link]
- Mentor contact: [Email]

---

## Timeline Recommendations

- **Assignments 1-2**: Week 1-2 (Module 1-2 coverage)
- **Assignments 3-4**: Week 2-3 (Module 2-3 coverage)
- **Assignments 5-6**: Week 3-4 (Module 4 coverage)
- **Assignment 7**: Week 4 (Ethics across all modules)
- **Assignment 8**: Week 4 (Capstone integration)

Each assignment should take 8-12 hours to complete thoroughly.

---

## Notes

1. **Start Early**: Don't wait until the deadline to begin
2. **Ask Questions**: Reach out to mentors when stuck
3. **Iterate**: Submit drafts for feedback before final submission
4. **Collaborate**: Discuss concepts with peers (but submit individual work)
5. **Document**: Keep notes on your learning process
6. **Test Thoroughly**: Don't skip testing and validation
7. **Think Production**: Write code as if it will be deployed
8. **Stay Curious**: Experiment beyond minimum requirements

Good luck with your assignments!