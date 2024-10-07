export default defineEventHandler(async(event) => {
  const data = await readJSONBody(event)
  return { data: data }
})