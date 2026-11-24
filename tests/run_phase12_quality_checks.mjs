import fs from "fs";
const html=fs.readFileSync("analytics/index.html","utf8"),css=fs.readFileSync("css/aics-analytics-dashboard.css","utf8"),js=fs.readFileSync("js/aics-analytics-dashboard.js","utf8");
const ids=[...html.matchAll(/\sid="([^"]+)"/g)].map((match)=>match[1]);const uniqueIds=new Set(ids);
const checks=[
  ["all ids are unique",ids.length===uniqueIds.size],
  ["workspace restores after session verification",js.includes("validateCredentials(saved.token).then")&&js.includes("sessionStorage.getItem(WORKSPACE_KEY)")],
  ["dialogs have accessible names",html.includes('aria-labelledby="search-dialog-title"')&&html.includes('aria-labelledby="notifications-dialog-title"')],
  ["operations fields have labels",(html.match(/class="ops-add-form(?: [^"]*)?"/g)||[]).length===5&&(html.match(/aria-label="[^"]+"/g)||[]).length>=15],
  ["global keyboard focus is visible",css.includes("button:focus-visible")&&css.includes("input:focus-visible")&&css.includes("select:focus-visible")],
  ["desktop and mobile breakpoints exist",css.includes("@media (max-width: 980px)")&&css.includes("@media (max-width: 560px)")],
  ["mobile shell uses safe width",css.includes("width: min(100% - 1rem, 1180px)")],
  ["charts cannot force mobile overflow",css.includes(".chart-frame canvas")&&css.includes("width: 100% !important")&&css.includes(".chart-frame { overflow: hidden; }")],
  ["wide tables scroll inside their panel",css.includes(".table-wrap { max-width: 100%; overflow-x: auto; }")],
  ["two-column grids can shrink without overflow",css.includes("grid-template-columns: minmax(0, 1.15fr) minmax(0, 1fr)")],
  ["native dialogs support keyboard close",html.includes('<form method="dialog" class="dialog-head">')],
];let failures=0;for(const[name,ok]of checks){console.log(`${ok?"PASS":"FAIL"} ${name}`);if(!ok)failures++;}if(failures)process.exit(1);console.log("\nAll Phase 12 quality checks passed.");
