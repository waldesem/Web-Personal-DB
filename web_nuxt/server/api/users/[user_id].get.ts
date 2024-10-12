export default defineEventHandler((event) => {
    const user_id = getRouterParam(event, 'user_id')
    const item = getQuery(event).item
    return { param: user_id, item: item }
  })