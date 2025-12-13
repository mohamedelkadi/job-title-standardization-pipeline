# Llama-3.2-1B-Instruct Classifier Setup Guide

This guide will help you set up and test the Llama-3.2-1B-Instruct classifier on your sample data.

## Prerequisites

1. **Python 3.8+** with pip
2. **PyTorch** (already installed ✓)
3. **Transformers library** (already installed ✓)
4. **HuggingFace account** and access to the model

## Step 1: Install Required Dependencies

```bash
pip install transformers torch huggingface_hub
```

## Step 2: Get HuggingFace Access Token

1. Go to https://huggingface.co/settings/tokens
2. Create a new token (read access is sufficient)
3. Copy the token

## Step 3: Request Access to Llama Model

1. Visit: https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct
2. Click "Agree and access repository"
3. Accept the Llama 3.2 Community License Agreement
4. Wait for access approval (usually instant)

## Step 4: Authenticate

Run the following command and paste your token when prompted:

```bash
huggingface-cli login
```

Or set the token as an environment variable:

```bash
export HF_TOKEN=your_token_here
```

## Step 5: Run the Test

Once authenticated, run the test script:

```bash
python3 test_llama_classifier.py
```

Or test the classifier directly:

```bash
python3 llama_classifier.py
```

## Expected Output

The test will:
- Load the Llama-3.2-1B-Instruct model (this may take a few minutes on first run)
- Classify 30 sample job titles
- Generate a detailed report with:
  - Classification results for each title
  - Department, Function, and Seniority assignments
  - Confidence scores
  - Performance metrics (time per classification)
  - Distribution analysis

## Performance Notes

- **First run**: Model download (~2GB) and loading may take 5-10 minutes
- **Subsequent runs**: Model loading takes ~30-60 seconds
- **Inference time**: ~1-5 seconds per job title (depending on hardware)
- **Memory**: Requires ~2-4GB RAM for the 1B model

## Troubleshooting

### "Cannot access gated repo" error
- Make sure you've requested access at https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct
- Verify you're logged in: `huggingface-cli whoami`
- Check your token: `huggingface-cli login`

### "CUDA out of memory" error
- The model will use CPU if CUDA is not available
- For GPU, ensure you have at least 2GB VRAM
- CPU inference is slower but works fine

### Slow performance
- First run includes model download
- CPU inference is slower than GPU
- Consider using a smaller batch size or quantized model

## Comparison with Other Classifiers

After running the test, you can compare results with:
- Rule-based classifier: `python3 rule_classifier.py`
- spaCy classifier: `python3 spacy_classifier.py`
- Comparison report: See `SPACY_CLASSIFIER_COMPARISON_REPORT.md`

## Files Created

- `llama_classifier.py` - Main classifier implementation
- `test_llama_classifier.py` - Test script with sample data
- `LLAMA_CLASSIFIER_TEST_RESULTS.md` - Generated test results (after running test)
