export default defineEventHandler(async(event) => {
  const item = getRouterParam(event, 'item')
  const item_id = getRouterParam(event, 'item_id')
  const data = await readBody(event)
  return { item: item, item_id: item_id, data: data }
})