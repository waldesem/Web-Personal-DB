<script setup lang="ts">
import { defineAsyncComponent } from 'vue';

const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

const props = defineProps({
  item: {
    type: Object as () => Record<string, any>,
    default: {},
  }
})
</script>

<template>
  <div class="card">
    <div class="card-body">
      <LabelSlot :label="'id'">
        {{ props.item['id'] }}
      </LabelSlot>
      <LabelSlot :label="'Компания'">
        {{ props.item['company'] }}
      </LabelSlot>
      <LabelSlot :label="'Название'">
        {{ props.item['name'] }}
      </LabelSlot>
      <LabelSlot :label="'Город'">
        {{ props.item['city'] }}
      </LabelSlot>
      <LabelSlot :label="'Имя'">
        {{ props.item['fullname'] }}
      </LabelSlot>
      <LabelSlot :label="'Телефон'">
        {{ props.item['phone'] }}
      </LabelSlot>
      <LabelSlot :label="'Добавочный'">
        {{ props.item['adding'] }}
      </LabelSlot>
      <LabelSlot :label="'Мобильный'">
        {{ props.item['mobile'] }}
      </LabelSlot>
      <LabelSlot :label="'E-mail'">
        {{ props.item['email'] }}
      </LabelSlot>
      <LabelSlot :label="'Примечание'">
        {{ props.item['note'] }}
      </LabelSlot>
      <LabelSlot :label="'Дата'">
        {{ new Date(String(props.item['data'])).toLocaleDateString("ru-RU") }}
      </LabelSlot>
    </div>
  </div>
</template>