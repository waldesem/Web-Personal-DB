/**
 * Use this file to store global state
 * such as user token, etc.
*/

import { useStorage } from '@vueuse/core'

export const userToken = useStorage(
  'userToken',
  '',
  localStorage,
  { mergeDefaults: true }
)