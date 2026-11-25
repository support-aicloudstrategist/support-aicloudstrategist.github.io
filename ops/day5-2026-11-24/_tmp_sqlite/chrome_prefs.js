const fs = require("fs");
const path = require("path");
const prefPath = path.join(
  process.env.LOCALAPPDATA,
  "Google",
  "Chrome",
  "User Data",
  "Default",
  "Preferences"
);
const pref = JSON.parse(fs.readFileSync(prefPath, "utf8"));
const emails = new Set();
JSON.stringify(pref).replace(
  /[A-Za-z0-9._%+-]+@gmail\.com/gi,
  (m) => emails.add(m.toLowerCase())
);
console.log(
  "profile",
  JSON.stringify(
    {
      name: pref.profile?.name,
      gaia: pref.profile?.gaia_name,
      user_name: pref.profile?.user_name,
    },
    null,
    2
  )
);
console.log("gmails_in_prefs", [...emails]);
if (pref.account_info) console.log("account_info", JSON.stringify(pref.account_info).slice(0, 1000));
