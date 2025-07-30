// import { useStorage } from "@vueuse/core";
import type { Token } from "@/types";

// export const accessToken = useStorage("accessToken", "", localStorage, {
//   mergeDefaults: true,
// });

export const useUser = () => useState("user", () => ({} as Token));

export const accessToken = useCookie("token");
