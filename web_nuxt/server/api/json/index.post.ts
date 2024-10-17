export default defineEventHandler(async(event) => {
  const files = await readBody(event)
  const reader = new FileReader();
  reader.readAsText(files[0].file);
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