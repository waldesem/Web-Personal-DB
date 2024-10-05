/**
 * Get the user token from ref.
*/
// export const userToken = ref("");

import { useStorage } from '@vueuse/core'

export const userToken = useStorage(
  'userToken',
  '',
  localStorage,
  { mergeDefaults: true }
)