// Static, no-backend data loading and rendering

const cleanPath = 'data/clean.json';
const rawPath = 'data/raw.json';

const state = {
  clean: [],
  raw: [],
  metrics: {
    jobs: 0,
    companies: 0,
    skills: 0,
    withSalary: 0,
    locations: 0,
  },
};

function uniq(arr) {
  return Array.from(new Set(arr));
}

function textLen(s) {
  return (s || '').trim().length;
}

function toSalaryMidpoints(records) {
  const mids = [];
  for (const r of records) {
    const sal = r.salary;
    if (sal == null) continue;
    if (Array.isArray(sal) && sal.length >= 1) {
      const a = Number(sal[0]);
      const b = Number(sal[1] ?? sal[0]);
      if (Number.isFinite(a) && Number.isFinite(b)) {
        mids.push((a + b) / 2);
      }
    } else if (typeof sal === 'number' && Number.isFinite(sal)) {
      mids.push(sal);
    }
  }
  return mids;
}

function topNCounts(values, n = 15) {
  const counts = new Map();
  for (const v of values) {
    if (!v) continue;
    counts.set(v, (counts.get(v) || 0) + 1);
  }
  return Array.from(counts.entries())
    .sort((a, b) => b[1] - a[1])
    .slice(0, n)
    .map(([x, y]) => ({ key: x, count: y }));
}

async function loadJSON(path) {
  const res = await fetch(path);
  if (!res.ok) throw new Error(`Failed to fetch ${path}`);
  return res.json();
}

function renderMetricCards() {
  const root = document.getElementById('metric-cards');
  const { jobs, companies, skills, withSalary, locations } = state.metrics;
  const pctSalary = jobs ? Math.round((withSalary / jobs) * 100) : 0;
  const cards = [
    { label: 'Jobs', value: jobs.toLocaleString() },
    { label: 'Companies', value: companies.toLocaleString() },
    { label: 'Unique skills', value: skills.toLocaleString() },
    { label: 'With salary', value: `${withSalary.toLocaleString()} (${pctSalary}%)` },
    { label: 'Locations', value: locations.toLocaleString() },
  ];
  root.innerHTML = cards
    .map(
      (c) => `
        <div class="stat">
          <div class="label">${c.label}</div>
          <div class="value">${c.value}</div>
        </div>`
    )
    .join('');
}

async function renderSkillsChart(topSkills) {
  if (!topSkills.length) {
    document.getElementById('skills-chart').innerHTML = '<p class="small">No skills extracted.</p>';
    return;
  }
  const spec = {
    $schema: 'https://vega.github.io/schema/vega-lite/v5.json',
    description: 'Top skills by frequency',
    width: 'container',
    height: 260,
    data: { values: topSkills },
    mark: { type: 'bar', cornerRadius: 2 },
    encoding: {
      y: { field: 'key', type: 'nominal', sort: '-x', title: null },
      x: { field: 'count', type: 'quantitative', title: 'Count' },
      color: { value: '#4db6ff' },
      tooltip: [ { field: 'key', title: 'Skill' }, { field: 'count', title: 'Count' } ],
    },
  };
  await vegaEmbed('#skills-chart', spec, { actions: false });
}

async function renderSalaryChart(mids) {
  const note = document.getElementById('salary-note');
  if (mids.length < 5) {
    document.getElementById('salary-chart').innerHTML = '<p class="small">Not enough salary data to chart a distribution.</p>';
    note.textContent = 'Some sources omit salary; parsing also depends on formatting.';
    return;
  }
  const values = mids.map((v) => ({ v }));
  const spec = {
    $schema: 'https://vega.github.io/schema/vega-lite/v5.json',
    description: 'Salary midpoints (unit depends on source)',
    width: 'container',
    height: 260,
    data: { values },
    mark: { type: 'bar', cornerRadiusTopLeft: 2, cornerRadiusTopRight: 2 },
    encoding: {
      x: { field: 'v', bin: { maxbins: 20 }, title: 'Salary (parsed units)' },
      y: { aggregate: 'count', title: 'Jobs' },
      color: { value: '#6ee7b7' },
      tooltip: [{ aggregate: 'count', title: 'Jobs' }],
    },
  };
  await vegaEmbed('#salary-chart', spec, { actions: false });
  note.textContent = 'Histogram uses parsed midpoints; treat as indicative only.';
}

function renderTopLocations(values) {
  const root = document.getElementById('top-locations');
  if (!values.length) {
    root.innerHTML = '<li class="small">No location data.</li>';
    return;
  }
  root.innerHTML = values
    .slice(0, 10)
    .map((d) => `<li>${d.key} — ${d.count}</li>`) 
    .join('');
}

function renderCoverage({ jobs, withSalary }) {
  const items = [
    `Total postings: ${jobs.toLocaleString()}`,
    `Salary present for: ${withSalary.toLocaleString()} postings`,
    `Fields: title, company, location, description, salary?, skills[]`,
  ];
  document.getElementById('coverage').innerHTML = items.map((t) => `<li>${t}</li>`).join('');
}

function byKeyIndex(list, keyFn) {
  const m = new Map();
  for (const x of list) {
    m.set(keyFn(x), x);
  }
  return m;
}

function pickComparisons(raw, clean, n = 3) {
  const kRaw = byKeyIndex(raw, (r) => `${(r.title || '').toLowerCase()}|${(r.location || '').toLowerCase()}`);
  const kClean = byKeyIndex(clean, (r) => `${(r.title || '').toLowerCase()}|${(r.location || '').toLowerCase()}`);
  const examples = [];
  for (const [k, r] of kClean.entries()) {
    const rawRec = kRaw.get(k);
    if (!rawRec) continue;
    examples.push({ raw: rawRec, clean: r });
    if (examples.length >= n) break;
  }
  return examples;
}

function renderComparisons(examples) {
  const root = document.getElementById('comparisons');
  if (!examples.length) {
    root.innerHTML = '<p class="small">Could not find matching records to compare.</p>';
    return;
  }
  root.innerHTML = examples
    .map(({ raw, clean }) => {
      const rawCompany = raw.company_name || raw.company || '';
      const cleanSkills = (clean.skills || []).join(', ');
      const salaryText = Array.isArray(clean.salary) ? clean.salary.join('–') : (clean.salary ?? '—');
      return `
        <div class="compare">
          <h4>${clean.title}</h4>
          <div class="kv">
            <div class="k">Company</div><div>${clean.company || rawCompany}</div>
            <div class="k">Location</div><div>${clean.location || raw.location || ''}</div>
            <div class="k">Desc len</div><div>${textLen(raw.description)} ➜ ${textLen(clean.description)}</div>
            <div class="k">Salary</div><div>${salaryText}</div>
            <div class="k">Skills</div><div>${cleanSkills || '—'}</div>
          </div>
        </div>`;
    })
    .join('');
}

async function init() {
  try {
    document.getElementById('year').textContent = new Date().getFullYear();

    const [clean, raw] = await Promise.all([loadJSON(cleanPath), loadJSON(rawPath)]);
    state.clean = clean;
    state.raw = raw;

    const jobs = clean.length;
    const companies = uniq(clean.map((d) => (d.company || '').trim()).filter(Boolean)).length;
    const skillsAll = clean.flatMap((d) => Array.isArray(d.skills) ? d.skills : []).map((s) => s.trim()).filter(Boolean);
    const skillsUnique = uniq(skillsAll).length;
    const withSalary = clean.filter((d) => d.salary != null).length;
    const locationsUnique = uniq(clean.map((d) => (d.location || '').trim()).filter(Boolean)).length;

    state.metrics = { jobs, companies, skills: skillsUnique, withSalary, locations: locationsUnique };
    renderMetricCards();

    const topSkills = topNCounts(skillsAll, 15);
    await renderSkillsChart(topSkills);

    const mids = toSalaryMidpoints(clean);
    await renderSalaryChart(mids);

    const topLoc = topNCounts(clean.map((d) => (d.location || '').trim()).filter(Boolean), 10);
    renderTopLocations(topLoc);

    renderCoverage({ jobs, withSalary });

    const examples = pickComparisons(raw, clean, 3);
    renderComparisons(examples);
  } catch (e) {
    console.error(e);
  }
}

init();
