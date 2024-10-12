export default defineEventHandler(async(event) => {
  const item = getRouterParam(event, 'item')
  const item_id = getRouterParam(event, 'item_id')
  const data = await readJSONBody(event)
  return { item: item, item_id: item_id, data: data }
})