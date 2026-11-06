#!/usr/bin/env python3
"""Run from the repository root. Captures real compiler/process evidence."""
import subprocess,pathlib,json,hashlib,datetime,os
R=pathlib.Path(__file__).resolve().parents[1]
os.chdir(R)
B=R/'.build';B.mkdir(exist_ok=True)
compiler=os.environ.get('CXX','g++')
version=subprocess.run([compiler,'--version'],capture_output=True,text=True).stdout
(R/'compiler.txt').write_text(version)
records=[]
expected={'Task02/predict_virtual.cpp':'Person Student Staff TA \n','Task02/predict_nonvirtual.cpp':'Person Student Person Staff TA \n','Task03/predict.cpp':'Vehicle Engine Car | ~Car ~Engine ~Vehicle \n','Task04/predict.cpp':'3.5 4 3.5\n','Task03/complete.cpp':'192311001 Kavya (19) Salem-636001\n','Task05/complete.cpp':'324.00\n'}
def execute(source,suffix='',flags=(),env=None,run=True,inp=None,expected_failure=False):
    p=pathlib.Path(source); folder=p.parent/'evidence';folder.mkdir(exist_ok=True)
    label=p.name.replace('.cpp.txt','').replace('.cpp','')+suffix
    binary=pathlib.Path('.build')/(p.parent.parent.name+'_'+p.parent.name+'_'+label)
    cmd=[compiler,'-std=c++17','-Wall','-Wextra',*flags]
    if source.endswith('.txt'):cmd+=['-x','c++']
    cmd += [source,'-o',str(binary)]
    c=subprocess.run(cmd,capture_output=True,text=True)
    data={'source':source,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'command':cmd,'compile_exit':c.returncode,'input':inp or 'embedded data; no stdin','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    (folder/(label+'.compile.txt')).write_text(c.stdout+c.stderr)
    if run and c.returncode==0:
        with open(inp) if inp else open(os.devnull) as f:
            r=subprocess.run([str(binary)],stdin=f,capture_output=True,text=True,env={**os.environ,**(env or {})})
        (folder/(label+'.stdout.txt')).write_text(r.stdout)
        (folder/(label+'.stderr.txt')).write_text(r.stderr)
        data.update(run_exit=r.returncode,environment=env or {})
        if source in expected and not suffix:
            assert r.stdout==expected[source],(source,r.stdout)
            data['exact_output_match']=True
        if not expected_failure: assert r.returncode==0,(source,r.stderr)
        if source=='Task06/fleet.cpp':
            for line in ['RETURN B1 charge=325.00','RETURN T1 charge=1500.00','RETURN C1 charge=3750.00','RETURN E1 charge=4100.00','RETURN EB1 charge=10400.00']:
                assert line in r.stdout,line
            assert r.stdout.count('ERROR ')==5
            data['independent_billing_and_error_checks']='passed'
    elif expected_failure: assert c.returncode!=0
    else: assert c.returncode==0,(source,c.stderr)
    (folder/(label+'.json')).write_text(json.dumps(data,indent=2)+'\n');records.append(data)
    print(source+suffix+': compile='+str(c.returncode)+' run='+str(data.get('run_exit','not run')))
for s in ['Task01/payroll.cpp','Task02/predict_virtual.cpp','Task02/predict_nonvirtual.cpp','Task02/relationships.cpp','Task03/predict.cpp','Task03/complete.cpp','Task03/hierarchy.cpp','Task03/address_pointer.cpp','Task04/predict.cpp','Task04/repaired.cpp','Task05/complete.cpp','Task05/cart_demo.cpp','Task06/tagged.cpp','Task06/fleet.cpp']:
    execute(s,inp='Task06/input.txt' if s=='Task06/fleet.cpp' else None)
execute('Task03/hierarchy.cpp','_nonvirtual',['-DNONVIRTUAL'])
execute('Task03/diagnostics/reordered.cpp.txt')
execute('Task02/diagnostics/ambiguous.cpp.txt',run=False,expected_failure=True)
execute('Task04/broken.cpp','_asan',['-fsanitize=address','-g','-fno-omit-frame-pointer'],expected_failure=True)
execute('Task04/broken.cpp','_leak_probe',['-fsanitize=address','-g'],env={'ASAN_OPTIONS':'detect_leaks=1'},expected_failure=True)
execute('Task04/repaired.cpp','_asan',['-fsanitize=address','-g'])
execute('Task03/address_pointer.cpp','_asan',['-fsanitize=address','-g'])
(R/'validation.json').write_text(json.dumps({'compiler':version,'records':records},indent=2)+'\n')
