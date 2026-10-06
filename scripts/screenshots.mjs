// Снимает экраны прототипа в assets/img/ для страницы кейса.
// Нужны Google Chrome и Node 22+; прототип должен быть доступен по адресу ниже:
//   python3 -m http.server 8766 --directory demo
//   node scripts/screenshots.mjs
import { spawn } from "node:child_process";
import { mkdirSync, writeFileSync } from "node:fs";

const DEMO = process.env.DEMO_URL || "http://localhost:8766/";
const OUT = new URL("../assets/img/", import.meta.url).pathname;
const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const PORT = 9333;
const W = 1440, H = 900;
// экран прототипа → имя файла и пауза на отрисовку карты и графиков
const SHOTS = [
  ["overview", "overview.png", 2500],
  ["map", "map.png", 6000], // затем: sips -s format jpeg assets/img/map.png --out assets/img/map.jpg,
  ["buildings", "house.png", 2000],
  ["forecasts", "forecasts.png", 2000],
  ["tickets", "tickets.png", 2000],
  ["brigades", "brigades.png", 2000],
  ["janitors", "cleaning.png", 6000], // затем тоже в JPEG
];

mkdirSync(OUT, { recursive: true });
const chrome = spawn(CHROME, ["--headless=new", `--remote-debugging-port=${PORT}`, `--window-size=${W},${H}`,
  "--hide-scrollbars", "--user-data-dir=/tmp/twin-shots", "about:blank"], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

let ws, id = 0;
const pending = new Map();
const send = (method, params = {}) => new Promise((resolve) => {
  const n = ++id; pending.set(n, resolve); ws.send(JSON.stringify({ id: n, method, params }));
});

try {
  let target;
  for (let i = 0; i < 40 && !target; i++) {
    await sleep(250);
    try { target = (await (await fetch(`http://127.0.0.1:${PORT}/json`)).json()).find((t) => t.type === "page"); } catch {}
  }
  ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((r) => ws.addEventListener("open", r));
  ws.addEventListener("message", (e) => {
    const m = JSON.parse(e.data);
    if (m.id && pending.has(m.id)) { pending.get(m.id)(m.result); pending.delete(m.id); }
  });
  await send("Emulation.setDeviceMetricsOverride", { width: W, height: H, deviceScaleFactor: 2, mobile: false });
  await send("Page.navigate", { url: DEMO });
  await sleep(4000);
  for (const [page, file, wait] of SHOTS) {
    await send("Runtime.evaluate", { expression: `navigate(${JSON.stringify(page)})` });
    await sleep(wait);
    const { data } = await send("Page.captureScreenshot", { format: "png" });
    writeFileSync(OUT + file, Buffer.from(data, "base64"));
    console.log("сохранён", file);
  }
} finally {
  ws?.close();
  chrome.kill();
}
