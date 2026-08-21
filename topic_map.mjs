/**
 * Who owns a topic on YouTube?
 *
 * Runs a keyword set under two sort orders, then ranks channels by how many
 * keywords they appear for. Appearing for one keyword is luck; appearing for
 * eight is a content strategy you can study.
 *
 *   node topic_map.mjs keywords.txt --max 20
 */
import { readFileSync } from "node:fs";
import { args, collect, flag } from "./qd.mjs";

const file = args[0];
if (!file || file.startsWith("--")) {
  console.error("usage: node topic_map.mjs keywords.txt [--max 20]");
  process.exit(1);
}

const keywords = readFileSync(file, "utf8").split("\n").map((s) => s.trim()).filter(Boolean);
const max = Number(flag("max", 20));

const channels = new Map(); // channel -> { keywords:Set, views:number, videos:number, url }

for (const query of keywords) {
  for (const sort of ["relevance", "view_count"]) {
    let rows = [];
    try {
      rows = await collect("youtube_search", { query, sort, max_results: max });
    } catch (err) {
      console.error(`${query} (${sort}): ${err.message}`);
      continue;
    }
    for (const r of rows) {
      if (!r.channel) continue;
      const entry = channels.get(r.channel) ?? {
        keywords: new Set(), views: 0, videos: 0, url: r.channel_url,
      };
      entry.keywords.add(query);
      entry.views += r.views_value ?? 0;
      entry.videos += 1;
      channels.set(r.channel, entry);
    }
  }
  console.log(`${query}: ${channels.size} channels seen so far`);
}

const ranked = [...channels.entries()].sort(
  (a, b) => b[1].keywords.size - a[1].keywords.size || b[1].views - a[1].views,
);

console.log(`\n${keywords.length} keywords, ${channels.size} channels\n`);
console.log(`${"channel".padEnd(32)}${"keywords".padStart(9)}${"videos".padStart(8)}${"views".padStart(14)}`);
for (const [name, e] of ranked.slice(0, 25)) {
  console.log(
    name.slice(0, 31).padEnd(32) +
      String(e.keywords.size).padStart(9) +
      String(e.videos).padStart(8) +
      e.views.toLocaleString().padStart(14),
  );
}
