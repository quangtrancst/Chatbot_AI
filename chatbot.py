import os
import sys
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import snapshot_download, list_models

def diagnose_huggingface_setup():
    print("=== HuggingFace and Model Diagnosis ===")
    
    # Check available models
    print("\n1. Checking available Vietnamese models:")
    try:
        vietnamese_models = [
            model for model in list_models(filter="vietnamese")[:5]
        ]
        for model in vietnamese_models:
            print(f"- {model.modelId}")
    except Exception as e:
        print(f"Error listing models: {e}")
    
    # Verify cache directory
    cache_dir = os.path.expanduser("~/.cache/huggingface")
    print(f"\n2. HuggingFace Cache Directory: {cache_dir}")
    print(f"   Exists: {os.path.exists(cache_dir)}")
    
    # Check environment variables
    print("\n3. Relevant Environment Variables:")
    env_vars = [
        "HUGGINGFACE_HUB_CACHE",
        "HF_HOME",
        "TRANSFORMERS_CACHE"
    ]
    for var in env_vars:
        print(f"   {var}: {os.environ.get(var, 'Not set')}")
    
    # System diagnostic
    print("\n4. System Diagnostics:")
    print(f"   Python Version: {sys.version}")
    print(f"   Torch Version: {torch.__version__}")
    print(f"   CUDA Available: {torch.cuda.is_available()}")
    
    # Library versions
    import transformers
    print(f"   Transformers Version: {transformers.__version__}")

def download_model(model_name="vinai/PhoGPT-4B-Chat", local_dir=None):
    print(f"\n=== Downloading Model: {model_name} ===")
    
    # Use default cache if no local_dir specified
    if local_dir is None:
        local_dir = os.path.expanduser("~/.cache/huggingface/models")
    
    os.makedirs(local_dir, exist_ok=True)
    
    try:
        # Detailed download with all files
        model_dir = snapshot_download(
            repo_id=model_name, 
            local_dir=local_dir,
            local_dir_use_symlinks=False,
            # Optional: specify file types if needed
            # file_pattern=["*.bin", "*.json", "*.txt"]
        )
        print(f"Model downloaded successfully to: {model_dir}")
        return model_dir
    except Exception as e:
        print(f"Download Error: {e}")
        return None

def test_model_loading(model_path):
    print("\n=== Testing Model Loading ===")
    try:
        print("Loading Tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        print("Tokenizer loaded successfully.")
        
        print("Loading Model...")
        model = AutoModelForCausalLM.from_pretrained(model_path)
        print("Model loaded successfully.")
        
        # Test generation
        test_input = "Xin chào"
        inputs = tokenizer(test_input, return_tensors="pt")
        outputs = model.generate(inputs.input_ids, max_length=50)
        test_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"Test Response: {test_response}")
        
    except Exception as e:
        print(f"Model Loading Error: {e}")
        import traceback
        traceback.print_exc()

def main():
    diagnose_huggingface_setup()
    
    # Specify your preferred download directory
    download_dir = r"D:\Code_Languages\huggingface_cache"
    
    model_path = download_model("vinai/PhoGPT-4B-Chat", local_dir=download_dir)
    
    if model_path:
        test_model_loading(model_path)

if __name__ == "__main__":
    main()