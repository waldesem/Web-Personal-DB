<script setup lang="ts">
import type { Person } from "@/types";
import type { PropType } from "vue";

const emit = defineEmits(["update"]);

const props = defineProps({
  resume: {
    type: Object as PropType<Person>,
    default: () => ({}),
  },
  method: {
    type: String as PropType<"POST" | "PATCH">,
    default: "POST",
  },
  candId: {
    type: Object as PropType<string | null>,
    default: null,
  },
});

const form = ref<Person>({
  ...props.resume,
  birthday: props.resume.birthday
    ? useDateFormat(props.resume.birthday, "YYYY-MM-DD").value
    : "",
});
</script>

<template>
  <UForm
    :state="form"
    :validate="validatorResume"
    @submit.prevent="emit('update', form)"
  >
    <UFormField label="Фамилия" name="surname" required>
      <UInput
        v-model.lazy.trim="form.surname"
        placeholder="Фамилия"
        maxlength="255"
        required
      />
    </UFormField>
    <UFormField label="Имя" name="firstname" required>
      <UInput
        v-model.lazy.trim="form.firstname"
        placeholder="Имя"
        maxlength="255"
        required
      />
    </UFormField>
    <UFormField label="Отчество" name="patronymic">
      <UInput
        v-model.lazy.trim="form.patronymic"
        placeholder="Отчество"
        maxlength="255"
      />
    </UFormField>
    <UFormField label="Дата рождения" name="birthday" required>
      <UInput
        v-model="form.birthday"
        type="date"
        :max="new Date().toISOString().split('T')[0]"
        min="1900-01-01"
        required
      />
    </UFormField>
    <UFormField label="Место рождения" name="birthplace">
      <UInput
        v-model.lazy.trim="form.birthplace"
        placeholder="Место рождения"
        maxlength="255"
      />
    </UFormField>
    <UFormField label="Гражданство" name="citizenship">
      <UInput
        v-model.lazy.trim="form.citizenship"
        placeholder="Гражданство"
        maxlength="255"
      />
    </UFormField>
    <UFormField label="Двойное гражданство" name="dual">
      <UInput
        v-model.lazy.trim="form.dual"
        placeholder="Двойное гражданство"
        maxlength="255"
      />
    </UFormField>
    <UFormField label="СНИЛС" name="snils">
      <UInput
        v-model.lazy.trim="form.snils"
        placeholder="СНИЛС"
        pattern="^[0-9]{11}$"
      />
    </UFormField>
    <UFormField label="ИНН" name="inn">
      <UInput
        v-model.lazy.trim="form.inn"
        placeholder="ИНН"
        pattern="^[0-9]{12}$"
      />
    </UFormField>
    <UFormField label="Семейное положение" name="marital">
      <UInput
        v-model.lazy.trim="form.marital"
        placeholder="Семейное положение"
        maxlength="255"
      />
    </UFormField>
    <UFormField label="Дополнительно" name="addition">
      <UTextarea
        v-model.lazy.trim="form.addition"
        placeholder="Дополнительно"
      />
    </UFormField>
    <ElementSubmitButton />
  </UForm>
</template>
