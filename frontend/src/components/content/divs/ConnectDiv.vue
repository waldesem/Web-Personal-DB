<script setup lang="ts">
import { defineAsyncComponent } from 'vue';
import { Connection } from '@/interfaces';

const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

const props = defineProps({
  item: {
    type: Object as () => Connection,
    default: {},
  }
})
</script>

<template>
  <div class="card">
    <div class="card-body">
      <LabelSlot 
        :label-class="'col-lg-4'" 
        :input-class="'col-lg-8'" 
        :label="'id'"
      >
        {{ props.item['id'] }}
      </LabelSlot>
      <LabelSlot 
        :label-class="'col-lg-4'" 
        :input-class="'col-lg-8'" 
        :label="'Компания'"
      >
        {{ props.item['company'] }}
      </LabelSlot>
      <LabelSlot 
        :label-class="'col-lg-4'" 
        :input-class="'col-lg-8'" 
        :label="'Название'"
      >
        {{ props.item['view'] }}
      </LabelSlot>
      <LabelSlot 
        :label-class="'col-lg-4'" 
        :input-class="'col-lg-8'" 
        :label="'Город'"
      >
        {{ props.item['city'] }}
      </LabelSlot>
      <LabelSlot 
        :label-class="'col-lg-4'" 
        :input-class="'col-lg-8'" 
        :label="'Имя'"
      >
        {{ props.item['fullname'] }}
      </LabelSlot>
      <LabelSlot 
        :label-class="'col-lg-4'" 
        :input-class="'col-lg-8'" 
        :label="'Телефон'"
      >
        {{ props.item['phone'] }}
      </LabelSlot>
      <LabelSlot 
        :label-class="'col-lg-4'" 
        :input-class="'col-lg-8'" 
        :label="'Добавочный'"
      >
        {{ props.item['adding'] }}
      </LabelSlot>
      <LabelSlot 
        :label-class="'col-lg-4'" 
        :input-class="'col-lg-8'" 
        :label="'Мобильный'"
      >
        {{ props.item['mobile'] }}
      </LabelSlot>
      <LabelSlot 
        :label-class="'col-lg-4'" 
        :input-class="'col-lg-8'" 
        :label="'E-mail'"
      >
        {{ props.item['email'] }}
      </LabelSlot>
      <LabelSlot 
        :label-class="'col-lg-4'" 
        :input-class="'col-lg-8'" 
        :label="'Комментарий'"
      >
        {{ props.item['comment'] }}
      </LabelSlot>
      <LabelSlot 
        :label-class="'col-lg-4'" 
        :input-class="'col-lg-8'" 
        :label="'Дата создания'"
      >
        {{ new Date(String(props.item['created'])).toLocaleDateString("ru-RU") }}
      </LabelSlot>
      <LabelSlot 
        :label-class="'col-lg-4'" 
        :input-class="'col-lg-8'" 
        :label="'Дата изменения'"
      >
        {{ new Date(String(props.item['updated'])).toLocaleDateString("ru-RU") }}
      </LabelSlot>
    </div>
  </div>
</template>