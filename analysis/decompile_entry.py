import angr, logging, hashlib
from pathlib import Path
logging.getLogger('angr').setLevel(logging.ERROR)
binary = Path(__file__).resolve().parent.parent / 'extracted' / 'Loader.exe'
expected = '06af42916823a3c8c85278e46c027b2cb43d23184c5f4bbde7bdf42f739bfa62'
if hashlib.sha256(binary.read_bytes()).hexdigest() != expected:
    raise SystemExit('Unexpected executable hash; addresses in this script apply only to the analyzed file.')
p=angr.Project(str(binary),auto_load_libs=False)
print('loaded',hex(p.entry),flush=True)
cfg=p.analyses.CFGFast(function_starts=[p.entry,0x1240a76],force_complete_scan=False,resolve_indirect_jumps=False,function_prologues=False,normalize=True)
print('nodes',len(list(cfg.graph.nodes())), 'functions',len(cfg.kb.functions),flush=True)
for addr in [p.entry,0x1be8304,0x1be9e5f,0x1240a76]:
 f=cfg.kb.functions.get(addr)
 print('\nFUNCTION',hex(addr),'found',bool(f),flush=True)
 if f:
  print('blocks',len(list(f.blocks)),flush=True)
  try:
   d=p.analyses.Decompiler(f,cfg=cfg.model)
   print(d.codegen.text if d.codegen else 'no code generated',flush=True)
  except Exception as e: print('error',repr(e),flush=True)
