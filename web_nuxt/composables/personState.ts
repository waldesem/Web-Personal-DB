import { createGlobalState } from '@vueuse/core'
import type { Persons } from "@/types";

export const usePersonState = createGlobalState(
  () => {
    const person = ref({} as Persons)
    return { person }
  }
)