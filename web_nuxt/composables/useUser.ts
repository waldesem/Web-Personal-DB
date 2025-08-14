import type { Token } from "@/types";

export const useStateUser = () =>
  useState("user", () => shallowRef({} as Token));
