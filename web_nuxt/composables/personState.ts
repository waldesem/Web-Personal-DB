import type { Persons } from "@/types";

export const usePersonState = () => useState("person", () => ({} as Persons));
