"""Integer-cent arithmetic and exact critical cells for a restricted time DSL."""
import copy
from datetime import datetime,timezone
import hashlib
import itertools
import json
from zoneinfo import ZoneInfo,ZoneInfoNotFoundError

def integer(value,low,high):
    if type(value)is not int or not low<=value<=high:raise ValueError("invalid_integer")
    return value

def utc_seconds(value):
    if isinstance(value,dict):
        if set(value)-{"local","zone","fold"}:raise ValueError("unknown_local_time_field")
        try:naive=datetime.fromisoformat(value["local"]);zone=ZoneInfo(value["zone"])
        except (ValueError,KeyError,TypeError,ZoneInfoNotFoundError):raise ValueError("invalid_local_time") from None
        if naive.tzinfo is not None or naive.microsecond:raise ValueError("invalid_local_time")
        candidates={}
        for fold in (0,1):
            aware=naive.replace(tzinfo=zone,fold=fold);utc=aware.astimezone(timezone.utc)
            if utc.astimezone(zone).replace(tzinfo=None)==naive:candidates[fold]=int(utc.timestamp())
        if not candidates:raise ValueError("nonexistent_local_time")
        if len(set(candidates.values()))>1 and "fold" not in value:raise ValueError("ambiguous_local_time")
        fold=value.get("fold",0)
        if type(fold)is not int or fold not in candidates:raise ValueError("invalid_fold")
        return candidates[fold]
    if not isinstance(value,str):raise ValueError("invalid_time")
    try:date=datetime.fromisoformat(value.replace("Z","+00:00"))
    except ValueError:raise ValueError("invalid_time") from None
    if date.tzinfo is None or date.microsecond:raise ValueError("explicit_timezone_required")
    return int(date.timestamp())

def iso(seconds):return datetime.fromtimestamp(seconds,timezone.utc).isoformat().replace("+00:00","Z")

def compile_rule(rule,events,depth=0):
    if not isinstance(rule,dict) or depth>6:raise ValueError("invalid_rule")
    op=rule.get("op")
    if op in ("before","at_or_before"):
        if set(rule)!={"op","event","deadline"} or rule["event"] not in events:raise ValueError("invalid_temporal_predicate")
        return {"op":op,"event":rule["event"],"deadline_utc":utc_seconds(rule["deadline"]),"source_deadline":copy.deepcopy(rule["deadline"])}
    if op=="not" and set(rule)=={"op","arg"}:return {"op":op,"arg":compile_rule(rule["arg"],events,depth+1)}
    if op in ("and","or") and set(rule)=={"op","args"} and isinstance(rule["args"],list) and 1<=len(rule["args"])<=6:return {"op":op,"args":[compile_rule(a,events,depth+1) for a in rule["args"]]}
    raise ValueError("unsupported_rule")

def evaluate(rule,world):
    op=rule["op"]
    if op in ("before","at_or_before"):
        time=world[rule["event"]]
        return time is not None and (time<rule["deadline_utc"] if op=="before" else time<=rule["deadline_utc"])
    if op=="not":return not evaluate(rule["arg"],world)
    values=[evaluate(a,world) for a in rule["args"]]
    return all(values) if op=="and" else any(values)

def leaves(rule):
    if rule["op"] in ("before","at_or_before"):return [rule]
    if rule["op"]=="not":return leaves(rule["arg"])
    return [leaf for a in rule["args"] for leaf in leaves(a)]

def validate(case):
    if not isinstance(case,dict) or case.get("fictional") is not True or not isinstance(case.get("events"),dict) or not 1<=len(case["events"])<=3:raise ValueError("fictional_case_required")
    events={}
    for name,domain in case["events"].items():
        if not isinstance(name,str) or not name or not isinstance(domain,dict) or type(domain.get("allow_absent"))is not bool:raise ValueError("invalid_event")
        start,end=utc_seconds(domain["start"]),utc_seconds(domain["end"])
        if start>end:raise ValueError("invalid_domain")
        events[name]={"start":start,"end":end,"allow_absent":domain["allow_absent"]}
    contracts=case.get("contracts")
    if not isinstance(contracts,list) or not 1<=len(contracts)<=6:raise ValueError("invalid_contracts")
    result=[];seen=set()
    for c in contracts:
        if not isinstance(c,dict) or not isinstance(c.get("id"),str) or not c["id"] or c["id"] in seen or c.get("side") not in ("yes","no") or c.get("settlement") not in ("resolved","unresolved"):raise ValueError("invalid_contract")
        seen.add(c["id"]);quantity=integer(c.get("quantity"),1,1000);price=integer(c.get("price_cents"),0,100);fee=integer(c.get("fee_per_unit_cents"),0,100);fixed=integer(c.get("fee_if_filled_cents"),0,10000)
        fills=c.get("fills")
        if not isinstance(fills,list) or not 1<=len(fills)<=5 or any(type(v)is not int or not 0<=v<=quantity for v in fills) or len(set(fills))!=len(fills) or quantity not in fills:raise ValueError("invalid_fills")
        result.append({**c,"quantity":quantity,"price_cents":price,"fee_per_unit_cents":fee,"fee_if_filled_cents":fixed,"compiled_rule":compile_rule(c["rule"],events)})
    return events,result

def critical_worlds(events,contracts):
    domains=[];all_leaves=[leaf for c in contracts for leaf in leaves(c["compiled_rule"])]
    if len(all_leaves)>20:raise ValueError("predicate_budget")
    for event,domain in events.items():
        points={domain["start"],domain["end"]}
        for leaf in all_leaves:
            if leaf["event"]==event:
                for time in (leaf["deadline_utc"]-1,leaf["deadline_utc"],leaf["deadline_utc"]+1):
                    if domain["start"]<=time<=domain["end"]:points.add(time)
        domains.append(sorted(points)+([None] if domain["allow_absent"] else []))
    count=1
    for domain in domains:count*=len(domain)
    if count>20000:raise ValueError("world_budget")
    # Worlds with identical atomic truth vectors are interchangeable for this DSL.
    unique={}
    for times in itertools.product(*domains):
        world=dict(zip(events,times));signature=tuple(evaluate(leaf,world) for leaf in all_leaves)
        unique.setdefault(signature,world)
    return list(unique.values()),count

def payoff(contracts,world,fills):
    legs=[];total_cost=lower=upper=locked=0;all_settled=True
    for c,q in zip(contracts,fills):
        q=integer(q,0,c["quantity"])
        if q not in c["fills"]:raise ValueError("undeclared_fill")
        outcome=evaluate(c["compiled_rule"],world);wins=outcome if c["side"]=="yes" else not outcome
        cost=q*(c["price_cents"]+c["fee_per_unit_cents"])+(c["fee_if_filled_cents"] if q else 0)
        unresolved=c["settlement"]=="unresolved" and q>0
        low,high=(0,q*100) if unresolved else (q*100*int(wins),)*2
        total_cost+=cost;lower+=low;upper+=high
        if unresolved:all_settled=False;locked+=cost
        legs.append({"contract":c["id"],"filled":q,"condition":outcome,"side":c["side"],"cost_cents":cost,"settlement":c["settlement"],"payout_interval_cents":[low,high],"net_interval_cents":[low-cost,high-cost]})
    return {"legs":legs,"cost_cents":total_cost,"net_interval_cents":[lower-total_cost,upper-total_cost],"settled_net_cents":lower-total_cost if all_settled else None,"unresolved_cost_cents":locked,"all_settled":all_settled}

def verify_witness(case,witness):
    try:
        events,contracts=validate(case);world={k:None if v is None else utc_seconds(v) for k,v in witness["events"].items()}
        if set(world)!=set(events):return {"valid":False}
        if not isinstance(witness.get("fills"),list) or len(witness["fills"])!=len(contracts):return {"valid":False}
        for event,time in world.items():
            d=events[event]
            if time is None and not d["allow_absent"] or time is not None and not d["start"]<=time<=d["end"]:return {"valid":False}
        actual=payoff(contracts,world,witness["fills"])
        return {"valid":actual==witness["payoff"],"recomputed":actual}
    except (ValueError,TypeError,KeyError):return {"valid":False}

def analyze(case,partial_fills=True):
    events,contracts=validate(case)
    if type(partial_fills)is not bool:raise ValueError("invalid_partial_fills")
    worlds,raw_count=critical_worlds(events,contracts);fill_sets=[c["fills"] if partial_fills else [c["quantity"]] for c in contracts]
    count=len(worlds)
    for fills in fill_sets:count*=len(fills)
    if count>100000:raise ValueError("trial_budget")
    worst=None;full_worst=None;negative=0
    def witness(world,fills,value):return {"events":{k:None if v is None else iso(v) for k,v in world.items()},"fills":list(fills),"payoff":value}
    for world in worlds:
        full=payoff(contracts,world,[c["quantity"] for c in contracts])
        if full_worst is None or full["net_interval_cents"][0]<full_worst["payoff"]["net_interval_cents"][0]:full_worst=witness(world,[c["quantity"] for c in contracts],full)
        for fills in itertools.product(*fill_sets):
            value=payoff(contracts,world,fills)
            if value["net_interval_cents"][0]<0:negative+=1
            if worst is None or value["net_interval_cents"][0]<worst["payoff"]["net_interval_cents"][0]:worst=witness(world,fills,value)
    assert verify_witness(case,worst)["valid"]
    return {"case_id":case.get("id"),"fictional":True,"case_sha256":hashlib.sha256(json.dumps(case,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest(),"critical_raw_worlds":raw_count,"truth_cells":len(worlds),"trials":count,"negative_lower_bound_trials":negative,"partial_fills":partial_fills,"worst":worst,"full_fill_worst":full_worst,"witness_replay":verify_witness(case,worst),"normalized_deadlines":[{"contract":c["id"],"event":leaf["event"],"source":leaf["source_deadline"],"utc":iso(leaf["deadline_utc"]),"operator":leaf["op"]} for c in contracts for leaf in leaves(c["compiled_rule"])],"exhaustive_scope":"declared_integer_second_domains_restricted_boolean_time_DSL_and_explicit_fill_sets","probabilities_estimated":False}
