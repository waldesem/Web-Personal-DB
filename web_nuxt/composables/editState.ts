const user = useUserState()
const person = usePersonState();

export const useEditableState = () => {
  return useState("editable", () =>
    computed(() => {
      return (
        person.value.editable &&
        user.value.role == "user" &&
        user.value.id == person.value.user_id
      );
    })
  );
};