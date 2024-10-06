export default defineEventHandler(async(event) => {
  const file = await readBody(event)
  const reader = new FileReader();
  reader.readAsText(file.file);

  try {
    const jsonData = await new Promise((resolve) => {
      reader.onload = () => {
        resolve(JSON.parse(reader.result as string));
      };
    });
    return { data: jsonData }
  } catch (error) {
    return { error: error }
  }
})