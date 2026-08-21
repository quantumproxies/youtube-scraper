/**
 * Which uploads beat their own channel's baseline?
 *
 * Raw view counts rank old videos first. Views-per-day since publication ranks
 * what is actually working now — and comparing each video against its channel's
 * own median removes channel size from the equation.
 *
 *   node velocity.mjs channels.txt --tab videos --max 40
 */
import { readFileSync } from "node:fs";
import { ageInDays, args, collect, flag } from "./qd.mjs";

const file = args[0];
if (!file || file.startsWith("--")) {
  console.error("usage: node velocity.mjs channels.txt [--tab videos] [--max 40]");
  process.exit(1);
}

const handles = readFileSync(file, "utf8").split("\n").map((s) => s.trim()).filter(Boolean);
const outliers = [];

for (const handle of handles) {
  let rows;
  try {
    rows = await collect("youtube_channel", {
      channel: handle,
      tab: flag("tab", "videos"),
      max_results: Number(flag("max", 40)),
    });
  } catch (err) {
    console.error(`${handle}: ${err.message}`);
    continue;
  }

  const scored = rows
    .map((r) => ({ ...r, days: ageInDays(r.published) }))
    .filter((r) => r.days && r.views_value)
    .map((r) => ({ ...r, perDay: r.views_value / r.days }));

  if (scored.length < 5) {
    console.log(`${handle}: only ${scored.length} datable uploads, skipping`);
    continue;
  }

  const sorted = [...scored].sort((a, b) => a.perDay - b.perDay);
  const median = sorted[Math.floor(sorted.length / 2)].perDay;
  console.log(`${handle}: ${scored.length} uploads, median ${Math.round(median).toLocaleString()} views/day`);

  for (const v of scored) {
    if (v.perDay > median * 3) {
      outliers.push({ handle, ratio: v.perDay / median, ...v });
    }
  }
}

outliers.sort((a, b) => b.ratio - a.ratio);
console.log(`\n${outliers.length} uploads at 3x+ their channel's median\n`);
for (const v of outliers.slice(0, 20)) {
  console.log(
    `${v.ratio.toFixed(1)}x  ${String(Math.round(v.perDay)).padStart(8)}/day  ` +
      `${v.handle.padEnd(18)}${(v.title ?? "").slice(0, 55)}`,
  );
}
