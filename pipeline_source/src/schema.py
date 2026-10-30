LESSON_SCHEMA={"type":"object","required":["chapter","section","scenes"],"properties":{"chapter":{"type":"string"},"section":{"type":"string"},
"scenes":{"type":"array","minItems":1,"items":{"type":"object","required":["scene_id","objective","claims","narration","visual","checkpoint"],
"properties":{"scene_id":{"type":"string","pattern":"^s[0-9]{2}$"},"objective":{"type":"string"},
"claims":{"type":"array","minItems":1,"items":{"type":"object","required":["text","span_ids"],"properties":{"text":{"type":"string"},"span_ids":{"type":"array","minItems":1,"items":{"type":"string"}}}}},
"narration":{"type":"string"},
"visual":{"type":"object","required":["render_tier","template","labels"],"properties":{"render_tier":{"enum":["A_deterministic","B_generative","C_video"]},"template":{"type":"string"},"labels":{"type":"array","items":{"type":"string"}}}},
"checkpoint":{"type":"object","required":["q_id","stem","options","answer","explanations","span_ids","remediation"],"properties":{"q_id":{"type":"string"},"stem":{"type":"string"},"options":{"type":"array","minItems":4,"maxItems":4,"items":{"type":"string"}},"answer":{"type":"integer","minimum":0,"maximum":3},"explanations":{"type":"array","minItems":4,"maxItems":4,"items":{"type":"string"}},"span_ids":{"type":"array","minItems":1,"items":{"type":"string"}},"remediation":{"type":"string"}}}}}}}}
