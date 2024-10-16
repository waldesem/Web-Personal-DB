import fs from "fs";

export default defineEventHandler((event) => {
  const folder = getQuery(event).folder as string;
  if (!fs.existsSync(folder)) {
    fs.mkdirSync(folder);
  }
  fs.opendir(folder, (err, _dir) => {
    if (err) throw err;
  });
  return "";
});
