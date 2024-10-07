export default defineEventHandler(async(event) => {
  const action = getQuery(event).action
  const json_data = await readJSONBody(event)
  return { data: json_data, action: action }
})