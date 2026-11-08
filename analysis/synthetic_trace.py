"""Follow one synthetic entry-point path, not a Windows execution."""
import hashlib
from pathlib import Path
import angr, logging
logging.getLogger('angr').setLevel(logging.ERROR)
binary = Path(__file__).resolve().parent.parent / 'extracted' / 'Loader.exe'
if hashlib.sha256(binary.read_bytes()).hexdigest() != '06af42916823a3c8c85278e46c027b2cb43d23184c5f4bbde7bdf42f739bfa62':
    raise SystemExit('Unexpected executable hash')
p=angr.Project(str(binary),auto_load_libs=False)
s=p.factory.blank_state(addr=p.entry, add_options={angr.options.ZERO_FILL_UNCONSTRAINED_REGISTERS, angr.options.ZERO_FILL_UNCONSTRAINED_MEMORY})
s.regs.esp=0x7fff0000
sm=p.factory.simulation_manager(s, save_unconstrained=True)
for i in range(12000):
 if not sm.active: break
 a=sm.active[0]
 try:
  b=p.factory.block(a.addr)
  
  if i % 100 == 0: print(f'{i:05} {a.addr:#010x} esp={a.solver.eval(a.regs.esp):#x}', flush=True)
  sm.step(num_inst=40)
  if len(sm.active)>1:
   print('multiple branches, stop',len(sm.active));break
  if sm.unconstrained:
   print('unconstrained address',sm.unconstrained[0].regs.eip);break
  if sm.errored:
   print('error',repr(sm.errored[0].error));break
 except Exception as e:
  print('exception',repr(e)); break
print('finished steps:',i,'active',len(sm.active),'unconstrained',len(sm.unconstrained),'errors',len(sm.errored))
