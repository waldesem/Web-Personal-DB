export const useEditStore = defineStore("editable", () => {
  const personStore = usePersonStore();

  const sessionStore = useSessionStore();

  const editable = computed(() => {
    return (
      personStore.person.editable &&
      sessionStore.user?.role === "user" &&
      sessionStore.user?.id === personStore.person.user_id &&
      !personStore.person.locked
    );
  });

  return { editable };
});
