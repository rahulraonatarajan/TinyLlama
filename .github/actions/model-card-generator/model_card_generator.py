
#!/usr/bin/env python3
"""TinyLlama Model Card Generator."""
import argparse, datetime
from pathlib import Path
try:
    from transformers import AutoConfig
except ImportError:
    AutoConfig = None

TEMPLATE = """# {name}
**Generated on {date}**

- **Architecture**: {arch}
- **Parameters**: {params}
- **License**: {license}
"""

def generate(model_path, output):
    meta = dict(name=Path(model_path).name, date=datetime.date.today(), arch='Unknown', params='N/A', license='N/A')
    if AutoConfig and Path(model_path).exists():
        try:
            cfg = AutoConfig.from_pretrained(model_path)
            meta.update(arch=(cfg.architectures[0] if getattr(cfg,'architectures',[]) else 'Unknown'),
                        params=getattr(cfg,'num_parameters','N/A'),
                        license=getattr(cfg,'license','N/A'),
                        name=cfg.name_or_path)
        except Exception as e:
            print('Warn:', e)
    Path(output).write_text(TEMPLATE.format(**meta))
    print('Wrote', output)

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--model_path', required=True)
    p.add_argument('--output', default='MODEL_CARD.md')
    args=p.parse_args()
    generate(args.model_path, args.output)
