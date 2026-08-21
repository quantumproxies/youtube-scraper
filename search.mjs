/**
 * YouTube keyword search.
 *   node search.mjs "residential proxies explained" --sort view_count --max 40 --csv out.csv
 */
import { writeFileSync } from "node:fs";
import { args, collect, flag, toCsv } from "./qd.mjs";

const query = args[0];
if (!query || query.startsWith("--")) {
  console.error('usage: node search.mjs "<query>" [--sort relevance|upload_date|view_count|rating] [--max 20]');
  process.exit(1);
}

const rows = await collect("youtube_search", {
  query,
  sort: flag("sort", "relevance"),
  country: flag("country", "us"),
  lang: flag("lang", "en"),
  max_results: Number(flag("max", 20)),
});

const views = rows.map((r) => r.views_value).filter((v) => typeof v === "number").sort((a, b) => a - b);
const channels = new Set(rows.map((r) => r.channel));

console.log(`${rows.length} videos, ${channels.size} distinct channels`);
if (views.length) {
  const median = views[Math.floor(views.length / 2)];
  console.log(`views: ${views[0].toLocaleString()} … ${views.at(-1).toLocaleString()} (median ${median.toLocaleString()})`);
}
console.log();

for (const r of rows.slice(0, 15)) {
  console.log(
    `${String(r.rank).padStart(3)}. ${String(r.views_value ?? 0).padStart(10)} views  ` +
      `${(r.duration ?? "").padStart(7)}  ${(r.channel ?? "").slice(0, 22).padEnd(23)}` +
      `${(r.title ?? "").slice(0, 60)}`,
  );
}

const csv = flag("csv", null);
if (csv) {
  writeFileSync(csv, toCsv(rows, ["rank", "video_id", "title", "channel", "channel_url",
    "views_value", "published", "duration", "live", "url"]));
  console.log(`\nwrote ${csv}`);
}
