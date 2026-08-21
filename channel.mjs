/**
 * One channel's uploads.
 *   node channel.mjs "@NASA" --tab videos --max 60 --csv nasa.csv
 */
import { writeFileSync } from "node:fs";
import { args, collect, flag, toCsv } from "./qd.mjs";

const channel = args[0];
if (!channel || channel.startsWith("--")) {
  console.error('usage: node channel.mjs "@handle" [--tab videos|shorts|streams] [--max 30]');
  process.exit(1);
}

const rows = await collect("youtube_channel", {
  channel,
  tab: flag("tab", "videos"),
  country: flag("country", "us"),
  max_results: Number(flag("max", 30)),
});

if (!rows.length) {
  console.log("no rows — check the handle, or try --tab shorts");
  process.exit(0);
}

const [first] = rows;
console.log(`${first.channel ?? channel}  (${first.channel_id ?? "?"})`);
console.log(`  ${(first.channel_subscribers ?? 0).toLocaleString()} subscribers, ` +
  `${(first.channel_videos ?? 0).toLocaleString()} videos`);
console.log(`  ${(first.channel_description ?? "").slice(0, 160)}\n`);

const total = rows.reduce((sum, r) => sum + (r.views_value ?? 0), 0);
console.log(`${rows.length} uploads on this tab, ${total.toLocaleString()} views combined\n`);

for (const r of rows.slice(0, 20)) {
  console.log(
    `${String(r.views_value ?? 0).padStart(10)}  ${(r.published ?? "").padEnd(16)}` +
      `${(r.duration ?? "").padStart(7)}  ${(r.title ?? "").slice(0, 60)}`,
  );
}

const csv = flag("csv", null);
if (csv) {
  writeFileSync(csv, toCsv(rows, ["rank", "video_id", "title", "url", "views_value",
    "published", "duration", "live", "channel", "channel_subscribers"]));
  console.log(`\nwrote ${csv}`);
}
