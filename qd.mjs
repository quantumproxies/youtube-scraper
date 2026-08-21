/** QuanticData Collectors client for the YouTube examples. Node 18+, no deps. */
const BASE = "https://api.quanticdata.io/v1";

const auth = () => {
  const key = process.env.QUANTICDATA_API_KEY;
  if (!key) {
    console.error("set QUANTICDATA_API_KEY — https://app.quanticdata.io/register");
    process.exit(1);
  }
  return { Authorization: `Bearer ${key}`, "Content-Type": "application/json" };
};

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function payloadOf(res, what) {
  const body = await res.json();
  if (!res.ok || body.type === "error") throw new Error(`${what} (${res.status}): ${body.message}`);
  return body.payload ?? {};
}

export async function collect(slug, input) {
  let run = await payloadOf(
    await fetch(`${BASE}/scraper/collectors/${slug}/run`, {
      method: "POST", headers: auth(), body: JSON.stringify(input),
    }),
    slug,
  );
  while (run.status === "queued" || run.status === "running") {
    await sleep(3000);
    run = await payloadOf(
      await fetch(`${BASE}/scraper/collectors/runs/${run.run_id}`, { headers: auth() }),
      "run status",
    );
  }
  return run.results ?? [];
}

export function toCsv(rows, cols) {
  const columns = cols ?? [...new Set(rows.flatMap(Object.keys))];
  const cell = (v) => {
    const s = Array.isArray(v) ? v.join(" | ") : v == null ? "" : String(v);
    return /[",\n]/.test(s) ? `"${s.replaceAll('"', '""')}"` : s;
  };
  return [columns.join(","), ...rows.map((r) => columns.map((c) => cell(r[c])).join(","))].join("\n") + "\n";
}

/** "3 years ago" / "2 weeks ago" -> approximate days. YouTube gives no exact date here. */
export function ageInDays(published) {
  const m = /(\d+)\s+(second|minute|hour|day|week|month|year)/.exec(published ?? "");
  if (!m) return null;
  const per = { second: 1 / 86400, minute: 1 / 1440, hour: 1 / 24, day: 1, week: 7, month: 30.44, year: 365.25 };
  return Number(m[1]) * per[m[2]];
}

export const args = process.argv.slice(2);
export const flag = (name, fallback) => {
  const i = args.indexOf(`--${name}`);
  return i === -1 ? fallback : args[i + 1];
};
