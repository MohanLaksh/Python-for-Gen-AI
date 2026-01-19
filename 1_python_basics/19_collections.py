"""
Python Collections Module - Detailed Examples for Gen AI Developers
====================================================================
This module demonstrates advanced Python collections with practical examples
relevant to AI/ML and Gen AI development workflows.
"""

from collections import Counter, deque, defaultdict, namedtuple, OrderedDict, ChainMap
from typing import List, Dict
import json


print("=" * 80)
print("PYTHON COLLECTIONS FOR GEN AI DEVELOPERS")
print("=" * 80)


# =============================================================================
# 1. Counter - Count hashable objects (Perfect for token/word frequency analysis)
# =============================================================================
print("\n" + "=" * 80)
print("1. COUNTER - Token and Word Frequency Analysis")
print("=" * 80)

# Example 1.1: Token frequency in AI-generated text
ai_response = """
The future of artificial intelligence is bright. Artificial intelligence 
will transform how we work and live. Intelligence augmentation through AI 
will enhance human capabilities.
"""

# Tokenize and count words
words = ai_response.lower().split()
word_counter = Counter(words)

print("\n--- Token Frequency Analysis ---")
print(f"Total tokens: {sum(word_counter.values())}")
print(f"Unique tokens: {len(word_counter)}")
print(f"\nTop 5 most common tokens:")
for word, count in word_counter.most_common(5):
    print(f"  '{word}': {count} occurrences")

# Example 1.2: Character frequency for tokenizer analysis
text_sample = "Hello, AI! How are you today?"
char_counter = Counter(text_sample.lower())
print(f"\n--- Character Frequency ---")
print(f"Most common characters: {char_counter.most_common(5)}")

# Example 1.3: Counting model predictions (useful for ensemble models)
model_predictions = ['positive', 'positive', 'negative', 'positive', 
                     'neutral', 'positive', 'negative', 'neutral']
prediction_counter = Counter(model_predictions)
print(f"\n--- Model Prediction Distribution ---")
for sentiment, count in prediction_counter.items():
    percentage = (count / len(model_predictions)) * 100
    print(f"  {sentiment}: {count} ({percentage:.1f}%)")

# Example 1.4: Finding most common labels in a dataset
labels = ['cat', 'dog', 'cat', 'bird', 'cat', 'dog', 'fish', 'cat', 'bird']
label_counter = Counter(labels)
most_common_label = label_counter.most_common(1)[0]
print(f"\n--- Dataset Label Analysis ---")
print(f"Most common label: '{most_common_label[0]}' with {most_common_label[1]} instances")
print(f"Class distribution: {dict(label_counter)}")


# =============================================================================
# 2. deque - Double-ended queue (Perfect for conversation history & sliding windows)
# =============================================================================
print("\n" + "=" * 80)
print("2. DEQUE - Conversation History & Sliding Window Management")
print("=" * 80)

# Example 2.1: Conversation history with limited context window
print("\n--- Chat History with Limited Context (LLM Memory) ---")
conversation_history = deque(maxlen=5)  # Keep only last 5 messages

messages = [
    "User: Hello!",
    "AI: Hi! How can I help you?",
    "User: What's the weather?",
    "AI: I don't have real-time weather data.",
    "User: Can you write code?",
    "AI: Yes, I can help with coding!",
    "User: Write a Python function",
    "AI: Here's a function for you..."
]

for msg in messages:
    conversation_history.append(msg)
    print(f"Added: {msg}")

print(f"\n--- Current Context Window (Last {conversation_history.maxlen} messages) ---")
for i, msg in enumerate(conversation_history, 1):
    print(f"{i}. {msg}")

# Example 2.2: Sliding window for time-series data (useful for streaming data)
print("\n--- Sliding Window for Real-time Token Processing ---")
token_stream = deque(maxlen=10)  # Process last 10 tokens

incoming_tokens = ["The", "quick", "brown", "fox", "jumps", "over", "the", 
                   "lazy", "dog", "in", "the", "forest", "today"]

for token in incoming_tokens:
    token_stream.append(token)
    if len(token_stream) == token_stream.maxlen:
        print(f"Current window: {' '.join(token_stream)}")

# Example 2.3: Efficient queue operations for batch processing
print("\n--- Batch Processing Queue ---")
processing_queue = deque(['task1', 'task2', 'task3', 'task4'])
print(f"Initial queue: {list(processing_queue)}")

# Process from left (FIFO)
processed = processing_queue.popleft()
print(f"Processed (FIFO): {processed}")
print(f"Remaining: {list(processing_queue)}")

# Add urgent task to front
processing_queue.appendleft('urgent_task')
print(f"After adding urgent task: {list(processing_queue)}")

# Add new task to end
processing_queue.append('task5')
print(f"After adding new task: {list(processing_queue)}")


# =============================================================================
# 3. defaultdict - Dictionary with default values (Perfect for grouping & counting)
# =============================================================================
print("\n" + "=" * 80)
print("3. DEFAULTDICT - Automatic Default Values for Data Grouping")
print("=" * 80)

# Example 3.1: Grouping training samples by label
print("\n--- Grouping Training Samples by Label ---")
samples_by_label = defaultdict(list)

training_data = [
    ("Sample text 1", "positive"),
    ("Sample text 2", "negative"),
    ("Sample text 3", "positive"),
    ("Sample text 4", "neutral"),
    ("Sample text 5", "positive"),
    ("Sample text 6", "negative"),
]

for text, label in training_data:
    samples_by_label[label].append(text)

for label, samples in samples_by_label.items():
    print(f"{label}: {len(samples)} samples")
    for sample in samples:
        print(f"  - {sample}")

# Example 3.2: Counting token occurrences per document
print("\n--- Token Occurrences Per Document ---")
token_docs = defaultdict(int)

documents = [
    "AI is transforming the world",
    "Machine learning is a subset of AI",
    "AI applications are everywhere"
]

for doc_id, doc in enumerate(documents):
    if 'AI' in doc:
        token_docs[f'doc_{doc_id}'] += doc.count('AI')

print(f"Documents containing 'AI': {dict(token_docs)}")

# Example 3.3: Building an inverted index for search
print("\n--- Inverted Index for Document Search ---")
inverted_index = defaultdict(set)

docs = {
    'doc1': 'artificial intelligence machine learning',
    'doc2': 'deep learning neural networks',
    'doc3': 'machine learning algorithms',
    'doc4': 'artificial neural networks'
}

for doc_id, content in docs.items():
    for word in content.split():
        inverted_index[word].add(doc_id)

print("Inverted Index:")
for word, doc_ids in sorted(inverted_index.items()):
    print(f"  '{word}': found in {sorted(doc_ids)}")

# Example 3.4: Tracking model metrics by epoch
print("\n--- Model Training Metrics by Epoch ---")
metrics = defaultdict(list)

# Simulating training loop
training_logs = [
    (1, 'loss', 0.5),
    (1, 'accuracy', 0.85),
    (2, 'loss', 0.3),
    (2, 'accuracy', 0.90),
    (3, 'loss', 0.2),
    (3, 'accuracy', 0.93),
]

for epoch, metric_name, value in training_logs:
    metrics[metric_name].append((epoch, value))

for metric_name, values in metrics.items():
    print(f"{metric_name}: {values}")


# =============================================================================
# 4. namedtuple - Lightweight, immutable data structures
# =============================================================================
print("\n" + "=" * 80)
print("4. NAMEDTUPLE - Structured Data for AI/ML Workflows")
print("=" * 80)

# Example 4.1: Model configuration
print("\n--- Model Configuration ---")
ModelConfig = namedtuple('ModelConfig', ['name', 'layers', 'learning_rate', 'batch_size'])

config1 = ModelConfig(name='GPT-Mini', layers=12, learning_rate=0.001, batch_size=32)
config2 = ModelConfig(name='BERT-Base', layers=12, learning_rate=0.0001, batch_size=16)

print(f"Config 1: {config1.name}, {config1.layers} layers, LR={config1.learning_rate}")
print(f"Config 2: {config2.name}, {config2.layers} layers, LR={config2.learning_rate}")

# Example 4.2: Training sample structure
print("\n--- Training Sample Structure ---")
TrainingSample = namedtuple('TrainingSample', ['text', 'label', 'confidence', 'source'])

sample1 = TrainingSample(
    text="This product is amazing!",
    label="positive",
    confidence=0.95,
    source="user_reviews"
)

sample2 = TrainingSample(
    text="Terrible experience, would not recommend",
    label="negative",
    confidence=0.88,
    source="user_reviews"
)

print(f"Sample 1: {sample1.label} ({sample1.confidence:.2f}) - '{sample1.text}'")
print(f"Sample 2: {sample2.label} ({sample2.confidence:.2f}) - '{sample2.text}'")

# Example 4.3: Token with metadata
print("\n--- Token with Metadata ---")
Token = namedtuple('Token', ['text', 'pos_tag', 'entity_type', 'start_idx', 'end_idx'])

tokens = [
    Token('OpenAI', 'PROPN', 'ORG', 0, 6),
    Token('released', 'VERB', None, 7, 15),
    Token('GPT-4', 'PROPN', 'PRODUCT', 16, 21),
]

print("Tokenized entities:")
for token in tokens:
    if token.entity_type:
        print(f"  {token.text} ({token.entity_type}) at position {token.start_idx}-{token.end_idx}")

# Example 4.4: Model prediction result
print("\n--- Model Prediction Result ---")
Prediction = namedtuple('Prediction', ['class_name', 'probability', 'model_version', 'timestamp'])

prediction = Prediction(
    class_name='spam',
    probability=0.92,
    model_version='v2.1.0',
    timestamp='2026-01-16T21:30:00'
)

print(f"Prediction: {prediction.class_name} (confidence: {prediction.probability:.2%})")
print(f"Model: {prediction.model_version}, Time: {prediction.timestamp}")


# =============================================================================
# 5. OrderedDict - Dictionary that maintains insertion order
# =============================================================================
print("\n" + "=" * 80)
print("5. ORDEREDDICT - Maintaining Order in Configurations")
print("=" * 80)

# Example 5.1: Layer configuration in neural network
print("\n--- Neural Network Layer Configuration ---")
network_layers = OrderedDict()
network_layers['input'] = {'type': 'Dense', 'units': 784, 'activation': None}
network_layers['hidden1'] = {'type': 'Dense', 'units': 256, 'activation': 'relu'}
network_layers['hidden2'] = {'type': 'Dense', 'units': 128, 'activation': 'relu'}
network_layers['output'] = {'type': 'Dense', 'units': 10, 'activation': 'softmax'}

print("Network Architecture (in order):")
for i, (layer_name, config) in enumerate(network_layers.items(), 1):
    print(f"  Layer {i} ({layer_name}): {config['type']} - {config['units']} units")

# Example 5.2: Processing pipeline stages
print("\n--- Data Processing Pipeline ---")
pipeline = OrderedDict()
pipeline['load_data'] = 'Load raw text data'
pipeline['tokenize'] = 'Tokenize text into words'
pipeline['normalize'] = 'Normalize and clean tokens'
pipeline['vectorize'] = 'Convert to numerical vectors'
pipeline['train'] = 'Train the model'

print("Pipeline stages (must execute in order):")
for step_num, (stage, description) in enumerate(pipeline.items(), 1):
    print(f"  Step {step_num}: {stage} - {description}")

# Example 5.3: Experiment tracking with chronological order
print("\n--- Experiment Results (Chronological) ---")
experiments = OrderedDict()
experiments['exp_001'] = {'accuracy': 0.85, 'loss': 0.45, 'date': '2026-01-10'}
experiments['exp_002'] = {'accuracy': 0.88, 'loss': 0.38, 'date': '2026-01-12'}
experiments['exp_003'] = {'accuracy': 0.91, 'loss': 0.32, 'date': '2026-01-15'}

print("Experiment history:")
for exp_id, results in experiments.items():
    print(f"  {exp_id} ({results['date']}): Acc={results['accuracy']:.2%}, Loss={results['loss']:.2f}")


# =============================================================================
# 6. ChainMap - Chain multiple dictionaries
# =============================================================================
print("\n" + "=" * 80)
print("6. CHAINMAP - Hierarchical Configuration Management")
print("=" * 80)

# Example 6.1: Configuration hierarchy (default -> user -> runtime)
print("\n--- Hierarchical Model Configuration ---")
default_config = {
    'model_name': 'default-model',
    'max_tokens': 100,
    'temperature': 0.7,
    'top_p': 0.9,
    'frequency_penalty': 0.0
}

user_config = {
    'model_name': 'gpt-4',
    'max_tokens': 500,
    'temperature': 0.8
}

runtime_config = {
    'temperature': 0.9,
    'stream': True
}

# ChainMap searches in order: runtime -> user -> default
final_config = ChainMap(runtime_config, user_config, default_config)

print("Final configuration (runtime overrides user overrides default):")
for key in ['model_name', 'max_tokens', 'temperature', 'top_p', 'stream']:
    value = final_config.get(key, 'Not set')
    print(f"  {key}: {value}")

# Example 6.2: Environment-specific settings
print("\n--- Environment-Specific Settings ---")
production_settings = {
    'api_endpoint': 'https://api.production.com',
    'timeout': 30,
    'retry_count': 3
}

development_settings = {
    'api_endpoint': 'https://api.dev.com',
    'debug': True,
    'timeout': 60
}

base_settings = {
    'timeout': 10,
    'retry_count': 1,
    'debug': False,
    'log_level': 'INFO'
}

# Simulate production environment
env = 'production'
if env == 'production':
    settings = ChainMap(production_settings, base_settings)
else:
    settings = ChainMap(development_settings, base_settings)

print(f"Settings for {env} environment:")
print(f"  API Endpoint: {settings['api_endpoint']}")
print(f"  Timeout: {settings['timeout']}s")
print(f"  Retry Count: {settings['retry_count']}")
print(f"  Debug Mode: {settings['debug']}")


# =============================================================================
# 7. PRACTICAL COMBINED EXAMPLE - Building a Simple RAG System Component
# =============================================================================
print("\n" + "=" * 80)
print("7. COMBINED EXAMPLE - RAG System Document Indexer")
print("=" * 80)

# Document structure using namedtuple
Document = namedtuple('Document', ['id', 'content', 'metadata'])

# Store documents with defaultdict
document_store = defaultdict(list)

# Inverted index using defaultdict
inverted_index = defaultdict(set)

# Recent queries using deque (limited history)
recent_queries = deque(maxlen=5)

# Sample documents
documents = [
    Document(id='doc1', content='Python is great for AI development', 
             metadata={'source': 'blog', 'date': '2026-01-10'}),
    Document(id='doc2', content='Machine learning with Python libraries', 
             metadata={'source': 'tutorial', 'date': '2026-01-12'}),
    Document(id='doc3', content='AI and machine learning fundamentals', 
             metadata={'source': 'course', 'date': '2026-01-15'}),
]

# Index documents
print("\n--- Indexing Documents ---")
for doc in documents:
    # Store by source
    document_store[doc.metadata['source']].append(doc)
    
    # Build inverted index
    words = doc.content.lower().split()
    for word in words:
        inverted_index[word].add(doc.id)
    
    print(f"Indexed: {doc.id} - '{doc.content[:40]}...'")

# Simulate search queries
print("\n--- Processing Search Queries ---")
queries = ['Python AI', 'machine learning', 'fundamentals']

for query in queries:
    recent_queries.append(query)
    query_words = query.lower().split()
    
    # Find matching documents
    matching_docs = set()
    for word in query_words:
        matching_docs.update(inverted_index.get(word, set()))
    
    print(f"\nQuery: '{query}'")
    print(f"  Matching documents: {sorted(matching_docs) if matching_docs else 'None'}")

print(f"\n--- Recent Query History ---")
print(f"Last {len(recent_queries)} queries: {list(recent_queries)}")

# Word frequency across all documents
print("\n--- Corpus Statistics ---")
all_words = []
for doc in documents:
    all_words.extend(doc.content.lower().split())

word_freq = Counter(all_words)
print(f"Total words in corpus: {len(all_words)}")
print(f"Unique words: {len(word_freq)}")
print(f"Top 5 words: {word_freq.most_common(5)}")


print("\n" + "=" * 80)
print("SUMMARY OF COLLECTIONS FOR GEN AI")
print("=" * 80)
print("""
Counter      → Token/word frequency, label distribution, ensemble voting
deque        → Conversation history, sliding windows, streaming data
defaultdict  → Grouping samples, inverted indexes, metric tracking
namedtuple   → Model configs, training samples, structured predictions
OrderedDict  → Network layers, pipelines, experiment tracking
ChainMap     → Configuration hierarchy, environment settings

All these collections are essential for efficient Gen AI development!
""")








