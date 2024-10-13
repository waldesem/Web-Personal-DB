export default defineEventHandler(async(event) => {
  const action = getQuery(event).action
  const json_data = await readBody(event)
  return { data: json_data, action: action }
})