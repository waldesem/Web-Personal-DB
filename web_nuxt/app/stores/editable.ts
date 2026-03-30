export const useEditStore = defineStore("editable", () => {
  const person = usePersonStore();
  const session = useSessionStore();

  const editable = computed(() => {
    return (
      person.data.editable &&
      session.user?.role === "user" &&
      session.user?.id === person.data.user_id &&
      !person.data.locked
    );
  });

  return { editable };
});
