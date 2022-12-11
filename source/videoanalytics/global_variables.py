from backend.model import InferenceModel
from backend.model_utils import load_models

models: dict[str, InferenceModel] = load_models()

# {port: subprocess.Popen}
subprocess_dict = {}
