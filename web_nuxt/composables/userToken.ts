import type { User } from "@/types";
import { useStorage, type RemovableRef } from "@vueuse/core";

export const accessToken = useStorage("accessToken", "", localStorage, {
  mergeDefaults: true,
});

export const stateUser = useStorage("stateUser", {}) as RemovableRef<User>;
