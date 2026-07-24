# Guard Model Collapse — Detection and Prevention

## Phenomenon

Guard model collapse occurs when benign domain fine-tuning unintentionally destroys a model's safety alignment. Safety representations, which exist as activation subspaces separate from task capabilities, are overwritten during fine-tuning on domain data. The model continues to perform well on task benchmarks while losing its ability to refuse harmful requests.

**Documented rates:** 10-20% of fine-tuned models show measurable safety degradation. Llama-3.1 family: 15% refusal rate drop after 1 epoch of medical domain fine-tuning. Mistral: 12% toxicity classification accuracy decline after legal domain fine-tuning.

## FW-SSR (Fisher Weighted Subspace Regularization)

Preserves safety-critical weight subspaces during fine-tuning by restricting gradient updates in directions that would collapse safety representations:

```python
import torch
import torch.nn as nn
from torch.nn.utils import vector_to_parameters, parameters_to_vector

class FWSSRRegularizer:
    """Fisher-Weighted Subspace Regularization for safety preservation."""

    def __init__(self, model: nn.Module, safety_weights: dict, lambda_reg: float = 0.01):
        self.model = model
        self.safety_weights = safety_weights
        self.lambda_reg = lambda_reg

    def compute_safety_loss(self) -> torch.Tensor:
        """Compute L2 distance between current and safety weights in Fisher subspace."""
        loss = 0.0
        for name, param in self.model.named_parameters():
            if name in self.safety_weights:
                safe_param = self.safety_weights[name]
                # Fisher information weights — prioritize critical safety params
                fisher = self._compute_fisher_for_layer(name)
                weighted_diff = fisher * (param - safe_param) ** 2
                loss += weighted_diff.sum()
        return self.lambda_reg * loss

    # Total fine-tuning loss = task_loss + safety_loss
    # optimizer.step() minimizes both simultaneously
```

## Geometry-Based Monitoring

Detect collapse by measuring cosine similarity between safety layer activations before and after fine-tuning:

```python
def detect_safety_collapse(
    pre_model: nn.Module,
    post_model: nn.Module,
    harmful_prompts: list[str],
    safety_layer: str = "lm_head",
    threshold: float = 0.7
) -> dict:
    """Detect safety alignment collapse via embedding geometry."""
    pre_embeddings = extract_layer_embeddings(pre_model, harmful_prompts, safety_layer)
    post_embeddings = extract_layer_embeddings(post_model, harmful_prompts, safety_layer)

    # Cosine similarity between pre and post safety representations
    similarities = []
    for pre_emb, post_emb in zip(pre_embeddings, post_embeddings):
        sim = torch.nn.functional.cosine_similarity(
            pre_emb.flatten(), post_emb.flatten(), dim=0
        ).item()
        similarities.append(sim)

    avg_similarity = sum(similarities) / len(similarities)
    collapsed = avg_similarity < threshold

    return {
        "collapsed": collapsed,
        "avg_similarity": avg_similarity,
        "per_prompt_similarity": similarities,
        "recommendation": "BLOCK deployment" if collapsed else "Safe to deploy"
    }
```

## Prevention Checklist

- [ ] Run FW-SSR analysis before and after every fine-tuning run
- [ ] Block deployment if cosine similarity drops below 0.7
- [ ] Monitor safety layer activations weekly in production
- [ ] Maintain safety regression test suite (100+ harmful prompts)
- [ ] Freeze safety-critical layers during fine-tuning (top 2 layers)
- [ ] Use LoRA instead of full fine-tuning when possible (isolates safety weights)
- [ ] Run LlamaGuard on fine-tuned model outputs before production deployment
