import fs from "node:fs";
import path from "node:path";

export function makeDestinationFolder(
  id: string,
  surname: string,
  firstname: string,
  patronymic: string
): string {
  const folderName = path.join(
    process.env.DESTINATION as string,
    "Главный офис",
    surname[0],
    `$${surname} ${firstname} ${patronymic ?? ""}-${id}`
      .toUpperCase()
  );
  if (!fs.existsSync(folderName)) {
    fs.mkdirSync(folderName);
  }
  return folderName;
}
