#!/usr/bin/env python3
"""
Minimal test to verify import structure is correct.
This doesn't import any external dependencies.
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def test_module_syntax():
    """Test that all modules have valid Python syntax."""
    print("Testing module syntax...\n")

    files_to_check = [
        'config.py',
        'models/base_model.py',
        'models/openai_client.py',
        'models/gemini_client.py',
        'models/claude_client.py',
        'roles/base_role.py',
        'roles/tutor.py',
        'roles/quiz_creator.py',
        'roles/summarizer.py',
        'router/task_classifier.py',
        'router/model_router.py',
        'session/session_manager.py',
        'utils/helpers.py',
        'main.py',
    ]

    all_ok = True
    for file_path in files_to_check:
        try:
            with open(file_path, 'r') as f:
                compile(f.read(), file_path, 'exec')
            print(f"   ✓ {file_path}")
        except SyntaxError as e:
            print(f"   ✗ {file_path}: {e}")
            all_ok = False

    return all_ok

def test_import_structure():
    """Test the absolute import structure."""
    print("\nTesting import structure (without external deps)...\n")

    # Test that can import modules with no external dependencies
    try:
        # router.task_classifier has no external deps
        exec(open('router/task_classifier.py').read())
        print("   ✓ router/task_classifier.py loads correctly")

        # session.session_manager has no external deps
        exec(open('session/session_manager.py').read())
        print("   ✓ session/session_manager.py loads correctly")

        # utils.helpers has no external deps
        exec(open('utils/helpers.py').read())
        print("   ✓ utils/helpers.py loads correctly")

        print("\n✅ Core modules work correctly!")
        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("="*50)
    print("Smart Study Assistant - Structure Test")
    print("="*50 + "\n")

    syntax_ok = test_module_syntax()
    structure_ok = test_import_structure()

    print("\n" + "="*50)
    if syntax_ok and structure_ok:
        print("✅ All structure tests passed!")
        print("\nTo run the application:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Configure API keys in .env file (copy from .env.example)")
        print("3. Run: python main.py chat")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    print("="*50)
