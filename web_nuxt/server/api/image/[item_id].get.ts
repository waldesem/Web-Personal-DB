import fs from "fs";
import path from "path";

export default defineEventHandler((event) => {
  const image = getQuery(event).image as string;
  const imagePath = path.join(image, "image", "image.jpg");
  if (!fs.existsSync(imagePath)) {
    const buffer = fs.readFileSync("./public/no-photo.png");
    event.respondWith(
      new Response(buffer, { headers: { "Content-Type": "image/jpeg" } })
    );
  }
  const buffer = fs.readFileSync(imagePath);
  send(event, buffer, "image/jpeg");
});
