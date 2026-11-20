import { initModel } from "@energetic-ai/embeddings";
import { modelSource } from "@energetic-ai/model-embeddings-en";
import fs from "fs";
const T = JSON.parse(fs.readFileSync("titles.json", "utf8"));
const model = await initModel(modelSource); const t0 = Date.now(); const out = [];
for (let i = 0; i < T.length; i += 256) { const e = await model.embed(T.slice(i, i + 256)); out.push(...e.map(v => Array.from(v))); }
const buf = Buffer.alloc(out.length * 512 * 4); let k = 0; out.forEach(v => v.forEach(x => { buf.writeFloatLE(x, k); k += 4; }));
fs.writeFileSync("titles.f32", buf); console.log(T.length, ((Date.now() - t0) / 1000).toFixed(0) + "s");
