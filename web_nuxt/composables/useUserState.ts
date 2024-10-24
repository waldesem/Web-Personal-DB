import type { User } from "@/types/interfaces";

export const useUserState = () => {
  const user = useState(
    "user",
    async () => (await $fetch("/api/auth")) as Ref<User>
  );
  return user;
};
