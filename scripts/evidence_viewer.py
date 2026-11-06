from pathlib import Path
import html,json
R=Path(__file__).resolve().parents[1]
for n in range(1,7):
 folder=R/f'Task{n:02}'
 chunks=[f'<h1>Task {n:02} - execution evidence</h1><p>Browser view of captured compiler and process output. This is an archived execution record, not a terminal screenshot.</p>']
 for p in sorted(folder.rglob('*.json')):
  d=json.loads(p.read_text()); stem=p.with_suffix('')
  if 'command' not in d:continue
  chunks.append('<section><h2>'+html.escape(d['source']+(' ['+p.stem+']'))+'</h2>')
  chunks.append('<p>Compile: <code>'+html.escape(' '.join(d['command']))+'</code></p>')
  chunks.append('<p>Compile exit: '+str(d['compile_exit'])+' | Run exit: '+str(d.get('run_exit','not run'))+' | Input: '+html.escape(d['input'])+'</p>')
  for ext,title in [('compile.txt','Compiler diagnostics'),('stdout.txt','stdout'),('stderr.txt','stderr')]:
   log=Path(str(stem)+'.'+ext)
   if log.exists():chunks.append('<h3>'+title+'</h3><pre>'+html.escape(log.read_text() or '(empty)')+'</pre>')
  chunks.append('</section>')
 (folder/'output-view.html').write_text('<!doctype html><meta charset="utf-8"><title>Task '+str(n)+' execution records</title><style>body{font:16px system-ui;color:#182238;background:#f4f6fa;margin:32px;max-width:1200px}section{background:white;border:1px solid #bdc8d8;padding:20px;margin:20px 0}h1{font-size:28px}h2{font-size:21px}h3{font-size:16px}pre,code{font:14px monospace;white-space:pre-wrap;overflow-wrap:anywhere}pre{border-left:3px solid #4c6fba;padding:10px;background:#eef2f8}</style>'+''.join(chunks))
