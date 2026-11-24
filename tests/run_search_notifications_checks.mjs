import fs from "fs";
const html=fs.readFileSync("analytics/index.html","utf8"), js=fs.readFileSync("js/aics-analytics-dashboard.js","utf8");
const checks=[
  ["search control and dialog",html.includes('id="global-search"')&&html.includes('id="search-dialog"')],
  ["search covers pages and persistent records",js.includes("workspacePages")&&js.includes("loadSearchRecords")&&js.includes('"decisions"')],
  ["search opens matching workspace",js.includes("data-search-workspace")&&js.includes("setWorkspace(workspace)")],
  ["notification bell and dialog",html.includes('id="notifications"')&&html.includes('id="notifications-dialog"')],
  ["notifications use real records",js.includes("loadNotifications")&&js.includes("incomplete")&&js.includes("proposed")],
  ["red dot is conditional",html.includes('id="notification-dot" hidden')&&js.includes("hidden = items.length === 0")],
  ["notifications deep-link",js.includes("data-notification-workspace")],
]; let failures=0;for(const [name,ok]of checks){console.log(`${ok?"PASS":"FAIL"} ${name}`);if(!ok)failures++;}if(failures)process.exit(1);console.log("\nAll search and notification checks passed.");
