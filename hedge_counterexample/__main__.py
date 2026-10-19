import json
from pathlib import Path
import sys
from .engine import analyze,verify_witness
ROOT=Path(__file__).resolve().parent
MESSAGES={"fr":{"help":"Utilisation : python -m hedge_counterexample demo|analyze cas.json|verify cas.json témoin.json|serve [port] [--lang fr|en|es]","error":"Entrée ou heure non valide ; préciser le fuseau et les ambiguïtés","ready":"Laboratoire de couverture local"},"en":{"help":"Usage: python -m hedge_counterexample demo|analyze case.json|verify case.json witness.json|serve [port] [--lang fr|en|es]","error":"Invalid input or time; supply timezone and resolve ambiguities","ready":"Local hedge laboratory"},"es":{"help":"Uso: python -m hedge_counterexample demo|analyze caso.json|verify caso.json testigo.json|serve [puerto] [--lang fr|en|es]","error":"Entrada u hora no válida; indicar zona y resolver ambigüedades","ready":"Laboratorio local de cobertura"}}
def example(name='timezone-gap'):return json.loads((ROOT/f'examples/{name}.json').read_text())
def main(argv=None):
    args=list(sys.argv[1:] if argv is None else argv);lang='en'
    try:
        if '--lang' in args:i=args.index('--lang');lang=args[i+1];del args[i:i+2]
        if lang not in MESSAGES:raise ValueError('language')
        if not args or args[0] in ('help','--help'):print(MESSAGES[lang]['help']);return 0
        cmd=args.pop(0)
        if cmd=='serve':
            from .server import serve
            port=int(args[0]) if args else 8773;print(f'{MESSAGES[lang]["ready"]}: http://127.0.0.1:{port}/?lang={lang}',flush=True);serve(port);return 0
        if cmd=='demo':result=analyze(example())
        elif cmd=='analyze':result=analyze(json.loads(Path(args[0]).read_text()))
        elif cmd=='verify':result=verify_witness(json.loads(Path(args[0]).read_text()),json.loads(Path(args[1]).read_text()))
        else:raise ValueError('command')
        print(json.dumps(result,ensure_ascii=False,indent=2));return 1 if result.get('valid') is False else 0
    except (ValueError,TypeError,KeyError,IndexError,OSError):print(json.dumps({'error':'invalid_input','message':MESSAGES.get(lang,MESSAGES['en'])['error']}),file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
