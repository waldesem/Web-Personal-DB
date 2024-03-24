<script setup lang="ts">
import { defineAsyncComponent } from 'vue';

const LabelValue = defineAsyncComponent(
  () => import("@components/content/staffsec/elements/LabelValue.vue")
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
      <LabelValue :label="'id'">
        {{ props.item['id'] }}
      </LabelValue>
      <LabelValue :label="'Компания'">
        {{ props.item['company'] }}
      </LabelValue>
      <LabelValue :label="'Название'">
        {{ props.item['name'] }}
      </LabelValue>
      <LabelValue :label="'Город'">
        {{ props.item['city'] }}
      </LabelValue>
      <LabelValue :label="'Имя'">
        {{ props.item['fullname'] }}
      </LabelValue>
      <LabelValue :label="'Телефон'">
        {{ props.item['phone'] }}
      </LabelValue>
      <LabelValue :label="'Добавочный'">
        {{ props.item['adding'] }}
      </LabelValue>
      <LabelValue :label="'Мобильный'">
        {{ props.item['mobile'] }}
      </LabelValue>
      <LabelValue :label="'E-mail'">
        {{ props.item['email'] }}
      </LabelValue>
      <LabelValue :label="'Примечание'">
        {{ props.item['note'] }}
      </LabelValue>
      <LabelValue :label="'Дата'">
        {{ new Date(String(props.item['data'])).toLocaleDateString("ru-RU") }}
      </LabelValue>
    </div>
  </div>
</template>