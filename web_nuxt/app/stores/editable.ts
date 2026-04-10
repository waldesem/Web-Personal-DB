export const useEditStore = defineStore("locked", () => {
  const person = usePersonStore();
  const session = useSessionStore();

  const locked = computed(() => {
    return (
      person.data.locked &&
      session.user?.role === "user" &&
      session.user?.id === person.data.user_id &&
      !person.data.locked
    );
  });

  return { locked };
});
