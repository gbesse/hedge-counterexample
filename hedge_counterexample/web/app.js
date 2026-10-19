const translations = {
  fr: {
    eyebrow: 'RÈGLES TEMPORELLES · EXÉCUTIONS PARTIELLES',
    title: 'La couverture tient. Jusqu’à ce détail.',
    lede: 'Deux jambes, des échéances presque identiques et un gain apparent. Explorez le scénario exact qui casse la couverture : fuseau, frontière temporelle ou quantité réellement exécutée.',
    assumptions: 'Choisir les hypothèses',
    example: 'Exercice fictif',
    'timezone-gap': 'Même heure affichée, fuseaux différents',
    'partial-fill-gap': 'Mêmes règles, exécutions différentes',
    partial: 'Autoriser les quantités 0, 5 et 10 par jambe',
    unresolved: 'Résolution encore en attente',
    analyze: 'Chercher un contre-exemple',
    fictional:
      'Contrats, prix et frais inventés pour cet exercice. Aucun marché réel, compte ou ordre connecté.',
    scope:
      'Recherche exhaustive dans le langage temporel restreint, le domaine déclaré et les quantités listées. Aucune probabilité d’occurrence estimée.',
    witness: 'Le témoin le plus défavorable',
    replayed: 'TÉMOIN REJOUÉ',
    worst: 'borne nette basse · centimes fictifs',
    full: 'borne basse avec exécution totale',
    trials: 'cellules de vérité × exécutions',
    deadlines: 'Ce que les échéances signifient en UTC',
    event: 'Événement du contre-exemple',
    legs: 'Ce qui a réellement été exécuté',
    fees: 'Frais fictifs : 1 centime par unité + 2 par jambe exécutée. Aucun frais fixe si quantité nulle. Ces frais ne sont ceux d’aucune plateforme.',
    download: 'Exporter le cas et les preuves',
    limits:
      'Prototype mathématique sur règles déclarées : pas d’analyse automatique de contrats juridiques, carnet réel, latence, liquidité ou recommandation de placement. Les titres ne prouvent pas l’équivalence des règles. Une résolution inconnue reste une fourchette, pas une perte réalisée. Aucune supériorité SOTA revendiquée.',
    pending:
      'Résolution en attente : montant net inconnu. Fourchette possible et coût engagé affichés séparément.',
    range: 'Fourchette nette',
    locked: 'Coût engagé non résolu',
    absent: 'Événement absent',
    filled: 'Quantité exécutée',
    condition: 'Condition de la règle',
    yes: 'oui',
    no: 'non',
    cost: 'Coût avec frais',
    net: 'Net',
    ready: 'Toutes les cellules autorisées sont examinées.',
    error: 'Entrée ou heure non valide.',
  },
  en: {
    eyebrow: 'TEMPORAL RULES · PARTIAL FILLS',
    title: 'The hedge holds. Until this detail.',
    lede: 'Two legs, almost identical deadlines and an apparent gain. Explore the exact scenario that breaks coverage: timezone, time boundary or quantity actually filled.',
    assumptions: 'Choose assumptions',
    example: 'Fictional exercise',
    'timezone-gap': 'Same displayed hour, different timezones',
    'partial-fill-gap': 'Same rules, different fills',
    partial: 'Allow quantities 0, 5 and 10 per leg',
    unresolved: 'Settlement still pending',
    analyze: 'Search for a counterexample',
    fictional:
      'Contracts, prices and fees are invented for this exercise. No real market, account or order connection.',
    scope:
      'Exhaustive search within the restricted time language, declared domain and listed fill quantities. No event probabilities estimated.',
    witness: 'The most adverse witness',
    replayed: 'WITNESS REPLAYED',
    worst: 'lower net bound · fictional cents',
    full: 'lower bound with full fills',
    trials: 'truth cells × fill combinations',
    deadlines: 'What deadlines mean in UTC',
    event: 'Counterexample event',
    legs: 'What actually filled',
    fees: 'Fictional fees: 1 cent per unit + 2 per filled leg. No fixed fee at zero quantity. These are not any platform’s fees.',
    download: 'Export case and evidence',
    limits:
      'Mathematical prototype over declared rules: no automatic legal-contract analysis, live orderbook, latency, liquidity or investment recommendation. Titles do not establish equivalent rules. Unknown settlement remains an interval, not a realized loss. No SOTA superiority claimed.',
    pending:
      'Settlement pending: net amount unknown. Possible interval and committed cost are shown separately.',
    range: 'Net interval',
    locked: 'Unresolved committed cost',
    absent: 'Event absent',
    filled: 'Filled quantity',
    condition: 'Rule condition',
    yes: 'yes',
    no: 'no',
    cost: 'Cost including fees',
    net: 'Net',
    ready: 'All permitted truth cells checked.',
    error: 'Invalid input or time.',
  },
  es: {
    eyebrow: 'REGLAS TEMPORALES · EJECUCIONES PARCIALES',
    title: 'La cobertura funciona. Hasta este detalle.',
    lede: 'Dos posiciones, plazos casi idénticos y una ganancia aparente. Explore el escenario que rompe la cobertura: zona horaria, límite temporal o cantidad ejecutada.',
    assumptions: 'Elegir hipótesis',
    example: 'Ejercicio ficticio',
    'timezone-gap': 'Misma hora mostrada, distintas zonas',
    'partial-fill-gap': 'Mismas reglas, distintas ejecuciones',
    partial: 'Permitir cantidades 0, 5 y 10 por posición',
    unresolved: 'Resolución pendiente',
    analyze: 'Buscar un contraejemplo',
    fictional:
      'Contratos, precios y comisiones inventados para el ejercicio. Sin mercado real, cuenta ni órdenes conectadas.',
    scope:
      'Búsqueda exhaustiva dentro del lenguaje temporal restringido, dominio declarado y cantidades listadas. Sin probabilidades estimadas.',
    witness: 'El testigo más adverso',
    replayed: 'TESTIGO REPRODUCIDO',
    worst: 'límite neto inferior · céntimos ficticios',
    full: 'límite inferior con ejecución total',
    trials: 'celdas de verdad × ejecuciones',
    deadlines: 'Qué significan los plazos en UTC',
    event: 'Evento del contraejemplo',
    legs: 'Lo que se ejecutó realmente',
    fees: 'Comisiones ficticias: 1 céntimo por unidad + 2 por posición ejecutada. Sin comisión fija con cantidad cero. No corresponden a ninguna plataforma.',
    download: 'Exportar caso y pruebas',
    limits:
      'Prototipo matemático con reglas declaradas: sin análisis automático de contratos jurídicos, libro real, latencia, liquidez ni recomendación de inversión. Los títulos no demuestran equivalencia. La resolución desconocida sigue siendo un intervalo, no una pérdida realizada. Sin superioridad SOTA.',
    pending:
      'Resolución pendiente: importe neto desconocido. Intervalo posible y coste comprometido mostrados por separado.',
    range: 'Intervalo neto',
    locked: 'Coste comprometido sin resolver',
    absent: 'Evento ausente',
    filled: 'Cantidad ejecutada',
    condition: 'Condición de la regla',
    yes: 'sí',
    no: 'no',
    cost: 'Coste con comisiones',
    net: 'Neto',
    ready: 'Todas las celdas permitidas verificadas.',
    error: 'Entrada u hora no válida.',
  },
};
const lang = new URLSearchParams(location.search).get('lang') || 'en',
  t = translations[lang] || translations.en;
document.documentElement.lang = translations[lang] ? lang : 'en';
document.querySelectorAll('[data-i18n]').forEach((e) => (e.textContent = t[e.dataset.i18n]));
const $ = (id) => document.getElementById(id);
let evidence;
function el(tag, text, cls) {
  const n = document.createElement(tag);
  n.textContent = text;
  if (cls) n.className = cls;
  return n;
}
async function run() {
  try {
    $('analyze').disabled = true;
    const response = await fetch('/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        example: $('example').value,
        partial_fills: $('partial').checked,
        unresolved: $('unresolved').checked,
      }),
    });
    if (!response.ok) throw Error();
    evidence = await response.json();
    const w = evidence.worst,
      p = w.payoff;
    $('worst').textContent = p.net_interval_cents[0];
    $('full').textContent = evidence.full_fill_worst.payoff.net_interval_cents[0];
    $('trials').textContent = evidence.trials;
    $('digest').textContent = evidence.case_sha256;
    $('pending').hidden = p.all_settled;
    $('pending').textContent =
      `${t.pending} ${t.range}: [${p.net_interval_cents.join(', ')}] · ${t.locked}: ${p.unresolved_cost_cents}`;
    $('deadlines').replaceChildren();
    for (const d of evidence.normalized_deadlines)
      $('deadlines').append(
        el(
          'div',
          `${d.contract} · ${typeof d.source === 'string' ? d.source : `${d.source.local} / ${d.source.zone}`} → ${d.utc} (${d.operator})`,
          'deadline',
        ),
      );
    $('timeline').textContent = Object.entries(w.events)
      .map(([k, v]) => `${k}: ${v ?? t.absent}`)
      .join('\n');
    $('legs').replaceChildren();
    for (const leg of p.legs) {
      const div = el('section', '', 'leg');
      div.append(
        el('h3', `${leg.contract} · ${leg.side === 'yes' ? t.yes : t.no}`),
        el('p', `${t.filled}: ${leg.filled} · ${t.condition}: ${leg.condition ? t.yes : t.no}`),
        el(
          'p',
          `${t.cost}: ${leg.cost_cents} · ${t.net}: [${leg.net_interval_cents.join(', ')}]`,
          leg.net_interval_cents[0] < 0 ? 'loss' : 'safe',
        ),
      );
      $('legs').append(div);
    }
    $('status').textContent = t.ready;
  } catch {
    $('status').textContent = t.error;
  } finally {
    $('analyze').disabled = false;
  }
}
$('analyze').onclick = run;
$('download').onclick = () => {
  if (!evidence) return;
  const url = URL.createObjectURL(
      new Blob([JSON.stringify(evidence, null, 2)], { type: 'application/json' }),
    ),
    a = document.createElement('a');
  a.href = url;
  a.download = 'hedge-counterexample-evidence.json';
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
};
await run();
