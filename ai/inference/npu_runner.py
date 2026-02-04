"""NPU inference wrapper placeholder."""


def run_inference(model_path, inputs):
    """Run inference with an NPU model.

    Args:
        model_path: Path to the ONNX model.
        inputs: Prepared model inputs.
    """
    return {
        "model": model_path,
        "inputs": inputs,
        "outputs": [],
    }
