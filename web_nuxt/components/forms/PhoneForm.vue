<script setup lang="ts">
import type { Phone } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps<{ phone: Phone }>();

const form = ref(props.phone as Phone);

async function submitForm() {
  const { message } = (await fetchAuth("/route/phones", {
    method: "POST",
    body: form.value,
  })) as Record<string, string>;
  if (message === "success") {
    emit("update");
    form.value = {} as Phone;
    makeToast("success", "Контакт успешно добавлен/изменен");
  } else {
    makeToast();
  }
}
</script>

<template>
  <UForm :state="form" @submit.prevent="submitForm">
    <UFormField label="Название организации" name="organization" required>
      <UInput
        v-model.lazy.trim="form.organization"
        placeholder="Название организации"
        maxlength="255"
        required
      />
    </UFormField>
    <UFormField label="Город" name="city">
      <UInput
        v-model.lazy.trim="form.city"
        placeholder="Город"
        maxlength="255"
        required
      />
    </UFormField>
    <UFormField label="Полное имя" name="fullname" required>
      <UInput
        v-model.lazy.trim="form.fullname"
        placeholder="Полное имя"
        maxlength="255"
        required
      />
    </UFormField>
    <UFormField label="Телефон" name="phone">
      <UInput
        v-model.lazy.trim="form.phone"
        placeholder="Телефон"
        maxlength="255"
        required
      />
    </UFormField>
    <UFormField label="Email" name="email" type="email">
      <UInput
        v-model.lazy.trim="form.email"
        placeholder="Email"
        maxlength="255"
        required
      />
    </UFormField>
    <UFormField label="Комментарий" name="comments">
      <UTextarea v-model.lazy="form.comments" autoresize />
    </UFormField>
    <UButton label="Принять" color="success" variant="outline" type="submit" />
  </UForm>
</template>
