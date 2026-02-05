import sys
from pathlib import Path

import pytest

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))

from predict_workflow_failures import WorkflowPredictor


class TestWorkflowPredictorSecurity:
    @pytest.fixture
    def predictor(self):
        model_path = Path("automation/ml/test_security_model.pkl")
        sig_path = Path("automation/ml/test_security_model.pkl.sig")

        # Cleanup
        if model_path.exists():
            model_path.unlink()
        if sig_path.exists():
            sig_path.unlink()

        p = WorkflowPredictor(model_path=str(model_path))
        p.model = "DUMMY_MODEL"
        p.feature_columns = ["col1"]

        yield p

        # Cleanup
        if model_path.exists():
            model_path.unlink()
        if sig_path.exists():
            sig_path.unlink()

    def test_save_creates_signature(self, predictor):
        predictor.save_model()
        assert predictor.model_path.exists()
        sig_path = predictor.model_path.with_suffix(".pkl.sig")
        assert sig_path.exists()
        assert sig_path.stat().st_size > 0

    def test_load_valid_signature_success(self, predictor):
        predictor.save_model()
        # Should load without error
        predictor.load_model()

    def test_load_missing_signature_fails(self, predictor):
        predictor.save_model()
        sig_path = predictor.model_path.with_suffix(".pkl.sig")
        sig_path.unlink()

        with pytest.raises(ValueError, match="Missing signature file"):
            predictor.load_model()

    def test_load_tampered_model_fails(self, predictor):
        predictor.save_model()

        # Tamper with model file
        with open(predictor.model_path, "wb") as f:
            f.write(b"garbage data")

        with pytest.raises(ValueError, match="Model signature verification failed"):
            predictor.load_model()

    def test_load_tampered_signature_fails(self, predictor):
        predictor.save_model()

        sig_path = predictor.model_path.with_suffix(".pkl.sig")
        with open(sig_path, "w") as f:
            f.write("badsignature")

        with pytest.raises(ValueError, match="Model signature verification failed"):
            predictor.load_model()
