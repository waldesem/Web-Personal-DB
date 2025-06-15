<script setup lang="ts">
import type { StepperItem } from "@nuxt/ui";
import type { Phone } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  phone: {
    type: Object as () => Phone,
    default: () => ({}),
  },
  organizations: {
    type: Array,
    default: () => [],
  },
});

const stepper = useTemplateRef("stepper");
const form = ref(props.phone as Phone);
const orgs = ref(props.organizations as string[]);

const items = [
  {
    slot: "organization" as const,
    title: "Название организации*",
    icon: "i-heroicons-building-office",
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
    slot: "email" as const,
    title: "Email",
    icon: "i-heroicons-envelope",
  },
  {
    slot: "comments" as const,
    title: "Комментарий",
    icon: "i-heroicons-book-open",
  },
] satisfies StepperItem[];
</script>

<template>
  <UForm :state="form" @submit.prevent="emit('update', form)">
    <UStepper ref="stepper" :items="items" class="w-full" disabled>
      <template #organization>
        <div class="flex my-4">
          <UInputMenu
            v-model="form.organization"
            create-item
            :items="orgs"
            required
            class="w-full"
            placeholder="Название организации"
            maxlength="255"
            @create="orgs = [...orgs, $event]"
          />
        </div>
      </template>
      <template #fullname>
        <div class="flex my-4">
          <UInput
            v-model.lazy.trim="form.fullname"
            placeholder="Полное имя"
            maxlength="255"
          />
        </div>
      </template>
      <template #phone>
        <div class="flex my-4">
          <UInput
            v-model.lazy.trim="form.phone"
            placeholder="Телефон"
            maxlength="255"
          />
        </div>
      </template>
      <template #mobile>
        <div class="flex my-4">
          <UInput
            v-model.lazy.trim="form.mobile"
            placeholder="Мобильный номер"
            maxlength="255"
          />
        </div>
      </template>
      <template #email>
        <div class="flex my-4">
          <UInput
            v-model.lazy.trim="form.email"
            placeholder="Email"
            maxlength="255"
          />
        </div>
      </template>
      <template #comments>
        <div class="flex my-4">
          <UInput
            v-model.lazy.trim="form.comments"
            placeholder="Комментарий"
            maxlength="255"
          />
        </div>
      </template>
    </UStepper>
    <div class="flex gap-2 justify-between mt-4">
      <UButton
        class="rounded-full"
        title="Назад"
        leading-icon="i-heroicons-arrow-left"
        :disabled="!stepper?.hasPrev"
        @click="stepper?.prev()"
      />
      <UButton
        v-if="!stepper?.hasNext"
        class="rounded-full"
        label="Принять"
        color="success"
        type="submit"
      />
      <UButton
        class="rounded-full"
        title="Вперед"
        trailing-icon="i-heroicons-arrow-right"
        :disabled="!stepper?.hasNext || !form.organization"
        @click="stepper?.next()"
      />
    </div>
  </UForm>
</template>
