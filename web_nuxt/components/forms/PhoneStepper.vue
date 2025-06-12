<script setup lang="ts">
import type { StepperItem } from "@nuxt/ui";
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

const items = [
  {
    slot: "organization" as const,
    title: "Название организации",
    icon: "i-heroicons-building-office",
  },
  {
    slot: "city" as const,
    title: "Город",
    icon: "i-heroicons-map",
  },
  {
    slot: "fullname" as const,
    title: "Полное имя",
    icon: "i-heroicons-user-circle",
  },
  {
    slot: "phone" as const,
    title: "Телефон",
    icon: "i-heroicons-phone",
  },
  {
    slot: "mobile" as const,
    title: "Мобильный телефон",
    icon: "i-heroicons-device-phone-mobile",
  },
  {
    slot: "comments" as const,
    title: "Комментарий",
    icon: "i-heroicons-book-open",
  },
] satisfies StepperItem[];

const stepper = useTemplateRef('stepper')
</script>

<template>
  <UForm :state="form" @submit.prevent="submitForm">
    <UStepper ref="stepper" :items="items" class="w-full">
      <template #organization>
        <PhoneBookOrganizationInput
          v-model="form.organization"
          :organization="props.phone.organization"
        />
      </template>
      <template #city>
        <PhoneBookCityInput v-model="form.city" :city="props.phone.city" />
      </template>
      <template #fullname>
        <PhoneBookFullnameInput
          v-model="form.fullname"
          :fullname="props.phone.fullname"
        />
      </template>
      <template #phone>
        <PhoneBookPhoneInput v-model="form.phone" :phone="props.phone.phone" />
      </template>
      <template #mobile>
        <PhoneBookMobileInput
          v-model="form.mobile"
          :mobile="props.phone.mobile"
        />
      </template>
      <template #comments>
        <PhoneBookCommentsInput
          v-model="form.comments"
          :comments="props.phone.comments"
        />
      </template>
    </UStepper>
    <div class="flex gap-2 justify-between mt-4">
      <UButton
        leading-icon="i-heroicons-arrow-left"
        :disabled="!stepper?.hasPrev"
        @click="stepper?.prev()"
      >
        Prev
      </UButton>

      <UButton
        trailing-icon="i-heroicons-arrow-right"
        :disabled="!stepper?.hasNext"
        @click="stepper?.next()"
      >
        Next
      </UButton>
    </div>

    <UButton label="Принять" color="success" variant="outline" type="submit" />
  </UForm>
</template>
